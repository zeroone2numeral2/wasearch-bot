import peewee
import datetime

from ..database import db

from playhouse.shortcuts import model_to_dict


class Anime(peewee.Model):
    anime_id = peewee.IntegerField(primary_key=True)  # corrisponde a "codCinemaVista"
    name = peewee.CharField(null=False, unique=True)
    url = peewee.CharField(null=True)
    category = peewee.CharField(null=True)
    updated_on = peewee.DateTimeField(null=True, default=datetime.datetime.now)

    class Meta:
        table_name = 'animes'
        database = db
        indexes = (
            (('anime_id', 'name'), True),
        )

    def __repr__(self):
        return '<Anime: {}>'.format(self.name)

    @classmethod
    def to_dict(cls):
        return model_to_dict(cls)

    @classmethod
    def upsert(cls, anime_dict):
        # upsert: http://docs.peewee-orm.com/en/latest/peewee/querying.html#upsert
        cls.replace(**anime_dict).execute()

    @classmethod
    def search(cls, query, as_dicts=False, limit=96, group_by_category=False):
        try:
            animes = (
                cls.select(cls.name, cls.url, cls.category)
                .where(cls.name ** '%{}%'.format(query))
                .order_by(cls.category, cls.name)
                .limit(limit)
            )
        except peewee.DoesNotExist:
            return None
        
        if as_dicts:
            return animes.dicts()
        
        if group_by_category:
            result_dict = dict()
            for anime in animes:
                if not result_dict.get(anime.category, None):
                    result_dict[anime.category] = [(anime.name, anime.url)]
                else:
                    result_dict[anime.category].append((anime.name, anime.url))
            return result_dict
        
        return animes
    
