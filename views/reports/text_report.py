"""
text_report.py - TextReportView to support tabbed view with both text and markdown
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from utils.file_operations import FileOperations
from views.reports import BaseReportView

class TextReportView(BaseReportView):
    """
    Text-based prioritization report view with tabs for text and markdown format
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
        """Create the text report content with tabs for different formats"""
        # Get priority tiers
        priority_tiers = self.model.get_priority_tiers()
        
        # Generate report text (plain text)
        self.report_text = FileOperations.generate_report_text(self.model.tests, priority_tiers, self.model)
        
        # Generate markdown report
        self.markdown_report = FileOperations.generate_enhanced_markdown_report(self.model.tests, priority_tiers, self.model)
        
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
        
        # Create tab for markdown report
        md_frame = ttk.Frame(self.notebook)
        self.notebook.add(md_frame, text="Markdown")
        
        # Add text widget to markdown tab
        self.md_widget = tk.Text(md_frame, wrap=tk.WORD, padx=10, pady=10)
        md_scrollbar = ttk.Scrollbar(md_frame, orient="vertical", command=self.md_widget.yview)
        self.md_widget.configure(yscrollcommand=md_scrollbar.set)
        
        self.md_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        md_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Insert markdown text
        self.md_widget.insert(tk.END, self.markdown_report)
        
        # Make markdown widget read-only
        self.md_widget.configure(state="disabled")
        
        # Try to style the markdown text if possible
        try:
            self.apply_basic_markdown_styling(self.md_widget)
        except Exception as e:
            # If styling fails, just show plain text
            print(f"Markdown styling error: {e}")
        
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
            text="Markdown (.md)", 
            command=self.export_markdown_report
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
    
    def export_html_report(self):
        """Export the report as HTML"""
        filename = filedialog.asksaveasfilename(
            parent=self.parent,
            defaultextension=".html",
            filetypes=[("HTML Files", "*.html"), ("All Files", "*.*")],
            title="Export HTML Report"
        )
        
        if filename:
            # Use FileOperations to export to HTML
            success = FileOperations.export_report_to_html(self.markdown_report, filename)
            
            if success:
                messagebox.showinfo(
                    "Export Successful", 
                    f"HTML report exported to {filename}",
                    parent=self.parent
                )
            else:
                messagebox.showerror(
                    "Export Error", 
                    f"An error occurred during HTML export. Do you have the 'markdown' package installed?",
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
            # Use FileOperations to export to Word
            success, error_message = FileOperations.export_report_to_docx(self.markdown_report, filename)
            
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
    
    def apply_basic_markdown_styling(self, text_widget):
        """
        Apply basic styling to markdown text widget
        
        Args:
            text_widget: The text widget to style
        """
        # Configure tags for various markdown elements
        text_widget.tag_configure("heading1", font=("", 16, "bold"))
        text_widget.tag_configure("heading2", font=("", 14, "bold"))
        text_widget.tag_configure("heading3", font=("", 12, "bold"))
        text_widget.tag_configure("bold", font=("", 10, "bold"))
        text_widget.tag_configure("italic", font=("", 10, "italic"))
        text_widget.tag_configure("bullet", lmargin1=20, lmargin2=30)
        
        # Find and tag all headings (using regex would be better but requires re module)
        content = self.markdown_report
        lines = content.split('\n')
        line_index = 1  # Tkinter starts at line 1
        
        for line in lines:
            start_pos = f"{line_index}.0"
            end_pos = f"{line_index}.end"
            
            # Apply heading styles
            if line.startswith('# '):
                text_widget.tag_add("heading1", start_pos, end_pos)
            elif line.startswith('## '):
                text_widget.tag_add("heading2", start_pos, end_pos)
            elif line.startswith('### '):
                text_widget.tag_add("heading3", start_pos, end_pos)
            
            # Apply bold to **text**
            pos = 0
            while True:
                pos = line.find('**', pos)
                if pos == -1:
                    break
                end = line.find('**', pos + 2)
                if end == -1:
                    break
                
                text_widget.tag_add("bold", f"{line_index}.{pos}", f"{line_index}.{end+2}")
                pos = end + 2
            
            # Apply bullet styling for list items
            if line.strip().startswith('* '):
                text_widget.tag_add("bullet", start_pos, end_pos)
            
            line_index += 1
    
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
    
    def export_markdown_report(self):
        """Export the markdown report to a file"""
        filename = filedialog.asksaveasfilename(
            parent=self.parent,
            defaultextension=".md",
            filetypes=[("Markdown Files", "*.md"), ("All Files", "*.*")],
            title="Export Markdown Report"
        )
        
        if filename:
            try:
                with open(filename, "w") as f:
                    f.write(self.markdown_report)
                messagebox.showinfo(
                    "Export Successful", 
                    f"Markdown report exported to {filename}",
                    parent=self.parent
                )
            except Exception as e:
                messagebox.showerror(
                    "Export Error", 
                    f"An error occurred during export: {str(e)}",
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
        elif tab_text == "Markdown":
            self.parent.clipboard_append(self.markdown_report)
            message = "Markdown report copied to clipboard"
        else:
            message = "No valid tab selected"
        
        # Show confirmation
        messagebox.showinfo("Copied to Clipboard", message, parent=self.parent)