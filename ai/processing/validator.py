class DataValidator:

    def validate(self, data):

        if not data:
            return False

        if not data.get("input"):
            return False

        if not data.get("action"):
            return False

        return True
