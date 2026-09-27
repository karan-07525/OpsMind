import os
import asyncio

from dotenv import load_dotenv
from hindsight_client import Hindsight


load_dotenv()


BANK_ID = os.getenv("HINDSIGHT_BANK_ID")
BASE_URL = os.getenv("HINDSIGHT_BASE_URL")
API_KEY = os.getenv("HINDSIGHT_API_KEY")


def ensure_event_loop():
    """
    Make sure the current thread has an open asyncio event loop.
    Streamlit can rerun code after a previous loop has been closed.
    """

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    return loop


def create_client():
    ensure_event_loop()

    return Hindsight(
        base_url=BASE_URL,
        api_key=API_KEY
    )


def remember_incident(incident):

    client = create_client()

    try:
        content = f"""
Incident ID: {incident['id']}
Problem: {incident['problem']}
Agent Diagnosis: {incident['diagnosis']}
Engineer Action: {incident['action']}
Outcome: {incident['outcome']}
Lesson: {incident['lesson']}
"""

        client.retain(
            bank_id=BANK_ID,
            content=content
        )

    finally:
        client.close()


def recall_similar_incidents(query):

    client = create_client()

    try:
        result = client.recall(
            bank_id=BANK_ID,
            query=query
        )

        return [
            memory.text
            for memory in result.results
        ]

    finally:
        client.close()


def learn_from_outcome(
    incident_id,
    action,
    outcome,
    lesson
):

    client = create_client()

    try:
        content = f"""
Incident ID: {incident_id}
Engineer Action: {action}
Outcome: {outcome}
Lesson Learned: {lesson}
"""

        client.retain(
            bank_id=BANK_ID,
            content=content
        )

    finally:
        client.close()


def get_hindsight_memories(query):

    client = create_client()

    try:
        result = client.recall(
            bank_id=BANK_ID,
            query=query
        )

        return [
            memory.text
            for memory in result.results
        ]

    finally:
        client.close()