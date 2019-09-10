import asyncio
import argparse
import sys
import traceback

import gatherer
import config

from termcolor import colored


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
                        const=config.Configuration.config["epoch_default"])
    parser.add_argument("-rt", nargs='?', help="[REALTIME] -rt <step> to gather currency values every seconds provided.",
                        const=config.Configuration.config["step_default"])
    parser.add_argument("-v", action='store_true', help="[VERBOSE] -v be verbose with output.")

    return parser


async def gather(args):
    g = gatherer.Gatherer(args)
    await g.gather()


async def main(parser):
    if len(sys.argv) == 1:
        p.print_help()
        return

    args = parser.parse_args()

    await gather(args)

    print("Happy predicting!")


if __name__ == "__main__":
    signature()

    config.Configuration.load()
    p = make_parser()

    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(p))
    except KeyboardInterrupt:
        print()
        print("Enigma aborted. Exiting!")
