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
NAME_SEP_2 = ' | '  # porcoddio porcalamadonna porco quello storpio di gesù incalcato


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
            a_all = li.find_all('a', href=True)
            
            i = 0
            for a in a_all:
                if li.text and '/t.me/' in a['href'].lower():
                    name = u.strip_emojis(li.text).strip().replace(' | TV', '')
                    
                    if len(a_all) > 1:
                        # può essere che l'elemento <li> nella lista contenga più link nella stessa riga (es. db super)
                        # se è così, allora contiamo quanti <a> vengono contati in a_all. Se sono più di uno, splittiamo
                        # la stringa (li.text, nome dell'anime) in due in corrispondenza del ' | '
                        
                        logger.info('two (or more) <a> tags in the same list element <li>: splitting "%s" at "%s"...', name, NAME_SEP_1)
                        name = u.split_li_item(name, index=i)
                        logger.info('...anime name post-split: %s', name)
                    
                    logger.info('upserting: %s', name)
                    Anime.upsert({
                        'name': name,
                        'url': a['href'],
                        'category': section.description
                    })
                    
                    i += 1
        
        time.sleep(config.jobs.requests_cooldown)
