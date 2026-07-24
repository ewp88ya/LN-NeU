import signal
import time


class GracefulShutdown:

    def __init__(self):

        self.handlers = {}

        self.is_shutdown = False

        self.register_signals()


    def register_signals(self):

        signal.signal(
            signal.SIGTERM,
            self.handle_signal
        )

        signal.signal(
            signal.SIGINT,
            self.handle_signal
        )


    def register(
        self,
        name,
        callback
    ):

        self.handlers[name] = callback


    def handle_signal(
        self,
        signum,
        frame
    ):

        print(
            f"Shutdown signal received: {signum}"
        )

        self.stop()


    def start(self):

        self.is_shutdown = False

        print(
            "Worker started"
        )


    def stop(self):

        if self.is_shutdown:
            return

        self.is_shutdown = True

        print(
            "Graceful shutdown started"
        )


        for name, handler in self.handlers.items():

            try:

                print(
                    f"Closing resource: {name}"
                )

                handler()

            except Exception as error:

                print(
                    f"Shutdown error {name}: {error}"
                )


        print(
            "Graceful shutdown completed"
        )


    def wait_until_shutdown(
        self,
        interval=1
    ):

        while not self.is_shutdown:

            time.sleep(interval)
