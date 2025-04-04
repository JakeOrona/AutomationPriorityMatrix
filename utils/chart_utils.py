"""
chart_utils.py - Utilities for creating charts and graphs
"""

class ChartUtils:
    """
    Utilities for creating charts and visualizations
    """
    
    @staticmethod
    def is_matplotlib_available():
        """
        Check if matplotlib is available
        
        Returns:
            bool: True if matplotlib is available, False otherwise
        """
        try:
            import matplotlib
            return True
        except ImportError:
            return False
    
    @staticmethod
    def create_priority_distribution_chart(tests, figure_size=(8, 6)):
        """
        Create a pie chart showing distribution of tests by priority
        
        Args:
            tests (list): List of test dictionaries
            figure_size (tuple): Size of the figure (width, height)
            
        Returns:
            tuple: (fig, ax) if matplotlib is available, None otherwise
        """
        if not ChartUtils.is_matplotlib_available():
            return None, None
        
        import matplotlib.pyplot as plt
        from matplotlib.figure import Figure
        
        # Create figure and axis
        fig = Figure(figsize=figure_size)
        ax = fig.add_subplot(111)
        
        # Count tests by priority
        priority_counts = {"High": 0, "Medium": 0, "Low": 0}
        for test in tests:
            priority_counts[test["priority"]] += 1
        
        # Create pie chart
        labels = list(priority_counts.keys())
        sizes = list(priority_counts.values())
        colors = ['green', 'orange', 'red']
        explode = (0.1, 0, 0)  # Explode the 1st slice (High priority)
        
        # Plot if there's data
        if sum(sizes) > 0:
            ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
                shadow=True, startangle=90)
            ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular
            ax.set_title('Test Priority Distribution')
        else:
            ax.text(0.5, 0.5, "No data available", horizontalalignment='center',
                  verticalalignment='center', transform=ax.transAxes)
        
        return fig, ax
    
    @staticmethod
    def create_score_distribution_chart(tests, figure_size=(8, 6)):
        """
        Create a histogram showing distribution of test scores
        
        Args:
            tests (list): List of test dictionaries
            figure_size (tuple): Size of the figure (width, height)
            
        Returns:
            tuple: (fig, ax) if matplotlib is available, None otherwise
        """
        if not ChartUtils.is_matplotlib_available():
            return None, None
        
        import matplotlib.pyplot as plt
        import numpy as np
        from matplotlib.figure import Figure
        
        # Create figure and axis
        fig = Figure(figsize=figure_size)
        ax = fig.add_subplot(111)
        
        # Get scores for histogram
        scores = [test["total_score"] for test in tests]
        
        if scores:
            # Create histogram
            bins = np.linspace(0, 100, 11)  # 10 bins from 0 to 100
            ax.hist(scores, bins=bins, color='skyblue', edgecolor='black')
            ax.set_title('Test Score Distribution')
            ax.set_xlabel('Priority Score')
            ax.set_ylabel('Number of Tests')
            ax.set_xticks(bins)
            
            # Calculate threshold values
            max_score = max(scores)
            high_threshold = max_score * 0.8
            medium_threshold = max_score * 0.5
            
            # Add vertical lines for threshold values
            ax.axvline(x=high_threshold, color='green', linestyle='--', 
                      label=f'High Threshold ({high_threshold:.1f})')
            ax.axvline(x=medium_threshold, color='orange', linestyle='--', 
                      label=f'Medium Threshold ({medium_threshold:.1f})')
            ax.legend()
        else:
            ax.text(0.5, 0.5, "No data available", horizontalalignment='center',
                  verticalalignment='center', transform=ax.transAxes)
        
        return fig, ax
    
    @staticmethod
    def create_factor_contribution_chart(tests, factors, figure_size=(8, 6)):
        """
        Create a bar chart showing average scores by factor
        
        Args:
            tests (list): List of test dictionaries
            factors (dict): Dictionary of factors
            figure_size (tuple): Size of the figure (width, height)
            
        Returns:
            tuple: (fig, ax) if matplotlib is available, None otherwise
        """
        if not ChartUtils.is_matplotlib_available():
            return None, None
        
        import matplotlib.pyplot as plt
        from matplotlib.figure import Figure
        
        # Create figure and axis
        fig = Figure(figsize=figure_size)
        ax = fig.add_subplot(111)
        
        if tests:
            # Calculate average scores for each factor
            factor_avgs = {}
            factor_names = {}
            
            for factor, info in factors.items():
                factor_scores = [test["scores"].get(factor, 0) for test in tests]
                factor_avgs[factor] = sum(factor_scores) / len(tests)
                factor_names[factor] = info["name"]
            
            # Create bar chart
            factor_keys = list(factor_avgs.keys())
            avg_scores = [factor_avgs[f] for f in factor_keys]
            bar_labels = [factor_names[f] for f in factor_keys]
            
            bars = ax.bar(range(len(factor_keys)), avg_scores, color='lightblue')
            ax.set_xticks(range(len(factor_keys)))
            ax.set_xticklabels(bar_labels, rotation=45, ha='right')
            ax.set_title('Average Score by Factor')
            ax.set_ylabel('Average Score (1-5)')
            ax.set_ylim(0, 5)
            
            # Add the score values on top of bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                        f'{height:.1f}', ha='center', va='bottom')
            
            fig.tight_layout()  # Adjust layout for rotated labels
        else:
            ax.text(0.5, 0.5, "No data available", horizontalalignment='center',
                  verticalalignment='center', transform=ax.transAxes)
        
        return fig, ax
    
    @staticmethod
    def create_top_tests_chart(tests, figure_size=(8, 6), max_tests=10):
        """
        Create a horizontal bar chart showing top tests by score
        
        Args:
            tests (list): List of test dictionaries
            figure_size (tuple): Size of the figure (width, height)
            max_tests (int): Maximum number of tests to show
            
        Returns:
            tuple: (fig, ax) if matplotlib is available, None otherwise
        """
        if not ChartUtils.is_matplotlib_available():
            return None, None
        
        import matplotlib.pyplot as plt
        from matplotlib.figure import Figure
        
        # Create figure and axis
        fig = Figure(figsize=figure_size)
        ax = fig.add_subplot(111)
        
        if tests:
            # Get sorted tests
            sorted_tests = sorted(tests, key=lambda x: x["total_score"], reverse=True)
            
            # Take top N or fewer
            top_n = min(max_tests, len(sorted_tests))
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
            bars = ax.barh(range(len(test_names)), test_scores, color=colors)
            ax.set_yticks(range(len(test_names)))
            ax.set_yticklabels(test_names)
            ax.set_title(f'Top {top_n} Tests by Priority Score')
            ax.set_xlabel('Priority Score')
            ax.set_xlim(0, 100)
            
            # Add the score values at the end of bars
            for i, bar in enumerate(bars):
                width = bar.get_width()
                ax.text(width + 1, bar.get_y() + bar.get_height()/2.,
                       f'{width:.1f}', va='center')
            
            fig.tight_layout()  # Adjust layout for long test names
        else:
            ax.text(0.5, 0.5, "No data available", horizontalalignment='center',
                  verticalalignment='center', transform=ax.transAxes)
        
        return fig, ax
    
    @staticmethod
    def create_prioritization_matrix(tests, x_factor, y_factor, factors, figure_size=(8, 6)):
        """
        Create a prioritization matrix (bubble chart) based on two factors
        
        Args:
            tests (list): List of test dictionaries
            x_factor (str): Factor key for x-axis
            y_factor (str): Factor key for y-axis
            factors (dict): Dictionary of factors
            figure_size (tuple): Size of the figure (width, height)
            
        Returns:
            tuple: (fig, ax) if matplotlib is available, None otherwise
        """
        if not ChartUtils.is_matplotlib_available():
            return None, None
        
        import matplotlib.pyplot as plt
        from matplotlib.lines import Line2D
        from matplotlib.figure import Figure
        
        # Create figure and axis
        fig = Figure(figsize=figure_size)
        ax = fig.add_subplot(111)
        
        # Extract data
        x_values = []
        y_values = []
        sizes = []
        labels = []
        colors = []
        
        for test in tests:
            if x_factor in test["scores"] and y_factor in test["scores"]:
                x_values.append(test["scores"][x_factor])
                y_values.append(test["scores"][y_factor])
                # Use normalized score for bubble size (scaled)
                sizes.append(test["total_score"] * 5)
                labels.append(test["name"])
                
                # Color based on priority
                if test["priority"] == "High":
                    colors.append("green")
                elif test["priority"] == "Medium":
                    colors.append("orange")
                else:
                    colors.append("red")
        
        # Create scatter plot (bubble chart)
        scatter = ax.scatter(x_values, y_values, s=sizes, c=colors, alpha=0.6)
        
        # Add labels for axes
        ax.set_xlabel(factors[x_factor]["name"])
        ax.set_ylabel(factors[y_factor]["name"])
        ax.set_title(f"Test Prioritization Matrix: {factors[x_factor]['name']} vs {factors[y_factor]['name']}")
        
        # Set axis limits with a bit of padding
        ax.set_xlim(0.5, 5.5)
        ax.set_ylim(0.5, 5.5)
        
        # Create a grid layout
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # Add quadrant labels
        ax.text(1.25, 4.75, "Low Value\nHigh Effort", ha='center', va='center', 
              bbox=dict(facecolor='white', alpha=0.5))
        ax.text(4.75, 4.75, "High Value\nHigh Effort", ha='center', va='center', 
              bbox=dict(facecolor='white', alpha=0.5))
        ax.text(1.25, 1.25, "Low Value\nLow Effort", ha='center', va='center', 
              bbox=dict(facecolor='white', alpha=0.5))
        ax.text(4.75, 1.25, "High Value\nLow Effort", ha='center', va='center', 
              bbox=dict(facecolor='white', alpha=0.5))
        
        # Add dividing lines
        ax.axvline(x=3, color='gray', linestyle='--')
        ax.axhline(y=3, color='gray', linestyle='--')
        
        # Add annotations for test names
        annotations = []
        for i, txt in enumerate(labels):
            # Truncate long test names
            if len(txt) > 15:
                txt = txt[:12] + "..."
            annotation = ax.annotate(txt, (x_values[i], y_values[i]),
                                  xytext=(5, 5), textcoords='offset points',
                                  fontsize=8, alpha=0.8)
            annotations.append(annotation)
        
        # Add a legend for priority colors
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=10, label='High Priority'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor='orange', markersize=10, label='Medium Priority'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='Low Priority')
        ]
        ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.05),
                fancybox=True, shadow=True, ncol=3)
        
        # Adjust layout
        fig.tight_layout()
        
        return fig, ax