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
        priority_counts = {"Highest": 0, "High": 0, "Medium": 0, "Low": 0, "Lowest": 0, "Can't Automate": 0}
        for test in tests:
            priority_counts[test["priority"]] += 1
        
        # Create pie chart
        labels = list(priority_counts.keys())
        sizes = list(priority_counts.values())
        colors = ['red', 'orange', 'yellow', 'blue', 'lightblue', 'gray']
        explode = (0.1, 0, 0, 0, 0, 0)  # Explode the 1st slice (Highest priority)
        
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
        
        # Filter out "Can't Automate" tests which have a score of 0
        scorable_tests = [test for test in tests if test["priority"] != "Can't Automate"]
        
        # Get scores for histogram
        scores = [test["total_score"] for test in scorable_tests]
        
        if scores:
            # Create histogram
            bins = np.linspace(0, 100, 21)  # 20 bins from 0 to 100
            ax.hist(scores, bins=bins, color='skyblue', edgecolor='black')
            ax.set_title('Test Score Distribution (Excludes "Can\'t Automate" Tests)')
            ax.set_xlabel('Priority Score')
            ax.set_ylabel('Number of Tests')
            ax.set_xticks(bins)
            
            # Calculate thresholds
            max_score = 100
            
            highest_threshold = max_score * 0.90
            high_threshold = max_score * 0.80
            medium_threshold = max_score * 0.60
            low_threshold = max_score * 0.40
            lowest_threshold = max_score * 0.20
            
            # Add vertical lines for threshold values
            ax.axvline(x=highest_threshold, color='red', linestyle='--', 
                        label=f'Highest Threshold ({highest_threshold:.1f})')
            ax.axvline(x=high_threshold, color='orange', linestyle='--', 
                        label=f'High Threshold ({high_threshold:.1f})')
            ax.axvline(x=medium_threshold, color='yellow', linestyle='--', 
                        label=f'Medium Threshold ({medium_threshold:.1f})')
            ax.axvline(x=low_threshold, color='blue', linestyle='--', 
                        label=f'Low Threshold ({low_threshold:.1f})')
            ax.axvline(x=lowest_threshold, color='lightblue', linestyle='--',
                        label=f'Lowest Threshold ({lowest_threshold:.1f})')
            ax.legend()
            
            # Add text about can't automate tests
            cant_automate_count = len(tests) - len(scorable_tests)
            if cant_automate_count > 0:
                ax.text(0.5, 0.95, f'Note: {cant_automate_count} "Can\'t Automate" tests excluded',
                        horizontalalignment='center', verticalalignment='top',
                        transform=ax.transAxes, bbox=dict(facecolor='white', alpha=0.8))
        else:
            ax.text(0.5, 0.5, "No scorable tests available", horizontalalignment='center',
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
        
        # Filter out "Can't Automate" tests
        scorable_tests = [test for test in tests if test["priority"] != "Can't Automate"]
        
        if scorable_tests:
            # Calculate average scores for each factor
            factor_avgs = {}
            factor_names = {}
            
            for factor, info in factors.items():
                # Skip the can_be_automated factor
                if factor == "can_be_automated":
                    continue
                    
                factor_scores = [test["scores"].get(factor, 0) for test in scorable_tests]
                factor_avgs[factor] = sum(factor_scores) / len(scorable_tests)
                factor_names[factor] = info["name"]
            
            # Create bar chart
            factor_keys = list(factor_avgs.keys())
            avg_scores = [factor_avgs[f] for f in factor_keys]
            bar_labels = [factor_names[f] for f in factor_keys]
            
            bars = ax.bar(range(len(factor_keys)), avg_scores, color='lightblue')
            ax.set_xticks(range(len(factor_keys)))
            ax.set_xticklabels(bar_labels, rotation=45, ha='right')
            ax.set_title('Average Score by Factor (Excludes "Can\'t Automate" Tests)')
            ax.set_ylabel('Average Score (1-5)')
            ax.set_ylim(0, 5)
            
            # Add the score values on top of bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                        f'{height:.1f}', ha='center', va='bottom')
            
            fig.tight_layout()  # Adjust layout for rotated labels
            
            # Add text about can't automate tests
            cant_automate_count = len(tests) - len(scorable_tests)
            if cant_automate_count > 0:
                ax.text(0.5, 0.95, f'Note: {cant_automate_count} "Can\'t Automate" tests excluded',
                        horizontalalignment='center', verticalalignment='top',
                        transform=ax.transAxes, bbox=dict(facecolor='white', alpha=0.8))
        else:
            ax.text(0.5, 0.5, "No scorable tests available", horizontalalignment='center',
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
        
        # Filter out "Can't Automate" tests
        scorable_tests = [test for test in tests if test["priority"] != "Can't Automate"]
        
        if scorable_tests:
            # Get sorted tests
            sorted_tests = sorted(scorable_tests, key=lambda x: x["total_score"], reverse=True)
            
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
                if test["priority"] == "Highest":
                    colors.append("red")
                elif test["priority"] == "High":
                    colors.append("orange")
                elif test["priority"] == "Medium":
                    colors.append("yellow")
                elif test["priority"] == "Low":
                    colors.append("blue")
                else:  # Lowest
                    colors.append("lightblue")
            
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
            
            # Add text about can't automate tests
            cant_automate_count = len(tests) - len(scorable_tests)
            if cant_automate_count > 0:
                ax.text(0.5, 0.95, f'Note: {cant_automate_count} "Can\'t Automate" tests excluded',
                        horizontalalignment='center', verticalalignment='top',
                        transform=ax.transAxes, bbox=dict(facecolor='white', alpha=0.8))
        else:
            ax.text(0.5, 0.5, "No scorable tests available", horizontalalignment='center',
                    verticalalignment='center', transform=ax.transAxes)
        
        return fig, ax