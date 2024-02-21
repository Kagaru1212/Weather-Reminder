from celery import shared_task


@shared_task
def test_task():
    return "test_task OK"
