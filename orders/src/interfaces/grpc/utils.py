import datetime
from typing import Optional

from google.protobuf.timestamp_pb2 import Timestamp


def to_proto_timestamp(dt: datetime.datetime) -> Optional[Timestamp]:
    if not dt:
        return None

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=datetime.timezone.utc)
    else:
        dt = dt.astimezone(datetime.timezone.utc)

    timestamp = Timestamp()
    timestamp.FromDatetime(dt)
    return timestamp
