from datetime import date, datetime, timedelta

class LessonMixin:
    dateformat = '%d %B %Y'
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @staticmethod
    def get_the_range_of_the_week(_date):
        while _date.weekday() != 0:
            _date -= timedelta(days=1)
        return _date, _date + timedelta(days=5)

    def get_the_range_of_the_week_str(self, _date):
        start_day, end_day = self.get_the_range_of_the_week(_date)
        return start_day.strftime(self.dateformat) + ' - ' + end_day.strftime(self.dateformat)

    @staticmethod
    def get_date_from_query_params(request):
        _date = request.GET.get('date', default=date.today())
        if isinstance(_date, str):
            _date = datetime.strptime(_date, "%Y-%m-%d").date()
            return _date
        return _date

    def get_days(self, _date):
        days = []
        start_day, end_day = self.get_the_range_of_the_week(_date)
        while start_day <= end_day:
            days.append(start_day)
            start_day += timedelta(days=1)
        return days

    @staticmethod
    def get_class_time():
        time_ranges_of_classes = [
            '8:45-10:20',
            '10:35-12:10',
            '12:25-14:00',
            '14:45-16:20',
            '16:35-18:10',
            '18:25-20:00',
            '20:15-21:50',
        ]
        class_time = []
        dateformat = '%H:%M'
        for time_range in time_ranges_of_classes:
            start, end = time_range.split('-')
            class_time.append({
                'start' : datetime.strptime(start, dateformat).time(),
                'end': datetime.strptime(end, dateformat).time()
            })
        return class_time
