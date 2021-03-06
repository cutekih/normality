import six
from datetime import datetime, date
from decimal import Decimal

from normality.cleaning import remove_byte_order_mark
from normality.encoding import guess_encoding


def stringify(value, encoding_default='utf-8', encoding=None):
    """Brute-force convert a given object to a string.

    This will attempt an increasingly mean set of conversions to make a given
    object into a unicode string. It is guaranteed to either return unicode or
    None, if all conversions failed (or the value is indeed empty).
    """
    if value is None:
        return None

    if not isinstance(value, six.text_type):
        if isinstance(value, (date, datetime)):
            return value.isoformat()
        elif isinstance(value, (float, Decimal)):
            return Decimal(value).to_eng_string()
        elif isinstance(value, six.binary_type):
            if encoding is None:
                encoding = guess_encoding(value)
            value = value.decode(encoding, 'ignore')
            value = remove_byte_order_mark(value)
        else:
            value = six.text_type(value)

    # XXX: is this really a good idea?
    value = value.strip()
    if not len(value):
        return None
    return value
