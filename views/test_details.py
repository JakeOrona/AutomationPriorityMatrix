"""
test_details.py - Component for displaying test details
"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class TestDetailsView:
    """
    Component for viewing and editing test details
    """
    def __init__(self, parent, model, test, on_update=None, on_delete=None):
        """
        Initialize the test details view
        
        Args:
            parent: The parent window
            model: The prioritization model
            test (dict): The test to display
            on_update (function, optional): Callback when the test is updated
            on_delete (function, optional): Callback when the test is deleted
        """
        self.parent = parent
        self.model = model
        self.test = test
        self.on_update = on_update
        self.on_delete = on_delete
        
        # Flag to track if we're in edit mode
        self.is_edit_mode = False
        
        # Create variables for editing
        self.init_variables()
        
        # Create the details view
        self.create_details_view()
    
    def init_variables(self):
        """Initialize variables for the view"""
        self.edit_name_var = tk.StringVar(value=self.test["name"])
        self.edit_desc_var = tk.StringVar(value=self.test["description"])
        self.edit_ticket_id_var = tk.StringVar(value=self.test["ticket_id"])
        self.edit_section_var = tk.StringVar(value=self.test.get("section", ""))
        self.edit_score_vars = {}
        self.edit_yes_no_vars = {}
    
    def create_details_view(self):
        """Create the details view"""
        # Set window title
        self.parent.title(f"Test Details: {self.test['name']}")
        self.parent.geometry("700x1000")
        
        # Create main frame with padding
        main_frame = ttk.Frame(self.parent, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create scrollable canvas
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Populate the view
        self.populate_view()
    
    def populate_view(self):
        """Populate the view with test data"""
        # Clear existing widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        row = 0
        
        # Basic info section with either labels or entry fields
        if self.is_edit_mode:
            # In edit mode - show input fields
            ttk.Label(self.scrollable_frame, text="Test Name:").grid(row=row, column=0, sticky=tk.W, pady=5)
            ttk.Entry(self.scrollable_frame, textvariable=self.edit_name_var, width=40).grid(
                row=row, column=1, sticky=tk.W, pady=5
            )
            row += 1
            
            ttk.Label(self.scrollable_frame, text="Description:").grid(row=row, column=0, sticky=tk.W, pady=5)
            ttk.Entry(self.scrollable_frame, textvariable=self.edit_desc_var, width=40).grid(
                row=row, column=1, sticky=tk.W, pady=5
            )
            row += 1
            
            ttk.Label(self.scrollable_frame, text="Ticket ID:").grid(row=row, column=0, sticky=tk.W, pady=5)
            ttk.Entry(self.scrollable_frame, textvariable=self.edit_ticket_id_var, width=40).grid(
                row=row, column=1, sticky=tk.W, pady=5
            )
            row += 1
            
            # Section dropdown
            ttk.Label(self.scrollable_frame, text="Section:").grid(row=row, column=0, sticky=tk.W, pady=5)

            # Create a frame for section selection
            section_frame = ttk.Frame(self.scrollable_frame)
            section_frame.grid(row=row, column=1, sticky=tk.W, pady=5)

            # Get available sections from the model - get the LATEST sections
            sections = list(self.model.sections)
            sections.sort()  # Sort alphabetically

            # Create the combobox with existing sections
            self.section_combo = ttk.Combobox(section_frame, textvariable=self.edit_section_var, width=25)
            self.section_combo['values'] = sections
            self.section_combo.pack(side=tk.LEFT, padx=(0, 5))
            
            # Option to add a new section
            ttk.Button(
                section_frame, 
                text="Add New", 
                command=self.add_new_section,
                width=10
            ).pack(side=tk.LEFT)
            
            row += 1
            
        else:
            # In view mode - show labels
            ttk.Label(self.scrollable_frame, text=f"Test Name: {self.test['name']}", font=("", 12)).grid(
                row=row, column=0, columnspan=2, sticky=tk.W, pady=5
            )
            row += 1
            
            ttk.Label(self.scrollable_frame, text=f"Description: {self.test['description']}", font=("", 12)).grid(
                row=row, column=0, columnspan=2, sticky=tk.W, pady=5
            )
            row += 1
            
            ttk.Label(self.scrollable_frame, text=f"Ticket ID: {self.test['ticket_id']}", font=("", 12)).grid(
                row=row, column=0, columnspan=2, sticky=tk.W, pady=5
            )
            row += 1
            
            # Show section if available
            if self.test.get("section"):
                ttk.Label(self.scrollable_frame, text=f"Section: {self.test['section']}", font=("", 12)).grid(
                    row=row, column=0, columnspan=2, sticky=tk.W, pady=5
                )
                row += 1
        
        # If test is in "Can't Automate" category, show simplified view with reason
        if self.test['priority'] == "Can't Automate":
            # Show raw score as 0 and note that it can't be automated
            ttk.Label(self.scrollable_frame, text=f"Raw Score: 0 (Test cannot be automated)", font=("", 12)).grid(
                row=row, column=0, columnspan=2, sticky=tk.W, pady=5
            )
            row += 1
            
            ttk.Label(self.scrollable_frame, text=f"Priority Score: 0 / 100", font=("", 12, "bold")).grid(
                row=row, column=0, columnspan=2, sticky=tk.W, pady=5
            )
            row += 1
            
            # Priority category with color
            priority_frame = ttk.Frame(self.scrollable_frame)
            priority_frame.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
            
            ttk.Label(priority_frame, text="Priority: ", font=("", 12)).pack(side=tk.LEFT)
            
            priority_value = tk.Label(
                priority_frame, 
                text=self.test['priority'],
                font=("", 12, "bold")
            )
            
            # Set color for "Can't Automate"
            priority_value.configure(foreground="gray")
            
            priority_value.pack(side=tk.LEFT)
            row += 1
            
            # Display the "Can it be automated?" factor first
            if "can_be_automated" in self.test["scores"]:
                factor_frame = ttk.LabelFrame(self.scrollable_frame, text="Can it be automated?")
                factor_frame.grid(row=row, column=0, columnspan=2, sticky=tk.W+tk.E, pady=5, padx=5)
                
                if self.is_edit_mode:
                    # In edit mode - show radio buttons
                    self.edit_score_vars["can_be_automated"] = tk.IntVar(value=self.test["scores"]["can_be_automated"])
                    
                    for score, label in self.model.score_options["can_be_automated"].items():
                        rb = ttk.Radiobutton(
                            factor_frame, 
                            text=f"{score} - {label}", 
                            variable=self.edit_score_vars["can_be_automated"], 
                            value=score
                        )
                        rb.pack(anchor=tk.W)
                else:
                    # In view mode - show current value
                    factor_description = self.model.score_options["can_be_automated"][1]  # "No"
                    ttk.Label(factor_frame, text=f"Score: 1 - {factor_description}").grid(
                        row=0, column=0, sticky=tk.W, padx=5, pady=2
                    )
                    ttk.Label(factor_frame, text=f"Weight: {self.model.factors['can_be_automated']['weight']}").grid(
                        row=1, column=0, sticky=tk.W, padx=5, pady=2
                    )
                    ttk.Label(factor_frame, text="Tests marked as 'Cannot be automated' are assigned zero priority.").grid(
                        row=2, column=0, sticky=tk.W, padx=5, pady=2
                    )
                
                row += 1
        else:
            # Regular test - show normal score information
            max_possible_raw = sum(5 * details["weight"] for factor, details in self.model.factors.items() 
                                if factor != "can_be_automated")
            ttk.Label(self.scrollable_frame, text=f"Raw Score: {self.test['raw_score']} / {max_possible_raw}", font=("", 12)).grid(
                row=row, column=0, columnspan=2, sticky=tk.W, pady=5
            )
            row += 1
            
            ttk.Label(self.scrollable_frame, text=f"Priority Score: {self.test['total_score']} / 100", font=("", 12, "bold")).grid(
                row=row, column=0, columnspan=2, sticky=tk.W, pady=5
            )
            row += 1
            
            # Priority category with color
            priority_frame = ttk.Frame(self.scrollable_frame)
            priority_frame.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
            
            ttk.Label(priority_frame, text="Priority: ", font=("", 12)).pack(side=tk.LEFT)
            
            priority_value = tk.Label(
                priority_frame, 
                text=self.test['priority'],
                font=("", 12, "bold")
            )
            
            # Set color based on priority
            if self.test['priority'] == "Highest":
                priority_value.configure(foreground="red")
            elif self.test['priority'] == "High":
                priority_value.configure(foreground="orange")
            elif self.test['priority'] == "Medium":
                priority_value.configure(foreground="yellow")
            elif self.test['priority'] == "Low":
                priority_value.configure(foreground="blue")
            else:  # Lowest
                priority_value.configure(foreground="lightblue")
            
            priority_value.pack(side=tk.LEFT)
            row += 1
        
        # Display factor scores
        ttk.Label(self.scrollable_frame, text="Score Breakdown:", font=("", 12, "underline")).grid(
            row=row, column=0, columnspan=2, sticky=tk.W, pady=10
        )
        row += 1
        
        for factor, details in self.model.factors.items():
            # For can't automate tests, skip displaying other factors if we're in view mode
            if self.test['priority'] == "Can't Automate" and factor != "can_be_automated" and not self.is_edit_mode:
                continue
                
            current_score = self.test["scores"].get(factor, 3)  # Default to 3 if missing
            
            # Create frame with border for each factor
            factor_frame = ttk.LabelFrame(self.scrollable_frame, text=details["name"])
            factor_frame.grid(row=row, column=0, columnspan=2, sticky=tk.W+tk.E, pady=5, padx=5)
            
            if self.is_edit_mode:
                # In edit mode - show radio buttons
                self.edit_score_vars[factor] = tk.IntVar(value=current_score)
                
                for score, label in self.model.score_options[factor].items():
                    rb = ttk.Radiobutton(
                        factor_frame, 
                        text=f"{score} - {label}", 
                        variable=self.edit_score_vars[factor], 
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
                
                # Only show contribution if not the "can_be_automated" factor (which has 0 weight)
                if factor != "can_be_automated":
                    ttk.Label(factor_frame, text=f"Contribution: {factor_contribution} points").grid(
                        row=2, column=0, sticky=tk.W, padx=5, pady=2
                    )
            
            row += 1
        
        # Display yes/no questions if available
        if hasattr(self.model, 'yes_no_questions') and len(self.model.yes_no_questions) > 0:
            ttk.Label(self.scrollable_frame, text="Additional Questions:", font=("", 12, "underline")).grid(
                row=row, column=0, columnspan=2, sticky=tk.W, pady=10
            )
            row += 1
            
            for key, question_info in self.model.yes_no_questions.items():
                current_answer = self.test.get('yes_no_answers', {}).get(key, False)
                
                question_frame = ttk.LabelFrame(self.scrollable_frame, text=question_info["question"])
                question_frame.grid(row=row, column=0, columnspan=2, sticky=tk.W+tk.E, pady=5, padx=5)
                
                if self.is_edit_mode:
                    # In edit mode - show checkbutton
                    self.edit_yes_no_vars[key] = tk.BooleanVar(value=current_answer)
                    cb = ttk.Checkbutton(
                        question_frame,
                        text="Yes",
                        variable=self.edit_yes_no_vars[key]
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
        button_frame = ttk.Frame(self.scrollable_frame)
        button_frame.grid(row=row, column=0, columnspan=2, pady=15)
        
        if self.is_edit_mode:
            # Buttons for edit mode
            ttk.Button(button_frame, text="Save Changes", command=self.save_edits).pack(side=tk.LEFT, padx=5)
            ttk.Button(button_frame, text="Cancel", command=self.toggle_edit_mode).pack(side=tk.LEFT, padx=5)
        else:
            # Buttons for view mode
            ttk.Button(button_frame, text="Edit Test", command=self.toggle_edit_mode).pack(side=tk.LEFT, padx=5)
            ttk.Button(button_frame, text="Delete Test", command=self.delete_test).pack(side=tk.LEFT, padx=5)
            ttk.Button(button_frame, text="Close", command=self.parent.destroy).pack(side=tk.LEFT, padx=5)
    
    def add_new_section(self):
        """Open a dialog to add a new section"""
        new_section = simpledialog.askstring("New Section", "Enter a new section name:", parent=self.parent)
        
        if new_section:
            # Add to model's sections
            self.model.sections.add(new_section)
            
            # Update combobox values
            sections = list(self.model.sections)
            sections.sort()
            self.section_combo['values'] = sections
            
            # Set the combobox to the new value
            self.edit_section_var.set(new_section)
    
    def toggle_edit_mode(self):
        """Toggle between view and edit modes"""
        self.is_edit_mode = not self.is_edit_mode
        self.populate_view()
    
    def save_edits(self):
        """Save edited test data"""
        # Gather updated scores
        scores = {factor: var.get() for factor, var in self.edit_score_vars.items()}
        
        # Gather updated yes/no answers
        yes_no_answers = {key: var.get() for key, var in self.edit_yes_no_vars.items()}
        
        # Update test using the model
        updated_test = self.model.update_test(
            self.test["id"],
            self.edit_name_var.get(),
            self.edit_section_var.get(),
            self.edit_desc_var.get(),
            self.edit_ticket_id_var.get(),
            scores,
            yes_no_answers
        )
        
        if updated_test:
            self.test = updated_test
            self.is_edit_mode = False
            self.populate_view()
            
            # Call update callback if provided
            if self.on_update:
                self.on_update()
            
            # Update window title
            self.parent.title(f"Test Details: {self.test['name']}")
    
    def delete_test(self):
        """Delete the test"""
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete test '{self.test['name']}'?"):
            if self.model.delete_one_test(self.test["id"]):
                # Call delete callback if provided
                if self.on_delete:
                    self.on_delete()
                
                # Close the window
                self.parent.destroy()