import decimal
import json


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return "{:.3f}".format(o)
        return super(DecimalEncoder, self).default(o)


class ULIDConverter:
    regex = "[0-9A-Z]{26}"

    def to_python(self, value):
        return str(value)

    def to_url(self, value):
        return str(value)
