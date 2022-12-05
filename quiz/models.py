from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils.timezone import now
from django.conf import settings as conf_setting

from datetime import timedelta

import short_url
import random

class QuizCategory(models.Model):

    title = models.CharField(max_length = 100)
    slug = models.SlugField(blank = True, null = True)
    image = models.ImageField(upload_to = 'catagory_img/')

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Category'

class QuizQuestion(models.Model):

    answer_choice = [
        ('1', 'Option 1'),
        ('2', 'Option 2'),
        ('3', 'Option 3'),
        ('4', 'Option 4'),
    ]

    category = models.ForeignKey(QuizCategory, on_delete = models.CASCADE)
    slug = models.SlugField(blank = True, null = True, max_length = 25, unique = True)
    question = models.TextField()
    option_1 = models.TextField()
    option_2 = models.TextField()
    option_3 = models.TextField()
    option_4 = models.TextField()
    time_limit = models.IntegerField()
    answer = models.CharField(max_length = 10, choices = answer_choice)

    def __str__(self):
        return self.question

    def save(self, *args, **kwargs):
        if self.slug is None and self.id is not None:
            cat_id = short_url.encode_url(self.id)
            self.slug = slugify(f"{self.category} {cat_id}")
        super().save(*args, **kwargs)
        if self.slug is None and self.id is not None:
            cat_id = short_url.encode_url(self.id)
            self.slug = slugify(f"{self.category} {cat_id}")
            self.save()

    class Meta:
        verbose_name_plural = 'Questions'

class QuizProfileManager(models.Manager):
    
    def get_new_question(self, user, quiz_category, start_time, end_time):
        used_questions_pk = AttemptedQuestion.objects.filter(user = user, 
            category = quiz_category, attempt_time__range = (start_time, end_time)).values_list('question__pk', flat=True)
        print(used_questions_pk)
        remaining_questions = QuizQuestion.objects.filter(category = quiz_category).exclude(id__in = used_questions_pk)
        if not remaining_questions.exists():
            return
        return random.choice(remaining_questions)
    
    def create_attempt(self, user, quiz_category, quiz_question):
        attempted_question = AttemptedQuestion(category = quiz_category, question = quiz_question, user = user)
        attempted_question.save()
        return attempted_question.pk

    def total_question(self, quiz_category):
        return QuizQuestion.objects.filter(category = quiz_category).count()
    
    def attempt_question(self, user, quiz_category, start_time, end_time):
        return AttemptedQuestion.objects.filter(user = user, 
            category = quiz_category, attempt_time__range = (start_time, end_time)).count()

    def get_attempt_question(self, user, quiz_category, start_time, end_time):
        return AttemptedQuestion.objects.filter(user = user, 
            category = quiz_category, attempt_time__range = (start_time, end_time))

    def update_attempt(self, attempt_id, answer):
        AttemptedQuestion.objects.filter(id = attempt_id).update(answer = answer)

    def update_score(self, attempt_id, answer, cat_attemp_id):
        attempt_question = AttemptedQuestion.objects.get(id = attempt_id)
        
        if attempt_question.answer == attempt_question.question.answer:
            category_attempt = UserCategoryManager().get_user_cat_attempt(cat_attemp_id)
            score = category_attempt.score
            update_score = score + 1
            UserCategoryManager().update_cat_attempt(cat_attemp_id, update_score)

class UserCategoryAttempt(models.Model):

    category = models.ForeignKey(QuizCategory, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    score = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    attempt_time = models.DateTimeField(auto_now_add = True)

    class Meta:
        verbose_name_plural = 'User Attempted Category'

class UserCategoryManager(models.Manager):
    
    def get_category_attempt(self, user, quiz_category):
        
        current_time = now()
        category_attempt = self.fetch_category_attempt(user, quiz_category)
        if not category_attempt.exists():
            self.create_category_attempt(user, quiz_category)
        else:
            category_attempt = category_attempt.first()
            start_time = category_attempt.attempt_time
            end_time = start_time + timedelta(hours = conf_setting.LAST_QUIZ_ATTEMPT)
            if current_time > end_time:
                self.create_category_attempt(user, quiz_category)

    def fetch_category_attempt(self, user, quiz_category):
        return UserCategoryAttempt.objects.filter(category = quiz_category, user = user).order_by('-attempt_time')

    def create_category_attempt(self, user, quiz_category):
        attempted_category = UserCategoryAttempt(category = quiz_category, user = user)
        attempted_category.save()
        return attempted_category
    
    def get_user_cat_attempt(self, cat_attemp_id):
        return UserCategoryAttempt.objects.get(id = cat_attemp_id)
    
    def update_cat_attempt(self, cat_attemp_id, score):
        UserCategoryAttempt.objects.filter(id = cat_attemp_id).update(score = score)

class AttemptedQuestion(models.Model):

    category = models.ForeignKey(QuizCategory, on_delete = models.CASCADE)
    question = models.ForeignKey(QuizQuestion, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    answer = models.CharField(max_length = 10, null = True, default = 'skip')
    attempt_time = models.DateTimeField(auto_now_add = True)

    class Meta:
        verbose_name_plural = 'User Attempted Questions'
    

