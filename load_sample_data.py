
from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent
DATA_PATH = PROJECT_DIR / "data" / "sample_dataset.csv"

df = pd.read_csv(DATA_PATH)

print("Number of rows:", df.shape[0])
print("Number of columns:", df.shape[1])

print("\nColumn data types:")
print(df.dtypes)

print("\nFirst five rows:")
print(df.head())


