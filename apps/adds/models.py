from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from apps.utils.fields import CompressedImageField
from apps.utils.validators import validate_email


class Banner(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = CompressedImageField(upload_to="banner", null=True, blank=True)

    class Meta:
        verbose_name = "banner"
        verbose_name_plural = "banners"

    def __str__(self):
        return self.title


class Notification(models.Model):
    image = CompressedImageField(upload_to="Bildirisler", null=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField()


class About(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text


class Contact(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    gmail = models.EmailField(max_length=200, validators=[validate_email])
    phone = PhoneNumberField()
    comment = models.TextField()

    def __str__(self):
        return f"{self.username}: {self.comment}"

    class Meta:
        verbose_name = "contact"
        verbose_name_plural = "contacts"
        db_table = "contact"
