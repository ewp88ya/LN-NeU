from processing.middleware import (
    InputValidator,
    InputNormalizer,
)


class ProcessingPipeline:

    def __init__(self):

        self.validator = InputValidator()
        self.normalizer = InputNormalizer()

    def process(self, task):

        task = self.validator.validate(task)

        task = self.normalizer.normalize(task)

        return task
