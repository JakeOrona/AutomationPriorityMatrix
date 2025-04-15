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
   - CSV import/export
   - Report generation
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
  - Regression Frequency (weight: 3)
  - Customer Impact (weight: 3)
  - Manual Test Effort (weight: 2)
  - Automation Complexity (weight: 2)
  - Existing Framework (weight: 2)
  - Angular Framework (weight: 1)
  - Repetitive (weight: 1)

- View tests ranked by priority score
- View and edit detailed test information directly in the detail view
- Delete tests from the detail view
- Import/export test data to/from CSV files
- Generate prioritized test reports with high/medium/low priority tiers
- Generate graphical reports with multiple visualizations:
  - Priority Distribution (pie chart)
  - Score Distribution (histogram)
  - Factor Contribution (bar chart)
  - Top Tests (horizontal bar chart)
- Export reports and charts to various formats (PNG, JPEG, PDF, SVG)
- Scoring guide for consistent evaluation

## Requirements

- Python 3.6 or higher
- tkinter (usually included with Python)
- matplotlib (for graphical reports)
- pandas (optional, for enhanced CSV handling)

## Installation

1. Download and install Python 3.6+ from https://www.python.org/downloads/
   - Windows users: Make sure to check "Add Python to PATH" during installation
   - Mac users: Use `python3` commands instead of `python`
   - Linux users: Install tkinter if not included (`sudo apt-get install python3-tk` for Ubuntu)

2. Open a command prompt/terminal and install required dependencies:
   ```bash
   pip install matplotlib pandas
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
- Set the priority factors using the radio buttons
- Click "Add Test" button

2. **Viewing tests**:
- All tests appear in the list on the right panel
- Double-click a test to view details
- Use the section filter to show tests from a specific section

3. **Generating reports**:
- Access reports from the "Reports" menu
- Choose between text-based priority report and graphical reports
- Export reports to files for sharing

4. **Importing/Exporting tests**:
- Use the "File" menu to import or export tests as CSV
- Useful for backing up data or transferring tests between installations

## Troubleshooting

- **"No module named 'matplotlib'"**: Run `pip install matplotlib`
- **"No module named 'pandas'"**: Run `pip install pandas`
- **UI elements not displaying correctly**: Make sure you have tkinter installed properly
- **Charts not showing**: Confirm matplotlib is installed and working

## License

MIT License

