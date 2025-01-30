# Inteligent-Data-Generator

## Installation:

### Requirements:
- **Faker**: Tested on version **30.8.0** - https://pypi.org/project/Faker/30.8.0/
- **Python**: Version **3.7 or newer** (tested on Python **3.12.2**) - https://www.python.org/downloads/

### Steps:

1. **Verify Python and Faker installation**
2. **Download the project**
  
## Usage:

There is only a need for an "input.json" file with a structure as provided in an example on the repository.

```
python main.py
```
It will by default try to read "input.json" file as an input, and output "sample_data.sql",

optional arguments:
- -i --schema_file | for input JSON file 
- -o --output_file | for output .sql file
- -s --script | for custom generation types script file

There is also an option to create an input.json file from a .sql file containing CREATE TABLE statements of the targeted database using converter.py.

### Usage:

```
python converter.py
```
As with the main script, it will by default try to read "test_schema.sql" file as an input, and output "input.json",

optionally you can pass input file and output file as arguments just as before: 

```
python converter.py -i input.sql -o output.json
```

Please note that the output JSON file will be using default generation for all the fields, it is suggested to modify the file.

## Supported settings:
- rows_per_table
- localization
- failsafe_limit

## Supported constraints:
- unique

## Supported generation types as of now:
- firstName
- lastName
- gender
- ssn
- date
- city
- country
- province
- postalCode
- amount
- by data type (integer, string, date, decimal, float, text)

### Custom generation:
To add custom generation methods, write a python script with your logic, then pass it through -s (--script) flag like:
```
python main.py -s script.py
```
To use your custom generation methods, simply specify 
```
"generation": "yourMethodName"
```
in the input JSON file. Remember to write the script in a way that the methods return the value you want in your data.

## Functionalities yet to be added:
- foreign key handling is to be improved
- more generation types
- custom script with seed support
- more primary key generation types

## Known issues:
- Tables are generated one-by-one after being sorted by the number of foreign key columns. If there is a situation where table A references table B, but table B references two more tables - table B will not yet be generated at the time of generating table A, therefore there will be no foreign keys to be added to table A.