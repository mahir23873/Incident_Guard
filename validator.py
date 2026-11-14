from datetime import datetime
from pydantic import ValidationError
from schema import Incident

DATE_FORMATS = ["%d %B %Y", "%Y-%m-%d", "%d/%m/%Y"]
TIME_FORMATS = ["%I:%M %p", "%H:%M"]


def is_valid_date(value):
    # "12 March" has no year, so add a leap year (2000) to allow 29 February
    if is_valid(value + " 2000", ["%d %B %Y"]):
        return True
    return is_valid(value, DATE_FORMATS)


def is_valid(value, formats):
    for f in formats:
        try:
            datetime.strptime(value, f)
            return True
        except ValueError:
            pass
    return False


def validate_incident(data):
    report = {"valid": [], "missing": [], "invalid": {}, "unexpected": []}
    expected = Incident.model_fields

    # 1. invented keys
    for key in data:
        if key not in expected:
            report["unexpected"].append(key)

    # 2. drop invented keys and nulls (null counts as missing)
    clean = {}
    for key in data:
        if key in expected and data[key] is not None:
            clean[key] = data[key]

    # 3. schema check
    try:
        Incident(**clean)
    except ValidationError as e:
        for err in e.errors():
            field = err["loc"][0]
            if err["type"] == "missing":
                report["missing"].append(field)
            else:
                report["invalid"][field] = err["msg"]

    # 4. real date/time check
    if "incident_date" in clean and "incident_date" not in report["invalid"]:
        if not is_valid_date(clean["incident_date"]):
            report["invalid"]["incident_date"] = "not a real date"
    if "incident_time" in clean and "incident_time" not in report["invalid"]:
        if not is_valid(clean["incident_time"], TIME_FORMATS):
            report["invalid"]["incident_time"] = "could not be parsed"

    # 5. everything else is valid
    for field in expected:
        if field not in report["missing"] and field not in report["invalid"]:
            report["valid"].append(field)

    return report


def print_report(report):
    for field in report["valid"]:
        print("VALID      ", field)
    for field in report["missing"]:
        print("MISSING    ", field)
    for field, msg in report["invalid"].items():
        print("INVALID    ", field, "-", msg)
    for key in report["unexpected"]:
        print("UNEXPECTED ", key)