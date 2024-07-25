import click
from ..core import Fits2db, get_all_fits


def validate_output_filename(ctx, param, value):
    if ctx.params.get("csv") and not value.endswith(".csv"):
        raise click.BadParameter(
            "CSV filename must have a .csv extension."
        )
    if ctx.params.get("excel") and not value.endswith(".xlsx"):
        raise click.BadParameter(
            "Excel filename must have a .xlsx extension."
        )
    if ctx.params.get("csv") or ctx.params.get("excel"):
        if not value:
            raise click.BadParameter(
                "Output filename is required when --csv or --excel is specified."
            )
    return value


@click.group()
def cli():
    """Fits2DB CLI"""
    pass


@click.command()
@click.argument("config_path", type=click.Path(exists=True))
@click.option(
    "-f",
    "--folder",
    default=False,
    is_flag=True,
    help="Show all fits files in given folder",
)
def files(folder, config_path):
    """Prints all files from given config.yaml file"""
    if folder:
        files = get_all_fits([config_path])
    else:
        fits = Fits2db(config_path)
        files = fits.get_files()
    for f in files:
        click.echo(f)


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


cli.add_command(files)
cli.add_command(tables)

if __name__ == "__main__":
    cli()
