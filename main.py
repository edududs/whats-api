# pyright: reportMissingTypeStubs=false
import logging
import os
from typing import Any, List, cast

import requests  # type: ignore
from dotenv import load_dotenv

from evolution_types import Group, Message

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


load_dotenv()

AUTHENTICATION_API_KEY = os.getenv("AUTHENTICATION_API_KEY", "xyz")
URL = os.getenv("EVO_URL", "http://localhost:8080")
INSTANCE = os.getenv("EVO_INSTANCE", "carpool")
DEFAULT_TIMEOUT_SECONDS = 60

HEADERS = {
    "apikey": AUTHENTICATION_API_KEY,
    "Content-Type": "application/json",
}


def get_information() -> Any:
    """Fetch Evolution API root information."""
    response = requests.get(f"{URL}", timeout=DEFAULT_TIMEOUT_SECONDS)
    response.raise_for_status()
    return response.json()


def get_connection_state(instance: str = INSTANCE, url: str = URL) -> Any:
    """Get connection state for the given instance."""
    url = f"{url}/instance/connectionState/{instance}"
    response = requests.get(url, headers=HEADERS, timeout=DEFAULT_TIMEOUT_SECONDS)
    response.raise_for_status()
    return response.json()


def find_chats(url: str = URL, instance: str = INSTANCE) -> list[dict[str, Any]]:
    """Find chats for the configured instance."""
    api = f"{url}/chat/findChats/{instance}"
    response = requests.get(api, headers=HEADERS, timeout=DEFAULT_TIMEOUT_SECONDS)
    response.raise_for_status()
    return cast("list[dict[str, Any]]", response.json())


def find_messages(
    remote_jid: str,
    url: str = URL,
    instance: str = INSTANCE,
) -> List[Message]:
    """Search messages in a group.

    POST /chat/findMessages/{instance}

    Docs: https://doc.evolution-api.com/v1/api-reference/chat-controller/find-messages
    """
    api = f"{url}/chat/findMessages/{instance}"
    payload = {
        "where": {
            "key": {
                "remoteJid": remote_jid,
            },
        },
        "limit": 10000,
    }
    response = requests.post(
        api,
        headers=HEADERS,
        json=payload,
        timeout=DEFAULT_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    data: list[Message] = response.json()
    logger.debug("Fetched %d messages for %s", len(data), remote_jid)

    messages: list[Message] = []
    for message in data:
        message_content = message.get("message")
        if not message_content:
            continue
        sender = message_content.get("senderKeyDistributionMessage")
        if not sender:
            continue
        if sender["groupId"] == remote_jid:
            messages.append(message)
    logger.debug("Filtered to %d group messages for %s", len(messages), remote_jid)
    return messages


def send_message(
    message: str,
    number: str,
    url: str = URL,
    instance: str = INSTANCE,
) -> Any:
    """Send a text message to a phone number."""
    api = f"{url}/message/sendText/{instance}"
    payload = {
        "number": number,
        "textMessage": {"text": message},
    }
    response = requests.post(
        api,
        headers=HEADERS,
        json=payload,
        timeout=DEFAULT_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    return response.json()


def get_all_groups(url: str, instance: str) -> "list[Group]":
    """Fetch all groups for an instance."""
    api = f"{url}/group/fetchAllGroups/{instance}"
    params = {"getParticipants": "true"}
    response = requests.get(
        api,
        headers=HEADERS,
        params=params,
        timeout=DEFAULT_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    return cast("list[Group]", response.json())


def get_carpool_groups(groups: list[Group] | None = None) -> List[Group]:
    """Filter groups that likely relate to carpool topics."""
    if not groups:
        groups = get_all_groups(URL, INSTANCE)
    words = ["carona", "rota", "solidaria", "solidária", "vagas"]
    exclude_words = ["LDO"]
    words_cf = [w.casefold() for w in words]
    exclude_cf = [w.casefold() for w in exclude_words]
    return [
        group
        for group in groups
        if (subject := group.get("subject", "").casefold())
        and any(word in subject for word in words_cf)
        and not any(word in subject for word in exclude_cf)
    ]


def main() -> None:
    """Entry point for basic connectivity check and sample listing."""
    try:
        chats = find_chats()
        logger.info("Found %d chats", len(chats) if isinstance(chats, list) else 0)
    except requests.HTTPError as exc:  # pragma: no cover - basic CLI handling
        logger.error("HTTP error while fetching chats: %s", exc)
    except requests.RequestException as exc:  # pragma: no cover
        logger.error("Network error while fetching chats: %s", exc)


if __name__ == "__main__":
    main()
