"""
test_form.py - Component for the test input form
"""
import tkinter as tk
from tkinter import ttk, messagebox

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
        
        # Test Name
        ttk.Label(scrollable_frame, text="Test Name:").grid(row=form_row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(scrollable_frame, textvariable=self.test_name_var, width=40).grid(
            row=form_row, column=1, sticky=tk.W, pady=5
        )
        form_row += 1
        
        # Test Description
        ttk.Label(scrollable_frame, text="Description:").grid(row=form_row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(scrollable_frame, textvariable=self.test_desc_var, width=40).grid(
            row=form_row, column=1, sticky=tk.W, pady=5
        )
        
        form_row += 1

        # Ticket ID
        ttk.Label(scrollable_frame, text="Ticket ID:").grid(row=form_row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(scrollable_frame, textvariable=self.ticket_id_var, width=40).grid(
            row=form_row, column=1, sticky=tk.W, pady=5
        )
        
        form_row += 1

        # Scoring factors - First add "Can it be automated?" with a note about its importance
        if "can_be_automated" in self.model.factors:
            automation_frame = ttk.LabelFrame(scrollable_frame, text="Automation Possibility Assessment")
            automation_frame.grid(row=form_row, column=0, columnspan=2, sticky=tk.W+tk.E, pady=10, padx=5)
            
            # Add an info label explaining the importance of this factor
            ttk.Label(
                automation_frame, 
                text="If 'No' is selected, the test will be categorized as 'Can't Automate'\n" +
                    "and will receive a priority score of 0.",
                font=("", 9, "italic")
            ).pack(pady=5, padx=5, anchor=tk.W)
            
            factor_frame = ttk.Frame(automation_frame)
            factor_frame.pack(fill=tk.X, padx=5, pady=5)
            
            ttk.Label(factor_frame, text=self.model.factors["can_be_automated"]["name"]).pack(side=tk.LEFT, padx=5)
            
            # Create radio buttons for the automation possibility
            self.score_vars["can_be_automated"] = tk.IntVar(value=5)  # Default to Yes (5)
            
            radio_frame = ttk.Frame(factor_frame)
            radio_frame.pack(side=tk.LEFT, padx=20)
            
            for score, label in self.model.score_options["can_be_automated"].items():
                rb = ttk.Radiobutton(
                    radio_frame, 
                    text=f"{label}", 
                    variable=self.score_vars["can_be_automated"], 
                    value=score
                )
                rb.pack(side=tk.LEFT, padx=10)
            
            form_row += 1
            
            # Add a separator
            ttk.Separator(scrollable_frame, orient='horizontal').grid(
                row=form_row, column=0, columnspan=2, sticky=tk.EW, pady=10
            )
            form_row += 1
            
            # Add a header for the remaining factors
            ttk.Label(
                scrollable_frame, 
                text="Prioritization Factors (Only applicable if the test can be automated)",
                font=("", 10, "bold")
            ).grid(row=form_row, column=0, columnspan=2, sticky=tk.W, pady=5)
            form_row += 1

        # Remaining scoring factors
        for factor, details in self.model.factors.items():
            # Skip the can_be_automated factor as it's already handled
            if factor == "can_be_automated":
                continue
                
            ttk.Label(scrollable_frame, text=f"{details['name']} (weight: {details['weight']}):").grid(
                row=form_row, column=0, sticky=tk.W, pady=5
            )
            
            self.score_vars[factor] = tk.IntVar(value=3)  # Default to medium (3)
            
            score_frame = ttk.Frame(scrollable_frame)
            score_frame.grid(row=form_row, column=1, sticky=tk.W, pady=5)
            
            for score, label in self.model.score_options[factor].items():
                rb = ttk.Radiobutton(
                    score_frame, 
                    text=f"{score} - {label}", 
                    variable=self.score_vars[factor], 
                    value=score
                )
                rb.pack(anchor=tk.W)
            
            form_row += 1
        
        # Yes/No questions section
        if self.model.yes_no_questions:
            ttk.Label(scrollable_frame, text="Additional Questions:", font=("", 10, "bold")).grid(
                row=form_row, column=0, columnspan=2, sticky=tk.W, pady=10
            )
            form_row += 1
            
            for key, question_data in self.model.yes_no_questions.items():
                self.yes_no_vars[key] = tk.BooleanVar(value=False)
                
                question_frame = ttk.Frame(scrollable_frame)
                question_frame.grid(row=form_row, column=0, columnspan=2, sticky=tk.W, pady=5)
                
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
                
                form_row += 1
        
        # Buttons for form actions
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.grid(row=form_row, column=0, columnspan=2, pady=15)
        
        ttk.Button(button_frame, text="Add Test", command=self.add_test).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_form).pack(side=tk.LEFT, padx=5)
    
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
    
    def clear_form(self):
        """Clear the input form"""
        self.test_name_var.set("")
        self.test_desc_var.set("")
        self.ticket_id_var.set("AUTO-")
        
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
        self.priority_var.set(test["priority"])
        
        for factor, score in test["scores"].items():
            if factor in self.score_vars:
                self.score_vars[factor].set(score)
        
        # Set yes/no question values
        if hasattr(self.model, 'yes_no_questions') and 'yes_no_answers' in test:
            for key in self.yes_no_vars:
                self.yes_no_vars[key].set(test['yes_no_answers'].get(key, False))