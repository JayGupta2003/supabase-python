import os
import pandas as pd
import kagglehub
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

# 1. Connect to Supabase
DB_URL = os.getenv("SUPABASE_DB_URL")
if not DB_URL:
    raise ValueError("❌ Error: SUPABASE_DB_URL not found in .env file.")

engine = create_engine(DB_URL)

#Dataset Setup
print("\nDownloading relational data engineering dataset from Kaggle...")
try:
    data_dir = kagglehub.dataset_download("iqbalrony/relational-data-engineering")
    print(f"✅ Downloaded to: {data_dir}")
except Exception as e:
    print(f"❌ Error downloading from Kaggle: {e}. Make sure credentials in .env are correct.")
    exit(1)

# 3. Define the upload sequence to respect Foreign Keys
upload_sequence = [
    ("user_table.csv", "user_table"),
    ("posts_table.csv", "posts_table"),
    ("reactions_table.csv", "reactions_table"),
    ("friends_table.csv", "friends_table")
]

print("\nStarting data stream to Supabase...")
downloaded_files = os.listdir(data_dir)
file_map = {f.lower(): f for f in downloaded_files}

for expected_file, table_name in upload_sequence:
    if expected_file in file_map:
        actual_filename = file_map[expected_file]
        file_path = os.path.join(data_dir, actual_filename)
        
        print(f"Processing {actual_filename} -> Loading into '{table_name}'...")
        
        # Load data to memory
        df = pd.read_csv(file_path)
        
        # 1. Standardize columns to lowercase and underscores
        df.columns = [c.lower().replace(" ", "_") for c in df.columns]
        
        # 2. Convert Unix timestamps to true Datetime objects
        for col in df.columns:
            if "date" in col:
                df[col] = pd.to_datetime(df[col], unit='s')
        
        try:
            # Stream data down to Supabase in chunks to avoid rate limiting
            df.to_sql(
                name=table_name,
                con=engine,
                if_exists="append",
                index=False,
                chunksize=500
            )
            
            print(f"✅ Successfully populated table '{table_name}'!")
        except Exception as e:
            print(f"❌ Failed to upload {actual_filename}: {e}")
            
    else:
        print(f"⚠️ Could not find '{expected_file}' in the downloaded folder.")

print("All tables populated successfully!")