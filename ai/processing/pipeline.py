from processing.parser import DataParser
from processing.validator import DataValidator
from processing.transformer import DataTransformer


class ProcessingPipeline:

    def __init__(self):

        self.parser = DataParser()
        self.validator = DataValidator()
        self.transformer = DataTransformer()


    def process(self, task):

        data = self.parser.parse(task)

        if not self.validator.validate(data):
            raise ValueError("Invalid task data")

        data = self.transformer.transform(data)

        return data
