from django.db import models
from django.db.models.base import Model
from django.db.models.fields.files import ImageField
from django.utils.text import slugify

class Team(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    position = models.CharField(max_length=200)
    about = models.TextField(blank=True)
    img = models.ImageField(upload_to='teams/')
    website = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)

    def __str__(self):
        return self.name

    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while Team.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug
 
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return f'/{self.slug}/'