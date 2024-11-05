import unicodedata
from django.utils.text import slugify






def arabic_slugify(text):
    import re
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    return re.sub(r'[-\s]+', '-', text)
