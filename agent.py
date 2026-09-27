import os
from dotenv import load_dotenv
from groq import Groq

from hindsight_memory import recall_similar_incidents

load_dotenv()

groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def analyze_incident(incident):

    query = f"""
Current production incident:

Service: {incident['service']}
Problem: {incident['problem']}
Symptoms: {incident['symptoms']}

Find previous incidents related to this problem.
Pay special attention to:
- successful fixes
- failed fixes
- lessons learned
"""

    memories = recall_similar_incidents(query)

    memory_text = "\n\n".join(memories)

    prompt = f"""
You are OpsMind, an engineering incident-response assistant.

You help engineers diagnose production incidents using
long-term experience retrieved from Hindsight memory.

CURRENT INCIDENT
----------------
Service: {incident['service']}
Problem: {incident['problem']}
Symptoms: {incident['symptoms']}


PAST EXPERIENCE FROM HINDSIGHT
------------------------------
{memory_text}


IMPORTANT REASONING RULES
-------------------------

1. Use the past incidents as evidence, not as absolute truth.

2. Identify successful approaches.

3. Identify failed approaches.

4. Never recommend a previously failed action as the first choice
   when the memory shows that it failed under similar circumstances.

5. Prefer lessons supported by multiple relevant memories.

6. Do not blindly copy an old solution.

7. Clearly state uncertainty when the evidence is incomplete.


Return your answer using EXACTLY these sections:


🧠 MEMORY EVIDENCE

✅ Successful Experience:
<describe relevant successful past experience>

❌ Failed Experience:
<describe relevant failed past experience>


🔎 DIAGNOSIS

<most likely explanation for the current incident>


🎯 RECOMMENDED ACTION

<what the engineer should investigate or do>


💡 WHY OPSMIND RECOMMENDS THIS

<explain how the past successful and failed experiences influenced
the recommendation>


⚠️ RISK / CAUTION

<what should not be done blindly>


CONFIDENCE

<Low / Medium / High>
"""

    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a careful production "
                    "incident-response assistant."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content