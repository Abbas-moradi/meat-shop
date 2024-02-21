from django.db import models


class ContactUs(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=250)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'contact us'
        verbose_name_plural = 'contact us'
        ordering = ('created',)

    def __str__(self) -> str:
        return self.subject