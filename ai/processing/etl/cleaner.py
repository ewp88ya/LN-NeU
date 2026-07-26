import re


class Cleaner:


    def clean(
        self,
        text: str
    ) -> str:

        text = text.strip()

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text
