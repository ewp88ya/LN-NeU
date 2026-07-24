import time

from task_queue.workflow_adapter import WorkflowQueueAdapter


def run_test():

    adapter = WorkflowQueueAdapter()


    # clean state

    adapter.queue_manager.clear()
    adapter.metrics.clear()
    adapter.scheduler.clear()


    print("\n[1] Submit workflow")

    adapter.submit_workflow(
        {
            "workflow": "integration-success"
        },
        priority="high"
    )


    task = adapter.get_workflow()


    assert task is not None

    print(
        "PASS:",
        task
    )


    adapter.metrics.record_processed()


    print("\n[2] Failed workflow")


    adapter.fail_workflow(
        {
            "workflow": "integration-failed"
        },
        "worker-error"
    )


    stats = adapter.stats()


    assert (
        stats["queue"]["default"]["dlq_size"]
        >= 1
    )

    assert (
        stats["metrics"]["failed"]
        >= 1
    )


    print(
        "PASS:",
        stats
    )


    print("\n[3] Scheduler workflow")


    execute_at = time.time() + 1


    adapter.schedule_workflow(
        {
            "workflow": "scheduled-job"
        },
        execute_at
    )


    assert (
        adapter.scheduler.size()
        == 1
    )


    print(
        "PASS: scheduled"
    )


    time.sleep(2)


    ready = adapter.scheduler.get_ready_tasks()


    assert len(ready) == 1


    print(
        "PASS:",
        ready
    )


    print(
        "\nSprint 17 Integration Test SUCCESS"
    )


if __name__ == "__main__":
    run_test()
