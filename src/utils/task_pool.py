import asyncio


class TaskPool(object):

    def __init__(self, workers):
        self.semaphore = asyncio.Semaphore(workers) if workers else None
        self.tasks = set()
        self.results = []
        self.closed = False

    async def put(self, coro):

        if self.closed:
            raise RuntimeError("Trying put items into a closed TaskPool")

        if self.semaphore:
            await self.semaphore.acquire()

        task = asyncio.create_task(coro)
        self.tasks.add(task)
        task.add_done_callback(self._on_task_done)
        task.set_exception

    def _on_task_done(self, task):
        self.results.append(task._result)
        self.tasks.remove(task)
        if self.semaphore:
            self.semaphore.release()

    async def _join(self):
        await asyncio.gather(*self.tasks)
        self.closed = True

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return await self._join()
