"""
gui.py - Contains the GUI components for the test prioritization application
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from models import TestPrioritizationModel
from file_util import FileOperations

class TestPrioritizationGUI:
    """
    GUI class for the test prioritization application
    """
    def __init__(self, root, model):
        """
        Initialize the GUI
        
        Args:
            root: The Tkinter root window
            model (TestPrioritizationModel): The model instance
        """
        self.root = root
        self.model = model
        
        # Configure root window
        self.root.title("Test Automation Prioritization Tool")
        self.root.geometry("1600x800")
        
        # Initialize variables for UI components
        self.test_id_var = tk.StringVar(value=self.model.current_id)
        self.test_name_var = tk.StringVar()
        self.test_desc_var = tk.StringVar()
        self.ticket_id_var = tk.StringVar(value="AUTO-")
        self.priority_var = tk.StringVar()
        self.score_vars = {}
        self.yes_no_vars = {}
        
        # Create main frames
        self.create_frames()
        self.create_input_form()
        self.create_test_list()
        self.create_menu()
    
    def create_frames(self):
        """Create the main frames for the application"""
        # Main container with padding
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel (for input form)
        self.input_frame = ttk.LabelFrame(self.main_frame, text="Test Details", padding="10")
        self.input_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Right panel (for test list)
        self.list_frame = ttk.LabelFrame(self.main_frame, text="Prioritized Tests", padding="10")
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
        report_menu.add_command(label="Prioritization Report", command=self.show_priority_report)
        menubar.add_cascade(label="Reports", menu=report_menu)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Scoring Guide", command=self.show_scoring_guide)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def create_input_form(self):
        """Create the input form for test details"""
        # Form container with scrollbar
        form_container = ttk.Frame(self.input_frame)
        form_container.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(form_container)
        scrollbar = ttk.Scrollbar(form_container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Test Name
        ttk.Label(scrollable_frame, text="Test Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(scrollable_frame, textvariable=self.test_name_var, width=40).grid(
            row=0, column=1, sticky=tk.W, pady=5
        )
        
        # Test Description
        ttk.Label(scrollable_frame, text="Description:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(scrollable_frame, textvariable=self.test_desc_var, width=40).grid(
            row=1, column=1, sticky=tk.W, pady=5

        )

        # Ticket ID
        ttk.Label(scrollable_frame, text="Ticket ID:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(scrollable_frame, textvariable=self.ticket_id_var, width=40).grid(
            row=2, column=1, sticky=tk.W, pady=5
        )
        
        
        # Scoring factors
        row = 3
        
        for factor, details in self.model.factors.items():
            ttk.Label(scrollable_frame, text=f"{details['name']} (weight: {details['weight']}):").grid(
                row=row, column=0, sticky=tk.W, pady=5
            )
            
            self.score_vars[factor] = tk.IntVar(value=3)  # Default to medium (3)
            
            score_frame = ttk.Frame(scrollable_frame)
            score_frame.grid(row=row, column=1, sticky=tk.W, pady=5)
            
            for score, label in self.model.score_options[factor].items():
                rb = ttk.Radiobutton(
                    score_frame, 
                    text=f"{score} - {label}", 
                    variable=self.score_vars[factor], 
                    value=score
                )
                rb.pack(anchor=tk.W)
            
            row += 1
        
        # Yes/No questions section
        if self.model.yes_no_questions:
            ttk.Label(scrollable_frame, text="Additional Questions:", font=("", 10, "bold")).grid(
                row=row, column=0, columnspan=2, sticky=tk.W, pady=10
            )
            row += 1
            
            for key, question_data in self.model.yes_no_questions.items():
                self.yes_no_vars[key] = tk.BooleanVar(value=False)
                
                question_frame = ttk.Frame(scrollable_frame)
                question_frame.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
                
                cb = ttk.Checkbutton(
                    question_frame,
                    text=question_data["question"],
                    variable=self.yes_no_vars[key]
                )
                cb.pack(side=tk.LEFT, anchor=tk.W)
                
                # Add a small label explaining the impact
                ttk.Label(
                    question_frame, 
                    text=f"({question_data['impact']})",
                    font=("", 8, "italic")
                ).pack(side=tk.LEFT, padx=10)
                
                row += 1
        
        # Buttons for form actions
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.grid(row=row, column=0, columnspan=2, pady=15)
        
        ttk.Button(button_frame, text="Add Test", command=self.add_test).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_form).pack(side=tk.LEFT, padx=5)
    
    def create_test_list(self):
        """Create the list view for prioritized tests"""
        # Create treeview for test list with scrollbar
        columns = ("rank", "ticket", "name", "priority", "score")
        
        self.tree_frame = ttk.Frame(self.list_frame)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)
        
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings", selectmode="browse")
        
        # Define column headings
        self.tree.heading("rank", text="Rank")
        self.tree.heading("ticket", text="Ticket ID")
        self.tree.heading("name", text="Test Name")
        self.tree.heading("priority", text="Priority")
        self.tree.heading("score", text="Priority Score")
        
        # Define column widths
        self.tree.column("rank", width=50)
        self.tree.column("ticket", width=80)
        self.tree.column("name", width=200)
        self.tree.column("priority", width=80)
        self.tree.column("score", width=100)
        
        # Add vertical scrollbar
        vsb = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        
        # Pack the treeview and scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add buttons for test actions
        button_frame = ttk.Frame(self.list_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="View Details", command=self.view_test_details).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Edit Test", command=self.edit_test).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Test", command=self.delete_one_test).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete All Tests", command=self.delete_all_tests).pack(side=tk.LEFT, padx=5)
        
        # Bind double-click event to view details
        self.tree.bind("<Double-1>", lambda e: self.view_test_details())
    
    def add_test(self):
        """Add a test based on form input"""
        # Validate input
        if not self.test_name_var.get().strip():
            messagebox.showerror("Input Error", "Test name cannot be empty")
            return
        
        # Gather scores from form
        scores = {factor: var.get() for factor, var in self.score_vars.items()}
        
        # Gather yes/no answers
        yes_no_answers = {key: var.get() for key, var in self.yes_no_vars.items()}
        
        # Add test using the model
        self.model.add_test(
            self.test_id_var.get(),
            self.test_name_var.get(),
            self.test_desc_var.get(),
            self.ticket_id_var.get(),
            scores,
            yes_no_answers,
            self.priority_var.get()
        )
        
        # Update display
        self.update_test_list()
        self.clear_form()
        
        # Update ID for next test
        self.test_id_var.set(self.model.current_id)
    
    def update_test_list(self):
        """Update the test list display with sorted tests"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get sorted tests and add to treeview
        sorted_tests = self.model.get_sorted_tests()
        
        for i, test in enumerate(sorted_tests):
            rank = i + 1
            self.tree.insert("", "end", values=(rank, test["ticket_id"], test["name"], test["priority"], test["total_score"]))
    
    def clear_form(self):
        """Clear the input form"""
        self.test_name_var.set("")
        self.test_desc_var.set("")
        for var in self.score_vars.values():
            var.set(3)  # Reset to medium (3)
        for var in self.yes_no_vars.values():
            var.set(False)  # Reset to No
    
    def view_test_details(self):
        """Show detailed view of the selected test"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showinfo("Selection", "Please select a test to view")
            return
        
        # Get test ID from the selected item
        test_id = self.model.find_test_id_by_name(
            self.tree.item(selected_item[0], "values")[2]  # Use the third column (name) to find the test
        )
        
        # Find the test in the model
        test = self.model.find_test_by_id(test_id)
        if not test:
            return
        
        # Create detail window
        detail_window = tk.Toplevel(self.root)
        detail_window.title(f"Test Details: {test['name']}")
        detail_window.geometry("600x600")  # Increased height for yes/no questions
        
        # Create scrollable frame
        main_frame = ttk.Frame(detail_window, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Display basic info
        
        ttk.Label(scrollable_frame, text=f"Test Name: {test['name']}", font=("", 12)).grid(
            row=0, column=0, columnspan=2, sticky=tk.W, pady=5
        )
        
        ttk.Label(scrollable_frame, text=f"Description: {test['description']}", font=("", 12)).grid(
            row=1, column=0, columnspan=2, sticky=tk.W, pady=5
        )

        ttk.Label(scrollable_frame, text=f"Ticket ID: {test['ticket_id']}", font=("", 12)).grid(
            row=2, column=0, sticky=tk.W, pady=5
        )
        
        # Show raw and normalized scores
        ttk.Label(scrollable_frame, text=f"Raw Score: {test['raw_score']} / 60", font=("", 12)).grid(
            row=3, column=0, columnspan=2, sticky=tk.W, pady=5
        )
        ttk.Label(scrollable_frame, text=f"Priority Score: {test['total_score']} / 100", font=("", 12, "bold")).grid(
            row=4, column=0, columnspan=2, sticky=tk.W, pady=5
        )
        row_index = 5
        
        # Display yes/no questions if available
        if hasattr(self.model, 'yes_no_questions') and test.get('yes_no_answers'):
            ttk.Label(scrollable_frame, text="Additional Questions:", font=("", 12, "underline")).grid(
                row=row_index, column=0, columnspan=2, sticky=tk.W, pady=10
            )
            row_index += 1
            
            for key, question_info in self.model.yes_no_questions.items():
                answer = test['yes_no_answers'].get(key, False)
                answer_text = "Yes" if answer else "No"
                
                question_frame = ttk.LabelFrame(scrollable_frame, text=question_info["question"])
                question_frame.grid(row=row_index, column=0, columnspan=2, sticky=tk.W+tk.E, pady=5, padx=5)
                
                ttk.Label(question_frame, text=f"Answer: {answer_text}").grid(
                    row=0, column=0, sticky=tk.W, padx=5, pady=2
                )
                ttk.Label(question_frame, text=f"Impact: {question_info['impact']}").grid(
                    row=1, column=0, sticky=tk.W, padx=5, pady=2
                )
                
                row_index += 1
        
        # Display factor scores with descriptions
        ttk.Label(scrollable_frame, text="Score Breakdown:", font=("", 12, "underline")).grid(
            row=row_index, column=0, columnspan=2, sticky=tk.W, pady=10
        )
        row_index += 1
        
        for factor, score in test["scores"].items():
            factor_name = self.model.factors[factor]["name"]
            factor_weight = self.model.factors[factor]["weight"]
            factor_description = self.model.score_options[factor][score]
            factor_contribution = score * factor_weight
            
            # Create frame with border for each factor
            factor_frame = ttk.LabelFrame(scrollable_frame, text=factor_name)
            factor_frame.grid(row=row_index, column=0, columnspan=2, sticky=tk.W+tk.E, pady=5, padx=5)
            
            ttk.Label(factor_frame, text=f"Score: {score} - {factor_description}").grid(
                row=0, column=0, sticky=tk.W, padx=5, pady=2
            )
            ttk.Label(factor_frame, text=f"Weight: {factor_weight}").grid(
                row=1, column=0, sticky=tk.W, padx=5, pady=2
            )
            ttk.Label(factor_frame, text=f"Contribution: {factor_contribution} points").grid(
                row=2, column=0, sticky=tk.W, padx=5, pady=2
            )
            
            row_index += 1
        
        # Add close button
        ttk.Button(scrollable_frame, text="Close", command=detail_window.destroy).grid(
            row=row_index, column=0, columnspan=2, pady=15
        )
    
    def edit_test(self):
        """Edit the selected test"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showinfo("Selection", "Please select a test to edit")
            return
        
        # Get test ID from the selected item's internal ID
        item_id = selected_item[0]  # Get the first selected item's ID
        test_name = self.tree.item(item_id, "values")[2]  # Use the third column (name) to find the test
        
        # Find the test in the model
        test = self.model.find_test_id_by_name(test_name)
        if not test:
            messagebox.showerror("Error", "Test not found")
            return
        
        # Get the full test data
        test = self.model.find_test_by_id(test)
        if not test:
            messagebox.showerror("Error", "Test not found")
            return
        
        # Populate form with test data
        self.test_name_var.set(test["name"])
        self.test_id_var.set(test["id"])
        self.test_desc_var.set(test["description"])
        self.ticket_id_var.set(test["ticket_id"])
        self.priority_var.set(test["priority"])
        
        for factor, score in test["scores"].items():
            self.score_vars[factor].set(score)
        
        # Set yes/no question values
        if hasattr(self.model, 'yes_no_questions') and 'yes_no_answers' in test:
            for key in self.yes_no_vars:
                self.yes_no_vars[key].set(test['yes_no_answers'].get(key, False))

        
        # Create edit window with save button
        edit_window = tk.Toplevel(self.root)
        edit_window.title(f"Edit Test: {test['name']}")
        
        edit_frame = ttk.Frame(edit_window, padding=10)
        edit_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(
            edit_frame,
            text="Editing test. Please update values in the main form and click Save.",
            font=("", 12)
        ).pack(pady=10)
        
        def save_edit():
            # Gather updated scores
            scores = {factor: var.get() for factor, var in self.score_vars.items()}
            
            # Gather updated yes/no answers
            yes_no_answers = {key: var.get() for key, var in self.yes_no_vars.items()}
            
            # Update test using the model
            self.model.update_test(
                self.test_id_var.get(),
                self.test_name_var.get(),
                self.test_desc_var.get(),
                self.ticket_id_var.get(),
                scores,
                yes_no_answers,
                self.priority_var.get()
            )
            
            # Update display
            self.update_test_list()
            
            # Clear form and reset ID
            self.clear_form()
            self.test_id_var.set(self.model.current_id)
            
            # Close edit window
            edit_window.destroy()
        
        def cancel_edit():
            # Clear form and reset ID
            self.clear_form()
            self.test_id_var.set(self.model.current_id)
            edit_window.destroy()
        
        button_frame = ttk.Frame(edit_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Save Changes", command=save_edit).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=cancel_edit).pack(side=tk.LEFT, padx=5)
    
    def delete_all_tests(self):
        """Delete all tests"""

        # Confirm deletion
        if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete all tests?"):
            return
        
        # Delete tests using the model
        self.model.delete_all_tests()
        
        # Update display
        self.update_test_list()

    def delete_one_test(self):
        """Delete the selected test"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showinfo("Selection", "Please select a test to delete")
            return
        
        # Get test ID from the selected item's internal ID
        item_id = selected_item[0]
        test_name = self.tree.item(item_id, "values")[2]  # Use the third column (name) to find the test
        test = self.model.find_test_id_by_name(test_name)
        if not test:  
            messagebox.showerror("Error", "Test not found")
            return
        # Confirm deletion
        if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete test '{test_name}'?"):
            return
        # Delete test using the model
        self.model.delete_one_test(test)
        # Update display
        self.update_test_list()
        # Clear form and reset ID
        self.clear_form()
        self.test_id_var.set(self.model.current_id - 1)
    
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
        self.update_test_list()
        self.test_id_var.set(f"{self.model.current_id:03d}")
        
        messagebox.showinfo("Import Successful", f"{count} tests imported from {filename}")
    
    def show_priority_report(self):
        """Show the prioritization report"""
        if not self.model.tests:
            messagebox.showinfo("Report", "No tests available for report")
            return
        
        # Get priority tiers from the model
        priority_tiers = self.model.get_priority_tiers()
        
        # Generate report text
        report_text = FileOperations.generate_report_text(self.model.tests, priority_tiers)
        
        # Create report window
        report_window = tk.Toplevel(self.root)
        report_window.title("Test Automation Priority Report")
        report_window.geometry("800x600")
        
        # Create scrollable text widget
        report_frame = ttk.Frame(report_window, padding=10)
        report_frame.pack(fill=tk.BOTH, expand=True)
        
        text_widget = tk.Text(report_frame, wrap=tk.WORD, padx=10, pady=10)
        scrollbar = ttk.Scrollbar(report_frame, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Insert report text
        text_widget.insert(tk.END, report_text)
        
        # Make text widget read-only
        text_widget.configure(state="disabled")
        
        # Add export button
        button_frame = ttk.Frame(report_window)
        button_frame.pack(fill=tk.X, pady=10, padx=10)
        
        def export_report():
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
                title="Export Report"
            )
            
            if filename:
                success = FileOperations.export_report_to_file(filename, report_text)
                if success:
                    messagebox.showinfo("Export Successful", f"Report exported to {filename}")
                else:
                    messagebox.showerror("Export Error", "An error occurred during export")
        
        ttk.Button(button_frame, text="Export Report", command=export_report).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Close", command=report_window.destroy).pack(side=tk.RIGHT, padx=5)
    
    def show_about(self):
        """Show the about dialog"""
        about_text = "Test Automation Prioritization Tool\n\n"
        about_text += "This application helps QA teams decide which manual tests to automate first.\n\n"
        about_text += "Using a weighted scoring system, it calculates which tests will provide\n"
        about_text += "the highest return on investment when automated."
        
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