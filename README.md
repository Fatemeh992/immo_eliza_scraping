
## Table of Contents
- [Project Overview](#project_overview)
- [Prerequisites](#Prerequisites)
- [Usage](#Usage)
- [Structure](#Structure)
- [Contributors](#Contributors)

# Project Overview
This is a project done as a part of Data Science and AI course at Becode in 2024.
To do the project we build a dataset gathering information about at least 10.000 properties all over Belgium. 
1. Web scraping the website Immoweb to gather properties data.
2. Saving the data in CSV format for further processing.

# Prerequisites
Make sure you have the following:

1. Python 3.x installed.
2. pip for managing Python packages.
3. for the required libraries please refer to 
    requirements.txt --- install using the command pip install -r requirements.txt


# Usage

This script will:
1. Retrieve a list of properties from the HTML page source of the website.
2. Extract poperties' information from immoweb for each property.
3. Save the output in a CSV file which could be used for related analysis.


# Structure
The project has the following core components:

1. utils: is a directory contains data files
    property_links.csv
    all_properties_output.csv
    
2. main.py --- To execute the project using python main.py

    fetch_links(): Uses Requests and BeautifulSoup to get a list of properties' URLs.
    get_property_data(): Uses BeautifulSoup to scrape the property's data and saves it to a CSV file, using the list of URLS.
    clean_save_dataset(): Uses Pandas to clean the dataset and saves it to another csv file.

3. requirements.txt : contains list of dependencies for the project.

# Contributors 
This proects is done by:
1. [Tumi](https://github.com/2moonyo)
2. [karthika](https://github.com/karthika-elimireddy)
3. [Fatemeh](https://github.com/Fatemeh992)


