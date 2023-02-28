# now-transact
Now Transact is a fictitious fintech company which provides fast online payments solutions to its users

## Application Features
- User Onboarding and Management
- User Authentication and Authorization
- Account Creation and Management
- Transactions (Deposits and Withdrawals)

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

## Documentation
Swagger is used for documentation, URL can be found on relative path `/api/v1/ui/` of the same host:port the application is running on.
