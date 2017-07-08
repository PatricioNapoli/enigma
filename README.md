# Enigma

Gathers historical or real time price data from a Cryptocurrency database.

# Install
> pip install -r requirements.txt

# Run (Python 3.5+ required)
- Execute project/database/dbmodel.sql file in your PostgreSQL server.
- Configure project/config/config.json file
- Execute the following command
> python start.py `option`

# Usage
> start.py [-h] [-s] [-f [F]] [-rt [RT]]

Arguments:
-  -h, --help  show this help message and exit
-  -s          [SYNC] -s to synchronize missing data.
-  -f [F]      [FULL] -f <epoch> to gather currency history from provided epoch
              to now.
-  -rt [RT]    [REALTIME] -rt <step> to gather currency values every seconds
              provided.

- EPOCH default: 1451692800 (January 1 2016)
- STEP default: 60
