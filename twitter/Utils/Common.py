import re
import unicodedata
from enum import Enum


def create_slug(title: str):
    """
    create slug based on tweet titles
    """

    title = unicodedata.normalize("NFKD", title)
    title = re.sub(r"[^\w\s-]", "", title).strip().lower()
    slug = re.sub(r"[-\s]+", "-", title)
    return slug


class Rating(Enum):
    VERYBAD = 1
    BAD = 2
    MEDIUM = 3
    GOOD = 4
    VERYGOOD = 5
