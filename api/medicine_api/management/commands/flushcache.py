import redis
import logging
from django.conf import settings
from django.core.management.base import BaseCommand

logger = logging.getLogger('medicine_api.readers.cache_flushing')

class Command(BaseCommand):
    """
    Flushes the Redis cache.
    """
    help = 'Flushes the Redis cache.'

    def handle(self, *args, **options):
        logger.info(f'Cache flushing started.')
        if settings.REDIS_ENABLED:
            try:
                connection = self.__connect_to_cache()
            except Exception:
                logger.error(f'Could not connect to caching server.')
                return
            
            connection.flushdb()
            connection.close()

            logger.info(f'Cache flushing complete.')
            self.stdout.write(self.style.SUCCESS('Cache flushed'))
            return
        
        logger.warn(f'Caching disabled! No action taken.')
        self.stdout.write(self.style.WARNING('Cache disabled; bypassing flushing'))

    def __connect_to_cache(self):
        """
        Attempts to connect to the Redis cache, and returns the object if successful.
        Raises an exception if this fails.
        """
        redis_conn = redis.StrictRedis(host=settings.REDIS_HOSTNAME,
                                        port=settings.REDIS_PORT,
                                        db=0)
        redis_conn.exists('test')  # Forces the connection to establish; failures are captured from here.
        
        return redis_conn