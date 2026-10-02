from typing import List
import re


class TopicFilter:
    """
    Keyword-based topic detector.

    The user provides a topic such as:
        "décès du président Jacques Chirac"

    The topic is automatically converted into keywords:
        ["décès", "président", "jacques", "chirac"]
    """

    def __init__(self, topic: str):
        self.topic = topic.strip()

        self.keywords = [
            word.lower()
            for word in re.findall(
                r"\b[\wÀ-ÿ]+\b",
                self.topic
            )
            if len(word) > 2
        ]

    def matches(self, text: str) -> bool:
        if not text:
            return False

        text = text.lower()

        return any(
            keyword in text
            for keyword in self.keywords
        )