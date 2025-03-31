from django.db import models

from mind_forge import settings
from tasks.models import Task
from users.models import User


class Submission(models.Model):
    class Meta:
        db_table = 'submissions'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    code = models.TextField()

    language = models.CharField(max_length=20, choices=[
        ('python', 'Python'),
        ('cpp', 'C++'),
        ('java', 'Java'),
        ('javascript', 'JavaScript'),
    ], default='python')

    status = models.CharField(
        choices=[
            ('pending', 'Pending'),
            ('correct', 'Correct'),
            ('wrong', 'Wrong'),
            ('runtime_error', 'Runtime Error'),
            ('time_limit_exceeded', 'Time Limit Exceeded'),
            ('memory_limit_exceeded', 'Memory Limit Exceeded'),
            ('compilation_error', 'Compilation Error'),
        ],
        default='pending'
    )

    execution_time = models.FloatField(null=True, blank=True)
    memory_used = models.IntegerField(null=True, blank=True)
    test_cases_passed = models.IntegerField(default=0)
    total_test_cases = models.IntegerField(default=0)

    stdout = models.TextField(blank=True, null=True)
    stderr = models.TextField(blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)

    submitted_at = models.DateTimeField(auto_now_add=True)
    submission_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.task.title} ({self.status})"
