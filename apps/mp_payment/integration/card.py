from django.utils.translation import ugettext_lazy as _

from apps.mp_payment.models import Card
from .exceptions import SynchronizationException
from .response_utils import process_response


def synchronize(instance: Card):
    """
    Synchronization to mercado pago.
    """

    if instance.deleted is True:
        raise SynchronizationException(
            status=0,
            error='cannot synchronize',
            message=_('Customer is scheduled to be deleted and cannot'
                      ' be synchronized')
        )

    if not instance.token:
        raise SynchronizationException(
            status=0,
            error='cannot synchronize',
            message=_('Card has not been tokenized to be related to customer'
                      ' in mercado pago.')
        )

    customer = instance.customer

    if customer.synchronized is False:
        raise SynchronizationException(
            status=0,
            error='cannot synchronize',
            message=_('Card with not synchronized customers cannot be'
                      ' processed.')
        )

    service = customer.account.service
    instance_data = instance.to_mp_representation()

    from pprint import pprint
    pprint(instance_data)

    if instance.synchronized is False:
        uri = '/v1/customers/{customer_id}/cards'.format(
            customer_id=customer.mp_id,
        )
        response = service.post(uri=uri, data={
            'token': instance.token,
        })
    else:
        uri = '/v1/customers/{customer_id}/cards/{id}'.format(
            customer_id=customer.mp_id,
            id=instance.mp_id,
        )
        print(uri)
        response = service.put(uri=uri, data=instance_data)

    status, data = process_response(response)

    instance.mp_id = data['id']
    instance.expiration_month = data['expiration_month']
    instance.expiration_year = data['expiration_year']
    instance.tmp_token = None
    instance.save()


def remove(instance: Card):
    """
    Deletes at mercado pago.
    """
    customer = instance.customer

    if customer.synchronized is False:
        raise SynchronizationException(
            status=0,
            error='cannot synchronize',
            message=_('Card with not synchronized customers cannot be'
                      ' deleted.')
        )

    if instance.deleted is False:
        raise SynchronizationException(
            status=0,
            error='cannot delete',
            message=_('Customer is not scheduled to be deleted and cannot'
                      ' be processed for deletion at mercado pago.')
        )

    if instance.synchronized is False:
        raise SynchronizationException(
            status=0,
            error='cannot delete',
            message=_('Customer has not been synchronized to be deleted.')
        )

    service = instance.customer.account.service

    print('mercado pago id:', instance.mp_id)
    response = service.delete(
        uri='/v1/customers/{customer_id}/cards/{id}'.format(
            customer_id=customer.mp_id,
            id=instance.mp_id,
        )
    )

    status, data = process_response(response)
    print(status)
    print(data)
