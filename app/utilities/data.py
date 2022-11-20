import json
from dataclasses import dataclass
from enum import Enum

@dataclass
class Application:
    """
    Parameters
    ----------
    id : int
        The id of the application
    type : json
        The type of the application
    notifications : json
        Notifications for the application
    
    Returns
    -------
    Application
        The application
    """
    id: int
    type: json
    notifications: json

@dataclass
class User:
    """
    Parameters
    ----------
    id : int
        The id of the user
    applications : json
        The applications the user has
    """
    id: int
    applications: json

class notificationType(Enum):
    """
    Supported types of notifications

    Returns
    -------
    notificationType
        The notification type
    """
    WEBHOOK = "WEBHOOK"
    EMAIL = "EMAIL"
    DISCORD_DM = "DISCORD_DM"
    DISCORD_CHANNEL = "DISCORD_CHANNEL"
    SMS = "SMS"