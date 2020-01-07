from .exceptions import SynchronizationException


def process_response(response):
    print(response)

    status = response['status']
    data = response['response']

    if status not in (200, 201):
        exc = SynchronizationException(
            status=status,
            error=data['error'],
            message=data['message'],
        )

        print(data['message'])

        if 'cause' in data and data['cause']:
            for cause in data['cause']:
                if cause:
                    print(' - {} - {}'.format(
                        cause['code'],
                        cause['description'])
                    )
                    exc.add_cause(cause['code'], cause['description'])

        raise exc

    return status, data
