from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField

class ServiceCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True)
    icon = models.ImageField(upload_to='category_icons/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Service Categories'
        ordering = ['order']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Service(models.Model):
    LEVEL_CHOICES = [
        ('entry', 'Entry Level'),
        ('mid', 'Mid-Career'),
        ('executive', 'Executive'),
        ('all', 'All Levels'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.TextField()
    description = RichTextField()
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='service_images/', blank=True, null=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='all')
    duration = models.CharField(max_length=100, blank=True, help_text='e.g., "2-3 days"')
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    @property
    def is_discounted(self):
        return self.discounted_price is not None and self.discounted_price < self.price

class ServicePackage(models.Model):
    PACKAGE_TYPE_CHOICES = [
        ('entry', 'Entry-Level Package'),
        ('professional', 'Professional Growth Package'),
        ('executive', 'Executive Success Package'),
        ('transition', 'Career Change & Transition Package'),
        ('scholarship', 'Scholarship & Admissions Package'),
        ('business', 'Business & Thought Leadership Package'),
    ]
    
    name = models.CharField(max_length=200)
    package_type = models.CharField(max_length=20, choices=PACKAGE_TYPE_CHOICES)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.TextField()
    description = RichTextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='package_images/', blank=True, null=True)
    services = models.ManyToManyField(Service, through='PackageService')
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    @property
    def is_discounted(self):
        return self.discounted_price is not None and self.discounted_price < self.price

class PackageService(models.Model):
    package = models.ForeignKey(ServicePackage, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        unique_together = ['package', 'service']
    
    def __str__(self):
        return f"{self.package.name} - {self.service.name}"

class ServiceFeature(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='features')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_highlighted = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.service.name} - {self.name}"

class PackageFeature(models.Model):
    package = models.ForeignKey(ServicePackage, on_delete=models.CASCADE, related_name='features')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_highlighted = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.package.name} - {self.name}"

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    content = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5, choices=[(i, i) for i in range(1, 6)])
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, related_name='testimonials', blank=True, null=True)
    package = models.ForeignKey(ServicePackage, on_delete=models.SET_NULL, related_name='testimonials', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_featured', 'order']
    
    def __str__(self):
        return f"Testimonial from {self.name}"
