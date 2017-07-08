import asyncio
import sys

from config.config import Configuration
from termcolor import colored

from gatherer import gatherers


def get_since():
    if len(sys.argv) == 3:
        since = sys.argv[2]
    else:
        print("No epoch provided, using default.")
        since = Configuration.config["epoch_default"]
    return since


def get_step():
    if len(sys.argv) == 3:
        step = sys.argv[2]
    else:
        print("No step provided, using default.")
        step = Configuration.config["step_default"]
    return step


async def gather():
    Configuration.load()

    if sys.argv[1] == "-f":
        gatherer = gatherers.FullGatherer(get_since(), False, 0)
        await gatherer.gather()
    elif sys.argv[1] == "-rt":
        gatherer = gatherers.RealtimeGatherer(get_step())
        await gatherer.gather()
    elif sys.argv[1] == "-rtf":
        gatherer = gatherers.FullGatherer(get_since(), True, get_step())
        await gatherer.gather()
    elif sys.argv[1] == "-s":
        gatherer = gatherers.SyncGatherer(False, 0)
        await gatherer.gather()
    elif sys.argv[1] == "-rts":
        gatherer = gatherers.SyncGatherer(True, get_step())
        await gatherer.gather()
    else:
        usage()


def usage():
    print("Usage:")
    print("[FULL] -f <epoch> to gather currency history from provided epoch to now.")
    print("[REALTIME] -rt <step> to gather currency values every seconds provided.")
    print("[SYNC] -s to synchronize missing data.")
    print("[REALTIME]+[FULL] -rtf <step> <epoch> gathers history since epoch and then starts realtime tracking.")
    print("[REALTIME]+[SYNC] -rts <step> synchronizes then starts realtime tracking.")
    print("<epoch> default: 1451692800 (January 1 2016)")
    print("<step> default: 60")


def print_signature():
    print()
    print(colored("?)^!(#^!@#&<!>#^<~^#$!$}&|*(_+#)!$%_^!&?", "red"))
    print(colored("   ___  , __   `   ___. , _ , _     ___ ", "blue"))
    print(colored(" .'   ` |'  `. | .'   ` |' `|' `.  /   `", "blue"))
    print(colored(" |----' |    | | |    | |   |   | |    |", "blue"))
    print(colored(" `.___, /    | /  `---| /   '   / `.__/|", "blue"))
    print(colored("                  \___/                 ", "blue"))
    print(colored("?~#^?{}:$&~@#%<@~#&>~#<%_@#)^$&~$^&}{&!?", "red"))
    print()


@asyncio.coroutine
def main():
    try:
        print_signature()

        if len(sys.argv) > 1:
            yield from gather()

            print("Done. Happy predicting!")
        else:
            usage()
    except KeyboardInterrupt:
        print()
        print("Enigma aborted. Exiting!")
    except FileNotFoundError:
        print()
        print("Configuration file not found!")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
