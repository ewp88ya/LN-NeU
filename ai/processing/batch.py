import asyncio


class BatchProcessor:


    def __init__(
        self,
        ingestion_pipeline
    ):

        self.pipeline = ingestion_pipeline



    async def process_files(
        self,
        files
    ):


        tasks = []


        for file_path in files:

            tasks.append(
                self.pipeline.ingest(
                    file_path
                )
            )


        results = await asyncio.gather(
            *tasks,
            return_exceptions=True
        )


        output = []


        for index, result in enumerate(results):


            if isinstance(
                result,
                Exception
            ):

                output.append({

                    "source": files[index],

                    "status": "failed",

                    "error": str(result)

                })


            else:

                output.append(
                    result
                )


        return {

            "status": "completed",

            "total": len(files),

            "results": output

        }
