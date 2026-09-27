from hindsight_memory import remember_incident, recall_similar_incidents


incident = {
    "id": "INC-TEST-001",
    "problem": "Payment API returned HTTP 503 errors",
    "diagnosis": "Database connection pool was exhausted",
    "action": "Increased the database connection pool from 50 to 150",
    "outcome": "RESOLVED",
    "lesson": "For similar 503 errors, check database connection pool exhaustion before restarting the service."
}


print("Storing incident in Hindsight...")

remember_incident(incident)

print("Incident stored successfully!")

print("\nSearching Hindsight for similar incidents...")

memories = recall_similar_incidents(
    "Payment API HTTP 503 database connection pool exhaustion"
)

print("\nRelevant memories:")

for memory in memories:
    print("\n---")
    print(memory)