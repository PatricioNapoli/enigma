import argparse

import sys
from termcolor import colored
from gatherer.gatherer import *


def signature():
    print()
    print(colored("?)^!(#^!@#&<!>#^<~^#$!$}&|*(_+#)!$%_^!&?", "red"))
    print(colored("   ___  , __   `   ___. , _ , _     ___ ", "blue"))
    print(colored(" .'   ` |'  `. | .'   ` |' `|' `.  /   `", "blue"))
    print(colored(" |----' |    | | |    | |   |   | |    |", "blue"))
    print(colored(" `.___, /    | /  `---| /   '   / `.__/|", "blue"))
    print(colored("                  \___/                 ", "blue"))
    print(colored("?~#^?{}:$&~@#%<@~#&>~#<%_@#)^$&~$^&}{&!?", "red"))
    print()


def make_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", action='store_true', help="[SYNC] -s to synchronize missing data.")
    parser.add_argument("-f", nargs='?', help="[FULL] -f <epoch> to gather currency history from provided epoch to now.",
                        const=Configuration.config["epoch_default"])
    parser.add_argument("-rt", nargs='?', help="[REALTIME] -rt <step> to gather currency values every seconds provided.",
                        const=Configuration.config["step_default"])

    return parser


async def gather(args):
    gatherer = Gatherer(args)
    await gatherer.gather()


@asyncio.coroutine
def main(parser):
    if len(sys.argv) == 1:
        p.print_help()
        return

    args = parser.parse_args()

    yield from gather(args)

    print("Happy predicting!")


if __name__ == "__main__":
    signature()

    Configuration.load()
    p = make_parser()

    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(p))
    except KeyboardInterrupt:
        print()
        print("Enigma aborted. Exiting!")
    except FileNotFoundError:
        print()
        print("Configuration file not found!")
