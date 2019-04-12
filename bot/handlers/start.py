import logging

from telegram.ext import CommandHandler
from telegram.ext import CallbackQueryHandler
from telegram import ParseMode

from bot import Plugins
from bot.markups import InlineKeyboard
from utilities import String
from config import config

logger = logging.getLogger(__name__)


@Plugins.add(CommandHandler, command=['start', 'help'])
def on_start_help(_, update):
    logger.debug('/start or /help')
    
    update.message.reply_text(String.START, reply_markup=InlineKeyboard.MORE_HELP)
    

@Plugins.add(CallbackQueryHandler, pattern=r'morehelp')
def on_more_help_button(_, update):
    logger.debug('more help inline button')
    
    update.callback_query.edit_message_text(
        String.MORE_HELP.format(source_code=config.vcs.source_code, issues_tracker=config.vcs.issues),
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboard.REDUCE_HELP,
        disable_web_page_preview=True
    )


@Plugins.add(CallbackQueryHandler, pattern=r'lesshelp')
def on_less_help_button(_, update):
    logger.debug('less help inline button')
    
    update.callback_query.edit_message_text(String.START, reply_markup=InlineKeyboard.MORE_HELP)
