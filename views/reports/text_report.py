"""
text_report.py - TextReportView with HTML preview instead of markdown
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import webbrowser
import tempfile
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
        
        # Create tab for HTML preview
        html_frame = ttk.Frame(self.notebook)
        self.notebook.add(html_frame, text="HTML Preview")
        
        # Create HTML preview using a temporary file and a button to open in browser
        html_preview_frame = ttk.Frame(html_frame, padding=10)
        html_preview_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add info and preview button
        preview_info = ttk.Label(
            html_preview_frame, 
            text="HTML preview is available in your default web browser.\nClick the button below to open the report.",
            justify=tk.CENTER
        )
        preview_info.pack(pady=20)
        
        # Create a temporary HTML file
        self.temp_html_file = self.create_temp_html_preview()
        
        # Add preview button
        ttk.Button(
            html_preview_frame, 
            text="Open HTML Preview in Browser",
            command=self.open_html_preview
        ).pack(pady=10)

        # Add note about browser preview
        preview_note = ttk.Label(
            html_preview_frame,
            text="Note: The HTML preview will open in your default web browser.\nThis provides the most accurate representation of the exported HTML report.",
            justify=tk.CENTER,
            font=("", 9, "italic")
        )
        preview_note.pack(pady=20)
        
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