from django.core.validators import MinValueValidator
from django.db import models


class Statistic(models.Model):
    class Meta:
        db_table = 'statistic'
        verbose_name_plural = "Статистики"
        verbose_name = "Статистика"

    date = models.DateField(verbose_name="Дата события")
    views = models.PositiveIntegerField(verbose_name="Количество показов", default=0)
    clicks = models.PositiveIntegerField(verbose_name="Количество откликов", default=0)
    cost = models.DecimalField(verbose_name="Стоимсть откликов в рублях", max_digits=10, decimal_places=2, null=True,
                               blank=True, validators=[MinValueValidator(0.0)])

    def __str__(self):
        return str("Статистика за дату: %s" % self.date)
