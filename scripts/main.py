import scanner.errors
import scanner.transactions
import scanner.subcriptions
import scanner.cli


def main():
    parser = scanner.cli.make_parser()
    args = parser.parse_args()
    try:
        output = scanner.cli.find_subscriptions(args.csv, args.format)
    except scanner.errors.ScannerException as e:
        print(e)
        exit(1)

    for subscription in output:
        print(subscription)


if __name__ == '__main__':
    main()
