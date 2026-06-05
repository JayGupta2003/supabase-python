from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

# 1. Connect to Supabase
DB_URL = os.getenv("SUPABASE_DB_URL")
if not DB_URL:
    raise ValueError("❌ Error: SUPABASE_DB_URL not found in .env file.")

engine = create_engine(DB_URL)

# 2. Define your exact SQL block
create_tables_sql = """
-- 1. Clear out the old, incorrect tables
DROP TABLE IF EXISTS reactions, posts, users CASCADE;
DROP TABLE IF EXISTS reactions_table, posts_table, friends_table, user_table CASCADE;

-- 2. Create the Parent Table
CREATE TABLE user_table (
    id SERIAL PRIMARY KEY,
    surname TEXT,
    name TEXT,
    age INT,
    subscription_date TIMESTAMP
);

-- 3. Create the Posts Table
CREATE TABLE posts_table (
    id SERIAL PRIMARY KEY,
    "user" TEXT,
    post_type TEXT,
    post_date TIMESTAMP
);

-- 4. Create the Reactions Table
CREATE TABLE reactions_table (
    id SERIAL PRIMARY KEY,
    "user" TEXT,
    reaction_type TEXT,
    reaction_date TIMESTAMP
);

-- 5. Create the Friends Table (Bonus table found in your dataset!)
CREATE TABLE friends_table (
    id SERIAL PRIMARY KEY,
    friend_1 TEXT,
    friend_2 TEXT
);
"""

print("Connecting to Supabase to create tables...")

# 3. Execute the SQL transaction
try:
    with engine.connect() as connection:
        connection.execute(text(create_tables_sql))
        connection.commit()
        print("✅ Database tables structural framework built successfully!")
except Exception as e:
    print(f"❌ Error creating tables: {e}")
    exit(1)