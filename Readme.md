# JoSAA College Data Analyzer

A Python GUI application that analyzes and visualizes JoSAA counseling data for engineering college admissions in India.

## Features
- Filter colleges by multiple parameters
- Interactive data visualization
- Rank-based college suggestions
- Support for all counseling rounds
- Institute-wise categorization (IIT/NIT/IIIT/GFTI)
- Gender and quota-based analysis
- Exportable data in CSV format

## Tech Stack
- Python 3.x
- Tkinter for GUI
- Pandas for data processing
- Matplotlib for visualization

## Installation

1. Clone the repository:
    ```bash
    https://github.com/rakshverma/JEE_COLLEGE_PREDICTOR.git
    ```

2. Install required packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the application:
    ```bash
    python main.py
    ```

## Data Format
Place your JoSAA round-wise data files in the root directory:

## Usage

1. Select counseling round
2. Choose filters:
   - Institute Type (IIT/NIT/IIIT/GFTI)
   - Specific Institute
   - Rank Range
   - Quota
   - Seat Type
   - Gender
3. View filtered results
4. Analyze visualizations

## Features in Detail

### Data Filtering
- Round-wise filtering
- Institute type categorization
- Rank-based filtering
- Gender and quota-based filtering

### Visualizations
- Opening/Closing rank trends
- Gender-wise analysis
- Quota-wise distribution
- Seat type comparisons

### Data Export
- Institute-wise CSV generation
- Round-wise data export
- Filtered results export

## Directory Structure
./ ├── main.py ├── requirements.txt ├── 2024_Round_.csv └── institutes_csv/ └── Round_/

##Dataset from
https://www.kaggle.com/datasets/aarshdesai2004/josaa-seat-matrix-and-cutoffs-2024/data
