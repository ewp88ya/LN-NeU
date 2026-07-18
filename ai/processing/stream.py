from typing import Any, Dict, AsyncGenerator
import asyncio
import time


class StreamEvent:

    def __init__(
        self,
        event: str,
        data: Dict[str, Any]
    ):

        self.event = event

        self.data = data

        self.timestamp = time.time()


    def to_dict(self):

        return {
            "event": self.event,
            "data": self.data,
            "timestamp": self.timestamp
        }



class StreamManager:


    def __init__(self):

        self.events = []


    def emit(
        self,
        event: str,
        data: Dict[str, Any]
    ):

        stream_event = StreamEvent(
            event,
            data
        )

        self.events.append(
            stream_event
        )

        return stream_event



    async def subscribe(
        self
    ) -> AsyncGenerator:

        index = 0


        while True:

            if index < len(self.events):

                event = self.events[index]

                index += 1

                yield event.to_dict()


            else:

                await asyncio.sleep(0.1)



    def history(self):

        return [
            event.to_dict()
            for event in self.events
        ]
