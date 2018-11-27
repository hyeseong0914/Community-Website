from django.db import models
from datetime import datetime
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible
class Board(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.CharField(null=False, max_length=50)
    title = models.CharField(null=False, max_length=120)
    hit = models.IntegerField(default=0)
    content = models.TextField(null=False)
    post_date = models.DateTimeField(default=datetime.now, blank=True)
    file_name = models.CharField(null=True, blank=True, default="", max_length=500)
    file_size = models.IntegerField(default=0)
    down = models.IntegerField(default=0)

    def hit_up(self):
        self.hit += 1
    def down_up(self):
        self.down += 1

    def set_title(self, new_title):
        self.title = new_title

    def set_content(self,new_content):
        self.content = new_content

@python_2_unicode_compatible
class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    board_id = models.IntegerField(null=False)
    author = models.CharField(null=False, max_length=50)
    content = models.TextField(null=False)
    post_date = models.DateTimeField(default=datetime.now, blank=True)

    def set_content(self,new_content):
        self.content = new_content