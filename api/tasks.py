from logging import getLogger
from celery import Task

from sesc_mate.celery import app
from api.services.cache.announcements import get_parsed_announcements

logger = getLogger('logdna')


@app.task(bind=True)
def announcements_polling(self: Task):
    try:
        announcements = get_parsed_announcements(True)
        logger.info(f'Successfully got {len(announcements)} announcement(s).', {
            'meta': {
                'announcements': announcements
            }
        })
        return 'OKAY'
    except Exception as e:
        logger.warning(f'Failed to parse announcements. Probably page is being generated.')
        logger.exception(e)
        self.retry(exc=e, max_retries=10, countdown=6)
