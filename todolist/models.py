from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Todo(models.Model):

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
    text = models.TextField(max_length=400, help_text="Text of todo")
    is_completed = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-last_updated", "-created_time"]

    def get_absolute_url(self):
        """
        Returns the url to access a particular blog-author instance.
        """
        return reverse('particulartodo', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.text