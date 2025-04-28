"""
markdown_report.py - Markdown report generator for test prioritization
"""
from datetime import datetime
from .base_report import BaseReportGenerator

class MarkdownReportGenerator(BaseReportGenerator):
    """
    Handles markdown report generation for the test prioritization application
    """

    @staticmethod
    def generate_report(tests, priority_tiers, model=None):
        """
        Generate markdown text for the prioritization report
        
        Args:
            tests (list): List of all test dictionaries
            priority_tiers (dict): Dictionary with priority tier tests
            model: The prioritization model
            
        Returns:
            str: Formatted markdown report text
        """
        # Report header
        header = f"# TEST AUTOMATION PRIORITY REPORT\n\n"
        header += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        header += f"**Total Tests:** {len(tests)}\n"
        
        # Group tests by section
        sections = BaseReportGenerator.group_tests_by_section(tests)
        
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
        wont_automate = priority_tiers.get("wont_automate", [])

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
        
        # Won't Automate section
        if wont_automate:
            report_text += f"## ⚪ TESTS THAT WON'T BE AUTOMATED\n\n"
            report_text += f"*These tests have been identified as not worth  automating yet*\n\n"
            
            for i, test in enumerate(wont_automate):
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
                priority_counts = {"Highest": 0, "High": 0, "Medium": 0, "Low": 0, "Lowest": 0, "Won't Automate": 0}
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
                        elif priority == "Won't Automate":
                            emoji = "⚪"
                        
                        report_text += f"* {emoji} **{priority}**: {count} tests\n"
                report_text += "\n"
            
            report_text += "---\n\n"
        
        return report_text

    @staticmethod
    def generate_enhanced_report(tests, priority_tiers, model=None):
        """
        Generate enhanced markdown text with better HTML compatibility
        
        Args:
            tests (list): List of all test dictionaries
            priority_tiers (dict): Dictionary with priority tier tests
            model: The prioritization model
                
        Returns:
            str: Formatted markdown report text with HTML enhancements
        """
        # Report header
        header = f"# TEST AUTOMATION PRIORITY REPORT\n\n"
        header += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        header += f"**Total Tests:** {len(tests)}\n"
        
        # Group tests by section
        sections = BaseReportGenerator.group_tests_by_section(tests)
        
        if sections:
            header += f"**Sections:** {len(sections)}\n"
        
        header += "\n---\n\n"
        
        # Add priority distribution summary
        highest_count = len(priority_tiers["highest"])
        high_count = len(priority_tiers["high"])
        medium_count = len(priority_tiers["medium"])
        low_count = len(priority_tiers["low"])
        lowest_count = len(priority_tiers["lowest"])
        wont_automate_count = len(priority_tiers.get("wont_automate", []))
        
        summary = "## Priority Distribution Summary\n\n"
        summary += "<div class='summary'>\n"
        summary += "<div class='summary-grid'>\n"
        summary += f"<div class='summary-item highest'><div class='summary-count'>{highest_count}</div><div class='summary-label'>Highest</div></div>\n"
        summary += f"<div class='summary-item high'><div class='summary-count'>{high_count}</div><div class='summary-label'>High</div></div>\n"
        summary += f"<div class='summary-item medium'><div class='summary-count'>{medium_count}</div><div class='summary-label'>Medium</div></div>\n"
        summary += f"<div class='summary-item low'><div class='summary-count'>{low_count}</div><div class='summary-label'>Low</div></div>\n"
        summary += f"<div class='summary-item lowest'><div class='summary-count'>{lowest_count}</div><div class='summary-label'>Lowest</div></div>\n"
        summary += f"<div class='summary-item wont-automate'><div class='summary-count'>{wont_automate_count}</div><div class='summary-label'>Won't Automate</div></div>\n"
        summary += "</div>\n</div>\n\n"
        
        report_text = header + summary
        
        # Get the tiers
        highest_priority = priority_tiers["highest"]
        high_priority = priority_tiers["high"]
        medium_priority = priority_tiers["medium"]
        low_priority = priority_tiers["low"]
        lowest_priority = priority_tiers["lowest"]
        wont_automate = priority_tiers.get("wont_automate", [])

        highest_threshold = priority_tiers["highest_threshold"]
        high_threshold = priority_tiers["high_threshold"]
        medium_threshold = priority_tiers["medium_threshold"]
        low_threshold = priority_tiers["low_threshold"]
        lowest_threshold = priority_tiers["lowest_threshold"]

        # Highest priority section
        report_text += f"## <div class='section-header section-highest'>🔴 HIGHEST PRIORITY TESTS (Score >= {highest_threshold:.1f})</div>\n\n"
        report_text += f"*Recommended for immediate automation*\n\n"
        
        if highest_priority:
            for i, test in enumerate(highest_priority):
                report_text += MarkdownReportGenerator.generate_test_card(test, i+1, "highest", model)
        else:
            report_text += "*No tests in this category*\n\n"
        
        report_text += "---\n\n"
        
        # High priority section
        report_text += f"## <div class='section-header section-high'>🟠 HIGH PRIORITY TESTS (Score {high_threshold:.1f} - {highest_threshold:.1f})</div>\n\n"
        report_text += f"*Recommended for second phase automation*\n\n"
        
        if high_priority:
            for i, test in enumerate(high_priority):
                report_text += MarkdownReportGenerator.generate_test_card(test, i+1, "high", model)
        else:
            report_text += "*No tests in this category*\n\n"
        
        report_text += "---\n\n"
        
        # Medium priority section
        report_text += f"## <div class='section-header section-medium'>🟡 MEDIUM PRIORITY TESTS (Score {medium_threshold:.1f} - {high_threshold:.1f})</div>\n\n"
        report_text += f"*Recommended for third phase automation*\n\n"
        
        if medium_priority:
            for i, test in enumerate(medium_priority):
                report_text += MarkdownReportGenerator.generate_test_card(test, i+1, "medium", model)
        else:
            report_text += "*No tests in this category*\n\n"
        
        report_text += "---\n\n"
        
        # Low priority section
        report_text += f"## <div class='section-header section-low'>🔵 LOW PRIORITY TESTS (Score {low_threshold:.1f} - {medium_threshold:.1f})</div>\n\n"
        report_text += f"*Consider for later phases or keep as manual tests*\n\n"
        
        if low_priority:
            for i, test in enumerate(low_priority):
                report_text += MarkdownReportGenerator.generate_test_card(test, i+1, "low", model)
        else:
            report_text += "*No tests in this category*\n\n"
        
        report_text += "---\n\n"
        
        # Lowest priority section
        report_text += f"## <div class='section-header section-lowest'>🔷 LOWEST PRIORITY TESTS (Score <= {low_threshold:.1f})</div>\n\n"
        report_text += f"*Not Recommended for automation*\n\n"
        
        if lowest_priority:
            for i, test in enumerate(lowest_priority):
                report_text += MarkdownReportGenerator.generate_test_card(test, i+1, "lowest", model)
        else:
            report_text += "*No tests in this category*\n\n"
        
        report_text += "---\n\n"
        
        # Won't Automate section
        if wont_automate:
            report_text += f"## <div class='section-header section-wontt-automate'>⚪ TESTS THAT WON'T BE AUTOMATED</div>\n\n"
            report_text += f"*These tests have been identified as not possible to automate*\n\n"
            
            for i, test in enumerate(wont_automate):
                report_text += MarkdownReportGenerator.generate_test_card(test, i+1, "wont-automate", model)
            
            report_text += "---\n\n"
        
        # Add section breakdown report
        if len(sections) > 1:  # Only add section breakdown if there's more than one section
            report_text += "## SECTION BREAKDOWN\n\n"
            
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
                
                report_text += f"<div class='breakdown-item'>\n"
                report_text += f"<div class='breakdown-title'>Section: {section_name}</div>\n"
                report_text += f"<p><strong>Total Tests:</strong> {len(section_tests)}</p>\n"
                report_text += "<div class='breakdown-stats'>\n"
                
                # Add emoji based on priority
                for priority, count in priority_counts.items():
                    if count > 0:
                        # Convert priority name to lowercase for CSS class
                        class_name = priority.lower().replace("'", "").replace(" ", "-")
                        
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
                        elif priority == "Won't Automate":
                            emoji = "⚪"
                        
                        report_text += f"<span class='stat-pill {class_name}'>{emoji} {priority}: {count} tests</span>\n"
                
                report_text += "</div>\n</div>\n\n"
        
        return report_text

    @staticmethod
    def generate_test_card(test, index, css_class, model):
        """
        Generate a markdown card for a test with HTML classes
        
        Args:
            test (dict): Test dictionary
            index (int): Index/rank of the test
            css_class (str): CSS class for styling
            model: The prioritization model
            
        Returns:
            str: Markdown text for the test card
        """
        card = f"<div class='test-card {css_class}'>\n"
        card += f"### {index}. {test['name']}\n"
        card += f"**Score:** {test['total_score']:.1f}\n"
        card += f"**Ticket:** {test['ticket_id']}\n"

        # Add section if available
        if test.get("section"):
            card += f"**Section:** {test['section']}\n"

        # Add description if available
        if test.get('description'):
            card += f"**Description:** {test['description']}\n"
        
        # Add score details with descriptions
        if model and hasattr(model, 'factors') and hasattr(model, 'score_options'):
            card += f"**Factor Scores:**\n"
            
            # Show "Can it be automated?" factor first for Won't Automate tests
            if test['priority'] == "Won't Automate" and "can_be_automated" in test['scores'] and test['scores']["can_be_automated"] == 1:
                factor_name = model.factors["can_be_automated"]["name"]
                score_description = model.score_options["can_be_automated"][1]
                card += f"* **{factor_name}**: 1 - {score_description}\n"
            
            # Show other factors
            for factor, score in test['scores'].items():
                # Skip can_be_automated if we already showed it
                if factor == "can_be_automated" and test['priority'] == "Won't Automate":
                    continue
                    
                if factor in model.factors and score in model.score_options.get(factor, {}):
                    factor_name = model.factors[factor]["name"]
                    score_description = model.score_options[factor][score]
                    card += f"* **{factor_name}**: {score} - {score_description}\n"
        
        # Add yes/no answers if available
        if test.get('yes_no_answers'):
            for key, answer in test['yes_no_answers'].items():
                card += f"* **{key}**: {answer}\n"
        
        card += "</div>\n\n"
        return card