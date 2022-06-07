from django.db import models

class Quote(models.Model):
    character = models.CharField(max_length=30)
    topic = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.character}, {self.topic}'