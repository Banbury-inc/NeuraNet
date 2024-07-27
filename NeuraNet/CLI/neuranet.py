import click
from commands import file

@click.group()
def cli():
    """NeuraNet CLI Tool"""
    pass

cli.add_command(file.print)

if __name__ == '__main__':
    cli()
