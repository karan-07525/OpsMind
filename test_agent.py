from agent import analyze_incident

incident = {
    "service": "Checkout API",
    "problem": "Intermittent HTTP 503 errors",
    "symptoms": "Requests fail during periods of high traffic and the service becomes slow before returning 503 responses."
}

print("Analyzing incident...\n")

result = analyze_incident(incident)

print(result)