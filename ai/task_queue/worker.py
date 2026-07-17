import asyncio


class AsyncWorker:


    def __init__(
        self,
        queue,
        workflow
    ):

        self.queue = queue
        self.workflow = workflow
        self.running = False



    async def start(self):

        self.running = True

        print(
            "Worker listening...",
            flush=True
        )


        while self.running:

            try:

                task = self.queue.pop()


                if task is None:

                    await asyncio.sleep(0.1)
                    continue



                print(
                    f"Processing task: {task.taskId}",
                    flush=True
                )


                result = await self.workflow.execute(
                    task
                )


                print(
                    "Task completed:",
                    result.get("status"),
                    flush=True
                )


            except Exception as e:

                print(
                    "Worker error:",
                    repr(e),
                    flush=True
                )


                await asyncio.sleep(1)



    def stop(self):

        self.running = False
