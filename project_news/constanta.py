from dataclasses import dataclass


@dataclass
class News:
    title: str
    url: str
    date: str
    category: str


@dataclass
class NormalizedNews:
    title: str
    url: str
    date: str
    category: str
    normalized_title: list
