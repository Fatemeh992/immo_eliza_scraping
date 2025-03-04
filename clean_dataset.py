import pandas as pd

def load_data(file_path):
    """Load dataset into a Pandas DataFrame."""
    return pd.read_csv(file_path)

def clean_data(df):
    """Clean the dataset by removing duplicates, handling missing values, and converting data types."""
    # Drop duplicate rows based on specific columns
    df.drop_duplicates(subset=['postal_code', 'street', 'number', 'box'], inplace=True)
    
    # Remove completely empty rows
    df.dropna(how='all', inplace=True)
    
    # Convert specific columns to categorical data type
    df['property_type'] = df['property_type'].astype('category')
    df['property_subtype'] = df['property_subtype'].astype('category')
    df['locality'] = df['locality'].astype('category')
    df['buildingState'] = df['buildingState'].astype('category')
    
    # Replace missing values with None
    df.map(lambda x: None if pd.isna(x) else x)
    
    # Remove an erroneous property entry with 200 bedrooms
    df.drop([18860], axis=0, inplace=True)
    
    return df

def save_data(df, output_path):
    """Save the cleaned dataset to a new CSV file."""
    # Set 'house_index' as the index
    df.set_index('house_index', drop=True, inplace=True)
    
    # Sort the dataset based on the index
    df.sort_index(inplace=True)
    
    # Save the cleaned dataset
    df.to_csv(output_path)

def main():
    file_path = "Data/all_properties_output.csv"
    output_path = "Data/cleaned_dataset.csv"
    
    df = load_data(file_path)
    cleaned_df = clean_data(df)
    save_data(cleaned_df, output_path)

if __name__ == "__main__":
    main()
