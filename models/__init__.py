__all__ = ["data_models", "issuers"]

from . import issuers


class DataModels(object):
    _issuers: issuers.DataIssuers = None

    @property
    def issuers(self):
        if self._issuers is None:
            self._issuers = issuers.DataIssuers()
        return self._issuers


data_models = DataModels()
