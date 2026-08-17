from django.db import models
from django.contrib.auth.models import AbstractUser

class UserModel(AbstractUser):
    USER_TYPES = [
        ('Recruiters','Recruiters'),
        ('Jobseekers','Jobseekers'),
    ]
    display_name = models.CharField(max_length=120,null=True)
    user_type = models.CharField(choices=USER_TYPES,max_length=20,null=True)

    def __str__(self):
        return f'{self.username}--{self.user_type}'

class RecruitersModel(models.Model):
    recruiter = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        related_name='recruiter_profile',
        null=True
        )
    company_name = models.CharField(null=True)
    address = models.TextField(null=True)
    contract = models.CharField(max_length=20,null=True)
    logo = models.ImageField(upload_to='company_logo',null=True)
    created_at = models.DateField(auto_now_add=True,null=True)
    updated_at = models.DateField(auto_now_add=True,null=True)

    def __str__(self):
        return f'{self.company_name}'

class SeekeerModel(models.Model):
    seeker = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        related_name='seeker_profile',
        null=True
        )
    name = models.CharField(max_length=120,null=True)
    profile_image = models.ImageField(upload_to='seeker_image',null=True)
    address = models.TextField(null=True)
    skill_set = models.TextField(null=True)
    resume = models.FileField(null=True)
    created_at = models.DateField(auto_now_add=True,null=True)
    updated_at = models.DateField(auto_now_add=True,null=True)

    def __str__(self):
        return f'{self.name}'

class categoryModel(models.Model):
    name = models.CharField(max_length=100,null=True)

    def __str__(self):
        return f'{self.name}'

class JobPostModel(models.Model):
    title = models.CharField(max_length=100,null=True)
    numer_of_opening = models.PositiveBigIntegerField(null=True)
    category = models.ForeignKey(
        categoryModel,
        on_delete=models.CASCADE,
        null=True
        )
    post_by = models.ForeignKey(
        RecruitersModel,
        on_delete=models.CASCADE,
        related_name='job_post_info',
        null=True
        )
    desciption = models.TextField(null=True)
    skill_set = models.CharField(null=True)
    deadline = models.DateField(null=True)
    created_at = models.DateField(auto_now_add=True,null=True)
    updated_at = models.DateField(auto_now_add=True,null=True)

    def __str__(self):
        return f'{self.title}'

class ApplyJobModel(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]
    applied_by = models.ForeignKey(
        SeekeerModel,
        on_delete=models.CASCADE,
        related_name='applied_by_info',
        null=True
    )
    applied_job = models.ForeignKey(
        JobPostModel,
        on_delete=models.CASCADE,
        related_name='applied_post_info',
        null=True
    )
    resume = models.FileField(null=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='Pending')
    applied_at = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.applied_by.name}-{self.applied_job.title}'


    




