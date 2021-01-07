from django.db import models
from django.conf import settings
from django.contrib.auth.models import User



class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)


class Contact(models.Model):

    user_from = models.ForeignKey('auth.User',
                                related_name='rel_from_set',
                                on_delete=models.CASCADE)
    user_to = models.ForeignKey('auth.User', related_name='rel_to_set',
                                on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    class Meta:
        ordering = ('-created',)
    def __str__(self):
        return '{} follows {}'.format(self.user_from, self.user_to)

User.add_to_class('following',
                models.ManyToManyField('self',
                through=Contact,
                related_name='followers',
                symmetrical=False))

class Post(models.Model):
    datetime = models.DateTimeField(verbose_name=u'Дата', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=u'Автор', related_name='posts')
    text = models.CharField(max_length=1000, verbose_name=u'Текст', null=True, blank=True)
    image = models.FileField(verbose_name=u'Картинка', null=True, blank=True)

    class Meta:
        ordering = ["-datetime"]

class Comment(models.Model):
    datetime = models.DateTimeField(verbose_name=u'Дата', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=u'Автор', related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name=u'Пост', related_name='comments')
    text = models.CharField(max_length=1000, verbose_name=u'Текст', null=True, blank=True)

    class Meta:
        ordering = ['datetime']
