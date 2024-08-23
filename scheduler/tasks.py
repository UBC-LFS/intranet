from django.conf import settings
from apscheduler.schedulers.background import BackgroundScheduler

from blog.views import get_data

def run():
    print('Scheduling tasks running...')
    scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)

    # Run it every day at 2 AM
    scheduler.add_job(get_data, 'cron', hour=2, minute=5)

    scheduler.start()