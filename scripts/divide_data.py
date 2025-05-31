import mysql.connector
import pandas as pd

# Database connection
conn = mysql.connector.connect(
    host="your_host",
    user="your_user",
    password="your_password",
    database="your_database"
)
cursor = conn.cursor()

BATCH_SIZE = 500000
batch_number = 1  # To track batch processing

while True:
    print(f"Processing batch {batch_number}...")

    # Step 1: Move batch to new table
    insert_query = f"""
        INSERT INTO processed_chartevents 
        SELECT * FROM chartevents WHERE itemid IN (220045, 220210) 
        ORDER BY subject_id LIMIT {BATCH_SIZE};
    """
    cursor.execute(insert_query)
    conn.commit()

    # Step 2: Run the complex query on the processed batch
    temp_query = """
        WITH Temp AS (
          WITH Temperory_table AS (
            SELECT 
              a.subject_id, 
              a.hospital_expire_flag, 
              CASE 
                WHEN c.itemid = 220045 THEN c.valuenum 
                ELSE NULL 
              END AS HeartRate,
              CASE 
                WHEN c.itemid = 220210 THEN c.valuenum  
                ELSE NULL 
              END AS Respiretory_Rate,
              c.charttime  
            FROM processed_chartevents c 
            JOIN admissions a ON c.subject_id = a.subject_id
          )
          SELECT 
            subject_id, 
            hospital_expire_flag,
            HeartRate, 
            LEAD(Respiretory_Rate, 4 , 0) OVER (PARTITION BY subject_id ORDER BY charttime) AS Lag_Respiratory_Rate
          FROM Temperory_table
        )
        SELECT subject_id, 
               hospital_expire_flag,
               AVG(HeartRate) AS avg_HeartRate,
               AVG(Lag_Respiratory_Rate) AS avg_Lag_Respiratory_Rate
        FROM Temp 
        WHERE HeartRate IS NOT NULL OR HeartRate != 0 
          AND Lag_Respiratory_Rate IS NOT NULL OR Lag_Respiratory_Rate != 0
        GROUP BY subject_id, hospital_expire_flag;
    """

    cursor.execute(temp_query)
    results = cursor.fetchall()
    
    # Step 3: Save results to a CSV file
    df = pd.DataFrame(results, columns=['subject_id', 'hospital_expire_flag', 'avg_HeartRate', 'avg_Lag_Respiratory_Rate'])
    df.to_csv(f"batch_{batch_number}_results.csv", index=False)

    # Step 4: Delete processed batch to free memory
    delete_query = f"""
        DELETE FROM chartevents WHERE itemid IN (220045, 220210) 
        ORDER BY subject_id LIMIT {BATCH_SIZE};
    """
    cursor.execute(delete_query)
    conn.commit()

    # Stop when no more rows are left
    if cursor.rowcount == 0:
        print("No more data to process.")
        break

    batch_number += 1  # Move to the next batch

# Cleanup
cursor.close()
conn.close()
print("Processing complete. All batches saved as CSV files.")
