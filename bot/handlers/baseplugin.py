import logging

from telegram.ext import CommandHandler

from bot import Plugins

logger = logging.getLogger(__name__)


@Plugins.add(CommandHandler, command=['command'])
def on_command(bot, update):
    logger.debug('/command from %s', update.effective_user.id)
    update.message.reply_text('.')
