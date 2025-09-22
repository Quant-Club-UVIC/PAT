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
Next we need to set up our docker environment. If you are unfamiliar with docker check out (https://docs.sevenbridges.com/docs/install-docker-on-linux).
```bash
docker compose up --build
```
## Contributors
Add here later
