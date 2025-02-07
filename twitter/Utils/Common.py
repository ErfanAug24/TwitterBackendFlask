import re
import unicodedata


def create_slug(title: str):
    """
    create slug based on tweet titles
    """

    title = unicodedata.normalize("NFKD", title)
    title = re.sub(r"[^\w\s-]", "", title).strip().lower()
    slug = re.sub(r"[-\s]+", "-", title)
    return slug
