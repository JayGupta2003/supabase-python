# Relational Data Engineering: Kaggle to Supabase Pipeline

## Overview

This project is an automated ETL (Extract, Transform, Load) pipeline. It programmatically downloads a raw social media dataset from Kaggle, cleans and transforms the data using Pandas (handling Unix timestamps and formatting), and streams it into a fully relational PostgreSQL database hosted on Supabase.

## Tech Stack

- **Language:** Python
- **Data Manipulation:** Pandas
- **Database:** PostgreSQL (Supabase)
- **ORM / Connections:** SQLAlchemy, psycopg2
- **APIs:** Kaggle API (`kagglehub`)

## Database Schema

The database consists of four related tables:

1. `user_table` (Primary user data)
2. `posts_table` (Linked to users)
3. `reactions_table` (Linked to users)
4. `friends_table` (Network mapping)

## How to Run This Project Locally

**1. Clone the repository**

```bash
git clone [https://github.com/YourUsername/YourRepoName.git](https://github.com/YourUsername/YourRepoName.git)
cd YourRepoName

```

**2. Install dependencies**

```bash
pip install -r requirements.txt

```

**3. Set up your environment variables**
Rename the `.env.example` file to `.env` and add your Kaggle and Supabase credentials.

**4. Run the pipeline**

```bash
python main.py
```

## Example Queries

Once the database is populated, you can run complex relational queries. For example, to find the most active users:

```sql
SELECT u.name, u.surname, COUNT(p.id) as total_posts
FROM user_table u
JOIN posts_table p ON u.id = p."user"::INTEGER
GROUP BY u.id, u.name, u.surname
ORDER BY total_posts DESC
LIMIT 5;
```
