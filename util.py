from typing import Dict
import click
from models import Coordinate

UNIT_ABBREVIATIONS_TO_METERS: Dict[str, float] = {
    "m": 1,
    "km": 1000,
    "mi": 1609.34,
    "ft": 0.3048,
    "meters": 1,
    "kilometers": 1000,
    "miles": 1609.34,
    "feet": 0.3048,
}

def parse_coordinates(
        ctx: click.Context,
        param: click.Parameter,
        value: str,
) -> Coordinate:
    """
    Docstring for parse_coordinates

    
    :param ctx: Description
    :type ctx: click.Context
    :param param: Description
    :type param: click.Parameter
    :param value: Description
    :type value: click.Argument
    :return: Description
    :rtype: Coordinate

    Expects a value like 40.706981526535955, -74.01094373134949 ->
    """
    try:
        values = value.split(",")
        # Now we need to trim the values
        x, y = float(values[0].strip()), float(values[1].strip())

        return Coordinate(
            x=x,
            y=y
        )
    except Exception:
        raise click.BadArgumentUsage(
            "Bad usage! Coordinates should be in the format 'x,y' where x and y are numbers."
        )




def parse_density(
        ctx: click.Context,
        param: click.Parameter,
        value: str,
) -> float:
    for unit in sorted(UNIT_ABBREVIATIONS_TO_METERS.keys(), key=len, reverse=True):
        if value.endswith(unit):
            number_part = value[:-len(unit)]
            unit_part = value[len(number_part):]
            return float(number_part) * UNIT_ABBREVIATIONS_TO_METERS[unit_part]



    raise click.BadArgumentUsage(
        "Bad usage! Density should end with a unit, e.g. 1km, 500m, 0.5mi, etc."
    )
