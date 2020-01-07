import logging

from mercadopago import MP

from project import settings

logger = logging.getLogger(__name__)


class MercadoPagoServiceException(Exception):
    pass


class MercadoPagoService(MP):
    """
    MercadoPago service (the same one from the SDK), lazy-initialized on first
    access.
    """

    def __init__(self, account):
        if settings.DEBUG is True:
            super().__init__(settings.ACCESS_TOKEN_SANDBOX_MODE)
            self.sandbox_mode(True)
        else:
            super().__init__(account.app_id, account.secret_key)
            self.sandbox_mode(account.sandbox)
