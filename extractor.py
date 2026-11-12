import ollama

def extract(narrative):
    prompt = (
        "Extract these fields from the incident report and reply with JSON only: "
        "incident_date, incident_time, location, units_responded, reporting_officer. "
        "If a field is not in the text, use null.\n\n"
        + narrative
    )
    response = ollama.chat(
        model="qwen2.5:3b",
        messages=[{"role": "user", "content": prompt}],
        format="json",
    )
    return response["message"]["content"]

if __name__ == "__main__":
    text = "At 2:30 PM on 12 March, a brush fire was reported near Pune Road. Two engines responded. No injuries."
    print(extract(text))