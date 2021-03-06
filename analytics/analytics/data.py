import functools
import hashlib

from .bitstream import BitStream, BitField

DESKTOP = 1
PHONE = 2
TABLET = 3
OTHER = 0
DEVICE_ID_LENGTH = 16

ACTIONS = ['html', 'image', 'audio', 'video', 'folder', 'download']
OS_FAMILIES = [
    'Android',
    'Arch Linux',
    'BackTrack',
    'Bada',
    'BlackBerry OS',
    'BlackBerry Tablet OS',
    'CentOS',
    'Chrome OS',
    'Debian',
    'Fedora',
    'Firefox OS',
    'FreeBSD',
    'Gentoo',
    'Intel Mac OS',
    'iOS',
    'Kindle',
    'Linux',
    'Linux Mint',
    'Lupuntu',
    'Mac OS',
    'Mac OS X',
    'Mageia',
    'Mandriva',
    'NetBSD',
    'OpenBSD',
    'openSUSE',
    'PCLinuxOS',
    'PPC Mac OS',
    'Puppy',
    'Red Hat',
    'Slackware',
    'Solaris',
    'SUSE',
    'Symbian OS',
    'Ubuntu',
    'Windows 10',
    'Windows 2000',
    'Windows 7',
    'Windows 8',
    'Windows 8.1',
    'Windows 95',
    'Windows 98',
    'Windows CE',
    'Windows ME',
    'Windows Mobile',
    'Windows Phone',
    'Windows RT',
    'Windows RT 8.1',
    'Windows Vista',
    'Windows XP',
]


def round_to_nearest(n):
    return round(n * 2) / 2


def get_timezone_table(start=-12, end=14, step=0.5):
    tz_range = range(start, end)
    return functools.reduce(lambda x, i: x + [i, i + step], tz_range, [])


class StatBitStream(BitStream):
    start_marker = 'OHD'
    end_marker = 'DHO'
    user_id = BitField(width=32, data_type='hex')
    timestamp = BitField(width=32, data_type='timestamp')
    timezone = BitField(width=6, data_type='integer')
    path = BitField(width=128, data_type='hex')
    action = BitField(width=4, data_type='integer')
    os_family = BitField(width=6, data_type='integer')
    agent_type = BitField(width=2, data_type='integer')

    def preprocess_path(self, value):
        return hashlib.md5(value).hexdigest()

    def preprocess_timezone(self, value):
        rounded_tz = round_to_nearest(value)
        return get_timezone_table().index(rounded_tz)

    def postprocess_timezone(self, value):
        return get_timezone_table()[value]

    def preprocess_action(self, value):
        return ACTIONS.index(value)

    def postprocess_action(self, value):
        return ACTIONS[value]

    def preprocess_os_family(self, value):
        return OS_FAMILIES.index(value)

    def postprocess_os_family(self, value):
        return OS_FAMILIES[value]
