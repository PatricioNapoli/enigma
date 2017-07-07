# Enigma

Stands for Enveloping of Information and Gateway Managing

# Install
> pip install -r requirements.txt

# Run (Python 3.5+ required)
> python -m gatherer

# Usage
- [FULL] -f EPOCH to gather currency history from provided epoch to now.
- [REALTIME] -rt STEP to gather currency values every seconds provided.
- [SYNC] -s to synchronize missing data.
- [REALTIME]+[FULL] -rtf STEP EPOCH gathers history since epoch and then starts realtime tracking.
- [REALTIME]+[SYNC] -rts STEP synchronizes then starts realtime tracking.
- epoch default: 1451692800 (January 1 2016)
- STEP default: 60