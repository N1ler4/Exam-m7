from django.conf import settings
from django.db import models

# Create your models here.

class Publication(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='publications'
    )
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.CharField(max_length=50)
    image = models.ImageField(upload_to='image/', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Publication'
        verbose_name_plural = 'Publications'
        db_table = 'publication'
        
    

class Papers(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='papers'
    )
    title = models.CharField(max_length=100)
    abstract = models.TextField()
    authors = models.CharField(max_length=255)
    publication_date = models.DateField()
    journal_name = models.CharField(max_length=100)
    keywords = models.CharField(max_length=255, blank=True)    
    view_count = models.PositiveIntegerField(default=0)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, related_name='papers')
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)      

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Paper'
        verbose_name_plural = 'Papers'
        db_table = 'paper'
 
    
class Requirements(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  
        on_delete=models.CASCADE,
        related_name='requirements'
    )

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Requirement'
        verbose_name_plural = 'Requirements'
        db_table = 'requirement'
    
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name    
    
    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'
        db_table = 'contact'
    
    