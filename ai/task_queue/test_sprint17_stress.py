import time

from task_queue.priority_queue import PriorityQueue
from task_queue.metrics import QueueMetrics


TOTAL_TASKS = 1000


def run_stress_test():

    queue = PriorityQueue()

    metrics = QueueMetrics()


    queue.clear()
    metrics.clear()


    print(
        f"Creating {TOTAL_TASKS} tasks..."
    )


    start = time.time()


    # Producer

    for i in range(TOTAL_TASKS):

        priority = "normal"

        if i % 10 == 0:
            priority = "high"

        elif i % 5 == 0:
            priority = "low"


        queue.push(
            {
                "task_id": i
            },
            priority=priority
        )

        metrics.record_enqueue()


    enqueue_time = time.time() - start


    print(
        "Enqueue completed:",
        enqueue_time,
        "seconds"
    )


    # Consumer simulation

    processed = 0

    start = time.time()


    while True:

        task = queue.pop()

        if task is None:
            break


        processed += 1

        metrics.record_processed()


    process_time = time.time() - start


    print(
        "Processed:",
        processed
    )


    print(
        "Processing time:",
        process_time,
        "seconds"
    )


    print(
        "Remaining queue:",
        queue.size()
    )


    print(
        "Metrics:",
        metrics.stats()
    )


    assert processed == TOTAL_TASKS

    assert queue.size() == 0


    print(
        "\nSprint 17 Stress Test SUCCESS"
    )


if __name__ == "__main__":
    run_stress_test()
