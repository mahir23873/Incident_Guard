🛡️ incident-guard

Don't trust the AI blindly. Validate it.✅

A beginner-friendly Python tool that takes an incident report written in plain English, asks a local AI model to extract the key details, and then checks the AI's answer for missing, wrong, or invented information.

🤔 Why does this project exist?

AI models are great at reading messy text, but they sometimes:

🕳️ Leave fields empty without telling you.

📅 Return impossible dates like 31 February.

📞 Produce broken phone numbers.

👻 Invent details that were never in the text (hallucinations).

In serious situations, like emergency-response paperwork, a silent mistake can cause real trouble.

'incident-guard' sits between the AI and your final output and reports exactly what is wrong instead of quietly accepting it.

✨ Planned Features

🔌 Talk to a local Ollama model (no internet or paid API needed)

🧱 Define the expected fields using a Pydantic schema

🔍 Detect missing required fields

📅 Detect invalid dates and malformed phone numbers

👻 Detect unexpected keys the model made up

🧪 A test suite with fake incident narratives

🤝 Contributing 
Suggestions and ideas are welcome! Open an issue to discuss a change before sending a pull request. 💬

⭐ If you find this project interesting, consider giving it a star! 
