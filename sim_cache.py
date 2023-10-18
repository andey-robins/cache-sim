import sys
import helpers.parsing as parsers


def cli_driver():
    config = parsers.arg_parser(sys.argv)
    print(config)


if __name__ == "__main__":
    cli_driver()
