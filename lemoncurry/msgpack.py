import msgpack
import pickle

from django_redis.serializers.base import BaseSerializer


def default(obj):
    # Pickle anything that MessagePack can't handle itself.
    return msgpack.ExtType(69, pickle.dumps(obj, protocol=4))


def ext_hook(code, data):
    # Unpickle if we pickled - otherwise do nothing.
    if code == 69:
        return pickle.loads(data)
    return msgpack.ExtType(code, data)


class MSGPackModernSerializer(BaseSerializer):
    def dumps(self, value):
        return msgpack.packb(value, default=default, use_bin_type=True)

    def loads(self, value):
        return msgpack.unpackb(value, ext_hook=ext_hook, raw=False)
