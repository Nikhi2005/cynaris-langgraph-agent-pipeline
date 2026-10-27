
from pathlib import Path
import pandas as pd

# Locate the sample dataset
PROJECT_DIR = Path(__file__).resolve().parent
DATA_PATH = PROJECT_DIR / "data" / "reasoning_dataset.csv"

# Load the dataset
df = pd.read_csv(DATA_PATH)

# Display the number of rows and columns
print("Number of rows:", df.shape[0])
print("Number of columns:", df.shape[1])

# Display column names and data types
print("\nColumn names:")
print(df.columns.tolist())

print("\nData types:")
print(df.dtypes)

# Display the first five rows
print("\nFirst five rows:")
print(df.head())
