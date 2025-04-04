"""
chart_report.py - Graphical chart report view
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
import os
from views.reports import BaseReportView
from utils.chart_utils import ChartUtils

class ChartReportView(BaseReportView):
    """
    Graphical chart report view
    """
    def __init__(self, parent, model):
        """
        Initialize the chart report view
        
        Args:
            parent: The parent window
            model: The prioritization model
        """
        # Check if matplotlib is available before initializing
        self.matplotlib_available = ChartUtils.is_matplotlib_available()
        if not self.matplotlib_available:
            # Configure parent window minimally since we'll show an error
            parent.title("Test Prioritization Graphical Report")
            parent.geometry("600x300")
            
            # Create a frame for the error message
            main_frame = ttk.Frame(parent, padding=20)
            main_frame.pack(fill=tk.BOTH, expand=True)
            
            # Show the error message
            ttk.Label(
                main_frame,
                text="Matplotlib is required for graphical reports.\n\n" +
                    "Please install it using:\n" +
                    "pip install matplotlib",
                font=("", 12)
            ).pack(pady=20)
            
            # Add a close button
            button_frame = ttk.Frame(parent)
            button_frame.pack(fill=tk.X, pady=10, padx=10)
            ttk.Button(
                button_frame, 
                text="Close", 
                command=parent.destroy
            ).pack(side=tk.RIGHT, padx=5)
            
            # Store references to frames for potential later use
            self.parent = parent
            self.model = model
            self.main_frame = main_frame
            self.button_frame = button_frame
            return
        
        # If matplotlib is available, proceed with normal initialization
        super().__init__(parent, model, "Test Prioritization Graphical Report")
    
    def create_report_content(self):
        """Create the graphical report content"""
        # If matplotlib isn't available, we've already shown an error in __init__
        if not self.matplotlib_available:
            return
            
        # Import necessary modules for chart display
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        
        # Create notebook for multiple graphs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Dictionary to store figures for export
        self.figures = {}
        
        # 1. Priority Distribution Tab
        priority_frame = ttk.Frame(self.notebook)
        self.notebook.add(priority_frame, text="Priority Distribution")
        
        fig1, _ = ChartUtils.create_priority_distribution_chart(self.model.tests)
        self.figures["Priority Distribution"] = fig1
        
        # Add the plot to the frame
        canvas1 = FigureCanvasTkAgg(fig1, master=priority_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 2. Score Distribution Tab
        score_frame = ttk.Frame(self.notebook)
        self.notebook.add(score_frame, text="Score Distribution")
        
        fig2, _ = ChartUtils.create_score_distribution_chart(self.model.tests)
        self.figures["Score Distribution"] = fig2
        
        # Add the plot to the frame
        canvas2 = FigureCanvasTkAgg(fig2, master=score_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 3. Factor Contribution Tab
        factor_frame = ttk.Frame(self.notebook)
        self.notebook.add(factor_frame, text="Factor Contribution")
        
        fig3, _ = ChartUtils.create_factor_contribution_chart(self.model.tests, self.model.factors)
        self.figures["Factor Contribution"] = fig3
        
        # Add the plot to the frame
        canvas3 = FigureCanvasTkAgg(fig3, master=factor_frame)
        canvas3.draw()
        canvas3.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 4. Top Tests Tab
        top_tests_frame = ttk.Frame(self.notebook)
        self.notebook.add(top_tests_frame, text="Top Tests")
        
        fig4, _ = ChartUtils.create_top_tests_chart(self.model.tests)
        self.figures["Top Tests"] = fig4
        
        # Add the plot to the frame
        canvas4 = FigureCanvasTkAgg(fig4, master=top_tests_frame)
        canvas4.draw()
        canvas4.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Add export buttons to button frame
        ttk.Button(
            self.button_frame, 
            text="Export Current Graph", 
            command=self.export_current_graph
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            self.button_frame, 
            text="Export All Graphs", 
            command=self.export_all_graphs
        ).pack(side=tk.LEFT, padx=5)
    
    def export_current_graph(self):
        """Export the current graph"""
        if not self.matplotlib_available or not hasattr(self, 'notebook'):
            return
            
        # Get the current tab name
        current_tab = self.notebook.tab(self.notebook.select(), "text")
        
        if current_tab in self.figures:
            # Ask for save location
            filename = filedialog.asksaveasfilename(
                parent=self.parent,
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
                    self.figures[current_tab].savefig(
                        filename, 
                        dpi=300, 
                        bbox_inches='tight', 
                        format=extension if extension != "jpg" else "jpeg"
                    )
                    messagebox.showinfo(
                        "Export Successful", 
                        f"Graph exported to {filename}",
                        parent=self.parent
                    )
                except Exception as e:
                    messagebox.showerror(
                        "Export Error", 
                        f"Error saving graph: {str(e)}",
                        parent=self.parent
                    )
    
    def export_all_graphs(self):
        """Export all graphs"""
        if not self.matplotlib_available or not hasattr(self, 'figures'):
            return
            
        # Ask for directory
        directory = filedialog.askdirectory(
            parent=self.parent,
            title="Select Directory for Exporting All Graphs"
        )
        
        if directory:
            # Generate timestamp for filenames
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Export each graph
            success_count = 0
            for graph_name, figure in self.figures.items():
                # Create filename with timestamp
                safe_name = graph_name.replace(" ", "_").lower()
                filename = os.path.join(directory, f"{safe_name}_{timestamp}.png")
                
                try:
                    # Save the figure
                    figure.savefig(filename, dpi=300, bbox_inches='tight')
                    success_count += 1
                except Exception as e:
                    messagebox.showerror(
                        "Export Error", 
                        f"Error saving {graph_name}: {str(e)}",
                        parent=self.parent
                    )
            
            if success_count > 0:
                messagebox.showinfo(
                    "Export Successful", 
                    f"Exported {success_count} graphs to {directory}",
                    parent=self.parent
                )