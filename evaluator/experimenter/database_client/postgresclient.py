import os
import subprocess
import pandas as pd
import wandb
import networkx as nx
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from psycopg2 import OperationalError, ProgrammingError, InterfaceError

class PostgresClient:
    def __init__(self, database, host=None, port=None, user=None, password=None):
        load_dotenv()
        self.host = os.getenv("POSTGRES_HOST") if host is None else host
        self.port = os.getenv("POSTGRES_PORT") if port is None else port
        self.user = os.getenv("POSTGRES_USER") if user is None else user
        self.password = os.getenv("POSTGRES_PASSWORD") if password is None else password
        self.database = database
        #self.engine = self.get_database_engine()

    def get_database_engine(self):
        """Creates and returns a SQLAlchemy engine for connecting to the database."""
        try:
            if self.password:
                engine_url = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
            else:
                engine_url = f"postgresql://{self.user}@{self.host}:{self.port}/{self.database}"
            # print("Connecting to database:", engine_url)
            engine = create_engine(engine_url)
            return engine
        except Exception as e:
            print(f"Error creating SQLAlchemy engine: {e}")
            return None
        


    def update_database(self, script_path, add_primary_keys=False):
        """Runs an SQL script file using psql command line."""
        print(f"Updating database {self.database} using script {script_path}")
        wandb.save(script_path, base_path=os.path.dirname(script_path))
        command = ['psql', '-q', '-f', script_path, '-U', self.user, '-d', 'postgres', '-h', self.host, '-v', 'ON_ERROR_STOP=1']
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Database updated successfully.")
        else:
            print("Database update failed with return code:", result.returncode)
            print("Error output:", result.stderr)
            raise ValueError("Database update failed")
        if add_primary_keys:
            self.add_primary_keys()

    def add_primary_keys(self):
        query = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        AND table_type = 'BASE TABLE'
        AND NOT EXISTS (
            SELECT 1
            FROM information_schema.table_constraints
            WHERE table_schema = 'public'
            AND table_name = tables.table_name
            AND constraint_type = 'PRIMARY KEY'
        );
        """
        try:
            engine = self.get_database_engine()
            tables_df = pd.read_sql(query, engine)
            tables = tables_df['table_name'].tolist()
            
            # If no tables without primary keys, exit the function
            if not tables:
                return

            # Add an `id` column as a primary key for each table without one
            with engine.connect() as connection:
                for table in tables:
                    try:
                        #verify_query = text(f'ALTER SCHEMA public OWNER TO lukaslaskowski;')
                        #result = connection.execute(verify_query)
                        alter_query = f"ALTER TABLE {table} ADD COLUMN artificial_id SERIAL PRIMARY KEY;"
                        res = connection.execute(text(alter_query))
                        connection.commit()
                        verify_query = text(f"""
                            SELECT column_name, data_type
                            FROM information_schema.columns
                            WHERE table_name = '{table}'
                            AND column_name = 'artificial_id';
                        """)
                        result = connection.execute(verify_query)
                        row = result.fetchone()
                    except SQLAlchemyError as e:
                        connection.rollback()
                        print(f"Failed to add primary key to {table}. Error:", str(e))
                        raise

            print("Primary keys added to all applicable tables.")

        except SQLAlchemyError as e:
            print("Failed to retrieve tables or add primary keys:", str(e))
            raise

    def get_primary_keys(self, table_name):
        """Returns the primary key columns for a given table."""
        query = f"""
            SELECT kcu.column_name
            FROM information_schema.table_constraints AS tc
            JOIN information_schema.key_column_usage AS kcu
            ON tc.constraint_name = kcu.constraint_name
            AND tc.table_schema = kcu.table_schema
            WHERE tc.table_name = '{table_name}'
            AND tc.constraint_type = 'PRIMARY KEY';
        """
        try:
            engine = self.get_database_engine()
            df = pd.read_sql(query, engine)
            if df.empty:
                return []
            else:
                return df['column_name'].tolist()
        except (OperationalError, ProgrammingError, InterfaceError) as e:
            print(f"Error fetching primary keys: {e}")
            return []

    def get_constraints(self):
        """Fetches all primary key, unique, and foreign key constraints."""
        query = """
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
        """
        try:
            engine = self.get_database_engine()
            df = pd.read_sql(query, engine)
            if df.empty:
                print("No constraints found in the database.")
            return df
        except (OperationalError, ProgrammingError, InterfaceError) as e:
            print(f"Error fetching constraints: {e}")
            return pd.DataFrame()

    def get_all_tables(self):
        """Retrieves all tables from the database and returns a dictionary with DataFrames for each table."""
        tables = {}
        try:
            engine = self.get_database_engine()
            # Get the list of tables
            table_names = pd.read_sql("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'", engine)
            table_names = table_names['table_name'].tolist()

            # Load each table into a DataFrame
            for table_name in table_names:
                query = f"SELECT * FROM {table_name}"
                df = pd.read_sql(query, engine)
                tables[table_name] = df
                # print(f"Table '{table_name}' loaded successfully.")

            return tables

        except Exception as e:
            print(f"Error fetching tables: {e}")
            return {}
        
    def get_foreign_keys_for_table(self, table_name: str, schema: str | None = None) -> pd.DataFrame:
        """Return foreign key constraints defined ON the given table (outgoing FKs)."""
        base_query = f"""
            SELECT
                con.conname AS constraint_name,
                src_ns.nspname AS table_schema,
                src.relname AS table_name,
                string_agg(src_att.attname, ', ' ORDER BY k.pos) AS column_names,
                tgt_ns.nspname AS foreign_table_schema,
                tgt.relname AS foreign_table_name,
                string_agg(tgt_att.attname, ', ' ORDER BY k.pos) AS foreign_column_names,
                CASE con.confupdtype
                    WHEN 'a' THEN 'NO ACTION'
                    WHEN 'r' THEN 'RESTRICT'
                    WHEN 'c' THEN 'CASCADE'
                    WHEN 'n' THEN 'SET NULL'
                    WHEN 'd' THEN 'SET DEFAULT'
                END AS on_update,
                CASE con.confdeltype
                    WHEN 'a' THEN 'NO ACTION'
                    WHEN 'r' THEN 'RESTRICT'
                    WHEN 'c' THEN 'CASCADE'
                    WHEN 'n' THEN 'SET NULL'
                    WHEN 'd' THEN 'SET DEFAULT'
                END AS on_delete
                FROM pg_constraint con
                JOIN pg_class src ON src.oid = con.conrelid
                JOIN pg_namespace src_ns ON src_ns.oid = src.relnamespace
                JOIN pg_class tgt ON tgt.oid = con.confrelid
                JOIN pg_namespace tgt_ns ON tgt_ns.oid = tgt.relnamespace
                JOIN LATERAL (
                SELECT i AS pos,
                        con.conkey[i]  AS src_attnum,
                        con.confkey[i] AS tgt_attnum
                FROM generate_subscripts(con.conkey, 1) AS i
                ) k ON TRUE
                JOIN pg_attribute src_att ON src_att.attrelid = src.oid AND src_att.attnum = k.src_attnum
                JOIN pg_attribute tgt_att ON tgt_att.attrelid = tgt.oid AND tgt_att.attnum = k.tgt_attnum
                WHERE con.contype = 'f'
                AND src_ns.nspname = 'public'
                AND src.relname = '{table_name}'
                GROUP BY con.conname, src_ns.nspname, src.relname,
                        tgt_ns.nspname, tgt.relname, con.confupdtype, con.confdeltype
                ORDER BY con.conname;
        """
        
        try:
            engine = self.get_database_engine()
            df = pd.read_sql(base_query, engine)
            if df.empty:
                print(f"No foreign keys found on table {schema+'.' if schema else ''}{table_name}.")
            return df
        except (OperationalError, ProgrammingError, InterfaceError) as e:
            print(f"Error fetching foreign keys: {e}")
            return pd.DataFrame()
        
    def get_foreign_keys(self):
        """Fetches all foreign key constraints in the database."""
        query = """
            SELECT 
                tc.constraint_name,
                tc.table_schema,
                tc.table_name,
                string_agg(kcu.column_name, ', ' ORDER BY kcu.ordinal_position) AS column_names,
                ccu.table_schema AS foreign_table_schema,
                ccu.table_name AS foreign_table_name,
                string_agg(ccu.column_name, ', ' ORDER BY kcu.ordinal_position) AS foreign_column_names
            FROM information_schema.table_constraints AS tc
            JOIN information_schema.key_column_usage AS kcu
            ON tc.constraint_name = kcu.constraint_name
            AND tc.table_schema = kcu.table_schema
            JOIN information_schema.constraint_column_usage AS ccu
            ON ccu.constraint_name = tc.constraint_name
            AND ccu.table_schema = tc.table_schema
            WHERE tc.constraint_type = 'FOREIGN KEY'
            GROUP BY tc.constraint_name, tc.table_schema, tc.table_name,
                    ccu.table_schema, ccu.table_name
            ORDER BY tc.table_name;
        """
        try:
            engine = self.get_database_engine()
            df = pd.read_sql(query, engine)
            if df.empty:
                print("No foreign keys found in the database.")
            else:
                print("Foreign keys successfully retrieved.")
            print("Foreign keys DataFrame:", df)
            return df
        except (OperationalError, ProgrammingError, InterfaceError) as e:
            print(f"Error fetching foreign keys: {e}")
            return pd.DataFrame()

    def get_distinct_values(self, table_name, column_name, limit=5):
        """Fetches distinct values for a specific column in a table."""
        try:
            engine = self.get_database_engine()
            # Use double quotes for table and column names to handle case sensitivity and special characters
            query = f'SELECT DISTINCT "{column_name}" FROM "{table_name}" LIMIT {limit}'
            df = pd.read_sql(query, engine)
            return df[column_name].tolist()
        except Exception as e:
            print(f"Error fetching distinct values for {table_name}.{column_name}: {e}")
            return []

    def generate_description(self, df):
        """Generates a summary description of the database constraints."""
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

    def to_networkx_graph(self, include_isolated_tables: bool = True) -> nx.DiGraph:
        """
        Returns the database schema as a NetworkX directed graph.
        
        Tables are represented as nodes, and foreign key relationships as directed edges.
        The edge direction follows the foreign key reference: from the table containing
        the foreign key to the table being referenced.
        
        Args:
            include_isolated_tables: If True, includes tables that have no foreign key
                                    relationships (neither incoming nor outgoing).
                                    
        Returns:
            nx.DiGraph: A directed graph where:
                - Nodes are table names with attributes:
                    - 'schema': The schema name (e.g., 'public')
                - Edges represent foreign key relationships with attributes:
                    - 'constraint_name': Name of the FK constraint
                    - 'column_names': Column(s) in the source table
                    - 'foreign_column_names': Column(s) in the target table
                    - 'on_update': ON UPDATE action
                    - 'on_delete': ON DELETE action
        
        Example:
            >>> client = PostgresClient('mydb')
            >>> G = client.to_networkx_graph()
            >>> print(G.nodes())  # List all tables
            >>> print(G.edges(data=True))  # List all FK relationships with attributes
            >>> # Find tables that reference 'users' table
            >>> predecessors = list(G.predecessors('users'))
        """
        G = nx.DiGraph()
        
        # Get all tables
        try:
            engine = self.get_database_engine()
            tables_query = """
                SELECT table_schema, table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_type = 'BASE TABLE'
            """
            tables_df = pd.read_sql(tables_query, engine)
            
            if include_isolated_tables:
                # Add all tables as nodes
                for _, row in tables_df.iterrows():
                    G.add_node(row['table_name'], schema=row['table_schema'])
        except Exception as e:
            print(f"Error fetching tables for graph: {e}")
            return G
        
        # Get all foreign keys
        fk_query = """
            SELECT
                con.conname AS constraint_name,
                src_ns.nspname AS table_schema,
                src.relname AS table_name,
                string_agg(src_att.attname, ', ' ORDER BY k.pos) AS column_names,
                tgt_ns.nspname AS foreign_table_schema,
                tgt.relname AS foreign_table_name,
                string_agg(tgt_att.attname, ', ' ORDER BY k.pos) AS foreign_column_names,
                CASE con.confupdtype
                    WHEN 'a' THEN 'NO ACTION'
                    WHEN 'r' THEN 'RESTRICT'
                    WHEN 'c' THEN 'CASCADE'
                    WHEN 'n' THEN 'SET NULL'
                    WHEN 'd' THEN 'SET DEFAULT'
                END AS on_update,
                CASE con.confdeltype
                    WHEN 'a' THEN 'NO ACTION'
                    WHEN 'r' THEN 'RESTRICT'
                    WHEN 'c' THEN 'CASCADE'
                    WHEN 'n' THEN 'SET NULL'
                    WHEN 'd' THEN 'SET DEFAULT'
                END AS on_delete
            FROM pg_constraint con
            JOIN pg_class src ON src.oid = con.conrelid
            JOIN pg_namespace src_ns ON src_ns.oid = src.relnamespace
            JOIN pg_class tgt ON tgt.oid = con.confrelid
            JOIN pg_namespace tgt_ns ON tgt_ns.oid = tgt.relnamespace
            JOIN LATERAL (
                SELECT i AS pos,
                       con.conkey[i]  AS src_attnum,
                       con.confkey[i] AS tgt_attnum
                FROM generate_subscripts(con.conkey, 1) AS i
            ) k ON TRUE
            JOIN pg_attribute src_att ON src_att.attrelid = src.oid AND src_att.attnum = k.src_attnum
            JOIN pg_attribute tgt_att ON tgt_att.attrelid = tgt.oid AND tgt_att.attnum = k.tgt_attnum
            WHERE con.contype = 'f'
            AND src_ns.nspname = 'public'
            GROUP BY con.conname, src_ns.nspname, src.relname,
                     tgt_ns.nspname, tgt.relname, con.confupdtype, con.confdeltype
            ORDER BY con.conname;
        """
        
        try:
            fk_df = pd.read_sql(fk_query, engine)
            
            # Add edges for each foreign key relationship
            for _, row in fk_df.iterrows():
                source_table = row['table_name']
                target_table = row['foreign_table_name']
                
                # Ensure nodes exist (in case include_isolated_tables is False)
                if source_table not in G:
                    G.add_node(source_table, schema=row['table_schema'])
                if target_table not in G:
                    G.add_node(target_table, schema=row['foreign_table_schema'])
                
                # Add edge with FK metadata
                G.add_edge(
                    source_table,
                    target_table,
                    constraint_name=row['constraint_name'],
                    column_names=row['column_names'],
                    foreign_column_names=row['foreign_column_names'],
                    on_update=row['on_update'],
                    on_delete=row['on_delete']
                )
                
        except Exception as e:
            print(f"Error fetching foreign keys for graph: {e}")
        
        return G

