from math import isfinite
from statistics import median

def analyze(data):
    def measurement(value):
        if type(value) not in (int, float) or not isfinite(value) or value < 0:
            raise ValueError("Measure sweetness and firmness with nonnegative finite numbers")
        return value
    sweet_min, firm_max = (measurement(data[key]) for key in ("sweet_min", "firm_max"))
    samples = data["samples"]
    if not isinstance(samples, list) or not samples:
        raise ValueError("Enter at least one sample")
    ready, rest, sweetness, firmness = [], [], [], []
    identifiers = set()
    for tag, sweet, firm in samples:
        if not isinstance(tag, str) or not tag.strip() or tag in identifiers:
            raise ValueError("Sample IDs must be unique nonempty strings")
        identifiers.add(tag)
        sweetness.append(measurement(sweet))
        firmness.append(measurement(firm))
        (ready if sweet >= sweet_min and firm <= firm_max else rest).append(tag)
    return {"ready":ready, "rest":rest, "median_sweetness":median(sweetness), "median_firmness":median(firmness)}

if __name__ == "__main__":
    import json
    from pathlib import Path
    import sys
    try:
        path, = sys.argv[1:]
        result = analyze(json.loads(Path(path).read_text(encoding="utf-8")))
        print(json.dumps(result, ensure_ascii=True, allow_nan=False))
    except (OSError, ValueError, TypeError, KeyError, AttributeError, OverflowError) as error:
        print(f"Invalid input: {error}", file=sys.stderr)
        sys.exit(2)
