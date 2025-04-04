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
    
    def add_test(self, id, name, description, ticket_id, scores, yes_no_answers=None, priority_category=None):
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
        test = TestModel(id, name, description, ticket_id, scores, yes_no_answers)
        
        # Calculate scores
        raw_score, normalized_score = self.scoring.calculate_score(scores, yes_no_answers)
        test.raw_score = raw_score
        test.total_score = normalized_score

        # Get priority category
        test.priority = priority_category or self.scoring.get_priority_category(normalized_score)
        
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
        
        # Calculate scores with the new values
        raw_score, normalized_score = self.scoring.calculate_score(scores, yes_no_answers)

        # Get priority category
        if priority_category is None:
            priority_category = self.scoring.get_priority_category(normalized_score)
        
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
            dict: Dictionary with 'high', 'medium', and 'low' priority test lists
                  and threshold values
        """
        if not self.tests:
            return {
                "high": [],
                "medium": [],
                "low": [],
                "high_threshold": 0,
                "medium_threshold": 0
            }
        
        # Get sorted tests
        sorted_tests = self.get_sorted_tests()
        
        # Calculate thresholds
        max_score = max(test["total_score"] for test in self.tests)
        high_threshold = max_score * 0.8
        medium_threshold = max_score * 0.5
        
        # Group tests by priority
        high_priority = [t for t in sorted_tests if t["total_score"] >= high_threshold]
        medium_priority = [t for t in sorted_tests if medium_threshold <= t["total_score"] < high_threshold]
        low_priority = [t for t in sorted_tests if t["total_score"] < medium_threshold]
        
        return {
            "high": high_priority,
            "medium": medium_priority,
            "low": low_priority,
            "high_threshold": high_threshold,
            "medium_threshold": medium_threshold
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
                        scores[factor_key] = 3  # Default to medium if invalid
                else:
                    scores[factor_key] = 3  # Default to medium if missing
            
            # Calculate raw score
            raw_score = sum(scores[factor] * self.factors[factor]["weight"] for factor in scores)

            # Calculate max possible score
            max_raw_score = sum(5 * self.factors[factor]["weight"] for factor in self.factors)

            # Calculate normalized score
            normalized_score = (raw_score / max_raw_score) * 100

            # Get priority category
            priority_category = self.scoring.get_priority_category(normalized_score)
            
            # Create test object
            test_id = data.get("Test ID", f"{self.current_id}")
            
            test = {
                "id": test_id,
                "name": data.get("Test Name", ""),
                "ticket_id": data.get("Ticket ID", ""),
                "description": data.get("Description", ""),
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