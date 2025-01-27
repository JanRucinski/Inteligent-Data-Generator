import re
import json

def parse_sql_to_json(sql_file_path, output_file_path):
    # Open and read the .sql file
    with open(sql_file_path, 'r') as sql_file:
        sql_content = sql_file.read()

    # Regex pattern to extract table names and their columns
    table_pattern = re.compile(r'CREATE TABLE (\w+) \((.*?)\);', re.S)
    column_pattern = re.compile(r'(\w+)\s+(\w+)(.*?),?\n')

    # Match tables
    tables = table_pattern.findall(sql_content)

    json_output = {
        "settings": {
            "localization": "en_US",
            "rows_per_table": 15
        },
        "tables": []
    }

    for table_name, table_content in tables:
        table = {"name": table_name, "columns": []}

        # Match columns
        columns = column_pattern.findall(table_content + '\n')
        for column_name, column_type, column_constraints in columns:
            column = {"name": column_name}

            # Map SQL types to JSON types
            sql_to_json_type = {
                "INT": "integer",
                "INTEGER": "integer",
                "VARCHAR": "string",
                "TEXT": "text",
                "DECIMAL": "decimal",
                "FLOAT": "float",
                "DATE": "date"
            }

            column["type"] = sql_to_json_type.get(column_type.upper(), "string")

            # Handle constraints
            if "PRIMARY KEY" in column_constraints.upper():
                column["primary_key"] = True
            if "FOREIGN KEY" in column_constraints.upper():
                # Extract foreign key reference
                fk_match = re.search(r'\bREFERENCES\s+(\w+)\((\w+)\)', column_constraints, re.I)
                if fk_match:
                    ref_table, ref_column = fk_match.groups()
                    column["foreign_key"] = f"{ref_table}.{ref_column}"

            # Add column to table
            table["columns"].append(column)

        # Add table to JSON output
        json_output["tables"].append(table)

    # Write the output to a JSON file
    with open(output_file_path, 'w') as json_file:
        json.dump(json_output, json_file, indent=2)

# Example usage
parse_sql_to_json("test_schema.sql", "input.json")
