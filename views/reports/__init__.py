"""
__init__.py - Package initialization for report views
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class BaseReportView:
    """
    Base class for report views
    """
    def __init__(self, parent, model, title="Report"):
        """
        Initialize the base report view
        
        Args:
            parent: The parent window
            model: The prioritization model
            title (str): The report window title
        """
        self.parent = parent
        self.model = model

        # Check if data is available
        if not self.check_if_data_available():
            return
        
        # Configure parent window
        self.parent.title(title)
        self.parent.geometry("1200x900")
        
        # Create main container
        self.main_frame = ttk.Frame(self.parent, padding=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create button frame - this should be used by all child classes
        self.button_frame = ttk.Frame(self.parent)
        self.button_frame.pack(fill=tk.X, pady=10, padx=10)
        
        # Add default close button
        ttk.Button(
            self.button_frame, 
            text="Close", 
            command=self.parent.destroy
        ).pack(side=tk.RIGHT, padx=5)
        
        # This must be implemented by child classes
        self.create_report_content()
    
    def create_report_content(self):
        """
        Create the report content
        
        This method must be implemented by child classes
        """
        raise NotImplementedError("Child classes must implement create_report_content()")
    
    def check_if_data_available(self):
        """
        Check if test data is available
        
        Returns:
            bool: True if data is available, False otherwise
        """
        if not self.model.tests:
            messagebox.showinfo("Report", "No tests available for report", parent=self.parent)
            self.parent.destroy()
            return False
        return True

from views.reports.text_report import TextReportView
from views.reports.chart_report import ChartReportView
from views.reports.html_report import HtmlReportView
from views.reports.enhanced_html_report import EnhancedHtmlReportView

__all__ = ['BaseReportView', 'TextReportView', 'ChartReportView', 'HtmlReportView', 'EnhancedHtmlReportView']