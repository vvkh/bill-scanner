import argparse


import scanner.transactions
import scanner.subcriptions
import scanner.cli


def main():
    parser = scanner.cli.make_parser()
    args = parser.parse_args()
    output = scanner.cli.find_subscriptions(args.csv)
    for subscription in output:
        print(subscription)


if __name__ == '__main__':
    main()
