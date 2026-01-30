from django.db import models

class TrangTrai(models.Model):
    ten = models.CharField(max_length=255)
    vi_do = models.FloatField()
    kinh_do = models.FloatField()
    mo_ta = models.TextField(blank=True)

    def __str__(self):
        return self.ten
