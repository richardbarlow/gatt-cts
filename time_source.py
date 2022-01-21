#!/usr/bin/env python3
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
import time


class TimeSource(ABC):
    @abstractmethod
    def current_time(self) -> datetime:
        """
        Return the current time in local time
        """

    @abstractmethod
    def current_local_time_info(self) -> (timedelta, timedelta):
        """
        Return the timezone offset and the dst offset
        """


class HostTimeSource(TimeSource):
    def current_time(self) -> datetime:
        time.tzset()  # Reset the time conversion rules, so that the local time provided by now() is always correct
        return datetime.now()

    def current_local_time_info(self) -> (timedelta, timedelta):
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
    print(f"CT: {host_time_source.current_time().isoformat(timespec='microseconds')}")
    time_zone_offset, dst_offset = host_time_source.current_local_time_info()
    print(f"TZ Offset: {time_zone_offset}")
    print(f"DST Offset: {dst_offset}")


if __name__ == '__main__':
    main()
