from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateField(default=timezone.now)
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    blog_views = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    def update_upvote(self):
        self.upvotes += 1
        self.save()

    def update_downvote(self):
        self.downvotes += 1
        self.save()

    @property
    def get_upvotes(self):
        return self.upvotes

    @property
    def get_downvotes(self):
        return self.downvotes

    @property
    def get_blogviews(self):
        return self.blog_views


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField(default=" ")
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.text
