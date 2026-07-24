class DataValidator:


    def validate(
        self,
        document: str
    ):

        errors = []


        if document is None:
            errors.append(
                "Document is None"
            )


        if not isinstance(
            document,
            str
        ):
            errors.append(
                "Document must be string"
            )


        if isinstance(
            document,
            str
        ):

            if len(document.strip()) == 0:
                errors.append(
                    "Document is empty"
                )


            if len(document) < 5:
                errors.append(
                    "Document too short"
                )



        return {

            "valid": len(errors) == 0,

            "errors": errors

        }
