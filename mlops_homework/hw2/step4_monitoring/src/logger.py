from colorama import Fore, Style
import os
import json
from datetime import datetime, timezone


def print_alert(text, level):
    if level == "green":
        print(Fore.GREEN + text + Style.RESET_ALL)
    elif level == "yellow":
        print(Fore.YELLOW + text + Style.RESET_ALL)
    elif level == "red":
        print(Fore.RED + text + Style.RESET_ALL)
    else:
        print(text)


class JSONLogger:
    def __init__(self, log_dir="logs/"):
        os.makedirs(log_dir, exist_ok=True)
        self.log_file = os.path.join(log_dir, "app.log")
        self.metrics_file = os.path.join(log_dir, "metrics.jsonl")

    def log(self, level, message, **kwargs):
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            "level": level,
            "message": message
        }
        entry.update(kwargs)
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        print(f"Log written: {entry}")  # Отладка записи

    def log_metric(self, metric_name, value, **kwargs):
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            "metric": metric_name,
            "value": value
        }
        entry.update(kwargs)
        with open(self.metrics_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        print(f"Metric log written: {entry}")  # Отладка записи