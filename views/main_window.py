"""
main_window.py - Main application window
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from views.test_form import TestForm
from views.test_list import TestList
from views.test_details import TestDetailsView
from views.reports.text_report import TextReportView
from views.reports.chart_report import ChartReportView
from utils.file_operations import FileOperations

class MainWindow:
    """
    Main application window
    """
    def __init__(self, root, model):
        """
        Initialize the main window
        
        Args:
            root: The root Tkinter instance
            model: The prioritization model
        """
        self.root = root
        self.model = model
        
        # Create main frames
        self.create_frames()
        
        # Create menu bar
        self.create_menu()
        
        # Create components
        self.create_components()
    
    def create_frames(self):
        """Create the main frames for the application"""
        # Main container with padding
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel (for input form)
        self.input_frame = ttk.LabelFrame(self.main_frame, text="Test Details", padding="5")
        self.input_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Right panel (for test list)
        self.list_frame = ttk.LabelFrame(self.main_frame, text="Prioritized Tests", padding="5")
        self.list_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
    
    def create_menu(self):
        """Create the application menu"""
        # Create menu bar
        menubar = tk.Menu(self.root)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Export to CSV", command=self.export_to_csv)
        file_menu.add_command(label="Import from CSV", command=self.import_from_csv)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Reports menu
        report_menu = tk.Menu(menubar, tearoff=0)
        report_menu.add_command(label="Text Report", command=self.show_text_report)
        report_menu.add_command(label="HTML Report", command=self.show_html_report)
        report_menu.add_command(label="Graphical Report", command=self.show_graphical_report)
        menubar.add_cascade(label="Reports", menu=report_menu)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Scoring Guide", command=self.show_scoring_guide)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def create_components(self):
        """Create the main components"""
        # Create the test form in the left panel
        self.test_form = TestForm(
            self.input_frame, 
            self.model, 
            on_test_added=self.on_test_updated
        )
        
        # Create the test list in the right panel
        self.test_list = TestList(
            self.list_frame, 
            self.model,
            on_view_details=self.show_test_details,
            on_edit=self.edit_test,
            on_delete=self.on_test_updated
        )
        
        # Initial list update
        self.test_list.update_list()
    
    def on_test_updated(self):
        """Callback when a test is added, updated, or deleted"""
        self.test_list.update_list()
        self.test_form.update_section_combobox()
    
    def show_test_details(self, test):
        """Show test details in a new window"""
        details_window = tk.Toplevel(self.root)
        TestDetailsView(
            details_window, 
            self.model, 
            test,
            on_update=self.on_test_updated,
            on_delete=self.on_test_updated
        )
    
    def edit_test(self, test):
        """Edit the selected test"""
        # Use the test form to edit the test
        self.test_form.set_test_for_editing(test)
    
    def export_to_csv(self):
        """Export tests to a CSV file"""
        if not self.model.tests:
            messagebox.showinfo("Export", "No tests to export")
            return
        
        # Ask for save location
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
            title="Export Tests to CSV"
        )
        
        if not filename:
            return
        
        # Use FileOperations to export
        success = FileOperations.export_to_csv(filename, self.model.tests, self.model.factors)
        
        if success:
            messagebox.showinfo("Export Successful", f"Tests exported to {filename}")
        else:
            messagebox.showerror("Export Error", "An error occurred during export")
    
    def import_from_csv(self):
        """Import tests from a CSV file"""
        # Ask for file location
        filename = filedialog.askopenfilename(
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
            title="Import Tests from CSV"
        )
        
        if not filename:
            return
        
        # Use FileOperations to import
        success, data = FileOperations.import_from_csv(filename)
        
        if not success:
            messagebox.showerror("Import Error", data)  # data contains error message
            return
        
        # Ask if user wants to replace or append
        replace = messagebox.askyesno(
            "Import", 
            "Do you want to replace all existing tests with imported data?"
        )
        
        # Import tests using the model
        count = self.model.import_tests(data, replace)
        
        # Update display
        self.on_test_updated()
        
        messagebox.showinfo("Import Successful", f"{count} tests imported from {filename}")
    
    def show_text_report(self):
        """Show the text report"""
        report_window = tk.Toplevel(self.root)
        TextReportView(report_window, self.model)

    def show_html_report(self):
        """Show HTML report"""
        report_window = tk.Toplevel(self.root)
        from views.reports.html_report import HtmlReportView
        HtmlReportView(report_window, self.model)
    
    def show_graphical_report(self):
        """Show graphical reports"""
        report_window = tk.Toplevel(self.root)
        ChartReportView(report_window, self.model)
    
    def show_about(self):
        """Show the about dialog"""
        about_text = "Test Automation Prioritization Tool\n\n"
        about_text += "This application helps QA teams decide which manual tests to automate first.\n\n"
        about_text += "Using a weighted scoring system, it calculates which tests will provide\n"
        about_text += "the highest return on investment when automated.\n\n"
        about_text += "Developed by Jake Orona\n"
        about_text += "Version: 1.0.0-beta\n"
        about_text += "License: MIT\n\n"
        about_text += "For more information, visit the GitHub repository:\n"
        about_text += "https://github.com/JakeOrona/AutomationPriorityMatrix\n"
        
        messagebox.showinfo("About", about_text)
    
    def show_scoring_guide(self):
        """Show the scoring guide"""
        # Generate guide text
        guide_text = FileOperations.generate_scoring_guide_text(
            self.model.factors,
            self.model.score_options
        )
        
        # Create guide window
        guide_window = tk.Toplevel(self.root)
        guide_window.title("Scoring Guide")
        guide_window.geometry("700x500")
        
        # Create scrollable text widget
        guide_frame = ttk.Frame(guide_window, padding=10)
        guide_frame.pack(fill=tk.BOTH, expand=True)
        
        text_widget = tk.Text(guide_frame, wrap=tk.WORD, padx=10, pady=10)
        scrollbar = ttk.Scrollbar(guide_frame, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Insert guide text
        text_widget.insert(tk.END, guide_text)
        
        # Make text widget read-only
        text_widget.configure(state="disabled")
        
        # Add close button
        ttk.Button(guide_window, text="Close", command=guide_window.destroy).pack(pady=10)