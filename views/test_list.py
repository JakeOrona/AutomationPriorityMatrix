"""
test_list.py - Component for displaying the list of tests
"""
import tkinter as tk
from tkinter import ttk, messagebox

class TestList:
    """
    Component for displaying and managing the list of tests
    """
    def __init__(self, parent, model, on_view_details=None, on_edit=None, on_delete=None):
        """
        Initialize the test list
        
        Args:
            parent: The parent frame
            model: The prioritization model
            on_view_details (function, optional): Callback when viewing test details
            on_edit (function, optional): Callback when editing a test
            on_delete (function, optional): Callback when deleting a test
        """
        self.parent = parent
        self.model = model
        self.on_view_details = on_view_details
        self.on_edit = on_edit
        self.on_delete = on_delete
        
        # Define color scheme for priority levels
        self.priority_colors = {
            "Highest": "#DC143C",  # Crimson
            "High": "#FF6347",      # Tomato
            "Medium": "#FFA500",   # Orange
            "Low": "#228B22",     # Forest Green
            "Lowest": "#4fc3f7"    # light blue
        }
        
        # Create the list view
        self.create_list_view()
    
    def create_list_view(self):
        """Create the list view for prioritized tests"""
        # Create treeview for test list with scrollbar
        columns = ("rank", "ticket", "name", "priority", "score")
        
        self.tree_frame = ttk.Frame(self.parent)
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
        button_frame = ttk.Frame(self.parent)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="View Details", command=self.view_details).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Edit Test", command=self.edit_test).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Test", command=self.delete_test).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete All Tests", command=self.delete_all_tests).pack(side=tk.LEFT, padx=5)
        
        # Bind double-click event to view details
        self.tree.bind("<Double-1>", lambda e: self.view_details())
        
        # Create custom tags for colored priority and score columns
        for priority, color in self.priority_colors.items():
            self.tree.tag_configure(priority, foreground=color)
    
    def update_list(self):
        """Update the test list display with sorted tests"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get sorted tests and add to treeview
        sorted_tests = self.model.get_sorted_tests()
        
        for i, test in enumerate(sorted_tests):
            rank = i + 1
            priority = test["priority"]
            
            # Insert item with appropriate tag for coloring
            item_id = self.tree.insert(
                "", 
                "end", 
                values=(rank, test["ticket_id"], test["name"], priority, test["total_score"]),
                tags=(priority,)
            )
        
    
    def get_selected_test(self):
        """
        Get the currently selected test
        
        Returns:
            dict: The selected test dictionary or None if no selection
        """
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showinfo("Selection", "Please select a test")
            return None
        
        # Get test name from the selected item
        test_name = self.tree.item(selected_item[0], "values")[2]
        
        # Find the test by name
        test_id = self.model.find_test_id_by_name(test_name)
        if not test_id:
            messagebox.showerror("Error", "Test not found")
            return None
        
        # Return the full test details
        return self.model.find_test_by_id(test_id)
    
    def view_details(self):
        """View details of the selected test"""
        test = self.get_selected_test()
        if test and self.on_view_details:
            self.on_view_details(test)
    
    def edit_test(self):
        """Edit the selected test"""
        test = self.get_selected_test()
        if test and self.on_edit:
            self.on_edit(test)
    
    def delete_test(self):
        """Delete the selected test"""
        test = self.get_selected_test()
        if not test:
            return
            
        # Confirm deletion
        if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete test '{test['name']}'?"):
            return
            
        # Delete the test
        if self.model.delete_one_test(test["id"]):
            self.update_list()
            if self.on_delete:
                self.on_delete()
    
    def delete_all_tests(self):
        """Delete all tests"""
        # Confirm deletion
        if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete ALL tests?"):
            return
        
        # Delete all tests
        if self.model.delete_all_tests():
            self.update_list()
            if self.on_delete:
                self.on_delete()