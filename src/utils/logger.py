import logging
from enum import Enum
from logging.handlers import RotatingFileHandler


class LogMessages(Enum):
    """
    Enum pour les messages de log.
    """

    DEBUG_MESSAGE = "Debut de la fonction"
    SUCCESS_QUERY_MESSAGE = "Requeete effectuee avec_succes"
    ERRUER_QUERY_MESSAGE = "Une erreur est survenue lors de l'execution de la requete: "


logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)

file_handler = RotatingFileHandler("app.log", maxBytes=1000000, backupCount=1)
file_handler.setFormatter(
    logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
)
logger.addHandler(file_handler)


