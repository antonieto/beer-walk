# pyre-strict
# TODO: Import click
import click
from util import parse_coordinates, parse_density


NY_STOCK_EXCHANGE = "40.706981526535955, -74.01094373134949"
NY_MET_MUSEUM = "40.77902603833201, -73.9623977615683"

@click.command()
@click.option(
    "--start",
    default=NY_STOCK_EXCHANGE,
    help="Where does your beer walk start?",
    callback=parse_coordinates
)
@click.option(
    "--end",
    default=NY_MET_MUSEUM,
    help="Duh...",
    callback=parse_coordinates
)
@click.option(
    "--density",
    default="1km",
    help="How often are you going to drink beer? I.e. how much distance between each beer?",
    callback=parse_density
)
@click.pass_context
def main(
    ctx: click.Context,
    # This should really be 
    start: str,
    end: str,
    # This is in meters
    density: float,
) -> None:
    """
    This is a beer walk script I'm building with the google maps API.

    This is a python click CLI. The usage is `python3 beer-walk.py --start "<coordinates>" --end "<coordinates>" --density "1km"`.

    The idea is, you set the start coordinates, in "x,y" format and the same for the end coordinates, and the CLI will output a list of places to stop for a beer at, stopping at one of the places.


    """
    click.echo("Hi! This is a work in progress hold on")
    click.echo(f'Start: {start}')
    click.echo(f'End: {end}')
    click.echo(f'Density: {density} meters')

    should_start_at_bar = click.confirm("Do you want to start by drinking a beer?", default=True)

    # Algorithm:
    # 1. Get the absolute closest bar to the start coordinate.
    # 2. Initialize search graph, with the first node being the closest bar to the start coordinate.
    # 3. List the nearest bars to current node, using Google Maps API, and add them to the search graph, with the distance from current node as the edge weight.




if __name__ == "__main__":
    main()