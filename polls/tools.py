import json
import urllib
from datetime import datetime
from calendar import monthrange

def get_answered_polls(request):
    if request.COOKIES.get('q_voted'):
        cookie_value = urllib.parse.unquote_plus(request.COOKIES['q_voted'])
        cookie_value = json.loads(cookie_value)
        answered_polls = [q_id for q_id in cookie_value['question_id']]
    else:
        answered_polls = []
    answered_polls = set(answered_polls)
    return answered_polls
 
def last_day_of_month(date_value=datetime.today()):
    end_of_month = date_value.replace(day = monthrange(date_value.year, date_value.month)[1])
    end_of_month = datetime(end_of_month.year, end_of_month.month, end_of_month.day, 23, 59, 59)
    return end_of_month
 