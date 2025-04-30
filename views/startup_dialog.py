"""
startup_dialog.py - Dialog for startup actions like CSV import
"""
import tkinter as tk
from tkinter import messagebox, filedialog
from utils.file_operations import FileOperations

class StartupDialog:
    """
    Dialog that appears on application startup to offer CSV import
    """
    def __init__(self, parent, model, app):
        """
        Initialize and show the startup dialog
        
        Args:
            parent: The parent window
            model: The prioritization model
            app: The main application window
        """
        self.parent = parent
        self.model = model
        self.app = app
        
        # Create the dialog window
        self.create_dialog()
        
    def create_dialog(self):
        """Create the dialog window"""
        # Create a top-level window for the prompt
        self.window = tk.Toplevel(self.parent)
        self.window.title("Import Tests")
        self.window.geometry("400x150")
        self.window.transient(self.parent)  # Make window modal
        self.window.grab_set()  # Make window modal
        
        # Center the window
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.parent.winfo_screenwidth() // 2) - (width // 2)
        y = (self.parent.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        
        # Create frame with padding
        frame = tk.Frame(self.window, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Add message
        message_label = tk.Label(
            frame, 
            text="Would you like to import tests from a CSV file?",
            font=("", 12)
        )
        message_label.pack(pady=(0, 20))
        
        # Add buttons
        button_frame = tk.Frame(frame)
        button_frame.pack()
        
        # Create Yes and No buttons
        yes_button = tk.Button(
            button_frame, 
            text="Yes",
            command=self.import_csv,
            width=10,
        )
        yes_button.pack(side=tk.LEFT, padx=10)
        
        no_button = tk.Button(
            button_frame, 
            text="No", 
            command=self.close_dialog,
            width=10
        )
        no_button.pack(side=tk.LEFT, padx=10)
        
        # Set focus to Yes button
        yes_button.focus_set()
        
        # Make the dialog respond to Return and Escape keys
        self.window.bind("<Return>", lambda event: self.import_csv())
        self.window.bind("<Escape>", lambda event: self.close_dialog())
        
    def import_csv(self):
        """Handle CSV import"""
        self.window.destroy()  # Close the dialog window
        
        # Show file dialog to select CSV file
        filename = filedialog.askopenfilename(
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
            title="Import Tests from CSV"
        )
        
        if filename:
            # Use FileOperations to import
            success, data = FileOperations.import_from_csv(filename)
            
            if not success:
                messagebox.showerror("Import Error", data)  # data contains error message
                return
            
            # Import tests using the model with the option to replace existing tests
            # This ensures only the imported tests are listed after startup import
            replace = True
            count = self.model.import_tests(data, replace)
            
            # Update display
            self.app.test_list.update_list()
            self.app.test_form.update_section_combobox()
            
            messagebox.showinfo("Import Successful", f"{count} tests imported from {filename}")
    
    def close_dialog(self):
        """Close the dialog without importing"""
        self.window.destroy()