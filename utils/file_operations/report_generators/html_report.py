"""
html_report.py - HTML report generator for test prioritization
"""
from datetime import datetime
from .base_report import BaseReportGenerator

class HTMLReportGenerator(BaseReportGenerator):
    """
    Handles HTML report generation for the test prioritization application
    """

    @staticmethod
    def export_report(tests, priority_tiers, model, filename):
        """
        Export tests as a modern HTML report
        
        Args:
            tests (list): List of test dictionaries
            priority_tiers (dict): Dictionary with priority tier tests
            model: The prioritization model
            filename (str): Path to the output HTML file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Count tests by priority
            priority_counts = {
                "Highest": len(priority_tiers["highest"]),
                "High": len(priority_tiers["high"]),
                "Medium": len(priority_tiers["medium"]),
                "Low": len(priority_tiers["low"]),
                "Lowest": len(priority_tiers["lowest"]),
                "Can't Automate": len(priority_tiers.get("cant_automate", []))
            }
            
            # Get thresholds
            highest_threshold = priority_tiers["highest_threshold"]
            high_threshold = priority_tiers["high_threshold"]
            medium_threshold = priority_tiers["medium_threshold"]
            low_threshold = priority_tiers["low_threshold"]
            
            # Generate full HTML content
            html = HTMLReportGenerator._generate_html_content(
                tests,
                priority_tiers,
                model,
                priority_counts,
                highest_threshold,
                high_threshold,
                medium_threshold,
                low_threshold
            )
            
            # Write to file with UTF-8 encoding
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html)
            
            return True
        
        except Exception as e:
            print(f"HTML export error: {e}")
            return False

    @staticmethod
    def _generate_html_content(tests, priority_tiers, model, priority_counts, 
                                highest_threshold, high_threshold, medium_threshold, low_threshold):
        """
        Generate the complete HTML content
        
        Args:
            tests (list): List of test dictionaries
            priority_tiers (dict): Dictionary with priority tier tests
            model: The prioritization model
            priority_counts (dict): Count of tests by priority
            highest_threshold (float): Threshold for highest priority
            high_threshold (float): Threshold for high priority
            medium_threshold (float): Threshold for medium priority
            low_threshold (float): Threshold for low priority
            
        Returns:
            str: Complete HTML content
        """
        html = f"""<!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Automation Priority Report</title>
    {HTMLReportGenerator._generate_css_styles()}
    </head>
    <body>
    <header>
        <div class="container">
            <div class="header-content">
                <h1>Test Automation Priority Report</h1>
                <div class="timestamp">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
            </div>
            <div class="header-meta">
                <div>Total Tests: {len(tests)}</div>
            </div>
        </div>
    </header>

    <div class="container">
        <!-- Summary Cards -->
        <div class="summary-cards">
            <div class="summary-card highest">
                <div class="card-header">
                    <span>Highest Priority</span>
                    <span class="card-count">{priority_counts["Highest"]}</span>
                </div>
                <div class="card-body">
                    <div>Recommended for immediate automation</div>
                    <div class="card-threshold">Score: ≥ {highest_threshold:.2f}</div>
                </div>
            </div>
            
            <div class="summary-card high">
                <div class="card-header">
                    <span>High Priority</span>
                    <span class="card-count">{priority_counts["High"]}</span>
                </div>
                <div class="card-body">
                    <div>Recommended for second phase</div>
                    <div class="card-threshold">Score: {high_threshold:.2f} - {highest_threshold - 0.1:.2f}</div>
                </div>
            </div>
            
            <div class="summary-card medium">
                <div class="card-header">
                    <span>Medium Priority</span>
                    <span class="card-count">{priority_counts["Medium"]}</span>
                </div>
                <div class="card-body">
                    <div>Recommended for third phase</div>
                    <div class="card-threshold">Score: {medium_threshold:.2f} - {high_threshold - 0.1:.2f}</div>
                </div>
            </div>
            
            <div class="summary-card low">
                <div class="card-header">
                    <span>Low Priority</span>
                    <span class="card-count">{priority_counts["Low"]}</span>
                </div>
                <div class="card-body">
                    <div>Consider for later phases</div>
                    <div class="card-threshold">Score: {low_threshold:.2f} - {medium_threshold - 0.1:.2f}</div>
                </div>
            </div>
            
            <div class="summary-card lowest">
                <div class="card-header">
                    <span>Lowest Priority</span>
                    <span class="card-count">{priority_counts["Lowest"]}</span>
                </div>
                <div class="card-body">
                    <div>Not recommended for automation</div>
                    <div class="card-threshold">Score: < {low_threshold:.2f}</div>
                </div>
            </div>
            
            <div class="summary-card cant-automate">
                <div class="card-header">
                    <span>Can't Automate</span>
                    <span class="card-count">{priority_counts["Can't Automate"]}</span>
                </div>
                <div class="card-body">
                    <div>Not possible to automate</div>
                    <div class="card-threshold">Manual testing only</div>
                </div>
            </div>
        </div>
    """
        # Add test sections by priority tier
        priority_sections = [
            ("Highest Priority Tests", priority_tiers["highest"], "highest", f"≥ {highest_threshold:.2f}", "Recommended for immediate automation"),
            ("High Priority Tests", priority_tiers["high"], "high", f"{high_threshold:.2f} - {highest_threshold - 0.1:.2f}", "Recommended for second phase automation"),
            ("Medium Priority Tests", priority_tiers["medium"], "medium", f"{medium_threshold:.2f} - {high_threshold - 0.1:.2f}", "Recommended for third phase automation"),
            ("Low Priority Tests", priority_tiers["low"], "low", f"{low_threshold:.2f} - {medium_threshold - 0.1:.2f}", "Consider for later phases or keep as manual tests"),
            ("Lowest Priority Tests", priority_tiers["lowest"], "lowest", f"< {low_threshold:.2f}", "Not recommended for automation")
        ]
        
        for title, tests_list, css_class, score_range, description in priority_sections:
            html += f"""
        <!-- {title} Section -->
        <section>
            <div class="section-header section-{css_class}">
                <span class="section-icon"></span>
                <h2>{title}</h2>
            </div>
            <div class="section-description">{description}. Score: {score_range}</div>
            
            <div class="test-cards">
    """
            
            # Add test cards
            if tests_list:
                for i, test in enumerate(tests_list):
                    html += HTMLReportGenerator.generate_test_card(test, i+1, css_class, model)
            else:
                html += '<div class="no-tests">No tests in this category</div>'
            
            html += """
            </div>
        </section>
    """
        
        # Add "Can't Automate" section if there are tests that can't be automated
        if "cant_automate" in priority_tiers and priority_tiers["cant_automate"]:
            html += """
        <!-- Can't Automate Section -->
        <section>
            <div class="section-header section-cant-automate">
                <span class="section-icon"></span>
                <h2>Tests That Can't Be Automated</h2>
            </div>
            <div class="section-description">These tests have been identified as not possible to automate</div>
            
            <div class="test-cards">
    """
            
            for i, test in enumerate(priority_tiers["cant_automate"]):
                html += HTMLReportGenerator.generate_test_card(test, i+1, "cant-automate", model)
            
            html += """
            </div>
        </section>
    """
        
        # Close HTML
        html += """
    </div>

    <footer>
        <div>Test Automation Priority Report</div>
        <div>Generated using the Test Prioritization Tool</div>
    </footer>
    </body>
    </html>"""
        
        return html

    @staticmethod
    def _generate_css_styles():
        """Generate CSS styles for the HTML report"""
        return """<style>
        :root {
            --highest-color: #d32f2f;
            --high-color: #f57c00;
            --medium-color: #fbc02d;
            --low-color: #29b6f6;
            --lowest-color: #4fc3f7;
            --cant-automate-color: #9e9e9e;
            --bg-color: #f5f5f5;
            --card-bg: #ffffff;
            --text-color: #333333;
            --secondary-text: #666666;
            --border-color: #e0e0e0;
            --header-bg: #37474f;
            --header-text: #ffffff;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: var(--text-color);
            background-color: var(--bg-color);
            padding: 0;
            margin: 0;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        header {
            background-color: var(--header-bg);
            color: var(--header-text);
            padding: 20px 0;
            margin-bottom: 30px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        header .container {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .header-content h1 {
            font-size: 24px;
            margin-bottom: 5px;
        }
        
        .timestamp {
            font-size: 14px;
            opacity: 0.8;
        }
        
        .summary-cards {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .summary-card {
            background-color: var(--card-bg);
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
            display: flex;
            flex-direction: column;
        }
        
        .card-header {
            padding: 15px;
            font-weight: bold;
            color: white;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .highest .card-header { background-color: var(--highest-color); }
        .high .card-header { background-color: var(--high-color); }
        .medium .card-header { background-color: var(--medium-color); }
        .low .card-header { background-color: var(--low-color); }
        .lowest .card-header { background-color: var(--lowest-color); }
        .cant-automate .card-header { background-color: var(--cant-automate-color); }
        
        .card-count {
            font-size: 24px;
            font-weight: bold;
        }
        
        .card-body {
            padding: 15px;
            font-size: 14px;
            color: var(--secondary-text);
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        
        .card-threshold {
            font-size: 13px;
            margin-top: 10px;
        }
        
        section {
            margin-bottom: 40px;
        }
        
        .section-header {
            border-bottom: 2px solid var(--border-color);
            padding-bottom: 10px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
        }
        
        .section-icon {
            width: 24px;
            height: 24px;
            border-radius: 50%;
            margin-right: 10px;
            display: inline-block;
        }
        
        .section-highest .section-icon { background-color: var(--highest-color); }
        .section-high .section-icon { background-color: var(--high-color); }
        .section-medium .section-icon { background-color: var(--medium-color); }
        .section-low .section-icon { background-color: var(--low-color); }
        .section-lowest .section-icon { background-color: var(--lowest-color); }
        .section-cant-automate .section-icon { background-color: var(--cant-automate-color); }
        
        .section-description {
            font-size: 14px;
            color: var(--secondary-text);
            margin-bottom: 15px;
            font-style: italic;
        }
        
        .test-cards {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
        }
        
        .test-card {
            background-color: var(--card-bg);
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
            transition: transform 0.2s ease-in-out;
        }
        
        .test-card:hover {
            transform: translateY(-5px);
        }
        
        .test-card-header {
            padding: 15px;
            border-bottom: 1px solid var(--border-color);
            position: relative;
        }
        
        .test-card-header h3 {
            margin-right: 50px;
            font-size: 16px;
        }
        
        .score-badge {
            position: absolute;
            top: 15px;
            right: 15px;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }
        
        .priority-highest .score-badge { background-color: var(--highest-color); }
        .priority-high .score-badge { background-color: var(--high-color); }
        .priority-medium .score-badge { background-color: var(--medium-color); }
        .priority-low .score-badge { background-color: var(--low-color); }
        .priority-lowest .score-badge { background-color: var(--lowest-color); }
        .priority-cant-automate .score-badge { background-color: var(--cant-automate-color); }
        
        .test-meta {
            display: flex;
            gap: 10px;
            margin-top: 5px;
            font-size: 13px;
        }
        
        .meta-item {
            background-color: var(--bg-color);
            border-radius: 4px;
            padding: 3px 8px;
        }
        
        .test-card-body {
            padding: 15px;
        }
        
        .test-description {
            margin-bottom: 15px;
            font-size: 14px;
            color: var(--secondary-text);
            border-left: 3px solid var(--border-color);
            padding-left: 10px;
        }
        
        .factor-list {
            list-style-type: none;
        }
        
        .factor-item {
            margin-bottom: 5px;
            font-size: 13px;
            display: flex;
            align-items: center;
        }
        
        .factor-score {
            display: inline-block;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background-color: var(--bg-color);
            color: var(--text-color);
            text-align: center;
            line-height: 20px;
            font-weight: bold;
            margin-right: 10px;
            font-size: 12px;
        }
        
        .factor-name {
            font-weight: bold;
            margin-right: 5px;
        }
        
        .factor-description {
            color: var(--secondary-text);
        }
        
        footer {
            text-align: center;
            padding: 20px;
            background-color: var(--header-bg);
            color: var(--header-text);
            font-size: 12px;
            margin-top: 50px;
        }
        
        .no-tests {
            text-align: center;
            padding: 50px;
            color: var(--secondary-text);
            font-style: italic;
        }
        
        @media (max-width: 768px) {
            .summary-cards {
                grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            }
            
            .test-cards {
                grid-template-columns: 1fr;
            }
            
            header .container {
                flex-direction: column;
                text-align: center;
            }
            
            .header-meta {
                margin-top: 10px;
            }
        }
    </style>"""

    @staticmethod
    def generate_test_card(test, index, priority_class, model):
        """
        Generate HTML for a test card
        
        Args:
            test (dict): Test dictionary
            index (int): Index/rank of the test
            priority_class (str): CSS class for priority styling
            model: The prioritization model for factor descriptions
        
        Returns:
            str: HTML for the test card
        """
        try:
            # Start card
            card = f"""
                <div class="test-card priority-{priority_class}">
                    <div class="test-card-header">
                        <h3>{index}. {test['name']}</h3>
                        <span class="score-badge">{test['total_score']}</span>
                        <div class="test-meta">
                            <span class="meta-item ticket">{test.get('ticket_id', 'N/A')}</span>
        """
        
            # Add section if available
            if test.get("section"):
                card += f'<span class="meta-item section">{test["section"]}</span>'
        
            card += """
                        </div>
                    </div>
                    <div class="test-card-body">
        """
        
            # Add description if available
            if test.get('description'):
                card += f'<div class="test-description">{test["description"]}</div>'
        
            # Start factor list
            card += '<ul class="factor-list">'
        
            # Add factors
            if model and hasattr(model, 'factors') and hasattr(model, 'score_options'):
                # Show the "Can it be automated?" factor first if in "Can't Automate" category
                if test['priority'] == "Can't Automate" and "can_be_automated" in test['scores']:
                    factor_key = "can_be_automated"
                    factor_name = model.factors[factor_key]["name"]
                    score = test['scores'][factor_key]
                    score_description = model.score_options[factor_key][score]
                
                    card += f"""
                        <li class="factor-item">
                            <span class="factor-score">{score}</span>
                            <span class="factor-name">{factor_name}:</span>
                            <span class="factor-description">{score_description}</span>
                        </li>
                """
            
                # Add other factors
                for factor_key, score in test['scores'].items():
                    # Skip the can_be_automated factor if already shown or if test can't be automated
                    if factor_key == "can_be_automated" and (test['priority'] == "Can't Automate"):
                        continue
                    
                    if factor_key in model.factors and score in model.score_options.get(factor_key, {}):
                        factor_name = model.factors[factor_key]["name"]
                        score_description = model.score_options[factor_key][score]
                    
                        card += f"""
                            <li class="factor-item">
                                <span class="factor-score">{score}</span>
                                <span class="factor-name">{factor_name}:</span>
                                <span class="factor-description">{score_description}</span>
                            </li>
                        """
        
            # Close factor list and card
            card += """
                        </ul>
                    </div>
                </div>
            """
        
            return card
        except Exception as e:
            print(f"Error generating test card: {e}")
            return f"<div>Error generating card for {test.get('name', 'Unknown Test')}</div>"