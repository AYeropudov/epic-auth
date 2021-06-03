from .local import ActivationService as ActivationSrvLocal
from .ya import ActivationService
from config import Config


def get_service():
    if Config.ACTIVATION_SERIVICE:
        return ActivationService
    return ActivationSrvLocal
