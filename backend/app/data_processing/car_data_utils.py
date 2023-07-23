# car_data_utils.py

import os
from typing import Any
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def preprocess_data(car_data: pd.DataFrame) -> pd.DataFrame:
    # Drop duplicates, if any
    car_data.drop_duplicates(inplace=True)
    
    # Convert 'Price' and 'Kilometer' columns to numeric types
    car_data['Price'] = car_data['Price'].str.replace(',', '').astype(float)
    car_data['Kilometer'] = car_data['Kilometer'].str.replace(' km', '').str.replace(',', '').astype(float)
    
    # Convert 'Year' column to datetime type and extract the year
    car_data['Year'] = pd.to_datetime(car_data['Year']).dt.year
    
    # Fill missing values in numerical columns with mean or median
    car_data['Price'].fillna(car_data['Price'].median(), inplace=True)
    car_data['Kilometer'].fillna(car_data['Kilometer'].median(), inplace=True)
    
    # Fill missing values in categorical columns with mode (most frequent value)
    car_data['Fuel Type'].fillna(car_data['Fuel Type'].mode()[0], inplace=True)
    car_data['Transmission'].fillna(car_data['Transmission'].mode()[0], inplace=True)
    car_data['Color'].fillna(car_data['Color'].mode()[0], inplace=True)
    car_data['Seating Capacity'].fillna(car_data['Seating Capacity'].mode()[0], inplace=True)

    return car_data

def extract_features(car_data: pd.DataFrame) -> pd.DataFrame:
    # Create a new feature for car age
    current_year = pd.Timestamp.now().year
    car_data['Car Age'] = current_year - car_data['Year']
    
    # Create a new feature for price per kilometer
    car_data['Price per Kilometer'] = car_data['Price'] / car_data['Kilometer']
    
    # Extract the car brand from the 'Make' feature
    car_data['Brand'] = car_data['Make'].str.split().str[0]

    return car_data


def perform_eda(car_data: pd.DataFrame) -> None:
    # Plot the distribution of car prices
    sns.histplot(car_data['Price'], bins=30)
    plt.title('Distribution of Car Prices')
    plt.xlabel('Price')
    plt.ylabel('Count')
    plt.show()

    # Plot the average price by car brand
    brand_avg_price = car_data.groupby('Brand')['Price'].mean().sort_values(ascending=False)
    sns.barplot(x=brand_avg_price.index, y=brand_avg_price.values)
    plt.title('Average Price by Car Brand')
    plt.xlabel('Brand')
    plt.ylabel('Average Price')
    plt.xticks(rotation=90)
    plt.show()

    # Plot the relationship between car age and price
    sns.scatterplot(x=car_data['Car Age'], y=car_data['Price'])
    plt.title('Car Age vs. Price')
    plt.xlabel('Car Age')
    plt.ylabel('Price')
    plt.show()

    # Plot the correlation heatmap between numerical features
    corr_matrix = car_data.corr()
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Correlation Heatmap')
    plt.show()

