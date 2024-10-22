import logging
from django.dispatch import Signal

user_blocked_signal = Signal()
logger = logging.getLogger(__name__)


def log_user_blocked(sender, **kwargs):
    ip = kwargs.get("ip")
    block_time = kwargs.get("block_time")
    logger.warning(f"IP {ip} has been blocked for {block_time} seconds.")


user_blocked_signal.connect(log_user_blocked)
