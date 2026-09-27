import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

client = Hindsight(
    base_url=os.getenv("HINDSIGHT_BASE_URL"),
    api_key=os.getenv("HINDSIGHT_API_KEY")
)

bank_id = os.getenv("HINDSIGHT_BANK_ID")

print("Connecting to Hindsight...")
print("Bank ID:", bank_id)

client.retain(
    bank_id=bank_id,
    content="Incident INC-001: Payment API returned HTTP 503 because the database connection pool was exhausted. Increasing the connection pool resolved the incident."
)

print("Memory retained successfully!")

result = client.recall(
    bank_id=bank_id,
    query="What previous incident involved HTTP 503 and database connection pool exhaustion?"
)

print("\nRecalled memories:")

for memory in result.results:
    print("-", memory.text)

print("\nHindsight connection test completed.")
client.close()