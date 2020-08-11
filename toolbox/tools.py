import json
import urllib
from time import time
from datetime import datetime, timedelta
from calendar import monthrange
from functools import wraps
from django.utils import timezone
from django.db.models import Count


def measure(func):
    @wraps(func)
    def _time_it(*args, **kwargs):
        start = int(round(time() * 1000))
        try:
            return func(*args, **kwargs)
        finally:
            end_ = int(round(time() * 1000)) - start
            print(
                f"Total execution time of {func.__name__}: {end_ if end_ > 0 else 0} ms"
            )
    return _time_it


def get_answered_polls(request):
    if request.COOKIES.get("q_voted"):
        cookie_value = urllib.parse.unquote_plus(request.COOKIES["q_voted"])
        cookie_value = json.loads(cookie_value)
        answered_polls = [q_id for q_id in cookie_value["question_id"]]
    else:
        answered_polls = []
    answered_polls = set(answered_polls)
    return answered_polls


def last_day_of_month(date_value=datetime.today()):
    end_of_month = date_value.replace(
        day=monthrange(date_value.year, date_value.month)[1])
    end_of_month = datetime(end_of_month.year, end_of_month.month,
                            end_of_month.day, 23, 59, 59)
    return end_of_month


def get_ipaddress(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ipaddress = x_forwarded_for.split(",")[-1].strip()
    else:
        ipaddress = request.META.get("REMOTE_ADDR")
    return ipaddress


def get_popular(model_object, days=7, obj_number=5):
    period = timezone.now() - timedelta(days=days)
    try:
        popular_objects = (model_object.objects.filter(
            hitcount__hit__created__gte=period, status=1).annotate(
                counts=Count("hitcount__hit")).order_by("-counts")[:obj_number])
        return popular_objects
    except:
        print("Object does not have an associated hitcount")
        popular_objects = ()
        return popular_objects
