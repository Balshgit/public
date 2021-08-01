from celery_config.app_celery import app_celery_instance


@app_celery_instance.task
def add(first: int, second: int) -> int:
    print(first + second)
    return first + second


# TODO: try with `@app.task(throws=(ZeroDivisionError,))`
@app_celery_instance.task
def div(first: int, second: int) -> float:
    # TODO: show how errors work
    return first / second
