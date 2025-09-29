# PAT (Portfolio Analysis Tool)
## Overview
PAT is a web application that allows user to input their holdings. The application will orchestrate the back-end to fetch real-time market data, perform calculations and display portfolio metrics - risk, sector allocations, implied growth, sentiment analysis. The user is then given the tools to compare their current portfolios to potential ones. Users are able to securely create profiles, save, and update their portfolio holdings.  
## Quick Set Up
We need to install the necessary python dependancies, in main/  
```bash
python3.12 -m venv venv  
source venv/bin/activate  
pip3 install -r requirements.txt
```
## Code-Base Structure  

This is for new contributors and for those who are curious to read. This project contains many directories, and files. A quick description is given below  
```
PAT/
├──documentation/ # Project related documentation
│ ├──database # Database related docs
│ │ ├──ER_Diagram.md # The ER diagram for the project
│ │ └──possible_data_source.md # A list of data vendors with pros and cons
│ ├──project_management
│ │ ├──PAT_Design_Document.md # The main document for PAT
│ │ └──PAT_Project_Timeline.md # TimeLine of the project
├──server/ # All BackEnd services
│ ├──src/ # Settings and stuff
│ │ ├──asgi.py
│ │ ├──settings.py
│ │ ├──urls.py
│ │ └──wsgi.py
│ ├──users/
│ ├──utils/
│ └──manage.py # For initializing the backend
│
│
└──notebooks/ # All Development Notebooks for Models

```
We are still yet to add a front-end component. If you are a contributor and wish to create a new feature for PAT, please go into server directory and type  
```bash
python3 manage.py startapp NEW_APP_NAME
```
## Contributors
Add here later
