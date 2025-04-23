"""
base_report.py - Base class for report generators
"""

class BaseReportGenerator:
    """
    Base class for all report generators
    
    This provides common functionality and interfaces that all report generators
    should implement or inherit.
    """
    
    @staticmethod
    def generate_report(tests, priority_tiers, model=None):
        """
        Generate a report based on test data
        
        Args:
            tests (list): List of all test dictionaries
            priority_tiers (dict): Dictionary with priority tier tests
            model: The prioritization model
            
        Returns:
            str: Formatted report text
        """
        raise NotImplementedError("Subclasses must implement generate_report()")
    
    @staticmethod
    def export_to_file(filename, report_text):
        """
        Export a report to a file
        
        Args:
            filename (str): Path to the output file
            report_text (str): The report text to export
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(report_text)
            return True
        except Exception as e:
            print(f"Export report error: {str(e)}")
            return False
    
    @staticmethod
    def group_tests_by_section(tests):
        """
        Group tests by section for reporting
        
        Args:
            tests (list): List of test dictionaries
            
        Returns:
            dict: Dictionary with section names as keys and lists of tests as values
        """
        sections = {}
        for test in tests:
            section = test.get("section", "")
            if section not in sections:
                sections[section] = []
            sections[section].append(test)
        return sections