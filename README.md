
## Table of Contents
- [Project Overview](#project_overview)
- [Prerequisites](#Prerequisites)
- [Usage](#Usage)
- [Structure](#Structure)
- [Contributors](#Contributors)

# Project Overview
This is a project done as a part of Data Science and AI course at Becode in 2024.
To so the project we build a dataset gathering information about at least 10.000 properties all over Belgium. 
1. Querying an API to retrieve a list of properties.
2. Scraping Immoweb to gather propertoes' data.
3. Saving the data in CSV format for further processing.

# Prerequisites
Make sure you have the following:

1. Python 3.x installed.
2. pip for managing Python packages.
3. To work with get_property_data() you need to get CSV file of URLs from fetch_links().


# Usage

This script will:
1. Retrieve a list of properties from the API.
2. Extract poperties' information from immoweb for each property.
3. Save the output in a CSV file which could be used for related analysis.


# Structure
The project has the following core components:

1. fetch_links(): Uses Requests and BeautifulSoup to get a list of properties' URLs.
2. get_property_data(): Uses BeautifulSoup to scrape the property's data and saves it to a CSV file, using the list of URLS.


# Contributors 
This proects is done by:
1. [Tumi](https://github.com/2moonyo)
2. [karthika](https://github.com/karthika-elimireddy)
3. [Fatemeh](https://github.com/Fatemeh992)


