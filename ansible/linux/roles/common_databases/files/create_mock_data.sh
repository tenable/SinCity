#!/bin/bash

# Create mock data for mongo
echo "Creating mock data for mongoose..."

docker-compose exec mongo sh -c \
    "mongoimport --db=admin --collection=user \
    --type=csv --headerline /shared/mock_data.csv mongodb://root:1sS39fMax@mongo:27017"

echo "Creating mock data for mysql..."

docker-compose exec mysql sh -c \
    'mysql --password="aA{5~HF" -e "CREATE DATABASE mydb"'

# Now create the data for MySQL
csvsql --tables users --insert \
    --db mysql+mysqlconnector://root:aA%7B5~HF@localhost:3306/mydb shared/mock_data.csv

echo "Creating mock data for postgres.."

docker-compose exec postgres sh -c \
    'createdb --username=admin mydb'

# Now create the data for Postgress
csvsql --tables users --insert \
    --db postgresql+pg8000://admin:oM889%21%2A@localhost/mydb shared/mock_data.csv

# Now create the data for MSSQL
csvsql --tables users --insert \
    --db mssql+pymssql://sa:xdv~JsG9=@localhost shared/mock_data.csv