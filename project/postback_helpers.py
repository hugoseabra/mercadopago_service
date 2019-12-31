import os
import tempfile

from django.conf import settings


def get_postback_url():
    if settings.DEBUG is True:
        return get_ngrok_host()

    return settings.BASE_POSTBACK_HOST


def get_ngrok_host():
    """
    NGROK é um serviço utilizado para criar um host público em qualquer
    ambiente fazendo um túnel de portas.

    O serviço é ativado no container específco para isso em
    conf/docker-compose_dev.yml no qual ele escreve o endereço gerado no
    ngrok em um arquivo e é compartilhado pelo host.
    """
    ngrok_dir = os.path.join(tempfile.gettempdir(), 'ngrok')

    if os.path.isdir(ngrok_dir) is False:
        os.mkdir(ngrok_dir)

    ngrok_file = os.path.join(tempfile.gettempdir(), 'ngrok', 'ngrok.txt')

    host = None

    if os.path.isfile(ngrok_file):
        with open(ngrok_file) as f:
            host = f.read()
            f.close()

    if not host:
        raise Exception(
            'Ngrok host was not found in existing file.'
        )

    return host.strip()
