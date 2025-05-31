import os
import shutil
import math
import pandas as pd

def divide_data(num_clients=10):
    # Read the data
    data = pd.read_csv('data/Final_Data_Processed.csv')  # Adjust file format if needed
    
    # Calculate records per client
    total_records = len(data)
    base_records_per_client = math.floor(total_records / num_clients)
    extra_records = total_records % num_clients
    
    # Create client directories if they don't exist
    os.makedirs('data', exist_ok=True)
    
    start_idx = 0
    for i in range(1, num_clients + 1):
        client_dir = f'data/client{i}'
        os.makedirs(client_dir, exist_ok=True)
        
        # Calculate records for this client
        records_for_client = base_records_per_client
        if extra_records > 0:
            records_for_client += 1
            extra_records -= 1
            
        end_idx = start_idx + records_for_client
        
        # Extract and save client data
        client_data = data.iloc[start_idx:end_idx]
        client_data.to_csv(f'{client_dir}/data.csv', index=False)
        
        start_idx = end_idx

        # Pivot the data to get heart_rate and respiratory_rate based on itemid
        df_pivot = client_data.pivot(index='Subject_id', 
                                      columns='itemid', 
                                      values='Average_Value').reset_index()

        # Debugging: Print the pivoted DataFrame
        print(f"Pivoted DataFrame for client {i}:")
        print(df_pivot.head())  # Show the first few rows of the pivoted DataFrame

        # Extract heart_rate and respiratory_rate based on itemid
        df_pivot['heart_rate'] = df_pivot.get(220045, None)  # Assuming itemid 220045 corresponds to heart_rate
        df_pivot['respiratory_rate'] = df_pivot.get(220210, None)  # Assuming itemid 220210 corresponds to respiratory_rate
        
        # Debugging: Print the DataFrame after extracting heart_rate and respiratory_rate
        print("DataFrame after extracting heart_rate and respiratory_rate:")
        print(df_pivot[['Subject_id', 'heart_rate', 'respiratory_rate']].head())  # Show relevant columns

        # Get the target variable (first occurrence for each Subject_id)
        targets = client_data.groupby('Subject_id')['Hospital_Expire_Flag'].first()
        df_pivot = df_pivot.merge(targets.reset_index(), on='Subject_id')

        # Drop the columns named 220045 and 220210
        df_pivot.drop(columns=[220045, 220210], inplace=True, errors='ignore')

        # Check if the required columns are present after merging
        if 'heart_rate' not in df_pivot.columns or 'respiratory_rate' not in df_pivot.columns:
            raise ValueError("Processed data must contain 'heart_rate' and 'respiratory_rate' columns.")

        # Save the processed data for the client
        df_pivot.to_csv(f'{client_dir}/processed_data.csv', index=False)

if __name__ == "__main__":
    divide_data()