# odentify
Query OMDB and format results

## Simple Examples
```bash
odentify search 'Mad Max Fury Road'
# List of movie matching 'Mad Max fury Road' ...

odentify --format '{Title}({Year})' fetch 'Interstellar'
# Interstellar(2014)
```

## Arguments
Option | Description | Example
-------|-------------|--------
--type | Output type requested (default to list) | list,csv,format
--format | Format to output the movie (implies --type format) | {Title} ({Year})
--separator | Delimit fields with this string( implies --type csv) | ;

**How to format movie name?**

Wrap the key you want displayed with {}. 


**How to find available keys?**

Fetch the movie with --type list
