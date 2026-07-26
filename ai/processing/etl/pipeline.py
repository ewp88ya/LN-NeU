from processing.etl.extractor import Extractor
from processing.etl.cleaner import Cleaner
from processing.etl.transformer import Transformer



class ETLPipeline:


    def __init__(self):

        self.extractor = Extractor()

        self.cleaner = Cleaner()

        self.transformer = Transformer()



    async def run(
        self,
        document
    ):

        extracted = await self.extractor.extract(
            document
        )


        extracted["content"] = self.cleaner.clean(
            extracted["content"]
        )


        result = self.transformer.transform(
            extracted
        )


        return result
