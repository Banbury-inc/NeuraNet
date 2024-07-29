import click
from commands import file, info

@click.group()
def cli():
    """NeuraNet CLI Tool"""
    pass

cli.add_command(file.print)
cli.add_command(info.version)

if __name__ == '__main__':
    cli()
