"""
enhanced_html_report.py - Template-based implementation of enhanced HTML report
"""
import os
import json
import base64
import io
import tempfile
import webbrowser
from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from string import Template
from pathlib import Path

from views.reports import BaseReportView
from utils.chart_utils import ChartUtils

class EnhancedHtmlReportView(BaseReportView):
    """
    HTML report view with integrated charts, using a template-based approach
    """
    def __init__(self, parent, model):
        """
        Initialize the HTML report view
        
        Args:
            parent: The parent window
            model: The prioritization model
        """
        self.temp_html_file = None
        
        # Check if matplotlib is available
        self.matplotlib_available = ChartUtils.is_matplotlib_available()
        
        super().__init__(parent, model, "Test Automation Report")
        
    def __del__(self):
        """Clean up temporary files when the object is destroyed"""
        if self.temp_html_file and os.path.exists(self.temp_html_file):
            try:
                os.remove(self.temp_html_file)
            except:
                pass
    
    def create_report_content(self):
        """Create the HTML report content"""
        # Create main container with padding
        main_frame = ttk.Frame(self.main_frame, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add info text
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=20)
        
        ttk.Label(
            header_frame,
            text="Test Automation Prioritization Report",
            font=("", 16, "bold")
        ).pack(anchor=tk.CENTER)
        
        description_text = """
This report combines detailed test information with interactive charts and visualizations.
Navigate through different views to analyze your test prioritization from various perspectives.
        """
        ttk.Label(
            header_frame,
            text=description_text,
            justify=tk.CENTER
        ).pack(pady=10, anchor=tk.CENTER)
        
        # Create a frame to display report preview options
        preview_frame = ttk.LabelFrame(main_frame, text="Report Preview Options")
        preview_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Create the temp HTML file for preview
        self.temp_html_file = self.create_temp_html_preview()
        
        # Add preview button
        preview_button = ttk.Button(
            preview_frame,
            text="Open Report in Browser",
            command=self.open_html_preview
        )
        preview_button.pack(padx=10, pady=10)
        
        # Add features frame
        features_frame = ttk.LabelFrame(main_frame, text="Report Features")
        features_frame.pack(fill=tk.X, padx=20, pady=10)
        
        features_text = """
• Modern tabbed interface for easy navigation
• Interactive charts and visualizations
• Priority distribution pie chart
• Score distribution histogram
• Factor contribution analysis
• Top tests bar chart
• Detailed test listing with filtering options
• Color-coded priority indicators
• Responsive design compatible with all modern browsers
        """
        
        ttk.Label(
            features_frame,
            text=features_text,
            justify=tk.LEFT
        ).pack(padx=10, pady=10)
        
        # Add a note about matplotlib if not available
        if not self.matplotlib_available:
            note_frame = ttk.LabelFrame(main_frame, text="Note")
            note_frame.pack(fill=tk.X, padx=20, pady=10)
            
            note_text = """
Matplotlib is required for generating charts. The report will be created without charts.
To include charts, please install matplotlib:

pip install matplotlib
            """
            
            ttk.Label(
                note_frame,
                text=note_text,
                justify=tk.LEFT,
                foreground="red"
            ).pack(padx=10, pady=10)
        
        # Create export frame
        export_frame = ttk.LabelFrame(self.button_frame, text="Export Options")
        export_frame.pack(side=tk.LEFT, padx=5, pady=5)
        
        ttk.Button(
            export_frame,
            text="Export Report",
            command=self.export_html_report
        ).pack(side=tk.LEFT, padx=5, pady=5)
    
    def create_temp_html_preview(self):
        """
        Create a temporary HTML file for preview
        
        Returns:
            str: Path to the temporary HTML file
        """
        try:
            # Get priority tiers
            priority_tiers = self.model.get_priority_tiers()
            
            # Create a temporary file
            fd, path = tempfile.mkstemp(suffix=".html", prefix="test_priority_report")
            
            # Close the file descriptor
            os.close(fd)
            
            # Generate enhanced HTML content using template
            html_content = self.generate_html_from_template(self.model.tests, priority_tiers)
            
            # Write the HTML content to the file
            with open(path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            return path
        except Exception as e:
            print(f"Error creating HTML preview: {e}")
            return None
    
    def open_html_preview(self):
        """Open the HTML preview in the default web browser"""
        if not self.temp_html_file or not os.path.exists(self.temp_html_file):
            # If the temp file doesn't exist, create a new one
            self.temp_html_file = self.create_temp_html_preview()
            
            if not self.temp_html_file:
                messagebox.showerror(
                    "Preview Error", 
                    "Could not create HTML preview.",
                    parent=self.parent
                )
                return
        
        # Open the HTML file in the default browser
        try:
            webbrowser.open(f"file://{os.path.abspath(self.temp_html_file)}")
        except Exception as e:
            messagebox.showerror(
                "Preview Error", 
                f"Could not open browser: {str(e)}",
                parent=self.parent
            )
    
    def export_html_report(self):
        """Export the report as HTML"""
        filename = filedialog.asksaveasfilename(
            parent=self.parent,
            defaultextension=".html",
            filetypes=[("HTML Files", "*.html"), ("All Files", "*.*")],
            title="Export HTML Report"
        )
        
        if filename:
            try:
                # Get priority tiers
                priority_tiers = self.model.get_priority_tiers()
                
                # Generate enhanced HTML content using template
                html_content = self.generate_html_from_template(self.model.tests, priority_tiers)
                
                # Write to file
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                messagebox.showinfo(
                    "Export Successful", 
                    f"Enhanced report exported to {filename}",
                    parent=self.parent
                )
                
                # Ask if user wants to open the exported file
                if messagebox.askyesno(
                    "Open File", 
                    "Would you like to open the exported HTML file?",
                    parent=self.parent
                ):
                    try:
                        webbrowser.open(f"file://{os.path.abspath(filename)}")
                    except Exception as e:
                        messagebox.showerror(
                            "Open Error", 
                            f"Could not open file: {str(e)}",
                            parent=self.parent
                        )
            except Exception as e:
                messagebox.showerror(
                    "Export Error", 
                    f"An error occurred during export: {str(e)}",
                    parent=self.parent
                )
    
    def load_template(self):
        """
        Load the HTML template file
        
        Returns:
            str: The HTML template content
        """
        # Get the current script directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Try to find the template in various potential locations
        template_paths = [
            os.path.join(current_dir, 'templates', 'report_template.html'),
            os.path.join(current_dir, '..', 'templates', 'report_template.html'),
            os.path.join(current_dir, '..', '..', 'templates', 'report_template.html'),
            os.path.join(current_dir, 'report_template.html'),
        ]
        
        for path in template_paths:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    return f.read()
        
        # If template not found, use default minimal template
        return self.get_default_template()
    
    def get_default_template(self):
        """
        Get a default minimal HTML template when the full template file is not found
        
        Returns:
            str: Default HTML template
        """
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Enhanced Test Automation Report</title>
    <style>
        body { font-family: sans-serif; margin: 0; padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { color: #333; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Enhanced Test Automation Report</h1>
        <p>Generated: {{timestamp}}</p>
        <p>Total Tests: {{total_tests}}</p>
        
        <h2>Test Summary</h2>
        <ul>
            <li>Highest Priority: {{highest_count}}</li>
            <li>High Priority: {{high_count}}</li>
            <li>Medium Priority: {{medium_count}}</li>
            <li>Low Priority: {{low_count}}</li>
            <li>Lowest Priority: {{lowest_count}}</li>
            <li>Can't Automate: {{cant_automate_count}}</li>
        </ul>
        
        {{priority_chart}}
        {{top_tests_chart}}
    </div>
</body>
</html>"""
    
    def generate_html_from_template(self, tests, priority_tiers):
        """
        Generate HTML content using a template
        
        Args:
            tests (list): List of test dictionaries
            priority_tiers (dict): Dictionary with priority tier tests
            
        Returns:
            str: Generated HTML content
        """
        # Load template
        template_content = self.load_template()
        
        # Prepare replacement values
        replacements = self.prepare_template_replacements(tests, priority_tiers)
        
        # Manual string replacement instead of using Template
        html_content = template_content
        for key, value in replacements.items():
            # Convert the value to string if it's not already
            if not isinstance(value, str):
                value = str(value)
            
            # Replace the placeholders with the actual values
            placeholder = f"{{{{{key}}}}}"
            html_content = html_content.replace(placeholder, value)
        
        # Debug information - you can remove this in production
        if "{{" in html_content:
            # Find unreplaced variables
            import re
            unreplaced = re.findall(r"{{(.*?)}}", html_content)
            print(f"Warning: The following variables were not replaced: {unreplaced}")
            print(f"Available keys in replacements: {replacements.keys()}")
        
        return html_content
    
    def prepare_template_replacements(self, tests, priority_tiers):
        """
        Prepare values to replace in the template
        
        Args:
            tests (list): List of test dictionaries
            priority_tiers (dict): Dictionary with priority tier tests
            
        Returns:
            dict: Dictionary of replacement values
        """
        # Count tests by priority
        priority_counts = {
            "highest_count": len(priority_tiers["highest"]),
            "high_count": len(priority_tiers["high"]),
            "medium_count": len(priority_tiers["medium"]),
            "low_count": len(priority_tiers["low"]),
            "lowest_count": len(priority_tiers["lowest"]),
            "cant_automate_count": len(priority_tiers.get("cant_automate", []))
        }
        
        # Get thresholds with 1 decimal place formatting
        highest_threshold = round(priority_tiers["highest_threshold"], 1)
        high_threshold = round(priority_tiers["high_threshold"], 1)
        medium_threshold = round(priority_tiers["medium_threshold"], 1)
        low_threshold = round(priority_tiers["low_threshold"], 1)
        
        # Generate charts as base64 images if matplotlib is available
        chart_images = self.generate_chart_images(tests)
        
        # Generate HTML for test cards by priority
        test_cards = {
            "highest_priority_cards": self.generate_test_cards_html(priority_tiers["highest"], "highest"),
            "high_priority_cards": self.generate_test_cards_html(priority_tiers["high"], "high"),
            "medium_priority_cards": self.generate_test_cards_html(priority_tiers["medium"], "medium"),
            "low_priority_cards": self.generate_test_cards_html(priority_tiers["low"], "low"),
            "lowest_priority_cards": self.generate_test_cards_html(priority_tiers["lowest"], "lowest"),
            "cant_automate_cards": self.generate_test_cards_html(priority_tiers.get("cant_automate", []), "cant-automate")
        }
        
        # Prepare JSON data for JavaScript
        test_data_json = self.generate_test_data_json(tests)
        
        # Combine all replacements
        replacements = {
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M'),
            "total_tests": len(tests),
            **priority_counts,  # This should include highest_count, high_count, etc.
            "highest_threshold": highest_threshold,
            "high_threshold": high_threshold,
            "medium_threshold": medium_threshold,
            "low_threshold": low_threshold,
            "highest_threshold_minus": highest_threshold - 0.1,
            "high_threshold_minus": high_threshold - 0.1,
            "medium_threshold_minus": medium_threshold - 0.1,
            "test_data_json": test_data_json,
            **chart_images,
            **test_cards
        }
        
        return replacements
    
    def generate_chart_images(self, tests):
        """
        Generate base64-encoded chart images
        
        Args:
            tests (list): List of test dictionaries
            
        Returns:
            dict: Dictionary containing base64-encoded chart images or placeholder messages
        """
        chart_images = {}
        
        if self.matplotlib_available:
            try:
                # Generate chart images
                fig1, _ = ChartUtils.create_priority_distribution_chart(tests)
                fig2, _ = ChartUtils.create_score_distribution_chart(tests)
                fig3, _ = ChartUtils.create_factor_contribution_chart(tests, self.model.factors)
                fig4, _ = ChartUtils.create_top_tests_chart(tests)
                
                # Convert figures to base64 for embedding in HTML
                def fig_to_base64_img_tag(fig):
                    img_buf = io.BytesIO()
                    fig.savefig(img_buf, format='png', dpi=100, bbox_inches='tight')
                    img_buf.seek(0)
                    img_str = base64.b64encode(img_buf.read()).decode('utf-8')
                    return f'<img class="chart-img" src="data:image/png;base64,{img_str}" alt="Chart">'
                
                chart_images = {
                    'priority_chart': fig_to_base64_img_tag(fig1),
                    'score_distribution_chart': fig_to_base64_img_tag(fig2),
                    'factor_contribution_chart': fig_to_base64_img_tag(fig3),
                    'top_tests_chart': fig_to_base64_img_tag(fig4)
                }
            except Exception as e:
                print(f"Error generating charts: {e}")
                chart_images = {
                    'priority_chart': '<p class="no-data-message">Error generating chart.</p>',
                    'score_distribution_chart': '<p class="no-data-message">Error generating chart.</p>',
                    'factor_contribution_chart': '<p class="no-data-message">Error generating chart.</p>',
                    'top_tests_chart': '<p class="no-data-message">Error generating chart.</p>'
                }
        else:
            chart_images = {
                'priority_chart': '<p class="no-data-message">Chart not available. Install matplotlib to enable charts.</p>',
                'score_distribution_chart': '<p class="no-data-message">Chart not available. Install matplotlib to enable charts.</p>',
                'factor_contribution_chart': '<p class="no-data-message">Chart not available. Install matplotlib to enable charts.</p>',
                'top_tests_chart': '<p class="no-data-message">Chart not available. Install matplotlib to enable charts.</p>'
            }
        
        return chart_images
    
    def generate_test_cards_html(self, tests, priority_class):
        """
        Generate HTML for test cards
        
        Args:
            tests (list): List of test dictionaries
            priority_class (str): CSS class for priority styling
            
        Returns:
            str: HTML for test cards
        """
        if not tests:
            return '<div class="no-data-message">No tests in this category</div>'
        
        html = ''
        for i, test in enumerate(tests):
            html += self.generate_test_card_html(test, i+1, priority_class)
        
        return html
    
    def generate_test_card_html(self, test, index, priority_class):
        """
        Generate HTML for a single test card
        
        Args:
            test (dict): Test dictionary
            index (int): Index for display
            priority_class (str): CSS class for priority
            
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
            if hasattr(self.model, 'factors') and hasattr(self.model, 'score_options'):
                # Show the "Can it be automated?" factor first if in "Can't Automate" category
                if test['priority'] == "Can't Automate" and "can_be_automated" in test['scores']:
                    factor_key = "can_be_automated"
                    factor_name = self.model.factors[factor_key]["name"]
                    score = test['scores'][factor_key]
                    score_description = self.model.score_options[factor_key][score]
                    
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
                        
                    if factor_key in self.model.factors and score in self.model.score_options.get(factor_key, {}):
                        factor_name = self.model.factors[factor_key]["name"]
                        score_description = self.model.score_options[factor_key][score]
                        
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
    
    def generate_test_data_json(self, tests):
        """
        Generate JSON data for tests to be used in JavaScript
        
        Args:
            tests (list): List of test dictionaries
            
        Returns:
            str: JSON string of test data
        """
        # Create a simplified version of test data for the table
        test_data = []
        for test in tests:
            test_data.append({
                'id': test['id'],
                'name': test['name'],
                'section': test.get('section', ''),
                'priority': test['priority'],
                'total_score': test['total_score'],
                'ticket_id': test.get('ticket_id', '')
            })
        
        # Sort by priority order
        priority_order = {"Highest": 0, "High": 1, "Medium": 2, "Low": 3, "Lowest": 4, "Can't Automate": 5}
        sorted_data = sorted(test_data, key=lambda x: (priority_order.get(x['priority'], 999), -x['total_score']))
        
        return json.dumps(sorted_data)