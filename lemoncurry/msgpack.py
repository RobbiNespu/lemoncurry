import msgpack

from django_redis.serializers.base import BaseSerializer


class MSGPackModernSerializer(BaseSerializer):
    def dumps(self, value):
        return msgpack.dumps(value)

    def loads(self, value):
        return msgpack.loads(value)
