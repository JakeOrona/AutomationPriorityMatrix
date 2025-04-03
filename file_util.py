"""
file_operations.py - Contains functions for file operations such as import/export and report generation
"""
from datetime import datetime
import csv
import os

# Try to import pandas, but provide alternatives if not available
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    print("Warning: pandas module not found. Using basic CSV handling instead.")

class FileOperations:
    """
    Handles file operations for the test prioritization application
    """
    @staticmethod
    def export_to_csv(filename, tests, factors):
        """
        Export tests to a CSV file
        
        Args:
            filename (str): Path to the CSV file
            tests (list): List of test dictionaries to export
            factors (dict): Dictionary of factors
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Sort tests by score (descending)
            sorted_tests = sorted(tests, key=lambda x: x["total_score"], reverse=True)
            
            # Create field names (column headers)
            field_names = ["Test ID", "Ticket ID", "Test Name", "Description", "Raw Score", "Total Score (100-point)"]
            
            # Add factor score headers
            for factor_key, factor_info in factors.items():
                field_names.append(factor_info["name"])
            
            # Check if we have yes/no questions to add to the CSV
            has_yes_no = False
            if len(sorted_tests) > 0 and 'yes_no_answers' in sorted_tests[0]:
                has_yes_no = True
                # Get the question texts from the first test's yes_no_answers
                for question_key in sorted_tests[0].get('yes_no_answers', {}):
                    # We'd need to get the question text from somewhere, 
                    # here we're assuming a model would be passed to get question text
                    if hasattr(sorted_tests[0], 'yes_no_questions'):
                        question_text = sorted_tests[0].yes_no_questions[question_key]["question"]
                        field_names.append(question_text)
                    else:
                        # Fallback to just using the key as header
                        field_names.append(f"Question: {question_key}")
            
            # Prepare data for export
            data = []
            for test in sorted_tests:
                row = {
                    "Test ID": test["id"],
                    "Ticket ID": test.get("ticket_id", "N/A"),
                    "Test Name": test["name"],
                    "Description": test["description"],
                    "Raw Score": test.get("raw_score", "N/A"),
                    "Total Score (100-point)": test["total_score"]
                }
                
                # Add factor scores
                for factor, score in test["scores"].items():
                    factor_name = factors[factor]["name"]
                    row[factor_name] = score
                
                # Add yes/no answers if available
                if has_yes_no and 'yes_no_answers' in test:
                    for question_key, answer in test['yes_no_answers'].items():
                        # Get the appropriate column header
                        if hasattr(test, 'yes_no_questions'):
                            question_text = test.yes_no_questions[question_key]["question"]
                        else:
                            question_text = f"Question: {question_key}"
                        
                        # Add the answer
                        row[question_text] = "Yes" if answer else "No"
                
                data.append(row)
            
            # Use pandas if available, otherwise use the built-in csv module
            if PANDAS_AVAILABLE:
                # Create DataFrame and export
                df = pd.DataFrame(data)
                df.to_csv(filename, index=False)
            else:
                # Use csv module
                with open(filename, 'w', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    for row in data:
                        writer.writerow(row)
            
            return True
        
        except Exception as e:
            print(f"Export error: {str(e)}")
            return False
    
    @staticmethod
    def import_from_csv(filename):
        """
        Import tests from a CSV file
        
        Args:
            filename (str): Path to the CSV file
            
        Returns:
            tuple: (success, data or error message)
                success (bool): True if successful, False otherwise
                data (list): List of dictionaries if successful, error message otherwise
        """
        try:
            if PANDAS_AVAILABLE:
                # Use pandas if available
                df = pd.read_csv(filename)
                data = df.to_dict(orient='records')
            else:
                # Use csv module if pandas not available
                data = []
                with open(filename, 'r', newline='') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        data.append(dict(row))
            
            return True, data
        
        except Exception as e:
            error_message = f"Import error: {str(e)}"
            print(error_message)
            return False, error_message
    
    @staticmethod
    def generate_report_text(tests, priority_tiers):
        """
        Generate text for the prioritization report
        
        Args:
            tests (list): List of all test dictionaries
            priority_tiers (dict): Dictionary with high, medium, and low priority tests
            
        Returns:
            str: Formatted report text
        """
        # Report header
        header = f"TEST AUTOMATION PRIORITY REPORT\n"
        header += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        header += f"Total Tests: {len(tests)}\n"
        header += "=" * 70 + "\n\n"
        
        report_text = header
        
        # Get the tiers
        high_priority = priority_tiers["high"]
        medium_priority = priority_tiers["medium"]
        low_priority = priority_tiers["low"]
        high_threshold = priority_tiers["high_threshold"]
        medium_threshold = priority_tiers["medium_threshold"]
        
        # High priority section
        report_text += f"HIGH PRIORITY TESTS (Score >= {high_threshold:.1f}):\n"
        report_text += f"Recommended for immediate automation\n"
        report_text += "-" * 70 + "\n"
        
        for i, test in enumerate(high_priority):
            report_text += f"{i+1}. {test['name']} (ID: {test['id']})\n"
            report_text += f"   Score: {test['total_score']:.1f}\n"
            report_text += f"   Description: {test['description']}\n"
            
            # Add yes/no answers if available
            if 'yes_no_answers' in test:
                for key, answer in test['yes_no_answers'].items():
                    report_text += f"   * {key}: {answer}\n"
            
            report_text += "\n"
        
        report_text += "\n"
        
        # Medium priority section
        report_text += f"MEDIUM PRIORITY TESTS (Score {medium_threshold:.1f} - {high_threshold:.1f}):\n"
        report_text += f"Recommended for second phase automation\n"
        report_text += "-" * 70 + "\n"
        
        for i, test in enumerate(medium_priority):
            report_text += f"{i+1}. {test['name']} (ID: {test['id']})\n"
            report_text += f"   Score: {test['total_score']:.1f}\n"
            
            # Add yes/no answers if available
            if 'yes_no_answers' in test:
                for key, answer in test['yes_no_answers'].items():
                    report_text += f"   * {key}: {answer}\n"
        
        report_text += "\n"
        
        # Low priority section
        report_text += f"LOW PRIORITY TESTS (Score < {medium_threshold:.1f}):\n"
        report_text += f"Consider for later phases or keep as manual tests\n"
        report_text += "-" * 70 + "\n"
        
        for i, test in enumerate(low_priority):
            report_text += f"{i+1}. {test['name']} (ID: {test['id']})\n"
            report_text += f"   Score: {test['total_score']:.1f}\n"

            if 'yes_no_answers' in test:
                for key, answer in test['yes_no_answers'].items():
                    report_text += f"   * {key}: {answer}\n"
        
        return report_text
    
    @staticmethod
    def generate_scoring_guide_text(factors, score_options):
        """
        Generate text for the scoring guide
        
        Args:
            factors (dict): Dictionary of factors and weights
            score_options (dict): Dictionary of scoring options
            
        Returns:
            str: Formatted guide text
        """
        guide = "TEST AUTOMATION PRIORITIZATION SCORING GUIDE\n"
        guide += "=" * 44 + "\n\n"
        
        guide += "This application uses the following weighted factors to calculate\n"
        guide += "which manual tests should be prioritized for automation:\n\n"
        
        for factor, details in factors.items():
            factor_name = details["name"]
            weight = details["weight"]
            
            guide += f"{factor_name} (Weight: {weight})\n"
            guide += "-" * 50 + "\n"
            
            for score, description in score_options[factor].items():
                guide += f"  {score} - {description}\n"
            
            guide += "\n"
        
        guide += "How scores are calculated:\n"
        guide += "-" * 50 + "\n"
        guide += "1. Each factor score is multiplied by its weight\n"
        guide += "2. These weighted scores are summed to get a raw score (max 70)\n"
        guide += "3. The raw score is converted to a 100-point scale\n\n"
        guide += "Formula: Final Score = (Raw Score / 70) × 100\n\n"
        guide += "Maximum possible score: 100\n"
        guide += "Minimum possible score: 20\n\n"
        
        # Add information about yes/no questions if available
        if hasattr(factors, 'yes_no_questions') and factors.yes_no_questions:
            guide += "Additional Yes/No Questions:\n"
            guide += "-" * 50 + "\n"
            
            for key, question_data in factors.yes_no_questions.items():
                guide += f"  {question_data['question']}\n"
                guide += f"    Impact: {question_data['impact']}\n\n"
        
        return guide
    
    @staticmethod
    def export_report_to_file(filename, report_text):
        """
        Export a report to a text file
        
        Args:
            filename (str): Path to the text file
            report_text (str): The report text to export
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(filename, "w") as f:
                f.write(report_text)
            return True
        except Exception as e:
            print(f"Export report error: {str(e)}")
            return False