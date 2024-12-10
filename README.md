# Inteligent-Data-Generator
## Usage:
```
python main.py
```
there is only a need for an "input.json" file with a structure as provided (subject to some changes)
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
- setting block
- foreign key handling
- more generation types
- regex support
- custom script support

7.11 - added semi-working settings (rows_per_table, and localization), foreign keys can be taken randomly from a pool of already generated primary keys (currently those need to be specified in order for it to work)