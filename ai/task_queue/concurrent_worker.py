import asyncio

from task_queue.adapter import TaskAdapter


class ConcurrentWorker:


    def __init__(
        self,
        queue,
        workflow,
        workers=3
    ):

        self.queue = queue

        self.workflow = workflow

        self.workers = workers

        self.adapter = TaskAdapter()

        self.running = False



    async def process_worker(
        self,
        worker_id
    ):

        print(
            f"Worker-{worker_id} started"
        )


        while self.running:

            payload = None
            result = None


            try:

                payload = self.queue.pop()


                if payload is None:

                    await asyncio.sleep(
                        0.2
                    )

                    continue



                print(
                    f"Worker-{worker_id} processing {payload.get('taskId')}"
                )



                task = self.adapter.convert(
                    payload
                )



                result = await self.workflow.execute(
                    task
                )



                print(
                    f"Worker-{worker_id} completed:"
                )

                print(
                    result
                )



            except Exception as error:


                print(
                    f"Worker-{worker_id} failed:"
                )

                print(
                    error
                )


                if payload:

                    print(
                        "Failed payload:",
                        payload
                    )



    async def start(self):

        self.running = True


        workers = []


        for index in range(
            self.workers
        ):

            workers.append(

                asyncio.create_task(

                    self.process_worker(
                        index + 1
                    )

                )

            )


        await asyncio.gather(
            *workers
        )



    def stop(self):

        self.running = False
