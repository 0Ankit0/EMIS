"""Main CLI entry point for EMIS."""
import click

from .db_commands import db
from .user_commands import user
from .task_commands import tasks


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """
    EMIS - Educational Management Information System CLI
    
    Management commands for the EMIS application.
    """
    pass


# Register command groups
cli.add_command(db)
cli.add_command(user)
cli.add_command(tasks)


if __name__ == "__main__":
    cli()
