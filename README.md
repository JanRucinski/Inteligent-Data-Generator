# Inteligent-Data-Generator

The **Intelligent Data Generator** is a tool designed to create dummy data for populating databases. It leverages the **Faker** library, supports custom scripts, and is configured via a JSON file. This tool is meant for developers and testers who need to generate large volumes of data for testing, development, or demonstration purposes.

## Suggested Workflow:
1. **Prepare an SQL file** containing `CREATE TABLE` statements for your database.
2. Use **converter.py** with your SQL file to generate a prototype JSON schema file.
3. Configure the JSON schema file with your desired data generation types and settings.
4. Use **main.py** with your JSON schema file to generate an SQL file containing `INSERT` statements with the dummy data.

## Installation:

### Requirements:
- **Faker**: Tested on version **30.8.0** - [Download Faker](https://pypi.org/project/Faker/30.8.0/)
- **Python**: Version **3.7 or newer** (tested on Python **3.12.2**) - [Download Python](https://www.python.org/downloads/)

### Steps:

1. **Verify Python and Faker installation:**

    Ensure Python and the Faker library are installed on your system.

2. **Download the project:**
   
    Clone or download the repository to your local machine.
  
## Generating Data with `main.py`:

To generate dummy data, you only need an `input.json` file with the appropriate structure. An example is provided in the repository.

Run the following command to generate data:

```bash
python main.py
```
By default, the script will:

- Read from input.json as the input schema file.

- Output the generated data to sample_data.sql.

Optional Arguments:

- `-i` or `--schema_file`: Specify the input JSON file.

- `-o` or `--output_file`: Specify the output SQL file.

- `-s` or `--script`: Provide a custom script for additional generation types.

- `-h`: Display help information.

Example:
```bash
python main.py -i input_schema.json -o output_data.sql -s custom_script.py
```

### Creating a JSON Schema with converter.py
You can generate a JSON schema file from an SQL file containing CREATE TABLE statements using converter.py.

Run the following command:
```bash
python converter.py
```
By default, the script will:

- Read from test_schema.sql as the input SQL file.
- Output the JSON schema to input.json.

Optional Arguments:

- `-i` or `--input_file`: Specify the input SQL file.
- `-o` or `--output_file`: Specify the output JSON file.
Example:
```bash
python converter.py -i my_input.sql -o my_output.json
```
**Note:** The generated JSON file will use default settings for all fields. It is recommended to modify the file to suit your needs.

## Supported Features

### Settings:
- **rows_per_table**: Number of rows to generate per table.
- **localization**: Localization settings for data generation (e.g., names, addresses).
- **failsafe_limit**: A limit to prevent infinite loops during data generation.

### Constraints:
- **unique**: Ensures unique values for specified fields.

### Generation Types:
- **firstName**
- **lastName**
- **gender**
- **ssn**
- **date**
- **city**
- **country**
- **province**
- **postalCode**
- **amount**
- **by data type:** `integer`, `string`, `date`, `decimal`, `float`, `text`

### Custom generation:
You can extend the tool's capabilities by adding custom generation methods. Write a Python script with your logic, like this:

```python
def car_make():
    return random.choice(["Toyota", "Ford", "Chevrolet", "Nissan", "Honda", "Jeep", "Dodge", "Subaru", "Hyundai", "BMW"])
```

Pass your script using the -s (or --script) flag:
```
python main.py -s script.py
```
To use your custom generation methods, specify the method name in the JSON file:
```
"generation": "car_make"
```
**Note:** Ensure your custom methods return the desired values for your data.

### Planned features:
- **Improved foreign key handling**: Better support for complex relationships between tables.
- **Additional generation types**: More built-in options for generating diverse data.
- **Custom script with seed support**: Allow seeding for reproducible data generation.
- **Enhanced primary key generation**: More options for generating primary keys.
- **Converter enhancements**: Automatically set generation types based on column names (e.g., `gender`, `firstName`).

## Known issues:
- **Foreign key dependencies**: Tables are generated one-by-one, sorted by the number of foreign key columns. If Table A references Table B, but Table B references other tables, Table B may not be generated in time for Table A, resulting in missing foreign keys.
