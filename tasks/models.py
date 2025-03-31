from django.db import models


class Difficulty(models.Model):
    class Meta:
        db_table = 'difficulty'
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    class Meta:
        db_table = 'tag'
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    class Meta:
        db_table = 'task'
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    difficulty = models.ForeignKey(Difficulty, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name="tasks", blank=True)
    time_limit = models.IntegerField(default=1)
    memory_limit = models.IntegerField(default=256)
    input_format = models.TextField(blank=True, null=True)
    output_format = models.TextField(blank=True, null=True)



    def __str__(self):
        return self.title


class TestCase(models.Model):
    class Meta:
        db_table = 'test_case'
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="test_cases")
    input_data = models.TextField()
    expected_output = models.TextField()
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return f"TestCase for {self.task.title}"
