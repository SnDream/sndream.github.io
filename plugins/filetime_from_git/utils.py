# -*- coding: utf-8 -*-
"""
Utility functions
"""
from datetime import datetime
import logging
from pelican.utils import set_date_tzinfo

try:
    from zoneinfo import ZoneInfo
except ModuleNotFoundError:
    from backports.zoneinfo import ZoneInfo

DEV_LOGGER = logging.getLogger(__name__)


STRING_BOOLS = {
    'yes': True,
    'no': False,
    'true': True,
    'false': False,
    '0': False,
    '1': True,
    'on': True,
    'off': False,
}


def string_to_bool(string):
    '''
    Convert a string to a bool based
    '''
    return STRING_BOOLS[string.strip().lower()]


def datetime_from_timestamp(timestamp, content):
    """
    Helper function to add timezone information to datetime,
    so that datetime is comparable to other datetime objects in recent versions
    that now also have timezone information.
    """
    tz_name=content.settings.get('TIMEZONE', None)
    tz_info=ZoneInfo(tz_name) if tz_name else None
    return set_date_tzinfo(
        datetime.fromtimestamp(timestamp, tz=tz_info) if timestamp else datetime.now(tz=tz_info),
        tz_name=tz_name)
