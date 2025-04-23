"""
html_report.py - HTML report view for test prioritization
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import webbrowser
import tempfile
from views.reports import BaseReportView
from utils.file_operations import FileOperations

class HtmlReportView(BaseReportView):
    """
    HTML report view for test prioritization
    """
    def __init__(self, parent, model):
        """
        Initialize the HTML report view
        
        Args:
            parent: The parent window
            model: The prioritization model
        """
        self.temp_html_file = None
        super().__init__(parent, model, "Test Automation Priority HTML Report")
        
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
            text="HTML Test Prioritization Report",
            font=("", 16, "bold")
        ).pack(anchor=tk.CENTER)
        
        description_text = """
The HTML report provides a modern, interactive view of your prioritized tests.
It includes color-coded priority levels, test details, and a responsive layout.
        """
        ttk.Label(
            header_frame,
            text=description_text,
            justify=tk.CENTER
        ).pack(pady=10, anchor=tk.CENTER)
        
        # Create a temporary HTML file
        self.temp_html_file = self.create_temp_html_preview()
        
        # Add preview button
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        preview_button = ttk.Button(
            button_frame,
            text="Open HTML Preview in Browser",
            command=self.open_html_preview
        )
        preview_button.pack(padx=5, pady=5)
        
        # Add features frame
        features_frame = ttk.LabelFrame(main_frame, text="HTML Report Features")
        features_frame.pack(fill=tk.X, padx=20, pady=10)
        
        features_text = """
• Modern layout with responsive design
• Summary cards showing distribution of tests by priority
• Color-coded priority levels
• Detailed test cards with all factor scores
• Interactive elements with hover effects
• Compatible with all modern browsers
        """
        
        ttk.Label(
            features_frame,
            text=features_text,
            justify=tk.LEFT
        ).pack(padx=10, pady=10)
        
        # Create export frame
        export_frame = ttk.LabelFrame(self.button_frame, text="Export Options")
        export_frame.pack(side=tk.LEFT, padx=5, pady=5)
        
        ttk.Button(
            export_frame,
            text="Export HTML Report",
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