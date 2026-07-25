import traceback

from observability.error_store import ErrorStore



class ErrorTracker:


    def __init__(self):

        self.store = ErrorStore()



    def capture(
        self,
        exception,
        service="ai"
    ):


        error = {

            "service": service,

            "type": exception.__class__.__name__,

            "message": str(exception),

            "trace": traceback.format_exc()

        }


        self.store.save(
            error
        )


        return error



    def recent(
        self,
        limit=10
    ):

        return self.store.latest(
            limit
        )



    def total(self):

        return self.store.count()
