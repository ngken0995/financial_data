# financial_data

## Summary
This is a tech stock price web application designed to provide users with access to stock and financial data for top technology companies. The application leverages the Financial Modeling Prep API to retrieve comprehensive datasets related to these companies. Utilizing Docker containers ensures version control of the libraries utilized within the application. This enables consistent deployment across various environments while ensuring compatibility with the specified library versions.

## Setup 

### Finanical API
Go to [finanical model prep](https://site.financialmodelingprep.com/developer/docs) and sign up for a API.

### env file 
create a `.env` file
add `API_KEY=<Replace with API KEY` in the file.

### install Docker
[docker install guide](https://docs.docker.com/desktop/) (Recommend to use mac)

## Run application

1. open docker destop
2. run `docker build -t my-app .`
3. run `docker run --env-file .env -p 8050:8050 my-app`
4. http://0.0.0.0:8050/ is the default webpage for the application


