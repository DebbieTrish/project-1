from django.db import models
from django.contrib.auth.models import AbstractUser

# -------------------------
# CustomUser Model (All users)
# -------------------------
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'Student'),
        (2, 'Academic Supervisor'),
        (3, 'Administrator'),
        (4, 'Workplace Supervisor'),
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

# -------------------------
# InternshipPlacement Model
# -------------------------
class InternshipPlacement(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 1})
    workplace_supervisor = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
                                             limit_choices_to={'user_type': 4})
    academic_supervisor = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
                                            limit_choices_to={'user_type': 2})
    company_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    STATUS_CHOICES = (
        ('Applied', 'Applied'),
        ('Under Review', 'Under Review'),
        ('Approved', 'Approved'),
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
        ('Rejected', 'Rejected'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Applied')

    def __str__(self):
        return f"{self.student.username} - {self.company_name} ({self.status})"

# -------------------------
# WeeklyLog Model
# -------------------------
class WeeklyLog(models.Model):
    internship = models.ForeignKey(InternshipPlacement, on_delete=models.CASCADE)
    week_number = models.PositiveIntegerField()
    report = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.internship.student.username} - Week {self.week_number}"

# -------------------------
# EvaluationCriteria Model
# -------------------------
class EvaluationCriteria(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    max_score = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.title} ({self.max_score})"

# -------------------------
# Evaluation Model
# -------------------------
class Evaluation(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 1})
    criteria = models.ForeignKey(EvaluationCriteria, on_delete=models.CASCADE)
    internship = models.ForeignKey(InternshipPlacement, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    comments = models.TextField(blank=True, null=True)
    evaluated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.criteria.title} ({self.score})"