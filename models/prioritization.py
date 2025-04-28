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
        
        # Track sections for filtering
        self.sections = set()
    
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
    
    def add_test(self, name, section, description, ticket_id, scores, yes_no_answers=None, priority_category=None):
        """
        Add a new test with calculated priority scores
        
        Args:
            name (str): Test name
            description (str): Test description
            section (str): Section or category the test belongs to
            ticket_id (str): Ticket ID associated with the test
            scores (dict): Dictionary of scores for each factor
            yes_no_answers (dict, optional): Dictionary of yes/no answers
            priority_category (str, optional): Predefined priority category
            
        Returns:
            Test: The newly created test object
        """
        # Create a new Test instance
        test = TestModel(self.current_id, name, section, description, ticket_id, scores, yes_no_answers)
        
        # Check if test can be automated
        can_be_automated = True
        if "can_be_automated" in scores and scores["can_be_automated"] == 1:  # Selected "No"
            can_be_automated = False
            raw_score = 0
            normalized_score = 0
            priority = "Won't Automate"
        else:
            # Calculate scores
            raw_score, normalized_score = self.scoring.calculate_score(scores, yes_no_answers)
            # Get priority category
            priority = priority_category or self.scoring.get_priority_category(normalized_score, can_be_automated)
        
        test.raw_score = raw_score
        test.total_score = normalized_score
        test.priority = priority
        
        # Add to list and convert to dict for consistency with existing functions
        test_dict = test.to_dict()
        self.tests.append(test_dict)
        
        # Add section to tracked sections if not empty
        if section:
            self.sections.add(section)
        
        # Increment ID counter for the next test
        self.current_id += 1
        
        return test_dict
    
    def update_test(self, test_id, name, section, description, ticket_id, scores, yes_no_answers=None, priority_category=None):
        """
        Update an existing test
        
        Args:
            test_id (str): ID of the test to update
            name (str): Updated test name
            section (str): Updated section
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
        if "can_be_automated" in scores and scores["can_be_automated"] == 1:  # Selected "No"
            can_be_automated = False
            raw_score = 0
            normalized_score = 0
            priority_category = "Won't Automate"
        else:
            # Calculate scores with the new values
            raw_score, normalized_score = self.scoring.calculate_score(scores, yes_no_answers)
            # Get priority category
            priority_category = self.scoring.get_priority_category(normalized_score, can_be_automated)
        
        # Store old section to check if we need to update tracked sections
        old_section = test_dict.get("section", "")
        
        # Update test
        test_dict["name"] = name
        test_dict["description"] = description
        test_dict["ticket_id"] = ticket_id
        test_dict["section"] = section
        test_dict["scores"] = scores
        test_dict["yes_no_answers"] = yes_no_answers or {}
        test_dict["raw_score"] = raw_score
        test_dict["total_score"] = normalized_score
        test_dict["priority"] = priority_category
        
        # Update tracked sections
        if section and section != old_section:
            self.sections.add(section)
            # Check if old_section is still used by any test
            if old_section and not any(t.get("section") == old_section for t in self.tests):
                self.sections.discard(old_section)
        
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
                # Clear sections
                self.sections.clear()
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
                section = test.get("section", "")
                del self.tests[i]
                
                # Check if section is still used by any test
                if section and not any(t.get("section") == section for t in self.tests):
                    self.sections.discard(section)
                    
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
    
    def get_sorted_tests(self, section_filter=None):
        """
        Get tests sorted by priority score (descending), optionally filtered by section
        
        Args:
            section_filter (str, optional): Filter tests by section
            
        Returns:
            list: Sorted list of test objects
        """
        # First, filter by section if specified
        if section_filter:
            filtered_tests = [t for t in self.tests if t.get("section", "") == section_filter]
        else:
            filtered_tests = self.tests
            
        # Then sort by priority category
        priority_order = {"Highest": 0, "High": 1, "Medium": 2, "Low": 3, "Lowest": 4, "Won't Automate": 5}
        return sorted(filtered_tests, key=lambda x: (priority_order.get(x["priority"], 999), -x["total_score"]))
    
    def get_tests_by_section(self, section):
        """
        Get all tests in a specific section
        
        Args:
            section (str): Section to filter by
            
        Returns:
            list: List of tests in the specified section
        """
        return [t for t in self.tests if t.get("section", "") == section]
    
    def get_priority_tiers(self, section_filter=None):
        """
        Get tests grouped into priority tiers, optionally filtered by section
        
        Args:
            section_filter (str, optional): Filter tests by section
            
        Returns:
            dict: Dictionary with 'high', 'medium', and 'low' priority test lists
                    and threshold values
        """
        # First, filter by section if specified
        if section_filter:
            filtered_tests = [t for t in self.tests if t.get("section", "") == section_filter]
        else:
            filtered_tests = self.tests
            
        if not filtered_tests:
            return {
                "highest": [],
                "high": [],
                "medium": [],
                "low": [],
                "lowest": [],
                "wont_automate": [],
                "high_threshold": 0,
                "medium_threshold": 0,
                "low_threshold": 0,
                "lowest_threshold": 0,
                "highest_threshold": 0,
                "max_score": 0
            }
        
        # Get sorted tests
        sorted_tests = self.get_sorted_tests(section_filter)
        
        # Calculate thresholds
        max_score = 100
        
        highest_threshold = max_score * 0.85
        high_threshold = max_score * 0.70
        medium_threshold = max_score * 0.55
        low_threshold = max_score * 0.40
        lowest_threshold = max_score * 0.20
        
        # Group tests by priority
        highest_priority = [t for t in sorted_tests if t["priority"] == "Highest"]
        high_priority = [t for t in sorted_tests if t["priority"] == "High"]
        medium_priority = [t for t in sorted_tests if t["priority"] == "Medium"]
        low_priority = [t for t in sorted_tests if t["priority"] == "Low"]
        lowest_priority = [t for t in sorted_tests if t["priority"] == "Lowest"]
        wont_automate = [t for t in sorted_tests if t["priority"] == "Won't Automate"]
        
        return {
            "highest": highest_priority,  
            "high": high_priority,
            "medium": medium_priority,
            "low": low_priority,
            "lowest": lowest_priority,
            "wont_automate": wont_automate,
            "lowest_threshold": lowest_threshold,
            "low_threshold": low_threshold,
            "medium_threshold": medium_threshold,
            "high_threshold": high_threshold,
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
            self.sections.clear()
        
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
                        # Default to yes for can_be_automated factor
                        if factor_key == "can_be_automated":
                            scores[factor_key] = 5  # Default to Yes
                        else:
                            scores[factor_key] = 3  # Default to medium if invalid
                else:
                    # Default to yes for can_be_automated factor
                    if factor_key == "can_be_automated":
                        scores[factor_key] = 5  # Default to Yes
                    else:
                        scores[factor_key] = 3  # Default to medium if missing
            
            # Check if test can be automated
            can_be_automated = True
            if "can_be_automated" in scores and scores["can_be_automated"] == 1:  # can_be_automated == "No"
                can_be_automated = False
                raw_score = 0
                normalized_score = 0
                priority_category = "Won't Automate"
            else:
                # Calculate raw score
                raw_score, normalized_score = self.scoring.calculate_score(scores, {})

                # Get priority category
                priority_category = self.scoring.get_priority_category(normalized_score, can_be_automated)
            
            # Create test object
            test_id = data.get("Test ID", int(self.current_id))

            # Handle potentially NaN description values
            description = data.get("Description", "")
            if description == "nan" or description is None or (hasattr(description, "lower") and description.lower() == "nan"):
                description = ""
                
            # Get section
            section = data.get("Section", "")
            if section and section != "nan" and section is not None:
                self.sections.add(section)
            else:
                section = ""
            
            test = {
                "id": test_id,
                "name": data.get("Test Name", ""),
                "section": section,
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