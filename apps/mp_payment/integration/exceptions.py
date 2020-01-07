class SynchronizationException(Exception):
    """ Errors in synchronization process. """

    def __init__(self,
                 status: int,
                 error: str,
                 message: str):
        self.status = status
        self.error = error

        self.causes = list()

        super().__init__(message)

    def add_cause(self, code, description):
        self.causes.append({
            'code': code,
            'description': description,
        })
