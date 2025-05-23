"""
text_report.py - Handles text report generation
"""
from datetime import datetime

class TextReportGenerator:
    """
    Handles text report generation for the test prioritization application
    """
    
    @staticmethod
    def generate_report(tests, priority_tiers, model=None):
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
        wont_automate = priority_tiers.get("wont_automate", [])  # Get "Won't Automate" tests if available

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
        
        # Won't Automate section
        if wont_automate:
            report_text += f"TESTS THAT WON'T BE AUTOMATED:\n"
            report_text += f"These tests have been identified as not willing to automate\n"
            report_text += "-" * 70 + "\n"
            
            for i, test in enumerate(wont_automate):
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
                priority_counts = {"Highest": 0, "High": 0, "Medium": 0, "Low": 0, "Lowest": 0, "Won't Automate": 0}
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
    def export_to_file(filename, report_text):
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
    def generate_scoring_guide(factors, score_options):
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
            guide += "If a test is marked as 'Won't be automated' (selecting 'No' for the\n"
            guide += "'Can it be automated?' factor), it will automatically receive:\n"
            guide += "  - A score of 0\n"
            guide += "  - Priority category of 'Won't Automate'\n"
            guide += "These tests are excluded from normal prioritization and shown separately.\n\n"
        
        return guide