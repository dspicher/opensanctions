import click
import logging
from followthemoney.cli.util import write_object

from opensanctions.core import Target, Context, setup


@click.group(help="OpenSanctions ETL toolkit")
@click.option("-v", "--verbose", is_flag=True, default=False)
@click.option("-q", "--quiet", is_flag=True, default=False)
def cli(verbose=False, quiet=False):
    level = logging.INFO
    if quiet:
        level = logging.ERROR
    if verbose:
        level = logging.DEBUG
    setup(log_level=level)


@cli.command("dump", help="Export the entities from a target")
@click.argument("target", default=Target.ALL, type=click.Choice(Target.names()))
@click.option("-o", "--outfile", type=click.File("w"), default="-")
def dump_target(target, outfile):
    target = Target.get(target)
    for dataset in target.datasets:
        # TODO: consolidate the data
        for entity in dataset.store:
            write_object(outfile, entity)


@cli.command("crawl", help="Crawl entities into the given target")
@click.argument("target", default=Target.ALL, type=click.Choice(Target.names()))
def crawl(target):
    target = Target.get(target)
    for dataset in target.datasets:
        Context(dataset).crawl()
