from uuid import uuid4


from memory.vector.schema import VectorDocument

from memory.vector.collection import VectorCollection

from memory.vector.index import VectorIndex



class VectorStore:



    def __init__(self):


        self.collections = {}


        self.index = VectorIndex()



        self.create_collection(
            "default"
        )



    def create_collection(

        self,

        name:str

    ):


        if name not in self.collections:


            self.collections[name] = VectorCollection(
                name
            )



        return self.collections[name]



    def get_collection(

        self,

        name="default"

    ):


        return self.collections.get(
            name
        )



    def add(

        self,

        text:str,

        metadata:dict,

        collection="default"

    ):


        col = self.create_collection(
            collection
        )


        document = VectorDocument(

            id=str(uuid4()),

            text=text,

            metadata=metadata

        )


        col.add(
            document
        )


        return document.id



    def search(

        self,

        query:str,

        top_k=5,

        collection="default"

    ):


        col = self.get_collection(
            collection
        )


        if not col:

            return []



        return self.index.search(

            query,

            col.get_all(),

            top_k

        )



    def filter(

        self,

        metadata_filter,

        collection="default"

    ):


        col = self.get_collection(
            collection
        )


        if not col:

            return []


        return col.filter(
            metadata_filter
        )



    def stats(self):


        return {


            name:

            collection.count()

            for name,collection

            in self.collections.items()

        }
