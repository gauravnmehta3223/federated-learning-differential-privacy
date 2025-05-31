import os
import pandas as pd

# Define file paths
input_path = r"C:\Users\gaura\OneDrive\Documents\FederatedLearning_Project\differential-privacy-fl\data\chartevents.csv"
output_path = r"C:\Users\gaura\OneDrive\Documents\FederatedLearning_Project\differential-privacy-fl\data\cleaned_chartevents.csv"

# Check if the input file exists
if not os.path.exists(input_path):
    raise FileNotFoundError(f"Error: Input file not found at {input_path}")

# Define required itemids
required_itemids = {220621, 220210, 223761, 220051, 220045, 220050}

# Define chunk size (adjust based on available memory)
chunk_size = 500000  # Process 500,000 rows at a time

# Open the output file and write headers first
header_written = False

# Read CSV in chunks
for chunk in pd.read_csv(input_path, usecols=["subject_id", "itemid", "valuenum"], chunksize=chunk_size):
    # Filter required itemids and remove rows with NaN values in 'valuenum'
    chunk_filtered = chunk[chunk["itemid"].isin(required_itemids)].dropna(subset=["valuenum"])

    # Append to the output file (write header only for the first chunk)
    chunk_filtered.to_csv(output_path, mode="a", index=False, header=not header_written)
    
    # Set flag to avoid writing header again
    header_written = True

print("Data cleaning completed successfully! Cleaned file saved at:", output_path)

import os
import pandas as pd

# Define file paths
input_path = r"C:\Users\gaura\OneDrive\Documents\FederatedLearning_Project\differential-privacy-fl\data\cleaned_chartevents.csv"
output_path = r"C:\Users\gaura\OneDrive\Documents\FederatedLearning_Project\differential-privacy-fl\data\pivoted_chartevents.csv"

# Check if the input file exists
if not os.path.exists(input_path):
    raise FileNotFoundError(f"Error: Input file not found at {input_path}")

# Define mapping of itemid to feature names
itemid_map = {
    220621: "Glucose",
    220210: "Respiratory Rate",
    223761: "Temperature (°F)",
    220051: "ABP Diastolic",
    220045: "Heart Rate",
    220050: "ABP Systolic"
}

# Define chunk size for processing
chunk_size = 500000  

# Initialize a list to store processed chunks
processed_chunks = []

# Read and process CSV in chunks
for chunk in pd.read_csv(input_path, chunksize=chunk_size):
    # Replace 'itemid' with feature names
    chunk["itemid"] = chunk["itemid"].map(itemid_map)  

    # Pivot using pivot_table() with mean aggregation and rounding to 2 decimal places
    chunk_pivoted = chunk.pivot_table(index="subject_id", columns="itemid", values="valuenum", aggfunc="mean").round(2)

    # Append processed chunk
    processed_chunks.append(chunk_pivoted)

# Concatenate all chunks into a final dataframe
df_final = pd.concat(processed_chunks)

# Save the final pivoted dataframe to CSV
df_final.to_csv(output_path, index=True)

print("Pivoting completed successfully! Pivoted file saved at:", output_path)


import os
import pandas as pd

# Define file paths
admissions_path = r"C:\Users\gaura\OneDrive\Documents\FederatedLearning_Project\differential-privacy-fl\data\admissions.csv"
pivoted_chart_path = r"C:\Users\gaura\OneDrive\Documents\FederatedLearning_Project\differential-privacy-fl\data\pivoted_chartevents.csv"
output_path = r"C:\Users\gaura\OneDrive\Documents\FederatedLearning_Project\differential-privacy-fl\data\merged_data.csv"

# Check if input files exist
if not os.path.exists(admissions_path) or not os.path.exists(pivoted_chart_path):
    raise FileNotFoundError("Error: One or both input files are missing.")

# Load admissions data, keeping only 'subject_id' and 'hospital_expire_flag'
admissions_df = pd.read_csv(admissions_path, usecols=["subject_id", "hospital_expire_flag"])

# Load pivoted chartevents data
pivoted_chart_df = pd.read_csv(pivoted_chart_path)

# Merge datasets using a left join on 'subject_id'
merged_df = pivoted_chart_df.merge(admissions_df, on="subject_id", how="left")

merged_df = merged_df.drop_duplicates(subset = ["subject_id"] , keep = 'last')

# Save the merged data to a new CSV file
merged_df.to_csv(output_path, index=False)

print("Merging completed successfully! Merged file saved at:", output_path)
