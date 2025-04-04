"""
test.py - Defines the Test model class
"""

class TestModel:
    """
    Represents a single test with its properties and scores
    """
    def __init__(self, id, name, description, ticket_id, scores, yes_no_answers=None):
        """
        Initialize a test instance
        
        Args:
            id (str): The test identifier
            name (str): Test name
            description (str): Test description
            ticket_id (str): Ticket ID associated with the test
            scores (dict): Dictionary of scores for each factor
            yes_no_answers (dict, optional): Dictionary of yes/no answers
        """
        self.id = id
        self.name = name
        self.description = description
        self.ticket_id = ticket_id
        self.scores = scores
        self.yes_no_answers = yes_no_answers or {}
        self.raw_score = 0
        self.total_score = 0
        self.priority = ""
        
    def to_dict(self):
        """
        Convert test object to a dictionary for easier handling
        
        Returns:
            dict: Dictionary representation of the test
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "ticket_id": self.ticket_id,
            "scores": self.scores,
            "yes_no_answers": self.yes_no_answers,
            "raw_score": self.raw_score,
            "total_score": self.total_score,
            "priority": self.priority
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Create a Test instance from a dictionary
        
        Args:
            data (dict): Dictionary containing test data
            
        Returns:
            Test: A new Test instance
        """
        test = cls(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            ticket_id=data["ticket_id"],
            scores=data["scores"],
            yes_no_answers=data.get("yes_no_answers", {})
        )
        test.raw_score = data["raw_score"]
        test.total_score = data["total_score"]
        test.priority = data["priority"]
        return test