"""
main.py - Main entry point for the test prioritization application
"""
import tkinter as tk
from models.prioritization import TestPrioritizationModel
from views.main_window import MainWindow
from views.startup_dialog import StartupDialog

def main():
    """
    Main function to run the application
    """
    # Create the root window
    root = tk.Tk()
    root.title("Test Automation Prioritization Tool")
    root.geometry("1430x870")
    
    # Create the model
    model = TestPrioritizationModel()
    
    # Initialize the main window with the model
    app = MainWindow(root, model)
    
    # Show import prompt after a short delay (allows main window to draw first)
    root.after(200, lambda: StartupDialog(root, model, app))
    
    # Start the main event loop
    root.mainloop()

if __name__ == "__main__":
    main()