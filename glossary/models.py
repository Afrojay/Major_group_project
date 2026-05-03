from django.db import models
from django.urls import reverse


class Organisation(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    contact_email = models.EmailField(blank=True)
    theme_colour = models.CharField(max_length=20, blank=True, help_text='Optional display colour, for example #1d4ed8')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('glossary:organisation_home', kwargs={'organisation_slug': self.slug})


class Category(models.Model):
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(fields=['organisation', 'slug'], name='unique_category_slug_per_organisation')
        ]
        verbose_name_plural = 'categories'

    def __str__(self):
        return f'{self.organisation.name} - {self.name}'

    def get_absolute_url(self):
        return reverse(
            'glossary:category_detail',
            kwargs={'organisation_slug': self.organisation.slug, 'category_slug': self.slug},
        )


class SignEntry(models.Model):
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='signs')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='signs')
    term = models.CharField(max_length=200)
    slug = models.SlugField()
    video_url = models.URLField(help_text='Use a verified video URL or clearly labelled placeholder during development.')
    description = models.TextField()
    usage_context = models.TextField(blank=True)
    tags = models.CharField(max_length=300, blank=True, help_text='Comma-separated keywords for search support.')
    is_quick_reference = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['term']
        constraints = [
            models.UniqueConstraint(fields=['organisation', 'slug'], name='unique_sign_slug_per_organisation')
        ]
        verbose_name_plural = 'sign entries'

    def __str__(self):
        return f'{self.term} ({self.organisation.name})'

    def get_absolute_url(self):
        return reverse(
            'glossary:sign_detail',
            kwargs={'organisation_slug': self.organisation.slug, 'sign_slug': self.slug},
        )


class FAQEntry(models.Model):
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(max_length=255)
    answer = models.TextField()
    related_category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='faqs')
    related_sign = models.ForeignKey(SignEntry, on_delete=models.SET_NULL, null=True, blank=True, related_name='faqs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['question']
        verbose_name = 'FAQ entry'
        verbose_name_plural = 'FAQ entries'

    def __str__(self):
        return f'{self.organisation.name} - {self.question}'
