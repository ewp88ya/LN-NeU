from uuid import uuid4
from datetime import datetime


from processing.document_loader import DocumentLoader
from processing.normalizer import DataNormalizer
from processing.chunker import TextChunker
from processing.embedding import EmbeddingPreparation
from processing.validator import DataValidator


from memory.vector.store import VectorStore



class DataIngestionPipeline:



    def __init__(self):


        self.loader = DocumentLoader()


        self.normalizer = DataNormalizer()


        self.validator = DataValidator()


        self.chunker = TextChunker(

            chunk_size=500

        )


        self.embedding = EmbeddingPreparation()


        self.vector = VectorStore()



    async def ingest(

        self,

        file_path:str

    ):


        document_id = str(
            uuid4()
        )


        created_at = datetime.utcnow().isoformat()



        try:


            #
            # LOAD
            #

            raw_document = self.loader.load(

                file_path

            )



            #
            # NORMALIZE
            #

            document = self.normalizer.normalize(

                raw_document

            )



            #
            # VALIDATE
            #

            validation = self.validator.validate(

                document

            )



            if not validation["valid"]:


                return {


                    "status":
                    "failed",


                    "document_id":
                    document_id,


                    "errors":
                    validation["errors"]

                }



            #
            # CHUNK
            #

            chunks = self.chunker.split(

                document

            )



            #
            # EMBEDDING PREPARE
            #

            embeddings = await self.embedding.prepare(

                chunks

            )



            indexed = 0



            #
            # VECTOR STORAGE
            #

            for item in embeddings:



                metadata = {


                    "document_id":

                    document_id,


                    "chunk_id":

                    item["id"],


                    "source":

                    file_path,


                    "type":

                    "document",


                    "created_at":

                    created_at,


                    "chunk_length":

                    len(
                        item["text"]
                    ),


                    "document_length":

                    len(document),


                    "chunk_index":

                    item["id"],


                    "embedding_ready":

                    True

                }



                self.vector.add(

                    item["text"],

                    metadata

                )



                indexed += 1



            return {


                "status":

                "completed",


                "document_id":

                document_id,


                "source":

                file_path,


                "chunks":

                len(chunks),


                "indexed":

                indexed,


                "metadata":{


                    "document_id":

                    document_id,


                    "source":

                    file_path,


                    "length":

                    len(document),


                    "created_at":

                    created_at,


                    "embedding":

                    True

                }

            }



        except Exception as error:


            return {


                "status":

                "failed",


                "document_id":

                document_id,


                "error":

                str(error),


                "error_type":

                type(error).__name__

            }
