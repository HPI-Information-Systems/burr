import psycopg2
import pandas as pd
from psycopg2 import sql, OperationalError, ProgrammingError, InterfaceError

def get_constraints(database, user, password, host="localhost", port="5432"):
    """
    Connects to a PostgreSQL database and retrieves all primary key, unique, and foreign key constraints.
    
    Parameters:
        database (str): Name of the PostgreSQL database.
        user (str): Username for the database.
        password (str): Password for the database.
        host (str): Database server host (default is "localhost").
        port (str): Database server port (default is "5432").
    
    Returns:
        pd.DataFrame: DataFrame containing the constraints.
    """
    conn = None
    try:
        # Connect to PostgreSQL database
        conn = psycopg2.connect(
            dbname=database,
            user=user,
            password=password,
            host=host,
            port=port
        )
        
        # Define the query to get constraints
        query = sql.SQL("""
            SELECT 
                tc.table_schema, 
                tc.table_name, 
                tc.constraint_name, 
                tc.constraint_type, 
                kcu.column_name AS column_name
            FROM 
                information_schema.table_constraints AS tc
            JOIN 
                information_schema.key_column_usage AS kcu 
            ON 
                tc.constraint_name = kcu.constraint_name
                AND tc.table_schema = kcu.table_schema
            WHERE 
                tc.constraint_type IN ('PRIMARY KEY', 'UNIQUE', 'FOREIGN KEY')
            ORDER BY 
                tc.table_name, 
                tc.constraint_type;
        """)
        
        # Execute the query and fetch results
        with conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

            # Check if rows were returned
            if not rows:
                print("No constraints found in the database.")
                return pd.DataFrame()

            # Fetch column names for the DataFrame
            colnames = [desc[0] for desc in cursor.description]

            # Convert results to a pandas DataFrame for better readability
            df = pd.DataFrame(rows, columns=colnames)
            print("Constraints successfully retrieved.")
            return df

    except OperationalError as e:
        print(f"Operational error: Could not connect to the database.\nDetails: {e}")
    except ProgrammingError as e:
        print(f"Programming error: Issue with SQL query execution.\nDetails: {e}")
    except InterfaceError as e:
        print(f"Interface error: Database connection issue.\nDetails: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # Ensure the connection is closed even if an error occurs
        if conn:
            conn.close()
            print("Database connection closed.")

def generate_description(df):
    """
    Generates a summary description of the constraints in the database based on the DataFrame content.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing constraints information.
    
    Returns:
        str: A descriptive summary of the constraints.
    """
    if df.empty:
        return "No constraints found in the database."

    description = "Database Constraint Summary:\n"
    constraint_counts = df['constraint_type'].value_counts()
    
    for constraint_type, count in constraint_counts.items():
        description += f"- {count} {constraint_type.lower()} constraint(s) found.\n"
    
    description += "\nTables and Constraints Overview:\n"
    
    grouped = df.groupby(['table_schema', 'table_name', 'constraint_type'])
    for (schema, table, constraint_type), group in grouped:
        columns = ', '.join(group['column_name'])
        description += f"Table '{schema}.{table}' has a {constraint_type.lower()} constraint on columns: {columns}.\n"
    
    return description

if __name__ == "__main__":
    # Replace with your actual PostgreSQL database credentials
    database = input("Enter the database name: ")
    user = input("Enter the database user: ")
    password = input("Enter the database password: ")
    host = input("Enter the database host (default is 'localhost'): ") or "localhost"
    port = input("Enter the database port (default is '5432'): ") or "5432"

    # Fetch constraints
    constraints_df = get_constraints(database, user, password, host, port)
    if not constraints_df.empty:
        # Generate and print a summary prompt
        prompt = generate_description(constraints_df)
        print("\n" + prompt)
