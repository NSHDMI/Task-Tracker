# Pandas Task Tracker

A high-performance, CLI-based task management system built with **Python** and **Pandas**. This project leverages data science tools to handle personal productivity with structured data.



## Key Features

- **Persistent Storage**: Uses the **Apache Parquet** format for efficient data storage (much faster and smaller than CSV).
- **Smart Status Management**: Track tasks through their lifecycle: `new`, `in progress`, `done`, and `abandoned`.
- **Intelligent Deadlines**:
  - `[SOON]` flag for tasks due within 3 days.
  - `[OVERDUE]` alert for missed deadlines.
- **Advanced Filtering**: View tasks by priority (1-5) or sort them chronologically.
- **Data-Driven Insights**: Built-in statistics module to track completion rates and priority distribution.

## Tech Stack

- **Python 3.x**
- **Pandas**: Core engine for data manipulation.
- **PyArrow**: Backend for Parquet file support.
- **Datetime**: Precise time tracking and delta calculations.

## Quick Start

1. **Clone the repository**:
   ```bash
   git clone [https://github.com/NSHDMI/Task-Tracker.git](https://github.com/NSHDMI/Task-Tracker.git)
   cd Task-Tracker
2. **Install dependencies**:
   ```bash
   pip install pandas pyarrow
3. **Run the application**:
   ```bash
   python TaskTracker.py
## Usage Example
Viewing Statistics
The statistics module provides a snapshot of your productivity:
```
--- Statistics ---
-----------------------------------
 Total tasks:          12
-----------------------------------
 By status:
    done             5 (42%)
    new              4 (33%)
    in progress      3 (25%)
 By priority:
    Priority 5:      2
    Priority 4:      5
-----------------------------------
```
## Project Structure
- TaskTracker.py: Main application logic.
- tasks.parquet: Local database (automatically created on first run).
## License
Distributed under the MIT License. See [LICENSE](LICENSE) for more information.
