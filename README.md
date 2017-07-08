# Enigma

Gathers historical or real time price data from a Cryptocurrency database.

# Install
> pip install -r requirements.txt

# Run (Python 3.5+ required)
- Execute project/database/dbmodel.sql file in your PostgreSQL server.
- Configure project/config/config.json file
- Execute the following command
> python project/start.py `option`

# Usage
- [FULL] `-f EPOCH` to gather currency history from provided epoch to now.
- [REALTIME] `-rt STEP` to gather currency values every seconds provided.
- [SYNC] `-s` to synchronize missing data.
- [REALTIME]+[FULL] `-rtf STEP EPOCH` gathers history since epoch and then starts real time tracking.
- [REALTIME]+[SYNC] `-rts STEP` synchronizes then starts real time tracking.
- EPOCH default: 1451692800 (January 1 2016)
- STEP default: 60
