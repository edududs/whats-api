from typing import TypedDict


class Group(TypedDict):
    id: str
    subject: str
    subject_owner: str
    subject_time: str
    picture_url: str
    owner: str
    participants: list[str] | None
    description: str | None
    creation: str | None
    restrict: bool


class MessageKey(TypedDict):
    """WhatsApp message key containing identifiers."""

    remoteJid: str
    fromMe: bool
    id: str
    participant: str | None


class MessageTimestamp(TypedDict):
    """Message timestamp structure."""

    low: int
    high: int
    unsigned: bool


class DisappearingMode(TypedDict):
    """Configuration for disappearing messages."""

    initiator: str
    trigger: str
    initiatedByMe: bool | None


class ContextInfo(TypedDict):
    """Message context information."""

    forwardingScore: int | None
    isForwarded: bool | None
    expiration: int | None
    disappearingMode: DisappearingMode | None


class ExtendedTextMessage(TypedDict):
    """Extended text message content."""

    text: str
    matchedText: str | None
    previewType: str | None
    contextInfo: ContextInfo | None
    inviteLinkGroupTypeV2: str | None


class SenderKeyDistributionMessage(TypedDict):
    """Sender key distribution for encryption."""

    groupId: str
    axolotlSenderKeyDistributionMessage: str


class MessageContent(TypedDict):
    """Main message content container."""

    extendedTextMessage: ExtendedTextMessage | None
    senderKeyDistributionMessage: SenderKeyDistributionMessage | None
    # Add other message types as needed (imageMessage, stickerMessage, etc.)


class DeviceListMetadata(TypedDict):
    """Device list metadata for encryption."""

    senderKeyHash: str | None
    senderTimestamp: str | None
    recipientKeyHash: str | None
    recipientTimestamp: str | None


class MessageContextInfo(TypedDict):
    """Message context information for encryption."""

    deviceListMetadata: DeviceListMetadata | None
    deviceListMetadataVersion: int | None
    messageSecret: str


class Message(TypedDict):
    """WhatsApp message structure from Evolution API."""

    key: MessageKey
    pushName: str
    message: MessageContent
    contextInfo: ContextInfo | None
    messageType: str
    messageTimestamp: int | MessageTimestamp
    owner: str
    source: str
    messageContextInfo: MessageContextInfo | None
