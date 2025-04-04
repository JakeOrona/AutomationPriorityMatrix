"""
text_report.py - Text-based prioritization report view
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from utils.file_operations import FileOperations
from views.reports import BaseReportView

class TextReportView(BaseReportView):
    """
    Text-based prioritization report view
    """
    def __init__(self, parent, model):
        """
        Initialize the text report view
        
        Args:
            parent: The parent window
            model: The prioritization model
        """
        super().__init__(parent, model, "Test Automation Priority Report")
    
    def create_report_content(self):
        """Create the text report content"""
        # Get priority tiers
        priority_tiers = self.model.get_priority_tiers()
        
        # Generate report text
        self.report_text = FileOperations.generate_report_text(self.model.tests, priority_tiers)
        
        # Create scrollable text widget
        text_frame = ttk.Frame(self.main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.text_widget = tk.Text(text_frame, wrap=tk.WORD, padx=10, pady=10)
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.text_widget.yview)
        self.text_widget.configure(yscrollcommand=scrollbar.set)
        
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Insert report text
        self.text_widget.insert(tk.END, self.report_text)
        
        # Make text widget read-only
        self.text_widget.configure(state="disabled")

        # Add export button to button frame
        ttk.Button(
            self.button_frame, 
            text="Export Report", 
            command=self.export_report
        ).pack(side=tk.LEFT, padx=5)
    
    def export_report(self):
        """Export the report to a text file"""
        filename = filedialog.asksaveasfilename(
            parent=self.parent,
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            title="Export Report"
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