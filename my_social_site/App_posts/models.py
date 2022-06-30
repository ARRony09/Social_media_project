from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Posts(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name='post')
    image=models.ImageField(upload_to='post_image')
    caption=models.CharField(max_length=500,blank=True)
    upload_date=models.DateTimeField(auto_now_add=True)
    update_date=models.DateTimeField(auto_now=True)

    class Meta:
        ordering=['-upload_date',]

class Like(models.Model):
    post=models.ForeignKey(Posts,on_delete=models.CASCADE,related_name='liked_post')
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='liker')
    date_created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} : {}'.format(self.user,self.post)


class Comment(models.Model):
    post=models.ForeignKey(Posts,on_delete=models.CASCADE,related_name="post_comment")
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_comment')
    comment=models.TextField()
    comment_date=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-comment_date',)

    def __str__(self):
        return self.user