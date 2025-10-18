#!/usr/bin/env python3
import argparse
from player_control.controllers import DelegatingController


def configure_argparser():
    parser = argparse.ArgumentParser(description="Player cli controller")
    parser.add_argument("command", type=str, help="command for the player to execute")
    parser.add_argument(
        "--target",
        type=str,
        dest="target",
        help="target player name to override current",
    )
    parser.add_argument(
        "--debug",
        type=bool,
        dest="debug",
        default=False,
        help="include additional debug info",
    )

    return parser


def execute(controller, command):
    if hasattr(controller, command):
        result = getattr(controller, command)()
        if result:
            print(result)
    else:
        print("unknown command")


def main():
    parser = configure_argparser()
    args = parser.parse_args()
    controller = DelegatingController(debug=args.debug)

    if args.target:
        controller.focus(args.target)
    execute(controller, args.command)


if __name__ == "__main__":
    main()
