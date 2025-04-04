"""
gui.py - Contains the GUI components for the test prioritization application
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import os
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
        report_menu.add_command(label="Text Priority Report", command=self.show_priority_report)
        report_menu.add_command(label="Graphical Report", command=self.show_graphical_report)
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
        """Show detailed view of the selected test with integrated editing functionality"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showinfo("Selection", "Please select a test to view")
            return
        
        # Get test ID from the selected item
        test_name = self.tree.item(selected_item[0], "values")[2]
        test_id = self.model.find_test_id_by_name(test_name)
        
        # Find the test in the model
        test = self.model.find_test_by_id(test_id)
        if not test:
            return
        
        # Create detail window
        detail_window = tk.Toplevel(self.root)
        detail_window.title(f"Test Details: {test['name']}")
        detail_window.geometry("700x800")
        
        # Create variables for editing
        edit_name_var = tk.StringVar(value=test["name"])
        edit_desc_var = tk.StringVar(value=test["description"])
        edit_ticket_id_var = tk.StringVar(value=test["ticket_id"])
        edit_score_vars = {}
        edit_yes_no_vars = {}
        
        # Flag to track if we're in edit mode
        is_edit_mode = tk.BooleanVar(value=False)
        
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
        
        # Function to refresh the view (used after saving or canceling edit)
        def refresh_view():
            # Clear the frame
            for widget in scrollable_frame.winfo_children():
                widget.destroy()
            
            # Get the updated test data
            updated_test = self.model.find_test_by_id(test_id)
            if not updated_test:
                detail_window.destroy()
                return
            
            # Re-populate with current test data
            populate_view(updated_test)

            # Reset edit mode
            is_edit_mode.set(False)
        
        # Function to toggle between view and edit modes
        def toggle_edit_mode():
            is_edit_mode.set(not is_edit_mode.get())
            refresh_view()
        
        # Function to save edits
        def save_edits():
            # Gather updated scores
            scores = {factor: var.get() for factor, var in edit_score_vars.items()}
            
            # Gather updated yes/no answers
            yes_no_answers = {key: var.get() for key, var in edit_yes_no_vars.items()}
            
            # Update test using the model
            self.model.update_test(
                test_id,
                edit_name_var.get(),
                edit_desc_var.get(),
                edit_ticket_id_var.get(),
                scores,
                yes_no_answers
            )
            
            # Update the main list
            self.update_test_list()
            
            # Refresh the detail view
            refresh_view()
        
        # Function to delete the test
        def delete_test():
            if messagebox.askyesno("Confirm Delete", 
                                f"Are you sure you want to delete test '{test['name']}'?", 
                                parent=detail_window):
                self.model.delete_one_test(test_id)
                self.update_test_list()
                detail_window.destroy()
        
        # Function to populate the view
        def populate_view(test_data):
            row = 0
            
            # Basic info section with either labels or entry fields
            if is_edit_mode.get():
                # In edit mode - show input fields
                ttk.Label(scrollable_frame, text="Test Name:").grid(row=row, column=0, sticky=tk.W, pady=5)
                ttk.Entry(scrollable_frame, textvariable=edit_name_var, width=40).grid(
                    row=row, column=1, sticky=tk.W, pady=5
                )
                row += 1
                
                ttk.Label(scrollable_frame, text="Description:").grid(row=row, column=0, sticky=tk.W, pady=5)
                ttk.Entry(scrollable_frame, textvariable=edit_desc_var, width=40).grid(
                    row=row, column=1, sticky=tk.W, pady=5
                )
                row += 1
                
                ttk.Label(scrollable_frame, text="Ticket ID:").grid(row=row, column=0, sticky=tk.W, pady=5)
                ttk.Entry(scrollable_frame, textvariable=edit_ticket_id_var, width=40).grid(
                    row=row, column=1, sticky=tk.W, pady=5
                )
                row += 1
                
            else:
                # In view mode - show labels
                ttk.Label(scrollable_frame, text=f"Test Name: {test_data['name']}", font=("", 12)).grid(
                    row=row, column=0, columnspan=2, sticky=tk.W, pady=5
                )
                row += 1
                
                ttk.Label(scrollable_frame, text=f"Description: {test_data['description']}", font=("", 12)).grid(
                    row=row, column=0, columnspan=2, sticky=tk.W, pady=5
                )
                row += 1
                
                ttk.Label(scrollable_frame, text=f"Ticket ID: {test_data['ticket_id']}", font=("", 12)).grid(
                    row=row, column=0, columnspan=2, sticky=tk.W, pady=5
                )
                row += 1
            
            # Show raw and normalized scores (always in view mode)
            ttk.Label(scrollable_frame, text=f"Raw Score: {test_data['raw_score']} / 60", font=("", 12)).grid(
                row=row, column=0, columnspan=2, sticky=tk.W, pady=5
            )
            row += 1
            
            ttk.Label(scrollable_frame, text=f"Priority Score: {test_data['total_score']} / 100", font=("", 12, "bold")).grid(
                row=row, column=0, columnspan=2, sticky=tk.W, pady=5
            )
            row += 1
            
            # Priority category with color
            priority_frame = ttk.Frame(scrollable_frame)
            priority_frame.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
            
            ttk.Label(priority_frame, text="Priority: ", font=("", 12)).pack(side=tk.LEFT)
            
            priority_value = tk.Label(
                priority_frame, 
                text=test_data['priority'],
                font=("", 12, "bold")
            )
            
            # Set color based on priority
            if test_data['priority'] == "High":
                priority_value.configure(foreground="green")
            elif test_data['priority'] == "Medium":
                priority_value.configure(foreground="orange")
            else:  # Low
                priority_value.configure(foreground="red")
            
            priority_value.pack(side=tk.LEFT)
            row += 1
            
            # Display factor scores
            ttk.Label(scrollable_frame, text="Score Breakdown:", font=("", 12, "underline")).grid(
                row=row, column=0, columnspan=2, sticky=tk.W, pady=10
            )
            row += 1
            
            for factor, details in self.model.factors.items():
                current_score = test_data["scores"].get(factor, 3)  # Default to 3 if missing
                
                # Create frame with border for each factor
                factor_frame = ttk.LabelFrame(scrollable_frame, text=details["name"])
                factor_frame.grid(row=row, column=0, columnspan=2, sticky=tk.W+tk.E, pady=5, padx=5)
                
                if is_edit_mode.get():
                    # In edit mode - show radio buttons
                    edit_score_vars[factor] = tk.IntVar(value=current_score)
                    
                    for score, label in self.model.score_options[factor].items():
                        rb = ttk.Radiobutton(
                            factor_frame, 
                            text=f"{score} - {label}", 
                            variable=edit_score_vars[factor], 
                            value=score
                        )
                        rb.pack(anchor=tk.W)
                else:
                    # In view mode - show current values
                    factor_description = self.model.score_options[factor][current_score]
                    factor_weight = details["weight"]
                    factor_contribution = current_score * factor_weight
                    
                    ttk.Label(factor_frame, text=f"Score: {current_score} - {factor_description}").grid(
                        row=0, column=0, sticky=tk.W, padx=5, pady=2
                    )
                    ttk.Label(factor_frame, text=f"Weight: {factor_weight}").grid(
                        row=1, column=0, sticky=tk.W, padx=5, pady=2
                    )
                    ttk.Label(factor_frame, text=f"Contribution: {factor_contribution} points").grid(
                        row=2, column=0, sticky=tk.W, padx=5, pady=2
                    )
                
                row += 1
            
            # Display yes/no questions if available
            if hasattr(self.model, 'yes_no_questions') and len(self.model.yes_no_questions) > 0:
                ttk.Label(scrollable_frame, text="Additional Questions:", font=("", 12, "underline")).grid(
                    row=row, column=0, columnspan=2, sticky=tk.W, pady=10
                )
                row += 1
                
                for key, question_info in self.model.yes_no_questions.items():
                    current_answer = test_data.get('yes_no_answers', {}).get(key, False)
                    
                    question_frame = ttk.LabelFrame(scrollable_frame, text=question_info["question"])
                    question_frame.grid(row=row, column=0, columnspan=2, sticky=tk.W+tk.E, pady=5, padx=5)
                    
                    if is_edit_mode.get():
                        # In edit mode - show checkbutton
                        edit_yes_no_vars[key] = tk.BooleanVar(value=current_answer)
                        cb = ttk.Checkbutton(
                            question_frame,
                            text="Yes",
                            variable=edit_yes_no_vars[key]
                        )
                        cb.grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
                        
                        ttk.Label(question_frame, text=f"Impact: {question_info['impact']}").grid(
                            row=1, column=0, sticky=tk.W, padx=5, pady=2
                        )
                    else:
                        # In view mode - show current value
                        answer_text = "Yes" if current_answer else "No"
                        ttk.Label(question_frame, text=f"Answer: {answer_text}").grid(
                            row=0, column=0, sticky=tk.W, padx=5, pady=2
                        )
                        ttk.Label(question_frame, text=f"Impact: {question_info['impact']}").grid(
                            row=1, column=0, sticky=tk.W, padx=5, pady=2
                        )
                    
                    row += 1
            
            # Add action buttons
            button_frame = ttk.Frame(scrollable_frame)
            button_frame.grid(row=row, column=0, columnspan=2, pady=15)
            
            if is_edit_mode.get():
                # Buttons for edit mode
                ttk.Button(button_frame, text="Save Changes", command=save_edits).pack(side=tk.LEFT, padx=5)
                ttk.Button(button_frame, text="Cancel", command=refresh_view).pack(side=tk.LEFT, padx=5)
            else:
                # Buttons for view mode
                ttk.Button(button_frame, text="Edit Test", command=toggle_edit_mode).pack(side=tk.LEFT, padx=5)
                ttk.Button(button_frame, text="Delete Test", command=delete_test).pack(side=tk.LEFT, padx=5)
                ttk.Button(button_frame, text="Close", command=detail_window.destroy).pack(side=tk.LEFT, padx=5)
        
        # Initial population of the view
        populate_view(test)
        
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
    
    def edit_test_by_id(self, test_id):
        """Edit a test by its ID (used from detail window)"""
        # Find the test in the model
        test = self.model.find_test_by_id(test_id)
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
            if factor in self.score_vars:
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
    
    def edit_test(self):
        """Edit the selected test from the list view"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showinfo("Selection", "Please select a test to edit")
            return
        
        # Get test ID from the selected item's internal ID
        item_id = selected_item[0]  # Get the first selected item's ID
        test_name = self.tree.item(item_id, "values")[2]  # Use the third column (name) to find the test
        
        # Find the test in the model
        test_id = self.model.find_test_id_by_name(test_name)
        if not test_id:
            messagebox.showerror("Error", "Test not found")
            return
        
        self.edit_test_by_id(test_id)
        
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
    
    def show_graphical_report(self):
        """Show a graphical report of test prioritization data with export capability"""
        if not self.model.tests:
            messagebox.showinfo("Report", "No tests available for graphical report")
            return
        
        # Create report window
        report_window = tk.Toplevel(self.root)
        report_window.title("Test Prioritization Graphical Report")
        report_window.geometry("1200x900")
        
        # Create notebook for multiple graphs
        notebook = ttk.Notebook(report_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Try to import matplotlib for plotting
        try:
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            from matplotlib.figure import Figure
            import numpy as np
            
            # Dictionary to store figures for export
            figures = {}
            
            # 1. Priority Distribution Tab
            priority_frame = ttk.Frame(notebook)
            notebook.add(priority_frame, text="Priority Distribution")
            
            fig1 = Figure(figsize=(8, 6))
            ax1 = fig1.add_subplot(111)
            figures["Priority Distribution"] = fig1
            
            # Count tests by priority
            priority_counts = {"High": 0, "Medium": 0, "Low": 0}
            for test in self.model.tests:
                priority_counts[test["priority"]] += 1
            
            # Create pie chart
            labels = list(priority_counts.keys())
            sizes = list(priority_counts.values())
            colors = ['green', 'orange', 'red']
            explode = (0.1, 0, 0)  # Explode the 1st slice (High priority)
            
            # Plot if there's data
            if sum(sizes) > 0:
                ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
                    shadow=True, startangle=90)
                ax1.axis('equal')  # Equal aspect ratio ensures the pie chart is circular
                ax1.set_title('Test Priority Distribution')
            else:
                ax1.text(0.5, 0.5, "No data available", horizontalalignment='center',
                        verticalalignment='center', transform=ax1.transAxes)
            
            # Add the plot to the frame
            canvas1 = FigureCanvasTkAgg(fig1, master=priority_frame)
            canvas1.draw()
            canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # 2. Score Distribution Tab
            score_frame = ttk.Frame(notebook)
            notebook.add(score_frame, text="Score Distribution")
            
            fig2 = Figure(figsize=(8, 6))
            ax2 = fig2.add_subplot(111)
            figures["Score Distribution"] = fig2
            
            # Get scores for histogram
            scores = [test["total_score"] for test in self.model.tests]
            
            if scores:
                # Create histogram
                bins = np.linspace(0, 100, 11)  # 10 bins from 0 to 100
                ax2.hist(scores, bins=bins, color='skyblue', edgecolor='black')
                ax2.set_title('Test Score Distribution')
                ax2.set_xlabel('Priority Score')
                ax2.set_ylabel('Number of Tests')
                ax2.set_xticks(bins)
                
                # Add vertical lines for threshold values
                priority_tiers = self.model.get_priority_tiers()
                ax2.axvline(x=priority_tiers["high_threshold"], color='green', linestyle='--', 
                            label=f'High Threshold ({priority_tiers["high_threshold"]:.1f})')
                ax2.axvline(x=priority_tiers["medium_threshold"], color='orange', linestyle='--', 
                            label=f'Medium Threshold ({priority_tiers["medium_threshold"]:.1f})')
                ax2.legend()
            else:
                ax2.text(0.5, 0.5, "No data available", horizontalalignment='center',
                        verticalalignment='center', transform=ax2.transAxes)
            
            # Add the plot to the frame
            canvas2 = FigureCanvasTkAgg(fig2, master=score_frame)
            canvas2.draw()
            canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # 3. Factor Contribution Tab
            factor_frame = ttk.Frame(notebook)
            notebook.add(factor_frame, text="Factor Contribution")
            
            fig3 = Figure(figsize=(8, 6))
            ax3 = fig3.add_subplot(111)
            figures["Factor Contribution"] = fig3
            
            if self.model.tests:
                # Calculate average scores for each factor
                factor_avgs = {}
                factor_names = {}
                
                for factor, info in self.model.factors.items():
                    factor_scores = [test["scores"].get(factor, 0) for test in self.model.tests]
                    factor_avgs[factor] = sum(factor_scores) / len(self.model.tests)
                    factor_names[factor] = info["name"]
                
                # Create bar chart
                factors = list(factor_avgs.keys())
                avg_scores = [factor_avgs[f] for f in factors]
                bar_labels = [factor_names[f] for f in factors]
                
                bars = ax3.bar(range(len(factors)), avg_scores, color='lightblue')
                ax3.set_xticks(range(len(factors)))
                ax3.set_xticklabels(bar_labels, rotation=45, ha='right')
                ax3.set_title('Average Score by Factor')
                ax3.set_ylabel('Average Score (1-5)')
                ax3.set_ylim(0, 5)
                
                # Add the score values on top of bars
                for bar in bars:
                    height = bar.get_height()
                    ax3.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                            f'{height:.1f}', ha='center', va='bottom')
                
                fig3.tight_layout()  # Adjust layout for rotated labels
            else:
                ax3.text(0.5, 0.5, "No data available", horizontalalignment='center',
                        verticalalignment='center', transform=ax3.transAxes)
            
            # Add the plot to the frame
            canvas3 = FigureCanvasTkAgg(fig3, master=factor_frame)
            canvas3.draw()
            canvas3.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # 4. Top Tests Tab
            top_tests_frame = ttk.Frame(notebook)
            notebook.add(top_tests_frame, text="Top Tests")
            
            fig4 = Figure(figsize=(8, 6))
            ax4 = fig4.add_subplot(111)
            figures["Top Tests"] = fig4
            
            if self.model.tests:
                # Get sorted tests
                sorted_tests = self.model.get_sorted_tests()
                
                # Take top 10 or fewer
                top_n = min(10, len(sorted_tests))
                top_tests = sorted_tests[:top_n]
                
                # Create horizontal bar chart
                test_names = [test["name"] if len(test["name"]) <= 20 else test["name"][:17] + "..." 
                            for test in top_tests]
                test_scores = [test["total_score"] for test in top_tests]
                
                # Reverse lists for bottom-to-top display
                test_names.reverse()
                test_scores.reverse()
                
                # Create color map based on priority
                colors = []
                for test in reversed(top_tests):
                    if test["priority"] == "High":
                        colors.append("green")
                    elif test["priority"] == "Medium":
                        colors.append("orange")
                    else:
                        colors.append("red")
                
                # Plot horizontal bars
                bars = ax4.barh(range(len(test_names)), test_scores, color=colors)
                ax4.set_yticks(range(len(test_names)))
                ax4.set_yticklabels(test_names)
                ax4.set_title(f'Top {top_n} Tests by Priority Score')
                ax4.set_xlabel('Priority Score')
                ax4.set_xlim(0, 100)
                
                # Add the score values at the end of bars
                for i, bar in enumerate(bars):
                    width = bar.get_width()
                    ax4.text(width + 1, bar.get_y() + bar.get_height()/2.,
                            f'{width:.1f}', va='center')
                
                fig4.tight_layout()  # Adjust layout for long test names
            else:
                ax4.text(0.5, 0.5, "No data available", horizontalalignment='center',
                        verticalalignment='center', transform=ax4.transAxes)
            
            # Add the plot to the frame
            canvas4 = FigureCanvasTkAgg(fig4, master=top_tests_frame)
            canvas4.draw()
            canvas4.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # Function to export the current graph
            def export_current_graph():
                # Get the current tab name
                current_tab = notebook.tab(notebook.select(), "text")
                
                if current_tab in figures:
                    # Ask for save location
                    filename = filedialog.asksaveasfilename(
                        defaultextension=".png",
                        filetypes=[
                            ("PNG files", "*.png"),
                            ("JPEG files", "*.jpg"),
                            ("PDF files", "*.pdf"),
                            ("SVG files", "*.svg"),
                            ("All files", "*.*")
                        ],
                        title=f"Export {current_tab} Graph"
                    )
                    
                    if filename:
                        # Get file extension to determine format
                        extension = filename.split(".")[-1].lower()
                        
                        try:
                            # Save the figure
                            figures[current_tab].savefig(filename, dpi=300, bbox_inches='tight', 
                                                        format=extension if extension != "jpg" else "jpeg")
                            messagebox.showinfo("Export Successful", f"Graph exported to {filename}")
                        except Exception as e:
                            messagebox.showerror("Export Error", f"Error saving graph: {str(e)}")
                            
            # Function to export all graphs
            def export_all_graphs():
                # Ask for directory
                directory = filedialog.askdirectory(title="Select Directory for Exporting All Graphs")
                
                if directory:
                    # Generate timestamp for filenames
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    
                    # Export each graph
                    success_count = 0
                    for graph_name, figure in figures.items():
                        # Create filename with timestamp
                        safe_name = graph_name.replace(" ", "_").lower()
                        filename = os.path.join(directory, f"{safe_name}_{timestamp}.png")
                        
                        try:
                            # Save the figure
                            figure.savefig(filename, dpi=300, bbox_inches='tight')
                            success_count += 1
                        except Exception as e:
                            messagebox.showerror("Export Error", 
                                            f"Error saving {graph_name}: {str(e)}")
                    
                    if success_count > 0:
                        messagebox.showinfo("Export Successful", 
                                        f"Exported {success_count} graphs to {directory}")
            
            # Create export buttons
            button_frame = ttk.Frame(report_window)
            button_frame.pack(fill=tk.X, pady=10)
            
            ttk.Button(button_frame, text="Export Current Graph", 
                    command=export_current_graph).pack(side=tk.LEFT, padx=5)
            ttk.Button(button_frame, text="Export All Graphs", 
                    command=export_all_graphs).pack(side=tk.LEFT, padx=5)
            ttk.Button(button_frame, text="Close", 
                    command=report_window.destroy).pack(side=tk.RIGHT, padx=5)
            
        except ImportError:
            # If matplotlib is not available, show error message
            error_frame = ttk.Frame(report_window, padding=20)
            error_frame.pack(fill=tk.BOTH, expand=True)
            
            ttk.Label(
                error_frame,
                text="Matplotlib is required for graphical reports.\n\n" +
                    "Please install it using:\n" +
                    "pip install matplotlib",
                font=("", 12)
            ).pack(pady=20)
            
            # Just add close button
            ttk.Button(report_window, text="Close", 
                    command=report_window.destroy).pack(pady=10)
        
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