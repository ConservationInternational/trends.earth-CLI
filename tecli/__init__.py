"""The GEF CLI Module."""

import logging

import fire

from tecli.commands import Commands

logging.basicConfig(
    level="DEBUG",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y%m%d-%H:%M%p",
)


def main():
    """Create the CLI"""
    fire.Fire(Commands)
