import psycopg2
from enum import Enum
from typing import List

from evaluator.database.data_parser import DataParser
from evaluator.database.sql_engine.table_context import TableContext, ForeignKeyRelation

class SchemaTypeEnum(Enum):
    Attribute = 1
    NMTable = 2     
    N1Relation = 3
    Table = 4
    PrimaryKey = 5

class DatabaseSchema:
    def __init__(self) -> None:
        self.tables = {}

    def add_table(self, table: TableContext):
        self.tables[table.table_name] = table

    def get_table(self, table_name) -> TableContext: return self.tables[table_name]
    def stringify(self) -> str: " ".join(map(lambda x: x.stringify(), self.tables.values()))
    def get_attributes(self, table_name) -> List[str]: self.get_table(table_name).attributes
    def get_foreign_keys(self, table_name) -> List[ForeignKeyRelation]: self.get_table(table_name).foreign_keys
    def get_primary_keys(self, table_name) -> List[str]: self.get_table(table_name).primary_keys

class SQLEngine(DataParser):
    def __init__(self, database_name, schema, user="lukaslaskowski", host="127.0.0.1", port="5432") -> None:
        super().__init__()
        self.credentials = {"database_name": database_name,
                            "user": user,
                            "host": host,
                            "port": port,
                            "schema": schema,
                            }
        self.connection = None
        self.cursor = None
        self.database_schema = DatabaseSchema()
        
        for table in list(map(lambda x: x[2], self.query_database("SELECT * FROM information_schema.tables WHERE table_schema = 'public'", keep_alive=True))):
            attributes = list(map(lambda x: x[0], self.query_database(f"select column_name from information_schema.columns where table_name = '{table}' AND table_schema = '{self.credentials['schema']}'", keep_alive=True)))
            foreign_keys = list(map(lambda x: ForeignKeyRelation(x[1], x[2], x[3], x[4], x[5]), self.query_database(foreign_key_constraint_query(table, self.credentials['schema']), keep_alive=True)))
            primary_keys = list(map(lambda x: x[0], self.query_database(primary_keys_query(table, self.credentials['schema']), keep_alive=True)))
            self.database_schema.add_table(TableContext(table, attributes, foreign_keys, primary_keys))
        self.end_connection()

    def get_tables(self):
        return self.tables

    def get_context(self, schema_type: SchemaTypeEnum, schema_element):
        if schema_type is SchemaTypeEnum.Attribute:
            #the mother table
            pass
        elif schema_type is SchemaTypeEnum.N1Relation:
            #detection: an attribute and an FOREIGN KEY constraint for that attribute exists
            #filter for given attribute the foreign key constraints and return table
            pass
        elif schema_type is SchemaTypeEnum.NMTable:
            #detection: only two columns with two FOREIGN KEY constraints AND those two columns construct PK.
            #collect for given table the two connected table
            pass
        elif schema_type is SchemaTypeEnum.Table:
            # no context (just analyze the table itself)
            # Do we need this? -> am ende doch einfach nur gucken ob alle attribute davon abgedeckt sind
            pass
        else:
            raise Exception("Schematype is unknown!")
    
    def get_schema_element_type(self, el, table_name):
        table_context = self.tables[table_name]
        if self.is_part_of_nm_table(table_context):
            return SchemaTypeEnum.NMTable
        elif self.is_n1_relation(el, table_context=table_context):
            return SchemaTypeEnum.N1Relation
        elif self.is_primary_key(el, table_context):
            return SchemaTypeEnum.PrimaryKey
        else: 
            return SchemaTypeEnum.Attribute
    
    def is_part_of_nm_table(self, table_context: TableContext):
        has_exactly_two_attributes = len(table_context.attributes) == 2
        column_has_foreign_key = lambda table_name, attribute: len(list(filter(lambda x: table_name == x.origin_table and x.origin_attribute == attribute))) == 1
        primary_key_is_two_attributes = len(table_context.primary_keys) == 2
        return  has_exactly_two_attributes and \
                primary_key_is_two_attributes and \
                column_has_foreign_key(table_context.table_name, table_context.attributes[0]) and \
                column_has_foreign_key(table_context.table_name, table_context.attributes[1]) 
    
    def is_primary_key(self, attribute, table_context: TableContext):
        return list(filter(lambda attr: attribute == attr, table_context.primary_keys)) == 1

    def is_n1_relation(self, attribute, table_context: TableContext):
        attribute_is_in_table = len(list(filter(lambda attr: attr == table_context.attributes))) == 1
        foreign_key_exists = attribute in list(map(lambda fk: fk.origin_attribute, table_context.foreign_keys))
        return attribute_is_in_table and foreign_key_exists

    def query_database(self, query, keep_alive=False):
        try:
            if self.cursor == None or self.connection == None:
                self.get_connection()
            self.cursor.execute(query)
            response = self.cursor.fetchall()
            return response
        except (Exception, psycopg2.Error) as error :
            print ("Error while connecting to PostgreSQL", error)
        finally:
                if(self.connection and self.cursor and not keep_alive):
                    self.end_connection()

    def get_connection(self):
        try:
            connection = psycopg2.connect(  user = self.credentials["user"],
                                        host = self.credentials["host"],
                                        port = self.credentials["port"],
                                        database = self.credentials["database_name"],
                                        )
            cursor = connection.cursor()
            self.connection = connection
            self.cursor = cursor
            print("Connection obtained")
        except (Exception, psycopg2.Error) as error :
            self.end_connection()
            raise ConnectionError("Error while connecting to PostgreSQL", error)
    
    def end_connection(self):
        if self.cursor != None and self.connection != None:
            self.cursor.close()
            self.connection.close()
            self.cursor=None
            self.connection = None
        print("PostgreSQL connection is closed")

foreign_key_constraint_query = lambda table_name, schema: f"SELECT tc.table_schema, tc.constraint_name,tc.table_name, kcu.column_name, ccu.table_schema AS foreign_table_schema,ccu.table_name AS foreign_table_name,ccu.column_name AS foreign_column_name FROM information_schema.table_constraints AS tc JOIN information_schema.key_column_usage AS kcu ON tc.constraint_name = kcu.constraint_name AND tc.table_schema = kcu.table_schema JOIN information_schema.constraint_column_usage AS ccu ON ccu.constraint_name = tc.constraint_name AND ccu.table_schema = tc.table_schema WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_name='{table_name}' AND tc.table_schema='{schema}';"

primary_keys_query = lambda table_name, schema: f"SELECT c.column_name \
FROM information_schema.table_constraints tc \
JOIN information_schema.constraint_column_usage AS ccu USING (constraint_schema, constraint_name) \
JOIN information_schema.columns AS c ON c.table_schema = tc.constraint_schema \
  AND tc.table_name = c.table_name AND ccu.column_name = c.column_name \
WHERE constraint_type = 'PRIMARY KEY' and tc.table_name = '{table_name}' AND tc.table_schema='{schema}';"
    


