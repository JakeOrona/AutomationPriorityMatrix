# file_operations/csv_handler.py
"""
csv_handler.py - Handles CSV file operations
"""
import csv

# Try to import pandas, but provide alternatives if not available
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    print("Warning: pandas module not found. Using basic CSV handling instead.")

class CSVHandler:
    """
    Handles CSV file operations for the test prioritization application
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
            sorted_tests = sorted(tests, key=lambda x: x.get("total_score", 0), reverse=True)
            
            # Create initial field names (column headers)
            initial_fields = ["Rank", "Priority", "Ticket ID", "Section", "Test Name", "Description"]
            post_fields = ["Total Score (100-point)", "Raw Score"]
            
            # Initialize field names with initial fields
            field_names = initial_fields.copy()
            
            # Check if we have yes/no questions to add to the CSV
            yes_no_fields = []
            has_yes_no = False
            if len(sorted_tests) > 0 and 'yes_no_answers' in sorted_tests[0]:
                has_yes_no = True
                # Get the question texts from the first test's yes_no_answers
                for question_key in sorted_tests[0].get('yes_no_answers', {}):
                    # Add the yes/no question fields right after description
                    yes_no_fields.append(f"Question: {question_key}")
            
            # Add yes/no fields right after Description
            field_names.extend(yes_no_fields)
            
            # Add scoring fields
            field_names.extend(post_fields)
            
            # Add factor score headers
            for factor_key, factor_info in factors.items():
                field_names.append(factor_info["name"])

            # Add Test ID at the end
            field_names.append("Test ID")
            
            # Prepare data for export
            data = []
            for i, test in enumerate(sorted_tests):
                # Ensure description is never None or NaN
                description = test.get("description", "")
                if description is None or description == "nan" or (hasattr(description, "lower") and description.lower() == "nan"):
                    description = ""
                
                # Create row dictionary    
                row = {
                    "Rank": i + 1,
                    "Priority": test.get("priority", ""),
                    "Ticket ID": test.get("ticket_id", "N/A"),
                    "Section": test.get("section", ""),
                    "Test Name": test.get("name", ""),
                    "Description": description,
                    "Total Score (100-point)": test.get("total_score", 0),
                    "Raw Score": test.get("raw_score", "N/A"),
                    "Test ID": test.get("id", "")
                }
                
                # Add yes/no answers if available
                if has_yes_no and 'yes_no_answers' in test:
                    for question_key, answer in test['yes_no_answers'].items():
                        question_text = f"Question: {question_key}"
                        row[question_text] = "Yes" if answer else "No"
                
                # Add factor scores
                for factor in factors:
                    factor_name = factors[factor]["name"]
                    # Get scores safely, defaulting to 0 if not present
                    scores = test.get("scores", {})
                    row[factor_name] = scores.get(factor, 0)
                
                data.append(row)
            
            # Use pandas if available, otherwise use the built-in csv module
            if PANDAS_AVAILABLE:
                # Create DataFrame and export
                df = pd.DataFrame(data)
                # Ensure columns are in the correct order
                df = df[field_names]
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