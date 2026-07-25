import logging
import json
import time
import sys


class StructuredFormatter(
    logging.Formatter
):


    def format(
        self,
        record
    ):

        payload = {

            "timestamp": time.time(),

            "level": record.levelname,

            "service": getattr(
                record,
                "service",
                "ln-neu-ai"
            ),

            "event": getattr(
                record,
                "event",
                None
            ),

            "message": record.getMessage(),

            "metadata": getattr(
                record,
                "metadata",
                {}
            )

        }


        return json.dumps(
            payload
        )



def get_logger(
    name="ln-neu"
):


    logger = logging.getLogger(
        name
    )


    if logger.handlers:

        return logger



    handler = logging.StreamHandler(
        sys.stdout
    )


    handler.setFormatter(
        StructuredFormatter()
    )


    logger.addHandler(
        handler
    )


    logger.setLevel(
        logging.INFO
    )


    return logger



def log_event(
    logger,
    level,
    message,
    event=None,
    service="ln-neu-ai",
    metadata=None
):


    extra = {

        "event": event,

        "service": service,

        "metadata": metadata or {}

    }


    log_function = getattr(
        logger,
        level.lower()
    )


    log_function(
        message,
        extra=extra
    )
