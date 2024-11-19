from django.db import models


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Use Django's built-in hashing for security

    def __str__(self):
        return self.username


class MartialArt(models.Model):
    martial_art_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Movement(models.Model):
    movement_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    martial_art_id = models.ForeignKey(MartialArt, related_name="movements", on_delete=models.CASCADE)
    tutorial = models.TextField()
    reference_file = models.FileField(upload_to="reference_files/")

    def __str__(self):
        return self.name


class PracticeSession(models.Model):
    session_id = models.AutoField(primary_key=True)
    movement_id = models.ForeignKey(Movement, related_name="practice_sessions", on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, related_name="practice_sessions", on_delete=models.CASCADE)
    score = models.FloatField()
    user_feedback = models.TextField(blank=True, null=True)
    session_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session for {self.user.username} on {self.movement.name}"


class ProgressHistory(models.Model):
    history_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, related_name="progress_histories", on_delete=models.CASCADE)
    movement_id = models.ForeignKey(Movement, related_name="progress_histories", on_delete=models.CASCADE)
    session_id = models.ForeignKey(PracticeSession, related_name="progress_histories", on_delete=models.CASCADE)
    progress_score = models.FloatField()

    def __str__(self):
        return f"Progress for {self.user.username} on {self.movement.name}"
