incident-guard

Extract details from an incident report with a local LLM, then check the result before trusting it.

incident-guard takes an incident report written in plain English and asks a local model (Ollama, qwen2.5:3b) to pull out five key fields as JSON. It then validates that JSON and reports what is missing, invalid, or unexpected.

This is an independent learning project, inspired by FireForm, an open-source "report once, file everywhere" system for first responders. FireForm extracts incident data with a local LLM. incident-guard explores one narrow question: can we trust that extraction? It is not affiliated with FireForm.

Why it exists

Language models read messy text well, but they can:

leave fields empty without saying so
return impossible dates such as 31 February
invent details that were never in the text

In emergency-response paperwork, a silent mistake like that can cause real problems. incident-guard sits between the model and the final output and lists exactly what is wrong instead of accepting it quietly.

How it works
Incident narrative (plain text)
        |
        v
Local LLM via Ollama  ->  raw JSON
        |
        v
Validation (Pydantic schema + custom checks)
        |
        v
Report: valid | missing | invalid | unexpected

Fields extracted (all required):

Field	Type
incident_date	string
incident_time	string
location	string
units_responded	integer
reporting_officer	string

What the validator reports:

Missing: a required field is absent or null.
Invalid: a field has the wrong type, an impossible date, or an impossible time. Three date formats and two time formats are accepted, and leap years are handled ("29 February" passes in a leap year, "31 February" fails).
Unexpected: the model returned a key that is not in the schema.
Status

Stages 1 to 3 are done. Stage 4 (automated tests) is in progress.

[x] Stage 1, Extract: send a narrative to Ollama and get JSON back
[x] Stage 2, Schema: define the expected fields with Pydantic
[x] Stage 3, Validate: report missing, invalid, and unexpected fields
[ ] Stage 4, Test: write 10-15 fake narratives and pytest tests

What has been tested so far: a small number of hand-written narratives in data/ (test1.txt, test2.txt), run manually. Bad input produced the expected valid / missing / invalid / unexpected report. There are no automated tests yet and no accuracy figures, so no claim is made about how often the model gets things right.

Installation

Requires Python 3.10+ and Ollama.

bash
# 1. Clone the repo
git clone https://github.com/<your-username>/Incident_Guard.git
cd Incident_Guard

# 2. Create and activate a virtual environment
python -m venv venv
source venv/Scripts/activate      # Git Bash on Windows
# source venv/bin/activate        # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Pull the model
ollama pull qwen2.5:3b
Usage

Pass the narrative as a command-line argument:

bash
python main.py "At 2:30 PM on 12 March, a brush fire was reported near Pune Road. Two engines responded. No injuries."

Or read it from a file:

bash
python main.py "$(cat data/test2.txt)"

The output lists each field under VALID, MISSING, INVALID, or UNEXPECTED.

Project structure
Incident_Guard/
├── main.py           # entry point: reads narrative, runs extract + validate
├── extractor.py      # extract(narrative): calls Ollama, returns JSON string
├── schema.py         # Incident model (Pydantic)
├── validator.py      # validate_incident() and print_report()
├── data/             # fake incident narratives
├── tests/            # pytest tests (Stage 4)
├── requirements.txt
└── README.md

The extraction prompt tells the model not to invent values, to use null for anything missing, and to return units_responded as a whole number. The call uses format="json" and temperature 0.

Known limitations
The validator only sees the JSON, not the original narrative. If the model "fixes" a bad date (for example, returns a real date for "31 February") or invents a plausible value, the validator cannot tell.
Model output can vary between runs. A 3B model is not fully consistent, so tests that call the real model may be flaky.
location is a plain string. The model may return text like "near Pune Road".
main.py does not stop on an empty narrative.
Future work
Check each extracted value against the original narrative.
Reject empty input in main.py.
Tighten the location check.
Test the validator with hand-written dicts so tests do not depend on the model.
Tech stack
Tool	Purpose
Python	Core language
Ollama (qwen2.5:3b)	Runs the LLM locally, free
Pydantic	Schema and validation
pytest	Automated testing
Git and GitHub	Version control
Contributing

Suggestions are welcome. Please open an issue to discuss a change before sending a pull request.

License

Released under the MIT License.