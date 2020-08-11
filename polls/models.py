import datetime

from django.db import models
from django.utils import timezone

from toolbox.plots import add_figure


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)
    on_focus = models.BooleanField(default=False)

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=6) <= self.created_on <= now

    def make_copy(self):
        choices = self.choice_set.all()
        self.pk = None
        self.save()
        for choice in choices:
            choice.question_id = self.id
            choice.pk = None
            choice.save()

    def update_created_on(self):
        self.created_on = timezone.now()
        self.save()

    def reset_votes(self):
        choices = self.choice_set.all()
        for choice in choices:
            choice.votes = 0
            choice.save()

    def update_figure(self):
        figures = self.plot_set.all()
        for figure in figures:
            # figure.graph = add_figure(self, figure.plot_type)
            figure.save()

    was_published_recently.admin_order_field = 'created_on'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Vote(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    voted_on = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(verbose_name="IP address",
                                              blank=True,
                                              null=True)
    country_code = models.CharField(max_length=2, blank=True, null=True)
    country_name = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        ordering = ['-voted_on']


TYPE = ((0, "Linear"), (1, "Histogram"))


class Plot(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    figure = models.TextField(blank=True, default='Figure placeholder')
    created_on = models.DateTimeField(auto_now_add=True)
    plot_type = models.IntegerField(choices=TYPE, default=1)
    allow_updates = models.BooleanField(default=True)
    carousel = models.BooleanField(default=False)

    def __str__(self):
        return str(self.question.question_text)

    def save(self, *args, **kwargs):
        if self.figure == 'Figure placeholder' or self.allow_updates:
            self.figure = str(add_figure(self.question, self.plot_type))
        super(Plot, self).save(*args, **kwargs)
