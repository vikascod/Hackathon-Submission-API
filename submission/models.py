from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone


User = get_user_model()


class SubmissionType(models.TextChoices):
    IMAGE = 'image', 'Image'
    FILE = 'file', 'File'
    LINK = 'link', 'Link'


class Hackathon(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    background_image = models.ImageField(upload_to='hackathon/backgrounds/')
    hackathon_image = models.ImageField(upload_to='hackathon/images/')
    submission_type = models.CharField(
        max_length=10,
        choices=SubmissionType.choices,
        default=SubmissionType.LINK
    )
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    reward_prize = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Hackathon'
        verbose_name_plural = 'Hackathons'
        ordering = ['-start_datetime']

    def is_active(self):
        return self.start_datetime <= timezone.now() <= self.end_datetime


class HackathonParticipant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="hackathon_participant")
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE, related_name="participants")

    def __str__(self) -> str:
        return f"{self.user.username} - {self.hackathon.title}"


class Submission(models.Model):
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE, related_name='submissions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    summary = models.TextField()
    submission_file = models.FileField(upload_to='submissions/files/', null=True, blank=True)
    submission_image = models.ImageField(upload_to='submissions/images/', null=True, blank=True)
    submission_link = models.URLField(max_length=500, null=True, blank=True)
    submission_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.hackathon.title}"

    class Meta:
        verbose_name = 'Submission'
        verbose_name_plural = 'Submissions'
        ordering = ['-submission_datetime']

    def clean(self):
        # Based on the type of submission mentioned above, submissions should be accepted. API should validate it.

        if self.hackathon.submission_type == SubmissionType.IMAGE and not self.submission_image:
            raise ValidationError("An image is required for this hackathon.")
        elif self.hackathon.submission_type == SubmissionType.FILE and not self.submission_file:
            raise ValidationError("A file is required for this hackathon.")
        elif self.hackathon.submission_type == SubmissionType.LINK and not self.submission_link:
            raise ValidationError("A link is required for this hackathon.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
