README
===========================
This is W21 SI507 Final project. The purpose of this project is to get information about restaurants in different cities or state based on category or restaurants' name in the US. Yelp has web API and restaurant related data can be retrieved from API, while the table of cities can be fetched via web scraping.

To run the program, users need to download the **Final_proj.db**, **FinalprojHelp.txt** and **final_project.py** and put them in a same folder. The main program file to run is **final_project.py**.

****
	
|Author|Qiyan Liu|
|---|---


****
**Data Sources**
------
1. Yelp (Yelp Fusion), which is the data source of table “Restaurants”.

2. The 200 Largest Cities in the United States by Population 2021(https://worldpopulationreview.com/us-cities) from world population review website, which is the data source of table “Cities”.

**Database Preparation**
------
There are two python files for this project. One is for the database preparation and the other one is for interactive prompt. 

The database_prep python file uses web scraping and API to fetch the restaurants related data in 200 cities, 
then a database is created and contains two tables, one is "Cities" and the other one is "Restaurants".


**API Requirement**
------
This project requires YELP API to fetch restaurants related data. 

Users could apply API key from:https://www.yelp.com/fusion. I store API key in the secrets.py and import 
the secrets.py in the database_prep.py to create the database for this project.


**Command Instructions**
------
There are two types of commands users could enter to find the restaurants information and data visualization.

1. Find ***[category|name|none]*** restaurants in ***[state|city|none]*** ***[price|rating]*** ***[top|bottom]*** ***[integer]***

Return a table contains parameters specified in the command
    
    e.g: Find [category=Asian Fusion] restaurants in[city=New York] rating top 5   

2. ***[category|name|none]*** restaurants in ***[state|city|none]*** ***[price|rating]*** distribution

Return a pie chart contains parameters specified in the command

    e.g: [category=chinese] restaurants in[state=NY] rating distribution   


**Python Package Requirement**
------
In the final_project python file:
```Python
import sqlite3
import pandas as pd
import re
from prettytable import PrettyTable
import plotly
import plotly.express as px  #Python
```

In the database_prep python file:
```python
import requests
import json
import numpy as np
import sqlite3
from itertools import product
import pandas as pd
import secrets
from sqlalchemy import create_engine #Python
```

