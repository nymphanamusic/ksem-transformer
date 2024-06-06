from pathlib import Path

import click

from ksem_transformer.cli.core import cli
from ksem_transformer.models.root import Root


@cli.command()
@click.option(
    "--input-file", "-i", help="YAML config file to read", required=True, type=Path
)
@click.option(
    "--output-dir",
    "-o",
    help="Directory to write new KSEM JSON files to. Multiple files may be written.",
    required=True,
    type=Path,
)
def to_ksem(input_file: Path, output_dir: Path):
    # Load the root configuration from a YAML file and write KSEM config files
    loaded = Root.from_file(input_file)
    loaded.write_ksem_config_files(output_dir)
