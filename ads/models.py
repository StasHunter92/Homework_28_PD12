from django.db import models

from users.models import User


# ----------------------------------------------------------------------------------------------------------------------
# Create category model
class Category(models.Model):
    name: str = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name: str = "Категория"
        verbose_name_plural: str = "Категории"


# ----------------------------------------------------------------------------------------------------------------------
# Create ad model
class Ad(models.Model):
    PUBLISHED: list[tuple] = [(True, "Опубликовано"), (False, "Не опубликовано")]

    name: str = models.CharField(max_length=60)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    price: int = models.PositiveIntegerField()
    description: str = models.CharField(max_length=500)
    is_published: bool = models.BooleanField(choices=PUBLISHED, default=False)
    image = models.ImageField(upload_to="images/")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name: str = "Объявление"
        verbose_name_plural: str = "Объявления"
