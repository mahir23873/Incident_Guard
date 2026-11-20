import sys
import json
from extractor import extract
from validator import validate_incident, print_report

narrative = sys.argv[1]

raw = extract(narrative)
data = json.loads(raw)

report = validate_incident(data)
print_report(report)