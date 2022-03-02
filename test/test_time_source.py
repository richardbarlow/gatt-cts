"""
Test that time_source.py calculates timezone and daylight savings offsets correctly.

All tests run time_source.py as a subprocess under various conditions to
make sure that the system time is properly modified by libfaketime.

Assumes you have libfaketime installed (dnf install faketime)
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
import json
import subprocess

import pytest
import pytz


PYTHON_CMD = ["python", "time_source.py"]

def _run_with_faketime(command, datetime_str, tz=pytz.utc.zone):
    full_command = ["faketime", datetime_str] + command
    env = {
        "TZ": tz
    }
    return subprocess.run(full_command, env=env, capture_output=True, text=True, check=True)


@dataclass
class TestCase:
    timezone: str
    datetime: str
    tz_o: int
    dst_o: int

    def __str__(self):
        return f"{self.timezone} {self.datetime}"


TESTS = [
    # Timezones / daylight savings
    TestCase("GB",         "2022-03-18T12:00:00",  0, 0),  # GB, no daylight savings
    TestCase("GB",         "2022-03-28T12:00:00",  0, 1),  # GB, daylight savings
    TestCase("Japan",      "2022-01-01T12:00:00",  9, 0),  # Japan (doesn't use daylight savings)
    TestCase("Japan",      "2022-06-06T12:00:00",  9, 0),  # Japan (doesn't use daylight savings)
    TestCase("US/Alaska",  "2022-01-01T12:00:00", -9, 0),  # Alaska, no daylight savings
    TestCase("US/Alaska",  "2022-06-06T12:00:00", -9, 1),  # Alaska, daylight savings
]


@pytest.mark.parametrize("testcase", TESTS, ids=lambda x: str(x))
def test_offsets(testcase: TestCase):
    result = _run_with_faketime(PYTHON_CMD, testcase.datetime, tz=pytz.timezone(testcase.timezone).zone)
    data = json.loads(result.stdout)

    assert data["tz offset"] == str(timedelta(hours=testcase.tz_o))
    assert data["dst offset"] == str(timedelta(hours=testcase.dst_o))
 