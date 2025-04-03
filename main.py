"""
main.py - Main entry point for the test prioritization application
"""
import tkinter as tk
from models import TestPrioritizationModel
from gui import TestPrioritizationGUI

def main():
    """
    Main function to run the application
    """
    # Create the root window
    root = tk.Tk()
    
    # Create the model
    model = TestPrioritizationModel()
    
    # Create the GUI with the model
    app = TestPrioritizationGUI(root, model)
    
    # Start the main event loop
    root.mainloop()

if __name__ == "__main__":
    main()