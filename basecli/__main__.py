import sys
import click


@click.group()
@click.version_option("0.0.2")
def main():
    """CLI for detabase"""
    pass


if __name__ == '__main__':
    args = sys.argv
    if "--help" in args or len(args) == 1:
        print("basecli")
    main()