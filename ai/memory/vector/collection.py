from memory.vector.schema import VectorDocument


class VectorCollection:


    def __init__(
        self,
        name:str
    ):

        self.name = name

        self.documents = {}



    def add(
        self,
        document: VectorDocument
    ):

        self.documents[
            document.id
        ] = document



    def get_all(self):

        return list(
            self.documents.values()
        )



    def count(self):

        return len(
            self.documents
        )



    def filter(
        self,
        metadata_filter:dict
    ):

        results = []


        for doc in self.documents.values():


            match = True


            for key,value in metadata_filter.items():

                if doc.metadata.get(key) != value:

                    match = False


            if match:

                results.append(doc)



        return results
