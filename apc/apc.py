import threading
import time

import subprocess
import re
from datetime import datetime

from .db import Session, APCReading


class APC(object):
    def __init__(self):
        pass

    @property
    def ups_name(self):
        return self._ups_name

    @property
    def model(self):
        return self._model

    @property
    def date(self):
        return self._date

    @property
    def load_percent(self):
        return self._load_percent

    @property
    def nominal_power(self):
        return self._nominal_power

    @property
    def load(self):
        return self.nominal_power * self.load_percent / 100

    def reload(self):
        apc_subprocess = self._apc_subprocess()
        self._parse(apc_subprocess.stdout)

    def _apc_subprocess(self):
        return subprocess.run(["apcaccess"], capture_output=True)

    def _parse(self, apc_subprocess_stdout):
        fields = {
            "UPSNAME": lambda obj, x: setattr(obj, "_ups_name", x),
            "MODEL": lambda obj, x: setattr(obj, "_model", x),
            "DATE": lambda obj, x: setattr(
                obj, "_date", datetime.strptime(x, "%Y-%m-%d %H:%M:%S %z")
            ),
            "LOADPCT": lambda obj, x: setattr(
                obj, "_load_percent", float(x.split(" ")[0])
            ),
            "NOMPOWER": lambda obj, x: setattr(
                obj, "_nominal_power", int(x.split(" ")[0])
            ),
        }
        for row in apc_subprocess_stdout.decode("utf-8").strip().split("\n"):
            match = re.search("^([A-Z]+\s*[A-Z]+)\s*:\s(.*)$", row.strip())
            if match.group(1) in fields:
                fields[match.group(1)](self, match.group(2))

    def __repr__(self) -> str:
        return "APC(ups_name={}, model={}, date={}, load_percent={}, nominal_power={}, load={})".format(
            self.ups_name,
            self.model,
            self.date,
            self.load_percent,
            self.nominal_power,
            self.load,
        )


class Collector(threading.Thread):
    def __init__(self):
        super(Collector, self).__init__(target=self._collect, daemon=True)
        self.apc = APC()

    def _collect(self):
        while True:
            self.apc.reload()
            date = datetime(
                self.apc.date.year,
                self.apc.date.month,
                self.apc.date.day,
                hour=self.apc.date.hour,
                minute=0,
                second=0,
                microsecond=0,
            )
            with Session.begin() as session:
                existing_reading = (
                    session.query(APCReading).filter_by(date=date).one_or_none()
                )
                if existing_reading is None:
                    apc_reading = APCReading(
                        date=date,
                        no_logs=1,
                        load=self.apc.load,
                    )
                    session.add(apc_reading)
                else:
                    existing_reading.load = existing_reading.load + self.apc.load
                    existing_reading.no_logs = existing_reading.no_logs + 1
                    session.add(existing_reading)
            time.sleep(1)
