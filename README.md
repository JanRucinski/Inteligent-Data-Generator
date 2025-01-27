# Inteligent-Data-Generator
## Usage:
```
python main.py
```
optionally you can pass input file and output file as arguments 

```
python main.py -i input.json -o output.json
```

## Supported settings:
- rows_per_table
- localization
- failsafe_limit

there is only a need for an "input.json" file with a structure as provided

Additionally, you can now use the `converter.py` script to convert a `.sql` file containing database schema with `CREATE` statements into a compatible `input.json` file.

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
## Functionalities yet to be added:
- foreign key handling is to be improved
- more generation types
- regex support for generation
- custom script support

