from .file_loader import FileLoader


class LoaderManager:


    def __init__(self):

        self.loaders = {
            "file": FileLoader()
        }



    def load(
        self,
        source_type,
        source
    ):

        loader = self.loaders.get(
            source_type
        )


        if not loader:
            raise ValueError(
                f"Unsupported loader: {source_type}"
            )


        return loader.load(
            source
        )
