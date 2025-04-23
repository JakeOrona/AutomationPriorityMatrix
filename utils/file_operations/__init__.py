"""
file_operations package - Handles file import/export and report generation
"""
from .csv_handler import CSVHandler
from .report_generators import (
    BaseReportGenerator,
    TextReportGenerator, 
    MarkdownReportGenerator, 
    HTMLReportGenerator, 
    DocxReportGenerator
)

# For backward compatibility
class FileOperations:
    """Compatibility class that combines functionality from the specialized handlers"""
    
    @staticmethod
    def export_to_csv(filename, tests, factors):
        return CSVHandler.export_to_csv(filename, tests, factors)
    
    @staticmethod
    def import_from_csv(filename):
        return CSVHandler.import_from_csv(filename)
    
    @staticmethod
    def generate_report_text(tests, priority_tiers, model=None):
        return TextReportGenerator.generate_report(tests, priority_tiers, model)
    
    @staticmethod
    def generate_markdown_report(tests, priority_tiers, model=None):
        return MarkdownReportGenerator.generate_report(tests, priority_tiers, model)
    
    @staticmethod
    def generate_enhanced_markdown_report(tests, priority_tiers, model=None):
        return MarkdownReportGenerator.generate_enhanced_report(tests, priority_tiers, model)
    
    @staticmethod
    def generate_test_card_markdown(test, index, css_class, model):
        return MarkdownReportGenerator.generate_test_card(test, index, css_class, model)
    
    @staticmethod
    def export_report_to_html(tests, priority_tiers, model, filename):
        return HTMLReportGenerator.export_report(tests, priority_tiers, model, filename)
    
    @staticmethod
    def _generate_test_card_html(test, index, priority_class, model):
        return HTMLReportGenerator.generate_test_card(test, index, priority_class, model)
    
    @staticmethod
    def export_report_to_docx(report_text, filename):
        return DocxReportGenerator.export_report(report_text, filename)
    
    @staticmethod
    def export_report_to_file(filename, report_text):
        return TextReportGenerator.export_to_file(filename, report_text)
    
    @staticmethod
    def generate_scoring_guide_text(factors, score_options):
        return TextReportGenerator.generate_scoring_guide(factors, score_options)