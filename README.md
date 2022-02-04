# usc-citation-parsing

This repository is where I am storing all code relevant to my research assistance work.

### Overview

This project is going to be a toolset for analyzing and visualizing United States Code citations in various ways.

### How to Use

If you would like to run these scripts, you'll need an auth key from [case.law](https://case.law/) stored in a top-level `secrets.py` file to download the court data. Functionality for choosing which reporter data to use or what report to generate is currently very limited. 

If you have an API key, `python helpers/helpersExcel.py` creates an Excel spreadsheet displaying all USC and USCA citations within the U.S. Reports dataset prefaced by an overview sheet with USC/USCA citation counts by year.

### Examples

Examples of processed spreadsheets are to come.

### TODO:

- Extract citation section numbers and put them into the Excel spreadsheet
- Lots more
