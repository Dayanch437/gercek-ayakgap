from django.db import models

class Banner(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="banner",null=True, blank=True)
    class Meta:
        verbose_name = 'banner'
        verbose_name_plural = 'banners'
    def __str__(self):
        return self.title

class Notification(models.Model):
    image = models.ImageField(upload_to="Bildirisler",null=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField()


class About(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text