from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
	name = models.CharField(max_length=50)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

	def __str__(self):
		return self.name

class Expense(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	amount = models.DecimalField(max_digits=10, decimal_places=2)
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
	description = models.CharField(max_length=255, blank=True)
	date = models.DateField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return f"{self.user.username}: {self.amount} on {self.date}"
