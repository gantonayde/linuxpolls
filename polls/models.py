import datetime
from django.db import models
from django.utils import timezone
from .plots import add_figure

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    
    def make_copy(self):
        choices = self.choice_set.all() #Choice.objects.filter(question_id=self.id)
        self.pk = None
        self.save()
        for choice in choices:
            choice.question_id = self.id
            choice.pk = None
            choice.save()
    
    def update_pub_date(self):
        self.pub_date = timezone.now()
        self.save()

    def reset_votes(self):
        choices = self.choice_set.all() #Choice.objects.filter(question_id=self.id)
        for choice in choices:
            choice.votes = 0
            choice.save()

    def update_figure(self):
        figures = self.plot_set.all()
        for figure in figures:           
           # figure.graph = add_figure(self, figure.plot_type) 
            figure.save()

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text

TYPE = (
    (0,"Linear"),
    (1,"Histogram")
)

class Plot(models.Model):  
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    script = models.TextField(blank=True, default='Graph script placeholder')
    div = models.TextField(blank=True, default='Graph div placeholder')
    created_on = models.DateTimeField(auto_now_add=True)
    plot_type = models.IntegerField(choices=TYPE, default=0)
    update = models.BooleanField(default=False)

    def __str__(self):
        return str(self.question.question_text)

    def save(self, *args, **kwargs):
        if self.script == 'Graph placeholder' or self.update == True:
            self.script, self.div = add_figure(self.question, self.plot_type)      
        super(Plot, self).save(*args, **kwargs)

    

               

    
    
