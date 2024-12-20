import click
from .helper_func import tables, files, build, init, update
from .utils import set_verbosity


@click.version_option("0.1.0", "--version")
@click.group(
    help="""
    Fits2DB CLI can be used to extract data from fits files and load them into a Database.
    For this, the CLI has various helper functions to inspect the content of fits files and run some
    checks to see if the expected content is available.

    ??? tips
        - Check files before loading them into the database to have fewer worries once loaded.
        - You can also set a fail flag to fail the ingestion if some columns or data points are missing.
    
    ???+ example "Example Usage"

        ```cmd
        fits2db upsert path/to/your/config.yaml
        ```
    """
)
@click.option(
    "-v",
    "--verbosity",
    count=True,
    callback=set_verbosity,
    expose_value=False,
    is_eager=True,
    help="Increase verbosity of the log output. Use -v for WARNING, -vv for INFO, -vvv for DEBUG.",
)
@click.pass_context
def cli(ctx):
    ctx.obj["logger"].info("Logger configured with verbosity level.")


cli.add_command(files)
cli.add_command(tables)
cli.add_command(build)
cli.add_command(init)
cli.add_command(update)

if __name__ == "__main__":
    cli()
