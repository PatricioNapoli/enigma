import sys
from gatherer import gatherers

CURRENCIES = ["BTC", "ETH", "LTC"]
PHYSICAL_CURRENCY = "USD"


def gather():
    if sys.argv[1] == "-f":
        if len(sys.argv) == 3:
            gatherer = gatherers.FullGatherer(CURRENCIES, PHYSICAL_CURRENCY, sys.argv[2])
            gatherer.gather()
        else:
            print("Using -f but no epoch was provided.")
    elif sys.argv[1] == "-rt":
        if len(sys.argv) == 3:
            gatherer = gatherers.RealtimeGatherer(CURRENCIES, PHYSICAL_CURRENCY, sys.argv[2])
            gatherer.gather()
        else:
            print("Using -rt but no step was provided.")
    else:
        usage()


def usage():
    print("Usage:")
    print("[FULL] -f <epoch> to gather 24 hourly currency values up to that time.")
    print("[REALTIME] -rt <seconds> to gather currency values every seconds provided.")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        gather()
    else:
        usage()

