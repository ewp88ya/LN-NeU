class VectorSearch:

    def __init__(self, store):

        self.store = store


    def search(self, query):

        results = []

        for item in self.store.all():

            if query.lower() in item["text"].lower():

                results.append(item)

        return results
