import pandas as pd
import os

def parse_car_csv_to_df() -> pd.DataFrame:
    # Define the columns we want to keep
    columns_to_keep = ['Make', 'Model', 'Price', 'Year', 'Kilometer', 'Fuel Type', 'Transmission', 'Color', 'Seating Capacity']

    script_path = os.path.abspath(__file__)

    # Construct the path to the data.csv file in the same directory as the script
    data_csv_path = os.path.join(os.path.dirname(os.path.dirname(script_path)), 'data', 'data.csv')

    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(data_csv_path, sep = ",")

    # Keep only the desired columns
    df = df[columns_to_keep]

    # handle the missing values
    # Replace empty values with 0
    df['Price'] = df['Price'].fillna(0).astype(float)
    df['Year'] = df['Year'].fillna(0).astype(int)
    df['Kilometer'] = df['Kilometer'].fillna(0).astype(int)
    df['Seating Capacity'] = df['Seating Capacity'].fillna(0).astype(int)

    return df
