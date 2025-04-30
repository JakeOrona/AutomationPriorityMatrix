# Test Prioritization Application

A Python application for prioritizing test automation based on weighted factors.

## Overview

This application helps QA teams decide which manual tests to automate first by calculating priority scores based on various weighted factors. It uses a tkinter GUI to provide an intuitive interface for managing and analyzing tests.

## Structure

1. **models/**: Contains all the business logic and data models
   - Manages tests and their data
   - Implements scoring algorithms
   - Provides priority analysis

2. **utils/**: Handles all utility operations
   - CSV import/export with proper format handling
   - Report generation (text, HTML, docx)
   - Chart generation

3. **views/**: Contains the GUI components
   - User interface layout
   - Event handling
   - User interaction

4. **main.py**: Application entry point
   - Initializes model and GUI
   - Connects components together

## Features

- Score and prioritize tests based on multiple weighted factors:
  - Can it be Automated (special factor)
  - Regression Frequency (weight: 3)
  - Customer Impact (weight: 3)
  - Manual Test Effort (weight: 2)
  - Automation Complexity (weight: 2)
  - Existing Framework (weight: 2)
  - Angular Framework (weight: 1)
  - Repetitive (weight: 1)

- Yes/No questions for additional context:
  - "Does this test case have steps?" with impact notes
  - Additional custom questions can be easily added

- View tests ranked by priority score
- Filter tests by section
- View and edit detailed test information directly in the detail view
- Delete tests from the detail view or main screen
- Import/export test data to/from CSV files

### Reports

- **Text Report**: Generate prioritized test reports with high/medium/low priority tiers
- **Enhanced HTML Report**: Interactive HTML reports with tabs for:
  - Priority summary cards
  - Filterable test listings
  - Interactive test cards
  - Priority breakdown sections

- **Graphical Reports**: Create visualizations showing:
  - Priority Distribution (pie chart)
  - Score Distribution (histogram)
  - Factor Contribution (bar chart)
  - Top Tests (horizontal bar chart)

- Export reports to various formats:
  - Plain Text
  - HTML (both simple and enhanced)
  - PNG, JPEG, PDF, SVG for charts

## Requirements

- Python 3.6 or higher
- tkinter (usually included with Python)
- matplotlib (for graphical reports)
- pandas (optional, for enhanced CSV handling)
- docx (docx priority report export)

## Installation

1. Download and install Python 3.6+ from https://www.python.org/downloads/
   - Windows users: Make sure to check "Add Python to PATH" during installation
   - Mac users: Use `python3` commands instead of `python`
   - Linux users: Install tkinter if not included (`sudo apt-get install python3-tk` for Ubuntu)

2. Open a command prompt/terminal and install required dependencies:
   
   Windows users:
   ```bash
   pip install matplotlib pandas python-docx
   ```
   
   Mac users:
   ```zsh
   pip3 install matplotlib pandas python-docx
   ```
   
3. Download this repository:
   - Click the green "Code" button above and select "Download ZIP"
   - Extract the ZIP file to a folder of your choice
   - Or use git: `git clone [repository-url]`

4. Navigate to the application folder in your command prompt/terminal:
   ```bash
   cd path/to/test-prioritization-app
   ```

5. Run the application:
   - Windows: 
   ```bash
   python main.py
   ```
   - Mac/Linux: 
   ```bash
   python3 main.py
   ```

## Usage

1. **Adding a test**:
   - Fill in the test details on the left panel
   - Set the "Can it be Automated?" factor - this determines if a test will be scored or marked as "Won't Automate"
   - Answer the yes/no questions that provide additional context
   - Set the priority factors using the radio buttons
   - Click "Add Test" button

2. **Viewing tests**:
   - All tests appear in the list on the right panel
   - Double-click a test to view details
   - Use the section filter to show tests from a specific section

3. **Editing tests**:
   - Double-click a test to open the details view
   - Click "Edit Test" to modify any test details
   - Save changes when done

4. **Generating reports**:
   - Access reports from the "Reports" menu
   - Choose between text-based priority report and graphical reports
   - Export reports to files for sharing
   - Open HTML reports in browser for interactive viewing

5. **Importing/Exporting tests**:
   - Use the "File" menu to import or export tests as CSV
   - CSV format includes all test details including yes/no questions
   - Useful for backing up data or transferring tests between installations

## CSV Format

The application exports and imports tests in CSV format with the following columns:

1. Basic info: Rank, Priority, Ticket ID, Section, Test Name, Description
2. Yes/No questions: Questions added directly after the Description column
3. Scoring info: Total Score, Raw Score
4. Factor scores: Individual scores for each prioritization factor
5. Test ID: Unique identifier for the test

## Enhanced Features

### Yes/No Questions
- Add yes/no questions to provide additional context for tests
- Answers are stored with tests and exported to CSV
- Questions appear after "Can it be automated?" factor in test details
- Impact notes explain the significance of each question

### Improved UI
- Logical grouping of related fields
- Clear separation of test information, yes/no questions, and scoring factors
- Color-coded priority labels for better visualization
- Scrollable views for handling large numbers of tests

### Enhanced Reports
- Interactive HTML reports with modern UI
- Collapsible test cards grouped by priority
- Filterable test tables
- Dynamic chart rendering
- Mobile-responsive design

## Troubleshooting

- **"No module named 'matplotlib'"**: Run `pip install matplotlib`
- **"No module named 'pandas'"**: Run `pip install pandas`
- **"No module named 'docx'"**: Run `pip install python-docx`
- **UI elements not displaying correctly**: Make sure you have tkinter installed properly
- **Charts not showing**: Confirm matplotlib is installed and working

## License

MIT License
