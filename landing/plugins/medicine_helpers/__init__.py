import logging
from pelican import signals
from . import medicine_helpers

# METADATA

__title__ = "medicine_helpers"
__description__ = "Jinja Helpers for Medicine for Ukraine website"
__author__ = "David Maxwell"

logger = logging.getLogger(__name__)


def add_all_filters(pelican):
    """Add (register) all filters to Pelican."""
    pelican.env.filters.update({"link": medicine_helpers.link})
    pelican.env.filters.update({"switch_language_link": medicine_helpers.switch_language_link})


def register():
    """Plugin registration."""
    signals.generator_init.connect(add_all_filters)
