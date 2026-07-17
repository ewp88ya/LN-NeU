import asyncio


class AsyncWorker:

    def __init__(self, queue, workflow):

        self.queue = queue
        self.workflow = workflow
        self.running = False

    async def start(self):

        self.running = True

        while self.running:

            task = self.queue.pop()

            if task is None:
                await asyncio.sleep(0.1)
                continue

            await self.workflow.execute(task)

    def stop(self):

        self.running = False
