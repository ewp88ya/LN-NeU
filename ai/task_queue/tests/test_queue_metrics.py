import os

from task_queue.metrics import QueueMetrics



def test_queue_metrics_snapshot():

    metrics = QueueMetrics(
        redis_url=os.getenv(
            "REDIS_URL",
            "redis://localhost:6379"
        )
    )


    metrics.clear()


    #
    # Queue events
    #

    metrics.record_enqueue()

    metrics.record_enqueue()


    metrics.record_processed()

    metrics.record_processed()


    metrics.record_failed()


    metrics.record_retry()



    #
    # Recovery metrics
    #

    metrics.record_recovery()



    #
    # DLQ
    #

    metrics.record_dead_letter()



    #
    # Queue depth
    #

    metrics.record_queue_depth(
        10
    )



    stats = metrics.stats()



    assert stats["queued"] == 2

    assert stats["processed"] == 2

    assert stats["failed"] == 1

    assert stats["retry"] == 1

    assert stats["recovery"] == 1

    assert stats["dead_letter"] == 1

    assert stats["queue_depth"] == 10
