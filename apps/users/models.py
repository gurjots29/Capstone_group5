from django.db import models
from django.contrib.auth.models import User  
from django.core.exceptions import ValidationError

class Category(models.Model):
    CATEGORY_TYPES = (
        ('interest', 'Interest'),
        ('skill', 'Skill'),
    )

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    category_type = models.CharField(max_length=10, choices=CATEGORY_TYPES, default='interest')

    def __str__(self):
        return f"{self.name} ({self.get_category_type_display()})"
    
class Interest(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category, related_name='interests', on_delete=models.CASCADE)
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if self.category.category_type != 'interest':
            raise ValidationError("La categoría seleccionada no es válida para un interés.")
        super(Interest, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Badge(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='badge_images/')

    def __str__(self):
        return self.name
    
class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category, related_name='skills', on_delete=models.CASCADE)
    description = models.TextField()
    
    def save(self, *args, **kwargs):
        if self.category.category_type != 'skill':
            raise ValidationError("La categoría seleccionada no es válida para una habilidad.")
        super(Skill, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Volunteer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='volunteer_profile/', blank=True, null=True)
    background_image = models.ImageField(upload_to='volunteer_profile/', blank=True, null=True)
    bio = models.TextField(blank=True)
    phone_number = models.CharField(max_length=20)
    experiences = models.TextField()
    interests = models.ManyToManyField(Interest, related_name='interested_volunteers', blank=True)
    badges = models.ManyToManyField(Badge, related_name='volunteers', blank=True)
    skills = models.ManyToManyField(Skill, related_name='volunteers', blank=True)
    location = models.CharField(max_length=255, blank=True, null=True)  # Consider using a more detailed location model or a library like django-cities for more granularity
    date_of_birth = models.DateField(null=True, blank=True)
    headline = models.TextField(max_length=80, blank=True)

    following_volunteers = models.ManyToManyField(
        'self',
        through='Relationship',
        through_fields=('from_volunteer', 'to_volunteer'),
        symmetrical=False,
        related_name='followed_by_volunteers'  # Cambiado para ser único
    )
    following_organizations = models.ManyToManyField(
        'Organization',
        through='Relationship',
        through_fields=('from_volunteer', 'to_organization'),
        related_name='volunteers_following_organizations'  # Cambiado para ser único
    )

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Organization(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='organization_profile/', blank=True)
    background_image = models.ImageField(upload_to='organization_profile/', blank=True, null=True)
    volunteers = models.ManyToManyField(Volunteer, through='OrganizationMembership', related_name='organizations')
    interests = models.ManyToManyField(Interest, related_name='interested_organizations', blank=True)
    required_skills = models.ManyToManyField(Skill, related_name='required_by_organizations', blank=True)
    
    followers_volunteers = models.ManyToManyField(
        'Volunteer',
        through='Relationship',
        through_fields=('to_organization', 'from_volunteer'),
        related_name='organizations_followed_by_volunteers'  # Cambiado para claridad
    )
    
    def __str__(self):
        return self.name
    
class OrganizationMembership(models.Model):
    ROLES = (
        ('owner', 'Owner'),
        ('admin', 'Admin'),
        ('member', 'Member'),
    )
    
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLES)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            # Asegurando que un Volunteer solo tenga un tipo de rol específico en una organización
            models.UniqueConstraint(
                fields=['volunteer', 'organization', 'role'],
                name='unique_membership'
            )
        ]

class Relationship(models.Model):
    from_volunteer = models.ForeignKey(
        Volunteer, 
        verbose_name="follower volunteer", 
        related_name="following_relationships", 
        on_delete=models.CASCADE
    )
    to_volunteer = models.ForeignKey(
        Volunteer, 
        verbose_name="followed volunteer", 
        related_name="follower_relationships", 
        on_delete=models.CASCADE, 
        null=True, blank=True
    )
    to_organization = models.ForeignKey(
        Organization, 
        verbose_name="following organization", 
        related_name="follower_organizations", 
        on_delete=models.CASCADE, 
        null=True, blank=True
    )
    date_followed = models.DateTimeField(auto_now_add=True)
    date_unfollowed = models.DateTimeField(null=True, blank=True)

    def clean(self):
        # Validación para asegurar que no se siga a un voluntario y una organización en la misma instancia
        if self.to_volunteer and self.to_organization:
            raise ValidationError("No se puede seguir a un voluntario y una organización en la misma relación.")

        # Validación para evitar que un voluntario se siga a sí mismo
        if self.to_volunteer == self.from_volunteer:
            raise ValidationError("No se puede seguir a sí mismo.")

        # Otras validaciones según sea necesario

    def __str__(self):
        if self.to_volunteer:
            return f"{self.from_volunteer} -> {self.to_volunteer}"
        elif self.to_organization:
            return f"{self.from_volunteer} -> {self.to_organization}"
        else:
            return f"{self.from_volunteer} -> [Relación no definida]"

    class Meta:
        # Manteniendo la restricción única para evitar duplicados
        unique_together = ['from_volunteer', 'to_volunteer', 'to_organization']
    