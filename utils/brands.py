import re


class BrandsDetector:
    def __init__(self, brands_regex):
        self.regex = brands_regex

    def find(self, text):
        for name, pattern in self.regex.items():
            if re.search(pattern, text.lower()):
                return name
        return '-'
