
import click

@click.group()
def inference():
    """Commands to manage distributed inference tasks"""
    pass

@inference.command()
@click.option('--model', required=True, help='Path to the model')
@click.option('--data', required=True, help='Path to the data')
def start(model, data):
    """Start a distributed inference task"""
    click.echo(f'Starting inference with model {model} and data {data}...')


