import hashlib


def get_product_id(url: str):
    """
    Generate stable hashed product ID from URL.
    Useful for tracking the same product across days.
    """
    return hashlib.md5(url.encode()).hexdigest()[:12]
