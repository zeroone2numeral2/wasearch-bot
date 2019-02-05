import logging

from telegram.ext import MessageHandler
from telegram.ext import Filters

from bot import Plugins
from database.models import Anime
from utilities import String
from utilities import utilities as u
from config import config

logger = logging.getLogger(__name__)


@Plugins.add(MessageHandler, filters=Filters.text)
def on_command(bot, update):
    logger.debug('new search query')
    
    query = update.message.text
    if len(query) < 3:
        update.message.reply_html(String.QUERY_TOO_SHORT)
        return
    
    result = Anime.search(query, group_by_category=True)
    if not result:
        update.message.reply_html(String.ANIME_NOT_FOUND.format(query=query, issues_tracker=config.vcs.issues),
                                  disable_web_page_preview=True)
        return
    
    text = ''
    for category in result.keys():
        text += '\n\n<b>{}</b> ({})'.format(category, len(result[category]))
        for anime in result[category]:
            text += '\n• <a href="{url}">{title}</a>'.format(title=u.html_escape(anime[0]), url=anime[1])
            
    update.message.reply_html(text, disable_web_page_preview=True)
