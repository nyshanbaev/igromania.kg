from celery import Celery
from time import sleep
from applications.news.management.commands.parser import news, news2
from celery import shared_task
app = Celery('tasks', broker='redis://localhost:6379/0')



@shared_task
def run_parser():
    news()
    news2()
