"""
    Survey module domain models
"""


class EntityMixin:
    """
    Mixin to add utilities to model
    """

    def is_new(self):
        return self._state.adding is True
