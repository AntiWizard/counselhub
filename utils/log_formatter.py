import json
import logging


class ConsoleFormatter(logging.Formatter):
    def format(self, record):
        pieces = [record.levelname, record.getMessage()]

        if hasattr(record, "additional_data"):
            additional_data = json.loads(getattr(record, "additional_data"))
            for k, v in additional_data.items():
                if not v:
                    continue
                pieces.append(f"{k}={v}")

        return " | ".join(pieces)
