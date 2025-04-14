"""
scoring.py - Contains the scoring logic for test prioritization
"""

class ScoringSystem:
    """
    Manages the scoring system for test prioritization
    """
    def __init__(self):
        """Initialize the scoring system with default factors and options"""
        # Factors and weights
        self.factors = {
            "regression_frequency": {"name": "Regression Frequency", "weight": 3},
            "customer_impact": {"name": "Customer Impact", "weight": 3},
            "manual_effort": {"name": "Manual Test Effort", "weight": 2},
            "automation_complexity": {"name": "Automation Complexity", "weight": 2},
            "existing_framework": {"name": "Existing Framework", "weight": 2},
            "angular_framework": {"name": "Angular Framework", "weight": 1},
            "repetitive": {"name": "Repetitive", "weight": 1}
        }
        
        # Scoring options
        self.score_options = {
            "regression_frequency": {
                1: "Semi-annual",
                3: "Quarterly",
                5: "Always"
            },
            "customer_impact": {
                1: "Minor functionality",
                3: "Important functionality",
                5: "Critical business process"
            },
            "manual_effort": {
                1: "< 5 minutes",
                3: "5-20 minutes",
                5: "> 20 minutes"
            },
            "automation_complexity": {
                1: "Very difficult to automate",
                3: "Moderate effort",
                5: "Easy to automate"
            },
            "existing_framework": {
                1: "No Page Objects",
                3: "Some Page Objects",
                5: "Established Page Objects"
            },
            "angular_framework": {
                1: "Old Angular JS framework",
                3: "Migrating soon",
                5: "New Angular framework"
            },
            "repetitive": {
                1: "Not repetitive",
                3: "Somewhat repetitive",
                5: "Highly repetitive"
            }
        }

        # Yes/No questions (currently empty, but kept for future extensibility)
        self.yes_no_questions = {}
    
    def calculate_score(self, scores, yes_no_answers=None):
        """
        Calculate priority score with optional yes/no question impacts
        
        Args:
            scores (dict): Dictionary of scores for each factor
            yes_no_answers (dict, optional): Dictionary of yes/no answers
                
        Returns:
            tuple: (raw_score, normalized_score)
        """
        # Make a copy of factors to avoid modifying the originals
        factors_copy = {key: {"name": value["name"], "weight": value["weight"]} 
                        for key, value in self.factors.items()}
        
        # Apply yes/no question impacts to weights if provided
        bonus_points = 0
        if yes_no_answers:
            # This is a placeholder for future yes/no question handling
            pass
        
        # Calculate raw score
        raw_score = sum(scores[factor] * factors_copy[factor]["weight"] 
                    for factor in factors_copy if factor in scores) + bonus_points
        
        # Calculate max possible score for normalization
        max_raw_score = sum(5 * factors_copy[factor]["weight"] for factor in factors_copy)
        
        # Normalize to 100-point scale
        normalized_score = (raw_score / max_raw_score) * 100
        
        return raw_score, round(normalized_score, 1)
    
    def get_priority_category(self, score):
        """
        Convert a numeric score to a priority category
        
        Args:
            score (float): The normalized priority score (0-100)
            
        Returns:
            str: Priority category ('High', 'Medium', or 'Low')
        """
        # Define thresholds for categories
        if score >= 90:
            return "Highest"
        elif score >= 80:
            return "High"
        elif score >= 60:
            return "Medium"
        elif score >= 40:
            return "Low"
        else:
            return "Lowest"