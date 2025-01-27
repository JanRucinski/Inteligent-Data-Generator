import json
import re
from faker import Faker
import random
import time
import json
import re
from faker import Faker
import random
import time
import argparse

fake = Faker()
settings = {}

# Constants
DEFAULT_ROWS_PER_TABLE = 10
DEFAULT_FAILSAFE_LIMIT = 100
PRIORITIZED_COLUMNS = ["ID", "gender", "state"]

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

def prescan_for_settings(json_file): #might handle foreign keys?
    """Extracts settings from the input and returns them."""
    global settings
    settings = json_file.get("settings", {})

    localization = settings.get("localization")
    if localization:
        global fake
fake = Faker()
settings = {}

# Constants
DEFAULT_ROWS_PER_TABLE = 10
DEFAULT_FAILSAFE_LIMIT = 100
PRIORITIZED_COLUMNS = ["ID", "gender", "state"]

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

def prescan_for_settings(json_file): #might handle foreign keys?
    """Extracts settings from the input and returns them."""
    global settings
    settings = json_file.get("settings", {})

    localization = settings.get("localization")
    if localization:
        global fake
        fake = Faker(localization)

    return settings

def sort_tables_by_dependencies(json_file):
    """Sorts the tables based on their dependencies."""
    tables = json_file.get("tables", [])
    table_dependencies = {table["name"]: set() for table in tables}

    for table in tables:
        for column in table["columns"]:
            if "foreign_key" in column:
                referenced_table = column["foreign_key"].split(".")[0]
                table_dependencies[table["name"]].add(referenced_table)

    sorted_tables = []
    while table_dependencies:
        tables_without_dependencies = {table for table, dependencies in table_dependencies.items() if not dependencies}
        if not tables_without_dependencies:
            raise ValueError("Circular dependency detected in the schema.")
        sorted_tables.extend(tables_without_dependencies)
        table_dependencies = {table: dependencies - tables_without_dependencies for table, dependencies in table_dependencies.items() if table not in tables_without_dependencies}

    return [next(table for table in tables if table["name"] == table_name) for table_name in sorted_tables]

def sort_columns_by_priority(columns):
    """Sorts the columns based on their priority."""
    sorted_columns = []
    for column_name in PRIORITIZED_COLUMNS:
        column = next((column for column in columns if column["name"] == column_name), None)
        if column:
            sorted_columns.append(column)
    for column in columns:
        if column not in sorted_columns:
            sorted_columns.append(column)
    return sorted_columns

def find_errors(json_file):
    """Finds errors in the schema, such as missing tables or columns."""
    tables = json_file.get("tables", [])
    table_names = [table["name"] for table in tables]
    errors = []
    global settings

    for table in tables:
        for column in table["columns"]:
            if "foreign_key" in column:
                referenced_table = column["foreign_key"].split(".")[0]
                if referenced_table not in table_names:
                    errors.append(f"Error: The table '{referenced_table}' does not exist.")
            if column.get("generation") == "state" and settings.get("localization") != "en":
                errors.append("Error: The 'state' generation type requires the 'en' localization.")

    return errors

def generate_sample_data(json_file):
    """Generates sample data for each table in the schema."""
    data = {}
    primary_keys = {}
    errors_in_generation = []

    sorted_tables = sort_tables_by_dependencies(json_file)

    # Define a dictionary to map generation types to Faker methods
    generation_methods = {
        "lastName": lambda: fake.last_name(),
        "gender": lambda: random.choice(["Male", "Female", "Non-Binary"]),
        "ssn": lambda: fake.unique.ssn(),
        "date": lambda: fake.date(),
        "city": lambda: fake.city(),
        "country": lambda: fake.country(),
        "state": lambda: fake.state(),
        "postcode": lambda: fake.postcode(),
        "amount": lambda: round(random.uniform(1, 1000), 2)
    }

    for table in sorted_tables:
        table_name = table["name"]
        columns = table["columns"]
        sample_rows = []

        generate_sample_data_table(primary_keys, errors_in_generation, generation_methods, table_name, columns, sample_rows)

        data[table_name] = sample_rows

    return data, errors_in_generation

def generate_sample_data_table(primary_keys, errors_in_generation, generation_methods, table_name, columns, sample_rows):
    for _ in range(settings.get("rows_per_table", DEFAULT_ROWS_PER_TABLE)):
        row = {}
        gender_value = None
        sorted_columns = sort_columns_by_priority(columns)

        for column in sorted_columns:
            column_name = column["name"]
            column_type = column["type"]
            generation = column.get("generation")

            failsafe = 0

            while failsafe < settings.get("failsafe_limit", DEFAULT_FAILSAFE_LIMIT):
                passed = True

                    # Generate data based on the "generation" type, or the column type
                if "foreign_key" in column:
                    referenced_table, referenced_column = column["foreign_key"].split(".")
                    if referenced_table in primary_keys and primary_keys[referenced_table]:
                        row[column_name] = random.choice(primary_keys[referenced_table])
                    else:
                        row[column_name] = None  # Set to None if no primary keys available
                else:
                    if generation in generation_methods:
                        row[column_name] = generation_methods[generation]()
                        if generation == "gender":
                            gender_value = row[column_name]
                        if generation == "firstName":
                            if gender_value == "Male":
                                row[column_name] = fake.first_name_male
                            elif gender_value == "Female":
                                row[column_name] = fake.first_name_female
                            else:
                                row[column_name] = fake.first_name()
                    else:
                            # Default generation types
                        if column_type == "integer":
                            row[column_name] = random.randint(1, 100)
                        elif column_type == "string":
                            row[column_name] = fake.word()
                        elif column_type == "date":
                            row[column_name] = fake.date()
                        elif column_type == "decimal":
                            row[column_name] = round(random.uniform(1, 1000), 2)
                        elif column_type == "float":
                            row[column_name] = round(random.uniform(-30, 50), 1)
                        elif column_type == "text":
                            row[column_name] = fake.sentence()
                        elif column_type == "boolean":
                            row[column_name] = random.choice([True, False])
                        else:
                            row[column_name] = None

                    # Handle unique constraints for SSN, PostalCode, etc.
                if "constraints" in column and "unique" in column["constraints"]:
                    row[column_name] = fake.unique.ssn() if column_name == "SSN" else fake.unique.zipcode()

                    # Primary key handling
                if "primary_key" in column:
                    if table_name not in primary_keys:
                        primary_keys[table_name] = []
                    primary_keys[table_name].append(row[column_name])  # Store primary key

                if row[column_name] is None:
                    print(column, generation, " was wrong")

                    # Regex validation
                if "regex" in column:
                    pattern = re.compile(column["regex"])
                    if not pattern.match(row[column_name]):
                        passed = False

                if passed:
                    break
                else:
                    failsafe += 1
                    if failsafe == 100:
                        errors_in_generation.append(f"Failed to generate data for the column '{column_name}' in the table '{table_name}' that fits criteria, row: {row} '\n'")
                
        sample_rows.append(row)

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
    parser = argparse.ArgumentParser(description="Generate sample data from a JSON schema.")
    parser.add_argument("--schema_file", "-i" , default="input.json", help="Path to the JSON schema file")
    parser.add_argument("--output_file", "-o", default="sample_data.sql", help="Path to the output SQL file")
    args = parser.parse_args()

    time_start = time.time()
    schema = read_json(args.schema_file)
    
    if schema:
        prescan_for_settings(schema)
        errors = find_errors(schema)

        if errors:
            for error in errors:
                print(error)
            print("No output generated")
        else:
            sample_data, errors = generate_sample_data(schema)
            sql_statements = generate_sql_insert_statements(sample_data)
            save_sql_file(sql_statements, args.output_file)

        print("Script closed in", time.time() - time_start, " seconds")
        if (errors):
            print("generation issues: ", errors)
    else:
        print("schema issues")
