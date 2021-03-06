import logging

from dateutil.tz import tzoffset

from .bitstream import bytes_to_hex
from .data import StatBitStream, DEVICE_ID_LENGTH


ANALYTICS_TABLE = 'stats'


def to_seconds(hours):
    return hours * 60 * 60


def process_stats(supervisor, data):
    device_id = bytes_to_hex(data[:DEVICE_ID_LENGTH])
    stats = StatBitStream.from_bytes(data[DEVICE_ID_LENGTH:])
    db = supervisor.exts.databases.reports
    for entry in stats:
        path_hash = entry.pop('path', None)
        try:
            path = supervisor.app.known_paths[path_hash]
        except KeyError:
            logging.error('Path hash not recognized: {}'.format(path_hash))
            continue

        data = dict(device_id=device_id, path=path)
        data.update(entry)
        utc_timestamp = data['timestamp']
        local_tz = tzoffset(None, to_seconds(data['timezone']))
        # converting both timestamps into naive datetime objects because
        # postgres does not perform automatic conversion
        data['local_timestamp'] = (utc_timestamp.astimezone(local_tz)
                                                .replace(tzinfo=None))
        data['timestamp'] = utc_timestamp.replace(tzinfo=None)
        q = db.Replace(ANALYTICS_TABLE,
                       cols=data.keys(),
                       constraints=('timestamp', 'device_id', 'user_id'))
        db.execute(q, data)
    logging.debug("%s stat entries stored from %s", len(stats), device_id)
