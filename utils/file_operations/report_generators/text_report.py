"""
text_report.py - TextReportView with HTML preview instead of markdown
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import webbrowser
import tempfile
from datetime import datetime
from utils.file_operations import FileOperations
from views.reports import BaseReportView

class TextReportView(BaseReportView):
    """
    Text-based prioritization report view with tabs for text and HTML preview
    """
    def __init__(self, parent, model):
        """
        Initialize the text report view
        
        Args:
            parent: The parent window
            model: The prioritization model
        """
        self.temp_html_file = None
        super().__init__(parent, model, "Test Automation Priority Report")
        
    def __del__(self):
        """Clean up temporary files when the object is destroyed"""
        if self.temp_html_file and os.path.exists(self.temp_html_file):
            try:
                os.remove(self.temp_html_file)
            except:
                pass
    
    def create_report_content(self):
        """Create the text report content with tabs for text and HTML preview"""
        # Get priority tiers
        priority_tiers = self.model.get_priority_tiers()
        
        # Generate report text (plain text)
        self.report_text = FileOperations.generate_report_text(self.model.tests, priority_tiers, self.model)
        
        # Create notebook with tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tab for plain text report
        text_frame = ttk.Frame(self.notebook)
        self.notebook.add(text_frame, text="Plain Text")
        
        # Add text widget to text tab
        self.text_widget = tk.Text(text_frame, wrap=tk.WORD, padx=10, pady=10)
        text_scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.text_widget.yview)
        self.text_widget.configure(yscrollcommand=text_scrollbar.set)
        
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Insert report text
        self.text_widget.insert(tk.END, self.report_text)
        
        # Make text widget read-only
        self.text_widget.configure(state="disabled")
        
        # Create an export options frame
        export_frame = ttk.LabelFrame(self.button_frame, text="Export Options")
        export_frame.pack(side=tk.LEFT, padx=1, pady=1, fill=tk.X)
        
        # Add export buttons
        ttk.Button(
            export_frame, 
            text="Text (.txt)", 
            command=self.export_text_report
        ).pack(side=tk.LEFT, padx=5, pady=5)
        
        ttk.Button(
            export_frame, 
            text="HTML (.html)", 
            command=self.export_html_report
        ).pack(side=tk.LEFT, padx=5, pady=5)
        
        ttk.Button(
            export_frame, 
            text="Word (.docx)", 
            command=self.export_word_report
        ).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Add copy to clipboard button
        ttk.Button(
            self.button_frame,
            text="Copy to Clipboard",
            command=self.copy_current_tab_to_clipboard
        ).pack(side=tk.RIGHT, padx=5)
    
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
            fd, path = tempfile.mkstemp(suffix=".html", prefix="test_priority_report_")
            
            # Close the file descriptor
            os.close(fd)
            
            # Export HTML to the temporary file
            FileOperations.export_report_to_html(self.model.tests, priority_tiers, self.model, path)
            
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
            # Get priority tiers
            priority_tiers = self.model.get_priority_tiers()
            
            # Use FileOperations to export to HTML
            success = FileOperations.export_report_to_html(
                self.model.tests, 
                priority_tiers, 
                self.model, 
                filename
            )
            
            if success:
                messagebox.showinfo(
                    "Export Successful", 
                    f"HTML report exported to {filename}",
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
            else:
                messagebox.showerror(
                    "Export Error", 
                    "An error occurred during HTML export.",
                    parent=self.parent
                )
    
    def export_word_report(self):
        """Export the report as Word (.docx)"""
        filename = filedialog.asksaveasfilename(
            parent=self.parent,
            defaultextension=".docx",
            filetypes=[("Word Documents", "*.docx"), ("All Files", "*.*")],
            title="Export Word Report"
        )
        
        if filename:
            # Get priority tiers
            priority_tiers = self.model.get_priority_tiers()
            
            # Use FileOperations to export to Word
            success, error_message = FileOperations.export_report_to_docx(
                self.model.tests, 
                priority_tiers, 
                self.model, 
                filename
            )
            
            if success:
                messagebox.showinfo(
                    "Export Successful", 
                    f"Word report exported to {filename}",
                    parent=self.parent
                )
            else:
                messagebox.showerror(
                    "Export Error", 
                    f"An error occurred during Word export: {error_message}",
                    parent=self.parent
                )
    
    def export_text_report(self):
        """Export the plain text report to a file"""
        filename = filedialog.asksaveasfilename(
            parent=self.parent,
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            title="Export Text Report"
        )
        
        if filename:
            success = FileOperations.export_report_to_file(filename, self.report_text)
            if success:
                messagebox.showinfo(
                    "Export Successful", 
                    f"Report exported to {filename}",
                    parent=self.parent
                )
            else:
                messagebox.showerror(
                    "Export Error", 
                    "An error occurred during export",
                    parent=self.parent
                )
    
    def copy_current_tab_to_clipboard(self):
        """Copy the content of the current tab to clipboard"""
        # Get the current tab
        current_tab = self.notebook.select()
        tab_text = self.notebook.tab(current_tab, "text")
        
        # Clear the clipboard
        self.parent.clipboard_clear()
        
        # Copy appropriate content based on current tab
        if tab_text == "Plain Text":
            self.parent.clipboard_append(self.report_text)
            message = "Plain text report copied to clipboard"
        else:
            message = "No valid tab selected for clipboard copy"
        
        # Show confirmation
        messagebox.showinfo("Copied to Clipboard", message, parent=self.parent)

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