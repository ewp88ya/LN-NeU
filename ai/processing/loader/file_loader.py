from pathlib import Path

from .base import BaseLoader


class FileLoader(BaseLoader):


    def load(self, source):

        path = Path(source)

        if not path.exists():
            raise FileNotFoundError(
                f"File not found: {source}"
            )


        content = path.read_text(
            encoding="utf-8"
        )


        return {
            "source": str(path),
            "content": content,
            "size": len(content)
        }
