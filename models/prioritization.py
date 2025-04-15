"""
prioritization.py - Contains the core prioritization model
"""
from .test_model import TestModel
from .scoring import ScoringSystem

class TestPrioritizationModel:
    """
    Model class that handles the business logic for test prioritization
    """
    def __init__(self):
        """Initialize the prioritization model"""
        # Initialize data storage
        self.tests = []
        self.current_id = 1
        
        # Create scoring system
        self.scoring = ScoringSystem()
    
    @property
    def factors(self):
        """Get factors from the scoring system"""
        return self.scoring.factors
    
    @property
    def score_options(self):
        """Get score options from the scoring system"""
        return self.scoring.score_options
    
    @property
    def yes_no_questions(self):
        """Get yes/no questions from the scoring system"""
        return self.scoring.yes_no_questions
    
    def add_test(self, name, description, ticket_id, scores, yes_no_answers=None, priority_category=None):
        """
        Add a new test with calculated priority scores
        
        Args:
            id (str): ID of the test
            name (str): Test name
            description (str): Test description
            ticket_id (str): Ticket ID associated with the test
            scores (dict): Dictionary of scores for each factor
            yes_no_answers (dict, optional): Dictionary of yes/no answers
            priority_category (str, optional): Predefined priority category
            
        Returns:
            Test: The newly created test object
        """
        # Create a new Test instance
        test = TestModel(self.current_id, name, description, ticket_id, scores, yes_no_answers)
        
        # Check if test can be automated
        can_be_automated = True
        if "can_be_automated" in scores and scores["can_be_automated"] == 1: # Selected "No"
            can_be_automated = False
            raw_score = 0
            normalized_score = 0
            priority = "Can't Automate"
        else:
            # Calculate raw score
            raw_score, normalized_score = self.scoring.calculate_score(scores, yes_no_answers)
            # Get priority category
            priority = priority_category or self.scoring.get_priority_category(normalized_score, can_be_automated)
        
        # Set scores
        test.raw_score = raw_score
        test.total_score = normalized_score
        test.priority = priority
        
        # Add to list and convert to dict for consistency with existing functions
        self.tests.append(test.to_dict())
        
        # Increment ID counter for the next test
        self.current_id += 1
        
        return test.to_dict()
    
    def update_test(self, test_id, name, description, ticket_id, scores, yes_no_answers=None, priority_category=None):
        """
        Update an existing test
        
        Args:
            test_id (str): ID of the test to update
            name (str): Updated test name
            description (str): Updated test description
            ticket_id (str): Updated ticket ID
            scores (dict): Updated scores for each factor
            yes_no_answers (dict, optional): Dictionary of yes/no answers
            priority_category (str, optional): Predefined priority category
            
        Returns:
            dict: The updated test object or None if not found
        """
        # Find the test in the list
        test_dict = self.find_test_by_id(test_id)
        if not test_dict:
            return None
        
        # Check if test can be automated
        can_be_automated = True
        if "can_be_automated" in scores and scores["can_be_automated"] == 1: # Selected "No"
            can_be_automated = False
            raw_score = 0
            normalized_score = 0
            priority_category = "Can't Automate"
        else:
            # Calculate new raw score
            raw_score, normalized_score = self.scoring.calculate_score(scores, yes_no_answers)
            # Get priority category
            priority_category = priority_category or self.scoring.get_priority_category(normalized_score, can_be_automated)
        
        # Update test
        test_dict["name"] = name
        test_dict["description"] = description
        test_dict["ticket_id"] = ticket_id
        test_dict["scores"] = scores
        test_dict["yes_no_answers"] = yes_no_answers or {}
        test_dict["raw_score"] = raw_score
        test_dict["total_score"] = normalized_score
        test_dict["priority"] = priority_category
        
        return test_dict
    
    def delete_all_tests(self):
        """
        Delete all tests in table
        
        Returns:
            bool: True if tests were deleted, False if none were found
        """
        initial_count = len(self.tests)
        if initial_count == 0:
            return False
        else:
            try:
                # Clear the list
                self.tests.clear()
                self.current_id = 1  # Reset ID counter
                return len(self.tests) < initial_count
            except Exception as e:
                print(f"Error clearing tests: {e}")
                return False

    def delete_one_test(self, test_id):
        """
        Delete a single test by ID
        
        Args:
            test_id (str): ID of the test to delete
            
        Returns:
            bool: True if the test was deleted, False if not found
        """
        for i, test in enumerate(self.tests):
            if test["id"] == test_id:
                del self.tests[i]
                return True
        return False
    
    def find_test_id_by_name(self, name):
        """
        Find a test by name
        
        Args:
            name (str): Name of the test to find
            
        Returns:
            str: The ID of the test or None if not found
        """
        for test in self.tests:
            if test["name"] == name:
                return test["id"]
        return None
    
    def find_test_by_id(self, test_id):
        """
        Find a test by ID
        
        Args:
            test_id (str): ID of the test to find
            
        Returns:
            dict: The test object or None if not found
        """
        for test in self.tests:
            if test["id"] == test_id:
                return test
        return None
    
    def get_sorted_tests(self):
        """
        Get tests sorted by priority score (descending)
        
        Returns:
            list: Sorted list of test objects
        """
        return sorted(self.tests, key=lambda x: x["total_score"], reverse=True)
    
    def get_priority_tiers(self):
        """
        Get tests grouped into priority tiers
        
        Returns:
            dict: Dictionary with 'highest', 'high', 'medium', 'low', 'lowest' and 'cant_automate' priority test lists
                    and threshold values
        """
        if not self.tests:
            return {
                "highest": [],
                "high": [],
                "medium": [],
                "low": [],
                "lowest": [],
                "cant_automate": [],
                "high_threshold": 0,
                "medium_threshold": 0
            }
        
        # Get sorted tests
        sorted_tests = self.get_sorted_tests()
        
        # Score thresholds
        max_score = 100
        highest_threshold = max_score * 0.90
        high_threshold = max_score * 0.80
        medium_threshold = max_score * 0.60
        low_threshold = max_score * 0.40
        lowest_threshold = max_score * 0.20
        
        # Group tests by priority
        highest_priority = [t for t in sorted_tests if t["priority"] == "Highest"]
        high_priority = [t for t in sorted_tests if t["priority"] == "High"]
        medium_priority = [t for t in sorted_tests if t["priority"] == "Medium"]
        low_priority = [t for t in sorted_tests if t["priority"] == "Low"]
        lowest_priority = [t for t in sorted_tests if t["priority"] == "Lowest"]
        cant_automate = [t for t in sorted_tests if t["priority"] == "Can't Automate"]
        
        return {
            "highest": highest_priority,  
            "high": high_priority,
            "medium": medium_priority,
            "low": low_priority,
            "lowest": lowest_priority,
            "cant_automate": cant_automate,
            "lowest_threshold": lowest_threshold,
            "low_threshold": low_threshold,
            "high_threshold": high_threshold,
            "medium_threshold": medium_threshold,
            "highest_threshold": highest_threshold,
            "max_score": max_score
        }
    
    def import_tests(self, tests_data, replace=False):
        """
        Import tests from external data (e.g., CSV)
        
        Args:
            tests_data (list): List of dictionaries containing test data
            replace (bool): If True, replace existing tests, otherwise append
            
        Returns:
            int: Number of tests imported
        """
        if replace:
            self.tests = []
        
        max_id = self.current_id
        
        for data in tests_data:
            # Extract factor scores
            scores = {}
            
            for factor_key, factor_info in self.factors.items():
                factor_name = factor_info["name"]
                if factor_name in data:
                    try:
                        scores[factor_key] = int(data[factor_name])
                    except (ValueError, TypeError):
                        if factor_key == "can_be_automated":
                            scores[factor_key] = 5 # Default to yes
                        else:
                            scores[factor_key] = 3  # Default to medium if invalid
                else:
                    # Default to yes for can_be_automated or medium for others
                    if factor_key == "can_be_automated":
                        scores[factor_key] = 5 # Default to yes
                    else:
                        scores[factor_key] = 3 # Default to medium if missing
            
            # Check if test can be automated
            can_be_automated = True
            if "can_be_automated" in scores and scores["can_be_automated"] == 1: # Selected "No"
                can_be_automated = False
                raw_score = 0
                normalized_score = 0
                priority_category = "Can't Automate"
            else:
                # Calculate raw score
                raw_score = sum(scores[factor] * self.factors[factor]["weight"]
                                for factor in scores if factor != "can_be_automated")
                # Calculate max possible score
                max_raw_score = sum(5 * self.factors[factor]["weight"]
                                    for factor in self.factors if factor != "can_be_automated")

                # Calculate normalized score
                normalized_score = (raw_score / max_raw_score) * 100 if max_raw_score > 0 else 0

                # Get priority category
                priority_category = self.scoring.get_priority_category(normalized_score, can_be_automated)
            
            # Create test object
            test_id = data.get("Test ID", int(self.current_id))

            # Handle potentially NaN description values
            description = data.get("Description", "")
            if description == "nan" or description is None or (hasattr(description, "lower") and description.lower() == "nan"):
                description = ""
            
            test = {
                "id": test_id,
                "name": data.get("Test Name", ""),
                "ticket_id": data.get("Ticket ID", ""),
                "description": description,
                "scores": scores,
                "raw_score": raw_score,
                "total_score": round(normalized_score, 1),  # Round to 1 decimal place
                "priority": priority_category
            }
            
            # Add to list
            self.tests.append(test)
            
            # Update current ID if needed
            try:
                id_num = int(test_id)
                if id_num >= max_id:
                    max_id = id_num + 1
            except (ValueError, IndexError):
                pass
        
        self.current_id = max_id
        
        return len(tests_data)