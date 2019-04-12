import logging
import time
import datetime
import requests
from collections import namedtuple
from pprint import pprint

from bs4 import BeautifulSoup

from bot import Jobs
from ..jobregistration import RUNNERS
from database.models import Anime
from utilities import utilities as u
from config import config

logger = logging.getLogger(__name__)


Section = namedtuple('Section', ['url_path', 'description'])

BASE_URL = 'https://watchfamily.wordpress.com/liste-anime/lista-anime/'
SECTIONS = [
    Section('lista-anime', 'anime'),
    Section('lista-film-anime', 'movie'),
    Section('lista-streaming', 'streaming'),
    Section('lista-cartoon', 'cartoon')
]
NAME_SEP_1 = ' | '


def process_li(li, section):
    a_all = li.find_all('a', href=True)

    i = 0
    for a in a_all:
        if li.text and '/t.me/' in a['href'].lower():
            logger.info('>>> processing list line  <%s>, <a> tag: %d/%d', li.text, i + 1, len(a_all))
            name = u.strip_emojis(li.text).strip().replace(' | TV', '').replace(' | TV', '')
            # per alcuni motivi, uno (o più) anime della lista hanno la stringa ' | TV' codificata in modo diverso
            # (notato con l'anime Dungeon ni Deai wo Motomeru no wa Machigatte Iru Darou ka?), quindi
            # dobbiamo fare il replace di entrambe
            # logger.info('%s', str(' | TV' == ' | TV'))  # il secondo è preso da un file di log. La if ritorna False

            if len(a_all) > 1:
                # può essere che l'elemento <li> nella lista contenga più link nella stessa riga (es. db super)
                # se è così, allora contiamo quanti <a> vengono contati in a_all. Se sono più di uno, splittiamo
                # la stringa (li.text, nome dell'anime) in due in corrispondenza del ' | '

                logger.info(
                    '%d <a> tags in the same list element <li>: splitting "%s" at character "%s"...',
                    len(a_all),
                    name,
                    NAME_SEP_1
                )
                name = u.split_li_item(name, index=i)
                logger.info('...anime name post-split: %s', name)

            logger.info('upserting: %s', name)
            Anime.upsert({
                'name': name,
                'url': a['href'],
                'category': section.description
            })

            i += 1


@Jobs.add(RUNNERS.run_daily, time=datetime.time(hour=4, minute=0))
# @Jobs.add(RUNNERS.run_repeating, interval=5000, first=0)
def populate_db(bot, job):
    logger.info('starting job')
    
    for section in SECTIONS:
        url = '{}{}/'.format(BASE_URL, section.url_path)
        
        logger.info('executing request for url %s', url)
        result = requests.get(url)
    
        soup = BeautifulSoup(result.text, features='html.parser')

        for li in soup.find_all('li'):
            try:
                process_li(li, section)
            except Exception as e:
                logger.error('error while processing <li> element: %s', str(e), exc_info=True)
        
        time.sleep(config.jobs.requests_cooldown)
