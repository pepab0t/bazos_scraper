import aiofiles


class VisitStore:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.visited: set[str] = set()

    async def __aenter__(self):
        async with aiofiles.open(self.file_path, "r") as file:
            async for line in file:
                self.visited.add(line.strip())
        return self

    async def __aexit__(self, exc_type, exc, tb):
        async with aiofiles.open(self.file_path, "w") as file:
            for path in self.visited:
                await file.write(path + "\n")

    def is_visited(self, path: str):
        return path in self.visited

    def visit(self, path: str):
        self.visited.add(path)
