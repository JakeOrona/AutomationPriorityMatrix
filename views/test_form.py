"""
test_form.py - Component for the test input form
"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class TestForm:
    """
    Test input form component
    """
    def __init__(self, parent, model, on_test_added=None):
        """
        Initialize the test form
        
        Args:
            parent: The parent frame
            model: The prioritization model
            on_test_added (function, optional): Callback when a test is added
        """
        self.parent = parent
        self.model = model
        self.on_test_added = on_test_added
        
        # Initialize variables for UI components
        self.test_id_var = tk.StringVar(value=self.model.current_id)
        self.test_name_var = tk.StringVar()
        self.test_desc_var = tk.StringVar()
        self.ticket_id_var = tk.StringVar(value="AUTO-")
        self.section_var = tk.StringVar()
        self.priority_var = tk.StringVar()
        self.score_vars = {}
        self.yes_no_vars = {}
        
        # Create the form
        self.create_form()
    
    def create_form(self):
        """Create the input form for test details"""
        # Form container with scrollbar
        form_container = ttk.Frame(self.parent)
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

        form_row = 0
        
        # Test basic info frame
        basic_info_frame = ttk.LabelFrame(scrollable_frame, text="Test Information")
        basic_info_frame.grid(row=form_row, column=0, columnspan=2, sticky=tk.W+tk.E, pady=(0,5), padx=5)
        
        info_row = 0
        
        # Test Name
        ttk.Label(basic_info_frame, text="Test Name:").grid(row=info_row, column=0, sticky=tk.W, pady=5, padx=5)
        ttk.Entry(basic_info_frame, textvariable=self.test_name_var, width=40).grid(
            row=info_row, column=1, sticky=tk.W, pady=5, padx=5
        )
        info_row += 1
        
        # Test Description
        ttk.Label(basic_info_frame, text="Description:").grid(row=info_row, column=0, sticky=tk.W, pady=5, padx=5)
        ttk.Entry(basic_info_frame, textvariable=self.test_desc_var, width=40).grid(
            row=info_row, column=1, sticky=tk.W, pady=5, padx=5
        )
        info_row += 1

        # Ticket ID
        ttk.Label(basic_info_frame, text="Ticket ID:").grid(row=info_row, column=0, sticky=tk.W, pady=5, padx=5)
        ttk.Entry(basic_info_frame, textvariable=self.ticket_id_var, width=40).grid(
            row=info_row, column=1, sticky=tk.W, pady=5, padx=5
        )
        info_row += 1
        
        # Section dropdown
        ttk.Label(basic_info_frame, text="Section:").grid(row=info_row, column=0, sticky=tk.W, pady=5, padx=5)
        
        # Create a combobox for section selection
        section_frame = ttk.Frame(basic_info_frame)
        section_frame.grid(row=info_row, column=1, sticky=tk.W, pady=5, padx=5)
        
        # Get available sections from the model
        sections = list(self.model.sections)
        sections.sort()  # Sort alphabetically
        
        # Create the combobox with existing sections
        self.section_combo = ttk.Combobox(section_frame, textvariable=self.section_var, width=25)
        self.section_combo['values'] = sections
        self.section_combo.pack(side=tk.LEFT, padx=(0, 5))
        
        # Option to add a new section
        ttk.Button(
            section_frame, 
            text="Add New", 
            command=self.add_new_section,
            width=10
        ).pack(side=tk.LEFT)
        
        info_row += 1
        
        # "Can it be automated?" factor moved to basic info section
        if "can_be_automated" in self.model.factors:
            # Add a separator
            ttk.Separator(basic_info_frame, orient='horizontal').grid(
                row=info_row, column=0, columnspan=2, sticky=tk.EW, pady=5
            )
            info_row += 1
            
            # Create radio buttons for the automation possibility
            ttk.Label(basic_info_frame, text=self.model.factors["can_be_automated"]["name"]).grid(
                row=info_row, column=0, sticky=tk.W, pady=5, padx=5
            )
            
            self.score_vars["can_be_automated"] = tk.IntVar(value=5)  # Default to Yes (5)
            
            radio_frame = ttk.Frame(basic_info_frame)
            radio_frame.grid(row=info_row, column=1, sticky=tk.W, pady=5, padx=5)
            
            for score, label in self.model.score_options["can_be_automated"].items():
                rb = ttk.Radiobutton(
                    radio_frame, 
                    text=f"{label}", 
                    variable=self.score_vars["can_be_automated"], 
                    value=score
                )
                rb.pack(side=tk.LEFT, padx=10)
            info_row += 1

            # Add info label explaining the importance of this factor
            info_label = ttk.Label(
                basic_info_frame, 
                text="If a test cannot be automated, it will be categorized as 'Can't Automate' and will receive a priority score of 0.",
                font=("", 9, "italic")
            )
            info_label.grid(row=info_row, column=0, columnspan=2, sticky=tk.W, pady=5, padx=5)
        
        form_row += 1
        
        # Prioritization factors section
        factors_frame = ttk.LabelFrame(scrollable_frame, text="Prioritization Factors")
        factors_frame.grid(row=form_row, column=0, columnspan=2, sticky=tk.W+tk.E, pady=5, padx=5)
        
        factor_row = 0
        
        # Iterate through scoring factors in an inner frame
        for factor, details in self.model.factors.items():
            # Skip the can_be_automated factor as it's in the basic info section
            if factor == "can_be_automated":
                continue
                
            ttk.Label(factors_frame, text=f"{details['name']} (weight: {details['weight']}):").grid(
                row=factor_row, column=0, sticky=tk.W, pady=5, padx=5
            )
            
            self.score_vars[factor] = tk.IntVar(value=3)  # Default to medium (3)
            
            score_frame = ttk.Frame(factors_frame)
            score_frame.grid(row=factor_row, column=1, sticky=tk.W, pady=5, padx=5)
            
            for score, label in self.model.score_options[factor].items():
                rb = ttk.Radiobutton(
                    score_frame, 
                    text=f"{score} - {label}", 
                    variable=self.score_vars[factor], 
                    value=score
                )
                rb.pack(anchor=tk.W)
            
            factor_row += 1
        
        form_row += 1
        
        # Yes/No questions section - only create if the model has yes/no questions
        if self.model.yes_no_questions:
            questions_frame = ttk.LabelFrame(scrollable_frame, text="Additional Questions")
            questions_frame.grid(row=form_row, column=0, columnspan=2, sticky=tk.W+tk.E, pady=5, padx=5)
            
            question_row = 0
            
            for key, question_data in self.model.yes_no_questions.items():
                self.yes_no_vars[key] = tk.BooleanVar(value=False)
                
                question_frame = ttk.Frame(questions_frame)
                question_frame.grid(row=question_row, column=0, columnspan=2, sticky=tk.W, pady=5, padx=5)
                
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
                
                question_row += 1
            
            form_row += 1
        
        # Buttons for form actions
        button_frame = ttk.Frame(self.parent)
        button_frame.pack(fill=tk.X, pady=5)
        
        # Create an inner frame to center the buttons
        center_button_frame = ttk.Frame(button_frame)
        center_button_frame.pack(anchor=tk.CENTER)

        ttk.Button(center_button_frame, text="Add Test", command=self.add_test).pack(side=tk.LEFT, padx=5)
        ttk.Button(center_button_frame, text="Clear Form", command=self.clear_form).pack(side=tk.LEFT, padx=5)
        
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
            self.section_var.set(new_section)
    
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
        test = self.model.add_test(
            self.test_name_var.get(),
            self.section_var.get(),
            self.test_desc_var.get(),
            self.ticket_id_var.get(),
            scores,
            yes_no_answers,
            self.priority_var.get()
        )
        
        # Call the callback if provided
        if self.on_test_added:
            self.on_test_added()
        
        # Clear form
        self.clear_form()
        
        # Update ID for next test
        self.test_id_var.set(self.model.current_id)
        
        # Update section combobox values in case new section was added
        sections = list(self.model.sections)
        sections.sort()
        self.section_combo['values'] = sections
        # Update section combobox values in case new section was added
        self.update_section_combobox()

    def update_section_combobox(self):
        """Update the section combobox with current sections from the model"""
        sections = list(self.model.sections)
        sections.sort()
        self.section_combo['values'] = sections
    
    def clear_form(self):
        """Clear the input form"""
        self.test_name_var.set("")
        self.test_desc_var.set("")
        self.ticket_id_var.set("AUTO-")
        self.section_var.set("")  # Clear section
        
        # Reset automation possibility to Yes (5)
        if "can_be_automated" in self.score_vars:
            self.score_vars["can_be_automated"].set(5)
            
        # Reset other scores to medium (3)
        for factor, var in self.score_vars.items():
            if factor != "can_be_automated":
                var.set(3)
                
        # Reset yes/no questions to No (False)
        for var in self.yes_no_vars.values():
            var.set(False)
    
    def set_test_for_editing(self, test):
        """
        Set form values for editing an existing test
        
        Args:
            test (dict): Test dictionary to edit
        """
        self.test_name_var.set(test["name"])
        self.test_id_var.set(test["id"])
        self.test_desc_var.set(test["description"])
        self.ticket_id_var.set(test["ticket_id"])
        self.section_var.set(test.get("section", ""))
        self.priority_var.set(test["priority"])
        
        # Update section combobox values in case sections were added
        sections = list(self.model.sections)
        sections.sort()
        self.section_combo['values'] = sections
        
        for factor, score in test["scores"].items():
            if factor in self.score_vars:
                self.score_vars[factor].set(score)
        
        # Set yes/no question values
        if hasattr(self.model, 'yes_no_questions') and 'yes_no_answers' in test:
            for key in self.yes_no_vars:
                self.yes_no_vars[key].set(test['yes_no_answers'].get(key, False))