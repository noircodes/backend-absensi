# ===== Module & Library
from datetime import datetime
from fastapi import HTTPException
from loguru import logger

import pytz

# ===== Header
INDONESIA_TIMEZONE = pytz.timezone("Asia/Jakarta")
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M:%S"

class DatetimeUtils:
# ===== Function
    def date_now():
        """Function to get current date with Asia/Jakarta time zone"""

        dt = datetime.strptime(
            datetime.now(tz=INDONESIA_TIMEZONE).strftime(DATETIME_FORMAT), DATETIME_FORMAT
        )
        return dt.date()


    def date_now_str():
        """Function to get current string date with Asia/Jakarta time zone"""

        dt = datetime.now(tz=INDONESIA_TIMEZONE).strftime(DATE_FORMAT)
        return dt


    def str_date_to_date(str_date: str):
        """Function to convert current string date to datetime date"""

        try:
            dt = datetime.strptime(str_date, DATE_FORMAT)
            return dt.date()
        except Exception as err:
            logger.warning(err)
            raise HTTPException(
                400,
                "Format tanggal tidak valid, contoh format = '2020-12-01'"
            )


    def time_now():
        """Function to get current time with Asia/Jakarta time zone"""

        dt = datetime.strptime(
            datetime.now(tz=INDONESIA_TIMEZONE).strftime(DATETIME_FORMAT), DATETIME_FORMAT
        )
        return dt.time()


    def time_now_str():
        """Function to get current string time with Asia/Jakarta time zone"""

        dt = datetime.now(tz=INDONESIA_TIMEZONE).strftime(TIME_FORMAT)
        return dt


    def str_time_to_time(str_time: str):
        """Function to convert current string time to datetime time"""

        try:
            dt = datetime.strptime(str_time, TIME_FORMAT)
            return dt.time()
        except Exception as err:
            logger.warning(err)
            raise HTTPException(
                400,
                "Format waktu tidak valid, contoh format = '08:00:00'"
            )


    def datetime_now():
        """Function to get current datetime with Asia/Jakarta time zone"""

        dt = datetime.strptime(
            datetime.now(tz=INDONESIA_TIMEZONE).strftime(DATETIME_FORMAT), DATETIME_FORMAT
        )
        return dt


    def datetime_now_str():
        """Function to get current string time with Asia/Jakarta time zone"""

        dt = datetime.now(tz=INDONESIA_TIMEZONE).strftime(DATETIME_FORMAT)
        return dt


    def str_datetime_to_datetime(str_datetime: str):
        """Function to convert current string datetime to datetime"""

        try:
            dt = datetime.strptime(str_datetime, DATETIME_FORMAT)
            return dt
        except Exception as err:
            logger.warning(err)
            raise HTTPException(
                400,
                "Format waktu tidak valid, contoh format = '2020-12-01 08:00:00'"
            )


    def str_month_to_month(str_month: str):
        """Function to convert current string month to str month number"""

        start_with = str_month[0:3].lower()
        if start_with == "jan":
            return "01"
        elif start_with == "feb":
            return "02"
        elif start_with == "mar":
            return "03"
        elif start_with == "apr":
            return "04"
        elif start_with == "mei" or start_with == "may":
            return "05"
        elif start_with == "jun":
            return "06"
        elif start_with == "jul":
            return "07"
        elif start_with == "agu" or start_with == "aug":
            return "08"
        elif start_with == "sep":
            return "09"
        elif start_with == "okt" or start_with == "oct":
            return "10"
        elif start_with == "nov":
            return "11"
        elif start_with == "des" or start_with == "dec":
            return "12"


    # ===== Class

    # ===== Main
