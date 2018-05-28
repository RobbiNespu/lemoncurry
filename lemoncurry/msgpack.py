import msgpack

from django_redis.serializers.base import BaseSerializer


class MSGPackModernSerializer(BaseSerializer):
    def dumps(self, value):
        return msgpack.packb(value, use_bin_type=True)

    def loads(self, value):
        return msgpack.unpackb(value, raw=False)
