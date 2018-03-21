from baseconv import BaseConverter
from string import ascii_lowercase, ascii_uppercase

# We have to create this collection ourselves because we want uppercase then
# lowercase, and string.ascii_letters is lowercase then uppercase.
chars = ascii_uppercase + ascii_lowercase
conv = BaseConverter(chars)


def abc_to_id(abc):
    return int(conv.decode(abc))


def id_to_abc(id):
    return conv.encode(id)
