import re


class BrandsDetector:
    def __init__(self, brands_regex):
        self.regex = brands_regex

    def find(self, text):
        res = {}
        for name, pattern in self.regex.items():
            res[name] = bool(re.search(pattern, text.lower()))
        return res
