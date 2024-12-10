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