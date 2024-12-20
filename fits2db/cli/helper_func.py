import click
from .utils import validate_output_filename
from ..core import Fits2db, get_all_fits
from ..config import generate_config


@click.command()
@click.argument("config_path", default=".", type=click.Path(exists=True))
@click.option(
    "-f",
    "--folder",
    default=False,
    is_flag=True,
    help="Show all fits files in given folder",
)
def files(folder, config_path):
    """Prints all files from given config.yaml file"""
    try:
        if folder:
            files = get_all_fits([config_path])

        else:
            fits = Fits2db(config_path)
            files = fits.get_file_names()
        for f in files:
            click.echo(f)
        click.echo(f"Total of {len(files)} files")
    except Exception as err:
        click.echo(err)


@click.command()
@click.argument("config_path", default=".", type=click.Path(exists=True))
@click.option(
    "-m",
    "--matrix",
    default=False,
    is_flag=True,
    help="Show all tables and files as matrix",
)
@click.option(
    "--csv", default=False, is_flag=True, help="Save the output as csv"
)
@click.option(
    "--excel", default=False, is_flag=True, help="Save the output as excel"
)
@click.option(
    "--filename",
    default="output.csv",
    callback=validate_output_filename,
    help="The filename for the output (required if --csv or --excel is specified).",
)
def tables(config_path, matrix, csv, excel, filename):
    """Prints all table names from all fits files from given config.yaml file"""
    fits = Fits2db(config_path)
    format = None
    if csv:
        format = "csv"
    elif excel:
        format = "excel"

    if matrix:
        m = fits.create_table_matrix(
            output_format=format, output_file=filename
        )
        if format is None:
            click.echo(m.to_string())
    else:
        names, _ = fits.get_table_names()
        for f in names:
            click.echo(f)


@click.command()
@click.argument("config_path", default=".", type=click.Path(exists=True))
@click.option(
    "-r",
    "--reset",
    default=True,
    is_flag=True,
    help="Rebuild entire database and drops old tables. If false it will error if there is already a able with the same name",
)
def build(config_path, reset):
    """Upsert all tables defnied in config.yml to databse"""
    fits = Fits2db(config_path)
    fits.build(reset)


@click.command()
@click.argument("config_path", default=".", type=click.Path(exists=True))
@click.option(
    "-f",
    "--force",
    default=False,
    is_flag=True,
    help="Force overwrite of files in config. Accepts skipping invalid files",
)
def update(config_path, force):
    """Upsert all tables defnied in config.yml to database"""
    fits = Fits2db(config_path)
    fits.update_db(force=force)


@click.command()
@click.argument("config_path", default=".", type=click.Path(exists=True))
@click.option(
    "-f",
    "--force",
    default=False,
    is_flag=True,
    help="Force overwrite of db. Accepts skipping invalid files",
)
def upsert(config_path, force):
    """Upsert all tables defnied in config.yml to databse"""
    fits = Fits2db(config_path)
    fits.upsert_to_db()


@click.command()
@click.argument("config_path", default=".", type=click.Path(exists=False))
def init(config_path):
    """Creates an example config file for you to change

    \b
    CONFIG_PATH     This argument can be a path to a folder or file.
                    If you pass a file make sure to have the ending
                    ".yml" or ".yaml" to get an valid config file

    """
    if generate_config(config_path):
        click.echo("File generated sucessfull")
    else:
        click.echo(
            click.style("Failed to generate file", blink=True, bold=True)
        )
