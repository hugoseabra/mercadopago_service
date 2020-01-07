import logging

from celery import Celery
from kombu import Queue, Exchange

CELERY_QUEUES = (
    Queue(
        'celery',
        Exchange('transient', delivery_mode=2),
        routing_key='celery',
        durable=True,
    ),
)

logger = logging.getLogger("Celery[MPPayment]")

app = Celery('mp_payment')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
