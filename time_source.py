#!/usr/bin/env python3
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
import json
import time
from typing import Tuple


class TimeSource(ABC):
    @abstractmethod
    def current_time(self) -> datetime:
        """
        Return the current time in local time
        """

    @abstractmethod
    def current_local_time_info(self) -> Tuple[timedelta, timedelta]:
        """
        Return the timezone offset and the dst offset
        """


class HostTimeSource(TimeSource):
    def current_time(self) -> datetime:
        time.tzset()  # Reset the time conversion rules, so that the local time provided by now() is always correct
        return datetime.now()

    def current_local_time_info(self) -> Tuple[timedelta, timedelta]:
        time.tzset()  # Reset the time conversion rules, so that timezone and altzone are always correct
        time_zone_offset = timedelta(seconds=-time.timezone)

        # If DST is in effect, then calculate the size of the offset purely due to DST
        if time.localtime().tm_isdst and time.daylight:
            dst_offset = timedelta(seconds=-time.altzone) - time_zone_offset
        else:
            dst_offset = timedelta()

        return time_zone_offset, dst_offset


def main():
    host_time_source = HostTimeSource()
    time_zone_offset, dst_offset = host_time_source.current_local_time_info()

    result = json.dumps({
        "ct": host_time_source.current_time().isoformat(timespec='microseconds'),
        "tz offset": str(time_zone_offset),
        "dst offset": str(dst_offset)
    })
    print(result)


if __name__ == '__main__':
    main()
