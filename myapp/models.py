from django.db import models
from django.contrib.auth.models import User

class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class Question(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def clean_body(self):
        """
        Clean the body field by stripping unwanted characters like newlines and extra spaces.
        """
        # Strip leading/trailing whitespace and replace newlines with a space
        return self.body.replace('\n', ' ').replace('\r', ' ').strip()

    def save(self, *args, **kwargs):
        self.body = self.clean_body()  # Clean the body text before saving
        super().save(*args, **kwargs)


class Answer(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='answers')
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_answers', blank=True)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f"Answer by {self.author.username} to '{self.question.title}'"
    
    def clean_body(self):
        """
        Clean the body field by stripping unwanted characters like newlines and extra spaces.
        """
        return self.body.replace('\n', ' ').replace('\r', ' ').strip()
    
    def save(self, *args,**kwargs):
        self.body = self.clean_body() 
        super().save(*args, **kwargs)
    
