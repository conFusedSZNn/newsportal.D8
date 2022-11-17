from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class AuthorUser(models.Model):
    rate_au = models.FloatField(default = 0.00)
    session_client = models.OneToOneField(User, on_delete= models.CASCADE)
    userAs = models.CharField(max_length=50, default = '')

    def update_rating(self):
        sum_rating_author = self.post_set.all().aggregate(Sum(' rating_post'))['rating_post__sum']*3
        sum_rating_comm = self.author_user.comment_set.all().aggregate(Sum('rating_comment'))['rating_comment__sum']
        sum_rate = self.post_set.all().aggregate(Sum('comment__rating_comment'))['comment__rating_comment__sum']
        self.rate_auth = sum_rating_author + sum_rating_comm + sum_rate
        self.save()





class Category(models.Model):
    categ_name = models.CharField(max_length=255, unique = True, default = 'Неизвестная категория')

class Post(models.Model):
    one_to_many_post = models.ForeignKey('AuthorUser', on_delete = models.PROTECT)
    CHOICES = (
        ('article', 'Статья'),
        ('news', 'Новость'),
    )
    datecr = models.DateField(auto_now_add=True)
    many_to_many_cat = models.ManyToManyField('Category', through = 'PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField(max_length=5000, default = '')
    rating_post = models.FloatField(default = 0.00)
    def likepost(self):
        self.rate_post += 1
        self.save()

    def dislikepost(self):
        self.rate_post -= 1
        self.save()

    def preview(self):
        return self.text[:125] + ". . ."




class PostCategory(models.Model):
    one_to_many_postcatpst = models.ForeignKey('Post', on_delete = models.CASCADE)
    one_to_many_postcatct = models.ForeignKey('Category', on_delete = models.CASCADE)

class Comment(models.Model):
    one_to_many_commpost = models.ForeignKey('Post', on_delete = models.CASCADE)
    one_to_many_commau = models.ForeignKey('AuthorUser', on_delete = models.PROTECT)
    textcomm = models.TextField(max_length = 500)
    datecomm = models.DateField(auto_now_add=True)
    rating_comment =  models.FloatField(default = 0.00)
    def likecomm(self):
        self.ratecomm += 1
        self.save()
    def dislikecomm(self):
        self.ratecomm -= 1
        self.save()