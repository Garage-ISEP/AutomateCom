import os
from api import *
import click
import logging

from api import api_generic

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@click.command()
@click.option('--arg', prompt='ARG', type=int, help='Enter the ARG')
def command_name():
    """Description of the command"""
    # Logic for the command
    logger.info('Greet command invoked')
    click.echo('This is an additional command.')


@click.command()
@click.option('--generate', prompt='Title', type=str, help='Enter the title to generate the text')
def generate_text(title):
    """
    Use the generate_text() from the
    api/api_generic script.
    """
    # Logic for the command
    logger.info('Generate command invoked')
    api_generic.generate_text(title)
    click.echo('This is an additional command.')


@click.group()
def cli():
    """A collection of CLI commands"""
    pass


cli.add_command(generate_text)

if __name__ == '__main__':
    cli()
