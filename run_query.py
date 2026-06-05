import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

# 1. Connect to Supabase
DB_URL = os.getenv("SUPABASE_DB_URL")
if not DB_URL:
    raise ValueError("❌ Error: SUPABASE_DB_URL not found in .env file.")

engine = create_engine(DB_URL)

#Set query
query_inner = """
    SELECT u.name, u.surname, p.post_type, p.post_date
    FROM user_table u
    INNER JOIN posts_table p ON u.id = p."user"::INTEGER 
    ORDER BY p.post_date DESC;
"""

#Run queries using pandas
df_results = pd.read_sql(query_inner, con=engine)
l = []
l.append(df_results)

query_left = """
    SELECT u.name, u.surname, p.post_type
    FROM user_table u
    LEFT JOIN posts_table p ON u.id = p."user"::INTEGER;
"""

df_results = pd.read_sql(query_left, con=engine)
l.append(df_results)

query_outer = """
    SELECT u.name, r.reaction_type, r.reaction_date
    FROM user_table u
    FULL OUTER JOIN reactions_table r ON u.id = r."user"::INTEGER;
"""

df_results = pd.read_sql(query_outer, con=engine)
l.append(df_results)

query_active = """
    SELECT u.name, u.surname, COUNT(p.id) as total_posts
    FROM user_table u
    JOIN posts_table p ON u.id = p."user"::INTEGER
    GROUP BY u.id, u.name, u.surname
    ORDER BY total_posts DESC;
"""

df_results = pd.read_sql(query_active, con=engine)
l.append(df_results)

query_metric = """
    SELECT reaction_type, COUNT(*) as reaction_count
    FROM reactions_table
    GROUP BY reaction_type
    ORDER BY reaction_count DESC;
"""

df_results = pd.read_sql(query_metric, con=engine)
l.append(df_results)

print(l)