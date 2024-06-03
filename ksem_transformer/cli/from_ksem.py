from pathlib import Path

import click

from ksem_transformer.cli.core import cli
from ksem_transformer.models.root import Root


@cli.command()
@click.option(
    "--input-file", "-i", help="KSEM JSON file to read", required=True, type=Path
)
@click.option(
    "--output-file",
    "-o",
    help="File to write new YAML config to",
    required=True,
    type=Path,
)
@click.option(
    "--product-name",
    help="Name of the product this config describes (e.g. VSL SYNCHRON-ized)",
)
@click.option(
    "--instrument-group-name",
    "--group-name",
    help="Name of the instrument group this config describes (e.g. Solo Strings)",
)
@click.option(
    "--instrument-name",
    help="Name of the instrument this config describes (e.g. 01 Violin 1 PLUS)",
)
def from_ksem(
    input_file: Path,
    output_file: Path,
    product_name: str | None,
    instrument_group_name: str | None,
    instrument_name: str | None,
):
    # Load the root configuration from a YAML file and write KSEM config files
    if output_file.exists():
        click.confirm(f"{output_file} already exists. Overwrite?", abort=True)
    loaded = Root.from_ksem_config(
        input_file,
        product_name=product_name or "Unknown product",
        instrument_group_name=instrument_group_name or "Unknown instrument group",
        instrument_name=instrument_name or "Unknown instrument",
    )
    output_file.write_text(loaded.to_yaml())
