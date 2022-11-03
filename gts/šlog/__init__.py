import logging
from datetime import datetime
import hashlib


class _Infarkt(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        level = record.levelname
        while len(level) < 7:
            level = " " + level

        line_number = str(record.lineno)
        while len(line_number) < 4:
            line_number += " "

        name_hash = hashlib.sha1(record.name.encode(encoding='utf-8')).hexdigest()[:10]

        function_name = record.funcName
        while len(function_name) < 15:
            if function_name[len(function_name) - 1] != '—':
                function_name += " "
                pass
            function_name += "—"
        if len(function_name) > 15:
            function_name = function_name[:14] + " "

        return (f"[{datetime.now().strftime('%H:%M:%S,%f')}] {level} : {name_hash} "
                f"@l {line_number} @f {function_name}→ {record.msg}")


def configure(name: str) -> logging.Logger:

    # creating the logfile if it doesn't exist
    logfile = f"šlog/logs/{str(datetime.now().date())}.log"
    file = open(file=logfile, mode='a')
    if name == 'gts':
        file.write("\n")
    file.close()

    # creating the Logger Handler
    handler = logging.FileHandler(
        filename=logfile,
        mode="a",
        encoding="utf-8"
    )
    handler.setFormatter(_Infarkt())  # setting the Infarkt formatter

    # creating the Logger
    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # logging the Logger name hash
    logger.info(
        f"< {hashlib.sha1(logger.name.encode(encoding='utf-8')).hexdigest()[:10]} = {logger.name} >"
    )
    return logger
