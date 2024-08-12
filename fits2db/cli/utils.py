import click
from typing import Optional
from ..log import configure_logger, LOG_LEVELS


def validate_output_filename(
    ctx: click.Context, param: Optional[click.Parameter], value: str
) -> str:
    """
    Validate the output filename based on the selected file format options.

    Args:
        ctx (click.Context): The Click context object.
        param (Optional[click.Parameter]): The Click parameter object (unused).
        value (str): The output filename provided by the user.

    Raises:
        click.BadParameter: If the filename does not meet the required conditions based on selected options.

    Returns:
        str: The validated output filename.
    """
    if ctx.params.get("csv") and not value.endswith(".csv"):
        raise click.BadParameter("CSV filename must have a .csv extension.")
    if ctx.params.get("excel") and not value.endswith(".xlsx"):
        raise click.BadParameter("Excel filename must have a .xlsx extension.")
    if ctx.params.get("csv") or ctx.params.get("excel"):
        if not value:
            raise click.BadParameter(
                "Output filename is required when --csv or --excel is specified."
            )
    return value


def set_verbosity(
    ctx: click.Context, param: Optional[click.Parameter], value: int
) -> int:
    """
    Set verbosity of logs.

    Args:
        ctx (click.Context): The Click context.
        param (Optional[click.Parameter]): The Click parameter (unused).
        value (int): The integer value of verbosity (number of `-v` flags).

    Returns:
        int: The verbosity value that was set.
    """
    levels = list(LOG_LEVELS.keys())
    level = levels[min(len(levels) - 1, value)]
    ctx.ensure_object(dict)
    ctx.obj["logger"] = configure_logger(level)
    return value
