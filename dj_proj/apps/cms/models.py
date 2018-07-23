from django.db import models


class Banners(models.Model):
    image_url = models.URLField()
    priority = models.IntegerField()
    jump_link = models.URLField()

    class Meta:
        ordering = ['-priority']