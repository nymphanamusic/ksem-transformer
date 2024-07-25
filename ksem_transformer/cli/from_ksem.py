from pathlib import Path
from typing import get_args

import click

from ksem_transformer.cli.core import cli
from ksem_transformer.models.root import Root, SettingsLocation


@cli.command()
@click.option(
    "--input-file", "-i", help="KSEM JSON file to read", required=True, type=Path
)
@click.option(
    "--output-file",
    "-o",
    help=(
        "File to write new YAML config to. If the file already exists, we'll insert "
        "the new data into it"
    ),
    required=True,
    type=Path,
)
@click.option(
    "--product-name",
    "--product",
    help="Name of the product this config describes (e.g. VSL SYNCHRON-ized)",
)
@click.option(
    "--instrument-group-name",
    "--group",
    help="Name of the instrument group this config describes (e.g. Solo Strings)",
)
@click.option(
    "--instrument-name",
    "--instrument",
    help="Name of the instrument this config describes (e.g. 01 Violin 1 PLUS)",
)
@click.option(
    "--store-settings-in",
    type=click.Choice(get_args(SettingsLocation.__value__)),
    help=(
        "When generating the settings field, at what level do you want it stored? "
        "`root` is the highest level, `instrument` is the lowest."
    ),
)
@click.option("--yes", help="Answer yes to any prompts", is_flag=True)
def from_ksem(
    *,
    input_file: Path,
    output_file: Path,
    product_name: str | None,
    instrument_group_name: str | None,
    instrument_name: str | None,
    store_settings_in: SettingsLocation | None,
    yes: bool,
):
    # Load the root configuration from a YAML file and write KSEM config files
    original_data = None
    if output_file.exists():
        if not yes:
            click.confirm(
                (
                    f"{output_file} already exists. Do you want to insert this new "
                    "data into it?"
                ),
                abort=True,
            )
        original_data = Root.from_file(output_file)

    data = Root.from_ksem_config(
        input_file,
        product_name=product_name or "Unknown product",
        instrument_group_name=instrument_group_name or "Unknown instrument group",
        instrument_name=instrument_name or "Unknown instrument",
        store_settings_in=store_settings_in,
    )
    if original_data:
        # Merge new data into the previous data
        data = Root.combine(original_data, data)

    output_file.write_text(data.to_yaml())
