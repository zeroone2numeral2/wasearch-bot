import logging

from database import db
from .models import Anime
logger = logging.getLogger(__name__)


def create_tables():
    with db:
        db.create_tables([Anime])


logger.info('initializing database...')
create_tables()
