import csv


class Issuer(object):
    name: str
    inn: str
    type: str
    ticker: str
    isin: str
    number: str
    date_registration: str
    price: float
    currency: str
    count: int

    def __init__(self, attrs):
        self.attributes = attrs

    @property
    def attributes(self) -> dict:
        return {
            'name':              self.name,
            'inn':               self.inn,
            'type':              self.type,
            'ticker':            self.ticker,
            'isin':              self.isin,
            'number':            self.number,
            'date_registration': self.date_registration,
            'price':             self.price,
            'currency':          self.currency,
            'count':             self.count,
        }

    @attributes.setter
    def attributes(self, attrs):
        self.name = 'name' in attrs and attrs['name'] or None
        self.inn = 'inn' in attrs and attrs['inn'] or None
        self.type = 'type' in attrs and attrs['type'] or None
        self.ticker = 'ticker' in attrs and attrs['ticker'] or None
        self.isin = 'isin' in attrs and attrs['isin'] or None
        self.number = 'number' in attrs and attrs['number'] or None
        self.date_registration = 'date_registration' in attrs and attrs['date_registration'] or None
        self.price = 'price' in attrs and attrs['price'] or None
        self.currency = 'currency' in attrs and attrs['currency'] or None
        self.count = 'count' in attrs and attrs['count'] or None


class DataIssuers(object):
    _issuers: list = None

    headers = {
        'name':              'Полное фирменное наименование эмитента',
        'inn':               'ИНН',
        'type':              'Тип ценной бумаги',
        'ticker':            'Идентификационный код',
        'isin':              'Международный код (номер) идентификации ценных бумаг (ISIN)',
        'number':            'Государственный регистрационный номер выпуска',
        'date_registration': 'Дата присвоения государственного регистрационного номера',
        'price':             'Номинальная стоимость',
        'currency':          'Единица измерения номинальной стоимости',
        'count':             'Общее количество ценных бумаг в выпуске',
    }

    def search(self, params: dict) -> list:
        return [
            issuer
            for issuer in self.issuers
            if ('ticker' not in params or params['ticker'] is None or issuer['ticker'] == params['ticker']) and
               ('number' not in params or params['number'] is None or issuer['number'] == params['number'])
        ]

    @property
    def issuers(self):
        self._issuers = (self._issuers is None) and self.reader()._issuers or self._issuers
        return self._issuers

    def reader(self) -> __qualname__:
        self._issuers = []
        with open('./data/issuers.csv', encoding = "utf8") as csv_file:
            reader = csv.DictReader(csv_file, delimiter = '\t', quotechar = '"', quoting = csv.QUOTE_MINIMAL, fieldnames = self.headers.keys())
            for row in reader:
                self._issuers.append(row)

        return self
