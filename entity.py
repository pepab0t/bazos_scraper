from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Advertisement:
    url: str
    title: str
    description: str
    name: str = ""
    location: str = ""
    seen: str = ""

    def to_text(self) -> str:
        return f"""url: {self.url}
name: {self.name}
seen: {self.seen}
title: {self.title}
description: {self.description}
        """

    @property
    def searchable_text(self) -> str:
        return f"{self.title}{self.description}".lower()
