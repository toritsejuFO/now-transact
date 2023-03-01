# now-transact
Now Transact is a fictitious fintech company which provides fast online payments solutions to its users

## Application Features
- User Onboarding and Management
- User Authentication and Authorization
- Account Creation and Management
- Transactions (Deposits and Withdrawals)
- Transactions Search (with pagination)

## Required Software Dependencies
- Python + pip (3.8.x recommended)
- PostgreSQL


## Getting started
- Clone repo
- `cd now-transact`
- `cp .env.sample .env` and  edit appropriately
- `python3 -m pip install --upgrade pip`
- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `python3 -m pip install -r requirements.txt`
- `python3 run.py` or `flask run`

## Running Tests
Without coverage
- `python -m pytest`

With coverage
- `python -m pytest --cov=app`

## Documentation
Swagger is used for documentation, URL can be found on relative path `/api/v1/ui/` of the same host:port the application is running on.

Don't fancy swagger? Got you covered over at Postman

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/5534062-de0fadc5-5110-4adb-992e-1ac771ae7cc7?action=collection%2Ffork&collection-url=entityId%3D5534062-de0fadc5-5110-4adb-992e-1ac771ae7cc7%26entityType%3Dcollection%26workspaceId%3Db35fd6d8-723a-4b38-ac07-0892d6d92e2d#?env%5BNow%20Transact%5D=W3sia2V5IjoiYmFzZVVybCIsInZhbHVlIjoiaHR0cDovLzEyNy4wLjAuMTozMDMwIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImRlZmF1bHQiLCJzZXNzaW9uVmFsdWUiOiJodHRwOi8vMTI3LjAuMC4xOjMwMzAiLCJzZXNzaW9uSW5kZXgiOjB9LHsia2V5IjoieC1hdXRoLXRva2VuIiwidmFsdWUiOiIiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiZGVmYXVsdCIsInNlc3Npb25WYWx1ZSI6IiIsInNlc3Npb25JbmRleCI6MX1d)

PS: There are no route placeholders :)
