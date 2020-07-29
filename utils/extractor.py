import re


class TextExtractor:
    def __init__(self, text):
        self.text = text

    def find_all(self, pattern):
        return re.findall(re.compile(pattern), self.text)

    def find_one(self, pattern):
        matches = self.find_all(pattern)
        if len(matches) == 0:
            return None
        return matches[0]
