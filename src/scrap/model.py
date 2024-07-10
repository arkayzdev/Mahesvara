from dataclasses import dataclass

@dataclass
class Image:
    title: str          # Image's title
    access_url: str     # URL that contains the image and all his content
    src: str            # HD quality image link
    website: str        # Website where was the image scraped
    author: str         # Person that posted the image
    alt: str            # Image's description
    format: str         # Image's format (jpg, png, gif ...)
    imported_date: str  # Date when the image was scraped