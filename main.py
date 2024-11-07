import json
from faker import Faker
import random

fake = Faker()
settings = {}

def read_json(file_path):
    """Reads a JSON file and returns its contents."""
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            return data
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except json.JSONDecodeError:
        print(f"Error: The file '{file_path}' is not a valid JSON format.")
    return None

def prescan_for_settings(schema): #might handle foreign keys?
    """Extracts settings from the schema and returns them."""
    settings = schema.get("settings", {})

    localization = settings.get("localization")
    if localization:
        global fake
        fake = Faker(localization)

    return settings


def generate_sample_data(schema):
    """Generates sample data for each table in the schema."""
    data = {}
    primary_keys = {}
    # TODO: settings
    for table in schema["tables"]:
        table_name = table["name"]
        columns = table["columns"]
        sample_rows = []
        
        for _ in range(settings.get("rows_per_table", 10)):
            row = {}
            gender_value = None  # Track gender if specified 
            """TODO: could be better, for this to work currently the gender has to be specified before the name 
                    and constraints like this will be plenty, maybe scan for those first before generating data?"""

            for column in columns:
                column_name = column["name"]
                column_type = column["type"]
                generation = column.get("generation")
                
                # Generate data based on the "generation" type, or the column type TODO: a lot (settings, constraints, REGEX, foreign keys, more data and generation types)
                # Foreign key handling
                if "foreign_key" in column:
                    referenced_table, referenced_column = column["foreign_key"].split(".")
                    if referenced_table in primary_keys and primary_keys[referenced_table]:
                        # Select a random primary key from the referenced table
                        row[column_name] = random.choice(primary_keys[referenced_table])
                    else:
                        row[column_name] = None  # Set to None if no primary keys available
                else:
                    if generation == "firstName":
                        if gender_value == "Male":
                            row[column_name] = fake.first_name_male()
                        elif gender_value == "Female":
                            row[column_name] = fake.first_name_female()
                        else:
                            row[column_name] = fake.first_name()
                    elif generation == "lastName":
                        row[column_name] = fake.last_name()
                    elif generation == "gender":
                        gender_value = random.choice(["Male", "Female", "Non-Binary"])
                        row[column_name] = gender_value
                    elif generation == "ssn":
                        row[column_name] = fake.unique.ssn()
                    elif generation == "date":
                        row[column_name] = fake.date()
                    elif generation == "city":
                        row[column_name] = fake.city()
                    elif generation == "country":
                        row[column_name] = fake.country()
                    elif generation == "province":
                        row[column_name] = fake.state()
                    elif generation == "postalCode":
                        row[column_name] = fake.postcode()
                    elif generation == "amount":
                        row[column_name] = round(random.uniform(1, 1000), 2)
                    elif column_type == "integer":
                        row[column_name] = random.randint(1, 100)
                    else:
                        row[column_name] = None  # Default to None for unsupported types
                    if column_type == "string" and not row[column_name]:
                        if "name" in column_name.lower():
                            row[column_name] = fake.name()
                        elif "city" in column_name.lower():
                            row[column_name] = fake.city()
                        elif "country" in column_name.lower():
                            row[column_name] = fake.country()
                        elif "province" in column_name.lower():
                            row[column_name] = fake.state()
                        elif "gender" in column_name.lower():
                            row[column_name] = random.choice(["Male", "Female", "Non-Binary"])
                        else:
                            row[column_name] = fake.word()
                    elif column_type == "integer":
                        row[column_name] = random.randint(1, 100)
                    elif column_type == "date":
                        row[column_name] = fake.date()
                    elif column_type == "decimal":
                        row[column_name] = round(random.uniform(1, 1000), 2)
                    elif column_type == "float":
                        row[column_name] = round(random.uniform(-30, 50), 1)
                    elif column_type == "text":
                        row[column_name] = fake.sentence() #TODO
                    else:
                        if not row[column_name]:
                            row[column_name] = None  # Default to None for unsupported types
                    
                # Handle unique constraints for SSN, PostalCode, etc.
                if "constraints" in column and "unique" in column["constraints"]:
                    row[column_name] = fake.unique.ssn() if column_name == "SSN" else fake.unique.zipcode()

                # Primary key handling
                if "primary_key" in column:
                    if table_name not in primary_keys:
                        primary_keys[table_name] = []
                    primary_keys[table_name].append(row[column_name])  # Store primary key

                if row[column_name] == None:
                    print(column, generation, " was wrong")
            
            sample_rows.append(row)
        
        data[table_name] = sample_rows
    return data

def generate_sql_insert_statements(data):
    """Generates SQL insert statements for the sample data."""
    sql_statements = []
    for table_name, rows in data.items():
        for row in rows:
            columns = ", ".join(row.keys())
            values = ", ".join(
                [f"'{value}'" if isinstance(value, str) else str(value) for value in row.values()]
            )
            sql_statement = f"INSERT INTO {table_name} ({columns}) VALUES ({values});"
            sql_statements.append(sql_statement)
    return sql_statements

def save_sql_file(sql_statements, output_file="sample_data.sql"):
    """Saves the generated SQL insert statements to a .sql file."""
    with open(output_file, 'w') as sql_file:
        sql_file.write("\n".join(sql_statements))
    print(f"SQL insert statements saved to {output_file}")

# Example usage
if __name__ == "__main__":
    schema_file = "input.json"  # Replace with your JSON schema file
    schema = read_json(schema_file)
    
    if schema:
        prescan_for_settings(schema)
        sample_data = generate_sample_data(schema)
        sql_statements = generate_sql_insert_statements(sample_data)
        save_sql_file(sql_statements)
    else:
        print("schema issues")
