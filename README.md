# Test Prioritization Application

A Python application for prioritizing test automation based on weighted factors.

## Overview

This application helps QA teams decide which manual tests to automate first by calculating priority scores based on various weighted factors. It uses a tkinter GUI to provide an intuitive interface for managing and analyzing tests.

## Structure

1. **models.py**: Contains all the business logic and data models
   - Manages tests and their data
   - Implements scoring algorithms
   - Provides priority analysis

2. **file_operations.py**: Handles all file-related operations
   - CSV import/export
   - Report generation
   - Documentation generation

3. **gui.py**: Contains the GUI components
   - User interface layout
   - Event handling
   - User interaction

4. **main.py**: Application entry point
   - Initializes model and GUI
   - Connects components together

## Features

- Score and prioritize tests based on multiple weighted factors:
  - Execution Frequency (weight: 3)
  - Business Impact (weight: 3)
  - Manual Test Effort (weight: 2)
  - Stability (weight: 2)
  - Automation Complexity (weight: 2)

- View tests ranked by priority score
- View detailed test information and score breakdown
- Import/export test data to/from CSV files
- Generate prioritized test reports with high/medium/low priority tiers
- Scoring guide for consistent evaluation

## Requirements

- Python 3.6 or higher
- pandas
- tkinter (usually included with Python)

## Installation

1. Ensure you have Python installed
2. Install required dependencies:
   ```
   pip install pandas
   ```
3. Clone or download this repository

## Usage

Run the application with:
```
python main.py
```

## Future Improvements

- Add unit tests
- Implement data visualization (charts, graphs)
- Add user authentication and multiple projects
- Create a web interface
- Add more scoring factors