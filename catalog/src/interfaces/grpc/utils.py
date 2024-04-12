from google.protobuf.timestamp_pb2 import Timestamp


def to_proto_timestamp(dt):
    if not dt:
        return None
    timestamp = Timestamp()
    timestamp.FromDatetime(dt)
    return timestamp
