# Enigma

Gathers historical or real time price data from a Cryptocurrency database.

# Install
> pip install -r requirements.txt

# Run (Python 3.5+ required)
- Execute gatherer/database/dbmodel.sql file in your PostgreSQL server.
- Configure gatherer/config/config.json file
- Execute the following command
> python start.py `option`

# Usage
> start.py [-h] [-s] [-f [F]] [-rt [RT]] [-p] [-v]


Arguments:
-  -h, --help  show help
-  -s          [SYNC] -s to synchronize missing data.
-  -f [F]      [FULL] -f <epoch> to gather currency history from provided epoch to now.
-  -rt [RT]    [REALTIME] -rt <step> to gather currency values every seconds provided.
-  -v          [VERBOSE] -v be verbose with output.

EPOCH default: 1451692800 (January 1 2016)

STEP default: 60
