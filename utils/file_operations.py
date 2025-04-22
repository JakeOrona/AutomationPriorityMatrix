"""
file_operations.py - Handles file import/export and report generation
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
            sorted_tests = sorted(tests, key=lambda x: x.get("total_score", 0), reverse=True)
            
            # Create field names (column headers)
            field_names = ["Rank", "Priority", "Ticket ID", "Section", "Test Name", "Description", 
                            "Total Score (100-point)", "Raw Score", "Test ID"]
            
            # Add factor score headers
            for factor_key, factor_info in factors.items():
                field_names.append(factor_info["name"])
            
            # Check if we have yes/no questions to add to the CSV
            has_yes_no = False
            if len(sorted_tests) > 0 and 'yes_no_answers' in sorted_tests[0]:
                has_yes_no = True
                # Get the question texts from the first test's yes_no_answers
                for question_key in sorted_tests[0].get('yes_no_answers', {}):
                    # Fallback to just using the key as header
                    field_names.append(f"Question: {question_key}")
            
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
                    "Raw Score": test.get("raw_score", "N/A")
                    
                }
                
                # Add factor scores
                for factor in factors:
                    factor_name = factors[factor]["name"]
                    # Get scores safely, defaulting to 0 if not present
                    scores = test.get("scores", {})
                    row[factor_name] = scores.get(factor, 0)
                
                # Add yes/no answers if available
                if has_yes_no and 'yes_no_answers' in test:
                    for question_key, answer in test['yes_no_answers'].items():
                        question_text = f"Question: {question_key}"
                        row[question_text] = "Yes" if answer else "No"
                
                row["Test ID"] = test.get("id", "")

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
    def generate_report_text(tests, priority_tiers, model=None):
        """
        Generate text for the prioritization report
        
        Args:
            tests (list): List of all test dictionaries
            priority_tiers (dict): Dictionary with priority tier tests
            model: The prioritization model (added parameter)
            
        Returns:
            str: Formatted report text
        """
        # Report header
        header = f"TEST AUTOMATION PRIORITY REPORT\n"
        header += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        header += f"Total Tests: {len(tests)}\n"
        
        # Group tests by section
        sections = {}
        for test in tests:
            section = test.get("section", "")
            if section not in sections:
                sections[section] = []
            sections[section].append(test)
        
        if sections:
            header += f"Sections: {len(sections)}\n"
        
        header += "=" * 70 + "\n\n"
        
        report_text = header
        
        # Get the tiers
        highest_priority = priority_tiers["highest"]
        high_priority = priority_tiers["high"]
        medium_priority = priority_tiers["medium"]
        low_priority = priority_tiers["low"]
        lowest_priority = priority_tiers["lowest"]
        cant_automate = priority_tiers.get("cant_automate", [])  # Get "Can't Automate" tests if available

        highest_threshold = priority_tiers["highest_threshold"]
        high_threshold = priority_tiers["high_threshold"]
        medium_threshold = priority_tiers["medium_threshold"]
        low_threshold = priority_tiers["low_threshold"]
        lowest_threshold = priority_tiers["lowest_threshold"]

        # Highest priority section
        report_text += f"HIGHEST PRIORITY TESTS (Score >= {highest_threshold:.1f}):\n"
        report_text += f"Recommended for immediate automation\n"
        report_text += "-" * 70 + "\n"
        
        for i, test in enumerate(highest_priority):
            report_text += f"| {i+1}. {test['name']} (ID: {test['id']})\n"
            report_text += f"|    Score: {test['total_score']:.1f}\n"

            # Add section if available
            if test.get("section"):
                report_text += f"|    Section: {test['section']}\n"

            # Add description if available
            if 'description' in test:
                report_text += f"|    Description: {test['description']}\n"
            
            # Add score details with descriptions
            if model and hasattr(model, 'factors') and hasattr(model, 'score_options'):
                report_text += f"|    Factor Scores:\n"
                for factor, score in test['scores'].items():
                    if factor in model.factors and score in model.score_options.get(factor, {}):
                        factor_name = model.factors[factor]["name"]
                        score_description = model.score_options[factor][score]
                        report_text += f"|      - {factor_name}: {score} - {score_description}\n"
            
            # Add yes/no answers if available
            if 'yes_no_answers' in test:
                for key, answer in test['yes_no_answers'].items():
                    report_text += f"|    * {key}: {answer}\n"
            
            report_text += "|\n"

        report_text += "-" * 70 + "\n"
        
        report_text += "\n"
        
        # High priority section
        report_text += f"HIGH PRIORITY TESTS (Score {high_threshold:.1f} - {highest_threshold:.1f}):\n"
        report_text += f"Recommended for second phase automation\n"
        report_text += "-" * 70 + "\n"
        
        for i, test in enumerate(high_priority):
            report_text += f"| {i+1}. {test['name']} (ID: {test['id']})\n"
            report_text += f"|    Score: {test['total_score']:.1f}\n"

            # Add section if available
            if test.get("section"):
                report_text += f"|    Section: {test['section']}\n"

            # Add description if available
            if 'description' in test:
                report_text += f"|    Description: {test['description']}\n"
            
            # Add score details with descriptions
            if model and hasattr(model, 'factors') and hasattr(model, 'score_options'):
                report_text += f"|    Factor Scores:\n"
                for factor, score in test['scores'].items():
                    if factor in model.factors and score in model.score_options.get(factor, {}):
                        factor_name = model.factors[factor]["name"]
                        score_description = model.score_options[factor][score]
                        report_text += f"|      - {factor_name}: {score} - {score_description}\n"
            
            # Add yes/no answers if available
            if 'yes_no_answers' in test:
                for key, answer in test['yes_no_answers'].items():
                    report_text += f"|    * {key}: {answer}\n"
            
            report_text += "|\n"

        report_text += "-" * 70 + "\n"
        
        report_text += "\n"
        
        # Medium priority section
        report_text += f"MEDIUM PRIORITY TESTS (Score {medium_threshold:.1f} - {high_threshold:.1f}):\n"
        report_text += f"Recommended for third phase automation\n"
        report_text += "-" * 70 + "\n"
        
        for i, test in enumerate(medium_priority):
            report_text += f"| {i+1}. {test['name']} (ID: {test['id']})\n"
            report_text += f"|    Score: {test['total_score']:.1f}\n"

            # Add section if available
            if test.get("section"):
                report_text += f"|    Section: {test['section']}\n"

            # Add description if available
            if 'description' in test:
                report_text += f"|    Description: {test['description']}\n"
            
            # Add score details with descriptions
            if model and hasattr(model, 'factors') and hasattr(model, 'score_options'):
                report_text += f"|    Factor Scores:\n"
                for factor, score in test['scores'].items():
                    if factor in model.factors and score in model.score_options.get(factor, {}):
                        factor_name = model.factors[factor]["name"]
                        score_description = model.score_options[factor][score]
                        report_text += f"|      - {factor_name}: {score} - {score_description}\n"
            
            # Add yes/no answers if available
            if 'yes_no_answers' in test:
                for key, answer in test['yes_no_answers'].items():
                    report_text += f"|    * {key}: {answer}\n"
            
            report_text += "|\n"

        report_text += "-" * 70 + "\n"
        
        report_text += "\n"
        
        # Low priority section
        report_text += f"LOW PRIORITY TESTS (Score {low_threshold:.1f} - {medium_threshold:.1f}):\n"
        report_text += f"Consider for later phases or keep as manual tests\n"
        report_text += "-" * 70 + "\n"
        
        for i, test in enumerate(low_priority):
            report_text += f"| {i+1}. {test['name']} (ID: {test['id']})\n"
            report_text += f"|    Score: {test['total_score']:.1f}\n"

            # Add section if available
            if test.get("section"):
                report_text += f"|    Section: {test['section']}\n"

            # Add description if available
            if 'description' in test:
                report_text += f"|    Description: {test['description']}\n"

            # Add score details with descriptions
            if model and hasattr(model, 'factors') and hasattr(model, 'score_options'):
                report_text += f"|    Factor Scores:\n"
                for factor, score in test['scores'].items():
                    if factor in model.factors and score in model.score_options.get(factor, {}):
                        factor_name = model.factors[factor]["name"]
                        score_description = model.score_options[factor][score]
                        report_text += f"|      - {factor_name}: {score} - {score_description}\n"

            if 'yes_no_answers' in test:
                for key, answer in test['yes_no_answers'].items():
                    report_text += f"|    * {key}: {answer}\n"
                    
            report_text += "|\n"

        report_text += "-" * 70 + "\n"

        report_text += "\n"

        # Lowest priority section
        report_text += f"LOWEST PRIORITY TESTS (Score <= {low_threshold:.1f}):\n"
        report_text += f"Not Recommended for automation\n"
        report_text += "-" * 70 + "\n"
        
        for i, test in enumerate(lowest_priority):
            report_text += f"| {i+1}. {test['name']} (ID: {test['id']})\n"
            report_text += f"|    Score: {test['total_score']:.1f}\n"
            
            # Add section if available
            if test.get("section"):
                report_text += f"|    Section: {test['section']}\n"
            
            # Add description if available
            if 'description' in test:
                report_text += f"|    Description: {test['description']}\n"
            
            # Add score details with descriptions
            if model and hasattr(model, 'factors') and hasattr(model, 'score_options'):
                report_text += f"|    Factor Scores:\n"
                for factor, score in test['scores'].items():
                    if factor in model.factors and score in model.score_options.get(factor, {}):
                        factor_name = model.factors[factor]["name"]
                        score_description = model.score_options[factor][score]
                        report_text += f"|      - {factor_name}: {score} - {score_description}\n"
            
            # Add yes/no answers if available
            if 'yes_no_answers' in test:
                for key, answer in test['yes_no_answers'].items():
                    report_text += f"|    * {key}: {answer}\n"
            
            report_text += "|\n"
        
        report_text += "-" * 70 + "\n"
        
        report_text += "\n"
        
        # Can't Automate section
        if cant_automate:
            report_text += f"TESTS THAT CAN'T BE AUTOMATED:\n"
            report_text += f"These tests have been identified as not possible to automate\n"
            report_text += "-" * 70 + "\n"
            
            for i, test in enumerate(cant_automate):
                report_text += f"| {i+1}. {test['name']} (ID: {test['id']})\n"
                
                # Add section if available
                if test.get("section"):
                    report_text += f"|    Section: {test['section']}\n"
                
                # Add description if available
                if 'description' in test:
                    report_text += f"|    Description: {test['description']}\n"
                
                # Add score details with descriptions
                if model and hasattr(model, 'factors') and hasattr(model, 'score_options'):
                    report_text += f"|    Factor Scores:\n"
                    # First show the "Can it be automated?" factor to explain why it's in this category
                    if "can_be_automated" in test['scores'] and test['scores']["can_be_automated"] == 1:
                        factor_name = model.factors["can_be_automated"]["name"]
                        score_description = model.score_options["can_be_automated"][1]
                        report_text += f"|      - {factor_name}: 1 - {score_description}\n"
                        
                    # Then show other factors
                    for factor, score in test['scores'].items():
                        if factor != "can_be_automated" and factor in model.factors and score in model.score_options.get(factor, {}):
                            factor_name = model.factors[factor]["name"]
                            score_description = model.score_options[factor][score]
                            report_text += f"|      - {factor_name}: {score} - {score_description}\n"
                
                # Add yes/no answers if available
                if 'yes_no_answers' in test:
                    for key, answer in test['yes_no_answers'].items():
                        report_text += f"|    * {key}: {answer}\n"
                
                report_text += "|\n"
            
            report_text += "-" * 70 + "\n"
            
        # Add section breakdown report
        if len(sections) > 1:  # Only add section breakdown if there's more than one section
            report_text += "\n"
            report_text += "SECTION BREAKDOWN:\n"
            report_text += "-" * 70 + "\n"
            
            for section_name, section_tests in sorted(sections.items()):
                # Skip empty section name
                if not section_name:
                    continue
                    
                # Count tests by priority in this section
                priority_counts = {"Highest": 0, "High": 0, "Medium": 0, "Low": 0, "Lowest": 0, "Can't Automate": 0}
                for test in section_tests:
                    priority = test.get("priority", "")
                    if priority in priority_counts:
                        priority_counts[priority] += 1
                
                report_text += f"Section: {section_name}\n"
                report_text += f"Total Tests: {len(section_tests)}\n"
                report_text += "Priority Distribution:\n"
                for priority, count in priority_counts.items():
                    if count > 0:
                        report_text += f"  - {priority}: {count} tests\n"
                report_text += "\n"
            
            report_text += "-" * 70 + "\n"
        
        return report_text
    
    @staticmethod
    def generate_markdown_report(tests, priority_tiers, model=None):
        """
        Generate markdown text for the prioritization report
        
        Args:
            tests (list): List of all test dictionaries
            priority_tiers (dict): Dictionary with priority tier tests
            model: The prioritization model
            
        Returns:
            str: Formatted markdown report text
        """
        from datetime import datetime
        
        # Report header
        header = f"# TEST AUTOMATION PRIORITY REPORT\n\n"
        header += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        header += f"**Total Tests:** {len(tests)}\n"
        
        # Group tests by section
        sections = {}
        for test in tests:
            section = test.get("section", "")
            if section not in sections:
                sections[section] = []
            sections[section].append(test)
        
        if sections:
            header += f"**Sections:** {len(sections)}\n"
        
        header += "\n---\n\n"
        
        report_text = header
        
        # Get the tiers
        highest_priority = priority_tiers["highest"]
        high_priority = priority_tiers["high"]
        medium_priority = priority_tiers["medium"]
        low_priority = priority_tiers["low"]
        lowest_priority = priority_tiers["lowest"]
        cant_automate = priority_tiers.get("cant_automate", [])

        highest_threshold = priority_tiers["highest_threshold"]
        high_threshold = priority_tiers["high_threshold"]
        medium_threshold = priority_tiers["medium_threshold"]
        low_threshold = priority_tiers["low_threshold"]
        lowest_threshold = priority_tiers["lowest_threshold"]

        # Highest priority section
        report_text += f"## 🔴 HIGHEST PRIORITY TESTS (Score >= {highest_threshold:.1f})\n\n"
        report_text += f"*Recommended for immediate automation*\n\n"
        
        if highest_priority:
            for i, test in enumerate(highest_priority):
                report_text += f"### {i+1}. {test['name']}\n"
                report_text += f"**Score:** {test['total_score']:.1f}\n"
                report_text += f"**Ticket:** {test['ticket_id']}\n"

                # Add section if available
                if test.get("section"):
                    report_text += f"**Section:** {test['section']}\n"

                # Add description if available
                if test.get('description'):
                    report_text += f"**Description:** {test['description']}\n"
                
                # Add score details with descriptions
                if model and hasattr(model, 'factors') and hasattr(model, 'score_options'):
                    report_text += f"**Factor Scores:**\n"
                    for factor, score in test['scores'].items():
                        if factor in model.factors and score in model.score_options.get(factor, {}):
                            factor_name = model.factors[factor]["name"]
                            score_description = model.score_options[factor][score]
                            report_text += f"* **{factor_name}**: {score} - {score_description}\n"
                
                # Add yes/no answers if available
                if test.get('yes_no_answers'):
                    for key, answer in test['yes_no_answers'].items():
                        report_text += f"* **{key}**: {answer}\n"
                
                report_text += "\n"
        else:
            report_text += "*No tests in this category*\n\n"
        
        report_text += "---\n\n"
        
        # High priority section
        report_text += f"## 🟠 HIGH PRIORITY TESTS (Score {high_threshold:.1f} - {highest_threshold:.1f})\n\n"
        report_text += f"*Recommended for second phase automation*\n\n"
        
        if high_priority:
            for i, test in enumerate(high_priority):
                report_text += f"### {i+1}. {test['name']}\n"
                report_text += f"**Score:** {test['total_score']:.1f}\n"
                report_text += f"**Ticket:** {test['ticket_id']}\n"

                # Add section if available
                if test.get("section"):
                    report_text += f"**Section:** {test['section']}\n"

                # Add description if available
                if test.get('description'):
                    report_text += f"**Description:** {test['description']}\n"
                
                # Add score details with descriptions
                if model and hasattr(model, 'factors') and hasattr(model, 'score_options'):
                    report_text += f"**Factor Scores:**\n"
                    for factor, score in test['scores'].items():
                        if factor in model.factors and score in model.score_options.get(factor, {}):
                            factor_name = model.factors[factor]["name"]
                            score_description = model.score_options[factor][score]
                            report_text += f"* **{factor_name}**: {score} - {score_description}\n"
                
                # Add yes/no answers if available
                if test.get('yes_no_answers'):
                    for key, answer in test['yes_no_answers'].items():
                        report_text += f"* **{key}**: {answer}\n"
                
                report_text += "\n"
        else:
            report_text += "*No tests in this category*\n\n"
        
        report_text += "---\n\n"
        
        # Medium priority section
        report_text += f"## 🟡 MEDIUM PRIORITY TESTS (Score {medium_threshold:.1f} - {high_threshold:.1f})\n\n"
        report_text += f"*Recommended for third phase automation*\n\n"
        
        if medium_priority:
            for i, test in enumerate(medium_priority):
                report_text += f"### {i+1}. {test['name']}\n"
                report_text += f"**Score:** {test['total_score']:.1f}\n"
                report_text += f"**Ticket:** {test['ticket_id']}\n"

                # Add section if available
                if test.get("section"):
                    report_text += f"**Section:** {test['section']}\n"

                # Add description if available
                if test.get('description'):
                    report_text += f"**Description:** {test['description']}\n"
                
                # Add score details with descriptions
                if model and hasattr(model, 'factors') and hasattr(model, 'score_options'):
                    report_text += f"**Factor Scores:**\n"
                    for factor, score in test['scores'].items():
                        if factor in model.factors and score in model.score_options.get(factor, {}):
                            factor_name = model.factors[factor]["name"]
                            score_description = model.score_options[factor][score]
                            report_text += f"* **{factor_name}**: {score} - {score_description}\n"
                
                # Add yes/no answers if available
                if test.get('yes_no_answers'):
                    for key, answer in test['yes_no_answers'].items():
                        report_text += f"* **{key}**: {answer}\n"
                
                report_text += "\n"
        else:
            report_text += "*No tests in this category*\n\n"
        
        report_text += "---\n\n"
        
        # Low priority section
        report_text += f"## 🔵 LOW PRIORITY TESTS (Score {low_threshold:.1f} - {medium_threshold:.1f})\n\n"
        report_text += f"*Consider for later phases or keep as manual tests*\n\n"
        
        if low_priority:
            for i, test in enumerate(low_priority):
                report_text += f"### {i+1}. {test['name']}\n"
                report_text += f"**Score:** {test['total_score']:.1f}\n"
                report_text += f"**Ticket:** {test['ticket_id']}\n"

                # Add section if available
                if test.get("section"):
                    report_text += f"**Section:** {test['section']}\n"

                # Add description if available
                if test.get('description'):
                    report_text += f"**Description:** {test['description']}\n"
                
                # Add score details with descriptions
                if model and hasattr(model, 'factors') and hasattr(model, 'score_options'):
                    report_text += f"**Factor Scores:**\n"
                    for factor, score in test['scores'].items():
                        if factor in model.factors and score in model.score_options.get(factor, {}):
                            factor_name = model.factors[factor]["name"]
                            score_description = model.score_options[factor][score]
                            report_text += f"* **{factor_name}**: {score} - {score_description}\n"
                
                # Add yes/no answers if available
                if test.get('yes_no_answers'):
                    for key, answer in test['yes_no_answers'].items():
                        report_text += f"* **{key}**: {answer}\n"
                
                report_text += "\n"
        else:
            report_text += "*No tests in this category*\n\n"
        
        report_text += "---\n\n"
        
        # Lowest priority section
        report_text += f"## 🔷 LOWEST PRIORITY TESTS (Score <= {low_threshold:.1f})\n\n"
        report_text += f"*Not Recommended for automation*\n\n"
        
        if lowest_priority:
            for i, test in enumerate(lowest_priority):
                report_text += f"### {i+1}. {test['name']}\n"
                report_text += f"**Score:** {test['total_score']:.1f}\n"
                report_text += f"**Ticket:** {test['ticket_id']}\n"

                # Add section if available
                if test.get("section"):
                    report_text += f"**Section:** {test['section']}\n"

                # Add description if available
                if test.get('description'):
                    report_text += f"**Description:** {test['description']}\n"
                
                # Add score details with descriptions
                if model and hasattr(model, 'factors') and hasattr(model, 'score_options'):
                    report_text += f"**Factor Scores:**\n"
                    for factor, score in test['scores'].items():
                        if factor in model.factors and score in model.score_options.get(factor, {}):
                            factor_name = model.factors[factor]["name"]
                            score_description = model.score_options[factor][score]
                            report_text += f"* **{factor_name}**: {score} - {score_description}\n"
                
                # Add yes/no answers if available
                if test.get('yes_no_answers'):
                    for key, answer in test['yes_no_answers'].items():
                        report_text += f"* **{key}**: {answer}\n"
                
                report_text += "\n"
        else:
            report_text += "*No tests in this category*\n\n"
        
        report_text += "---\n\n"
        
        # Can't Automate section
        if cant_automate:
            report_text += f"## ⚪ TESTS THAT CAN'T BE AUTOMATED\n\n"
            report_text += f"*These tests have been identified as not possible to automate*\n\n"
            
            for i, test in enumerate(cant_automate):
                report_text += f"### {i+1}. {test['name']}\n"
                report_text += f"**Ticket:** {test['ticket_id']}\n"
                
                # Add section if available
                if test.get("section"):
                    report_text += f"**Section:** {test['section']}\n"
                
                # Add description if available
                if test.get('description'):
                    report_text += f"**Description:** {test['description']}\n"
                
                # Add score details with descriptions
                if model and hasattr(model, 'factors') and hasattr(model, 'score_options'):
                    report_text += f"**Factor Scores:**\n"
                    # First show the "Can it be automated?" factor to explain why it's in this category
                    if "can_be_automated" in test['scores'] and test['scores']["can_be_automated"] == 1:
                        factor_name = model.factors["can_be_automated"]["name"]
                        score_description = model.score_options["can_be_automated"][1]
                        report_text += f"* **{factor_name}**: 1 - {score_description}\n"
                        
                    # Then show other factors
                    for factor, score in test['scores'].items():
                        if factor != "can_be_automated" and factor in model.factors and score in model.score_options.get(factor, {}):
                            factor_name = model.factors[factor]["name"]
                            score_description = model.score_options[factor][score]
                            report_text += f"* **{factor_name}**: {score} - {score_description}\n"
                
                # Add yes/no answers if available
                if test.get('yes_no_answers'):
                    for key, answer in test['yes_no_answers'].items():
                        report_text += f"* **{key}**: {answer}\n"
                
                report_text += "\n"
            
            report_text += "---\n\n"
        
        # Add section breakdown report
        if len(sections) > 1:  # Only add section breakdown if there's more than one section
            report_text += "## SECTION BREAKDOWN\n\n"
            
            for section_name, section_tests in sorted(sections.items()):
                # Skip empty section name
                if not section_name:
                    continue
                    
                # Count tests by priority in this section
                priority_counts = {"Highest": 0, "High": 0, "Medium": 0, "Low": 0, "Lowest": 0, "Can't Automate": 0}
                for test in section_tests:
                    priority = test.get("priority", "")
                    if priority in priority_counts:
                        priority_counts[priority] += 1
                
                report_text += f"### Section: {section_name}\n"
                report_text += f"**Total Tests:** {len(section_tests)}\n"
                report_text += "**Priority Distribution:**\n"
                for priority, count in priority_counts.items():
                    if count > 0:
                        # Add emoji based on priority
                        emoji = ""
                        if priority == "Highest":
                            emoji = "🔴"
                        elif priority == "High":
                            emoji = "🟠"
                        elif priority == "Medium":
                            emoji = "🟡"
                        elif priority == "Low":
                            emoji = "🔵"
                        elif priority == "Lowest":
                            emoji = "🔷"
                        elif priority == "Can't Automate":
                            emoji = "⚪"
                        
                        report_text += f"* {emoji} **{priority}**: {count} tests\n"
                report_text += "\n"
            
            report_text += "---\n\n"
        
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
        guide += "2. These weighted scores are summed to get a raw score\n"
        guide += "3. The raw score is converted to a 100-point scale\n\n"
        guide += "Formula: Final Score = (Raw Score / Max Possible Raw Score) × 100\n\n"
        
        # Skip the "can_be_automated" factor (which has weight 0) when calculating max possible score
        max_possible_raw = sum(5 * details["weight"] for factor, details in factors.items() 
                            if factor != "can_be_automated")
        guide += f"Maximum possible raw score: {max_possible_raw}\n"
        guide += "Maximum possible final score: 100\n"
        guide += f"Minimum possible raw score: {sum(1 * details['weight'] for factor, details in factors.items() if factor != 'can_be_automated')}\n"
        guide += "Minimum possible final score: 20\n\n"
        
        # Special note for "Can it be automated?" factor
        if "can_be_automated" in factors:
            guide += "Special Case - Tests that cannot be automated:\n"
            guide += "-" * 50 + "\n"
            guide += "If a test is marked as 'Cannot be automated' (selecting 'No' for the\n"
            guide += "'Can it be automated?' factor), it will automatically receive:\n"
            guide += "  - A score of 0\n"
            guide += "  - Priority category of 'Can't Automate'\n"
            guide += "These tests are excluded from normal prioritization and shown separately.\n\n"
        
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
        
    @staticmethod
    def export_report_to_html(report_text, filename):
        """
        Export markdown report to HTML file
        
        Args:
            report_text (str): Markdown formatted report text
            filename (str): Path to the output HTML file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Try to import markdown module
            try:
                import markdown
                has_markdown = True
            except ImportError:
                has_markdown = False
                
            if has_markdown:
                # Convert markdown to HTML using the markdown library
                html_content = markdown.markdown(report_text)
                
                # Add some basic styling
                styled_html = f"""<!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Test Automation Priority Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; max-width: 900px; margin: 0 auto; padding: 20px; }}
            h1 {{ color: #2c3e50; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
            h2 {{ color: #3498db; margin-top: 30px; border-top: 1px solid #eee; padding-top: 20px; }}
            h3 {{ color: #2980b9; }}
            hr {{ border: 0; height: 1px; background: #eee; margin: 30px 0; }}
            ul {{ margin-left: 20px; }}
            li {{ margin-bottom: 5px; }}
            code {{ background: #f8f8f8; padding: 2px 4px; border-radius: 4px; }}
            strong {{ color: #333; }}
            em {{ color: #444; }}
        </style>
    </head>
    <body>
    {html_content}
    </body>
    </html>"""
                
                # Write to file
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(styled_html)
            else:
                # Fallback to basic HTML conversion
                html_lines = []
                html_lines.append("<!DOCTYPE html>")
                html_lines.append("<html><head><meta charset='UTF-8'>")
                html_lines.append("<title>Test Automation Priority Report</title>")
                html_lines.append("<style>")
                html_lines.append("body { font-family: Arial, sans-serif; line-height: 1.6; max-width: 900px; margin: 0 auto; padding: 20px; }")
                html_lines.append("h1 { color: #2c3e50; border-bottom: 2px solid #eee; padding-bottom: 10px; }")
                html_lines.append("h2 { color: #3498db; margin-top: 30px; border-top: 1px solid #eee; padding-top: 20px; }")
                html_lines.append("h3 { color: #2980b9; }")
                html_lines.append("hr { border: 0; height: 1px; background: #eee; margin: 30px 0; }")
                html_lines.append("</style></head><body>")
                
                # Very basic markdown to HTML conversion
                in_list = False
                for line in report_text.split('\n'):
                    # Handle empty lines
                    if not line.strip():
                        if in_list:
                            html_lines.append("</ul>")
                            in_list = False
                        html_lines.append("<br>")
                        continue
                    
                    # Handle headings
                    if line.startswith('# '):
                        html_lines.append(f"<h1>{line[2:]}</h1>")
                    elif line.startswith('## '):
                        html_lines.append(f"<h2>{line[3:]}</h2>")
                    elif line.startswith('### '):
                        html_lines.append(f"<h3>{line[4:]}</h3>")
                    # Handle lists
                    elif line.startswith('* '):
                        if not in_list:
                            html_lines.append("<ul>")
                            in_list = True
                        html_lines.append(f"<li>{line[2:]}</li>")
                    # Handle horizontal rules
                    elif line.startswith('---'):
                        if in_list:
                            html_lines.append("</ul>")
                            in_list = False
                        html_lines.append("<hr>")
                    # Handle normal text, preserving bold and italic
                    else:
                        if in_list:
                            html_lines.append("</ul>")
                            in_list = False
                        
                        # Replace ** with <strong> tags
                        processed_line = ""
                        bold_parts = line.split('**')
                        for i, part in enumerate(bold_parts):
                            if i % 2 == 1:  # Odd indices are bold
                                processed_line += f"<strong>{part}</strong>"
                            else:
                                processed_line += part
                        
                        # Replace * with <em> tags (for italic)
                        final_line = ""
                        italic_parts = processed_line.split('*')
                        if len(italic_parts) > 1:  # Only process if there are asterisks
                            for i, part in enumerate(italic_parts):
                                if i % 2 == 1:  # Odd indices are italic
                                    final_line += f"<em>{part}</em>"
                                else:
                                    final_line += part
                        else:
                            final_line = processed_line
                        
                        html_lines.append(f"<p>{final_line}</p>")
                
                # Close any open lists and the HTML document
                if in_list:
                    html_lines.append("</ul>")
                html_lines.append("</body></html>")
                
                # Write to file
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(html_lines))
            
            return True
        except Exception as e:
            print(f"HTML export error: {str(e)}")
            return False, str(e)

    @staticmethod
    def export_report_to_docx(report_text, filename):
        """
        Export markdown report to Word (.docx) file
        
        Args:
            report_text (str): Markdown formatted report text
            filename (str): Path to the output .docx file
            
        Returns:
            tuple: (success, error_message)
                success (bool): True if successful, False otherwise
                error_message (str): Error message if unsuccessful, None otherwise
        """
        try:
            # Try to import python-docx module
            try:
                import docx
                from docx.shared import Pt, RGBColor
                from docx.enum.text import WD_ALIGN_PARAGRAPH
                has_docx = True
            except ImportError:
                has_docx = False
                
            if not has_docx:
                return False, "python-docx module not installed. Install it with 'pip install python-docx'"
            
            # Create a new document
            doc = docx.Document()
            
            # Define styles for different heading levels and text
            styles = {
                'title': {'size': 16, 'bold': True, 'color': RGBColor(44, 62, 80)},
                'heading1': {'size': 14, 'bold': True, 'color': RGBColor(52, 152, 219)},
                'heading2': {'size': 12, 'bold': True, 'color': RGBColor(41, 128, 185)},
                'heading3': {'size': 11, 'bold': True, 'color': RGBColor(36, 113, 163)},
                'normal': {'size': 10, 'bold': False, 'color': RGBColor(0, 0, 0)},
                'emphasis': {'size': 10, 'bold': False, 'italic': True, 'color': RGBColor(0, 0, 0)},
                'strong': {'size': 10, 'bold': True, 'color': RGBColor(0, 0, 0)}
            }
            
            # Process markdown line by line
            lines = report_text.split('\n')
            in_list = False
            list_items = []
            
            for line in lines:
                # Skip empty lines
                if not line.strip():
                    if in_list:
                        # End current list
                        for item in list_items:
                            p = doc.add_paragraph(style='List Bullet')
                            p.add_run(item)
                        list_items = []
                        in_list = False
                    doc.add_paragraph()
                    continue
                
                # Handle headings
                if line.startswith('# '):
                    if in_list:
                        # End current list
                        for item in list_items:
                            p = doc.add_paragraph(style='List Bullet')
                            p.add_run(item)
                        list_items = []
                        in_list = False
                        
                    p = doc.add_paragraph()
                    run = p.add_run(line[2:])
                    font = run.font
                    font.size = Pt(styles['title']['size'])
                    font.bold = styles['title']['bold']
                    font.color.rgb = styles['title']['color']
                    
                elif line.startswith('## '):
                    if in_list:
                        # End current list
                        for item in list_items:
                            p = doc.add_paragraph(style='List Bullet')
                            p.add_run(item)
                        list_items = []
                        in_list = False
                        
                    p = doc.add_paragraph()
                    run = p.add_run(line[3:])
                    font = run.font
                    font.size = Pt(styles['heading1']['size'])
                    font.bold = styles['heading1']['bold']
                    font.color.rgb = styles['heading1']['color']
                    
                elif line.startswith('### '):
                    if in_list:
                        # End current list
                        for item in list_items:
                            p = doc.add_paragraph(style='List Bullet')
                            p.add_run(item)
                        list_items = []
                        in_list = False
                        
                    p = doc.add_paragraph()
                    run = p.add_run(line[4:])
                    font = run.font
                    font.size = Pt(styles['heading2']['size'])
                    font.bold = styles['heading2']['bold']
                    font.color.rgb = styles['heading2']['color']
                    
                # Handle horizontal rule
                elif line.startswith('---'):
                    if in_list:
                        # End current list
                        for item in list_items:
                            p = doc.add_paragraph(style='List Bullet')
                            p.add_run(item)
                        list_items = []
                        in_list = False
                        
                    p = doc.add_paragraph('_' * 50)
                    
                # Handle list items
                elif line.startswith('* '):
                    in_list = True
                    list_items.append(line[2:])
                    
                # Handle normal paragraphs
                else:
                    if in_list:
                        # End current list
                        for item in list_items:
                            p = doc.add_paragraph(style='List Bullet')
                            p.add_run(item)
                        list_items = []
                        in_list = False
                    
                    # Handle bold and italic formatting
                    p = doc.add_paragraph()
                    
                    # Replace emojis with their names
                    line = (line.replace('🔴', '[HIGHEST] ')
                            .replace('🟠', '[HIGH] ')
                            .replace('🟡', '[MEDIUM] ')
                            .replace('🔵', '[LOW] ')
                            .replace('🔷', '[LOWEST] ')
                            .replace('⚪', '[NOT AUTOMATABLE] '))
                    
                    # Process bold sections
                    parts = line.split('**')
                    for i, part in enumerate(parts):
                        if i % 2 == 1:  # Bold text (odd indices)
                            run = p.add_run(part)
                            font = run.font
                            font.bold = True
                        else:  # Normal text (even indices)
                            # Process italic sections within normal text
                            italic_parts = part.split('*')
                            for j, italic_part in enumerate(italic_parts):
                                if j % 2 == 1:  # Italic text (odd indices)
                                    run = p.add_run(italic_part)
                                    font = run.font
                                    font.italic = True
                                else:  # Regular text (even indices)
                                    if italic_part:
                                        run = p.add_run(italic_part)
            
            # End any open list
            if in_list:
                for item in list_items:
                    p = doc.add_paragraph(style='List Bullet')
                    p.add_run(item)
            
            # Save the document
            doc.save(filename)
            return True, None
            
        except Exception as e:
            print(f"Word export error: {str(e)}")
            return False, str(e)