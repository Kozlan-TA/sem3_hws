import json
import sys

import yaml


# Threshold from params.yaml
def load_params():
    with open("params.yaml", "r") as f:
        return yaml.safe_load(f)


# Load accuracy from metrics.json
def load_metrics():
    with open("metrics/metrics.json", "r") as f:
        return json.load(f)


params = load_params()
metrics = load_metrics()

accuracy_min = params.get("accuracy_min", 0.9)
accuracy = metrics.get("accuracy", None)


if accuracy < accuracy_min:
    sys.exit(1) # просто сделал != 0 если не проходит по минимуму (поставил 0.8 в params)
else:
    sys.exit(0)