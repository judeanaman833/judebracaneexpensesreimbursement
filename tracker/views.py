from django.shortcuts import redirect
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.db import models
import csv
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from calendar import monthrange
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Expense, Category
from .forms import ExpenseForm

def export_expenses_pdf(request):
	user = request.user
	expenses = Expense.objects.filter(user=user).order_by('-date')
	if not expenses.exists():
		messages.error(request, "No expenses to export.")
		return redirect('expense-list')
	buffer = BytesIO()
	p = canvas.Canvas(buffer, pagesize=letter)
	p.setFont("Helvetica-Bold", 16)
	p.drawString(50, 750, "Expense Report")
	p.setFont("Helvetica", 12)
	y = 720
	p.drawString(50, y, "Date")
	p.drawString(150, y, "Amount")
	p.drawString(250, y, "Category")
	p.drawString(400, y, "Description")
	y -= 20
	for exp in expenses:
		p.drawString(50, y, str(exp.date))
		p.drawString(150, y, str(exp.amount))
		p.drawString(250, y, exp.category.name if exp.category else '')
		p.drawString(400, y, exp.description or '')
		y -= 20
		if y < 50:
			p.showPage()
			y = 750
	p.save()
	buffer.seek(0)
	return HttpResponse(buffer, content_type='application/pdf')

def export_expenses_csv(request):
	user = request.user
	expenses = Expense.objects.filter(user=user).order_by('-date')
	if not expenses.exists():
		messages.error(request, "No expenses to export.")
		return redirect('expense-list')
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="expenses.csv"'
	writer = csv.writer(response)
	writer.writerow(['Date', 'Amount', 'Category', 'Description'])
	for exp in expenses:
		writer.writerow([exp.date, exp.amount, exp.category.name if exp.category else '', exp.description])
	return response

class DashboardView(LoginRequiredMixin, ListView):
	model = Expense
	template_name = 'tracker/dashboard.html'
	context_object_name = 'expenses'

	def get_queryset(self):
		user = self.request.user
		today = timezone.now().date()
		month_start = today.replace(day=1)
		month_end = today.replace(day=monthrange(today.year, today.month)[1])
		qs = Expense.objects.filter(user=user, date__range=[month_start, month_end])
		category = self.request.GET.get('category')
		start_date = self.request.GET.get('start_date')
		end_date = self.request.GET.get('end_date')
		if category:
			qs = qs.filter(category__id=category)
		if start_date:
			qs = qs.filter(date__gte=start_date)
		if end_date:
			qs = qs.filter(date__lte=end_date)
		return qs
	
	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)
		qs = ctx['expenses']
		summary = qs.values('category__name').annotate(total=Sum('amount')).order_by('-total')
		overall_total = qs.aggregate(total=Sum('amount'))['total'] or 0
		ctx['summary'] = summary
		ctx['overall_total'] = overall_total
		ctx['month'] = timezone.now().strftime('%B %Y')
		ctx['categories'] = Category.objects.filter(models.Q(user=self.request.user) | models.Q(user=None))
		ctx['selected_category'] = self.request.GET.get('category', '')
		ctx['selected_start_date'] = self.request.GET.get('start_date', '')
		ctx['selected_end_date'] = self.request.GET.get('end_date', '')
		return ctx
	
class CategoryListView(LoginRequiredMixin, ListView):
	model = Category
	template_name = 'tracker/category_list.html'
	context_object_name = 'categories'

	def get_queryset(self):
		return Category.objects.filter(models.Q(user=self.request.user) | models.Q(user=None))

class CategoryCreateView(LoginRequiredMixin, CreateView):
	model = Category
	fields = ['name']
	template_name = 'tracker/category_form.html'
	success_url = reverse_lazy('category-list')

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
	model = Category
	fields = ['name']
	template_name = 'tracker/category_form.html'
	success_url = reverse_lazy('category-list')

	def get_queryset(self):
		return Category.objects.filter(user=self.request.user)

class CategoryDeleteView(LoginRequiredMixin, DeleteView):
	model = Category
	template_name = 'tracker/category_confirm_delete.html'
	success_url = reverse_lazy('category-list')

	def get_queryset(self):
		return Category.objects.filter(user=self.request.user)

class ExpenseListView(LoginRequiredMixin, ListView):
	model = Expense
	template_name = 'tracker/expense_list.html'
	context_object_name = 'expenses'
	paginate_by = 10

	def get_queryset(self):
		qs = Expense.objects.filter(user=self.request.user).order_by('-date')
		category = self.request.GET.get('category')
		start_date = self.request.GET.get('start_date')
		end_date = self.request.GET.get('end_date')
		if category:
			qs = qs.filter(category__id=category)
		if start_date:
			qs = qs.filter(date__gte=start_date)
		if end_date:
			qs = qs.filter(date__lte=end_date)
		return qs
	
	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)
		ctx['categories'] = Category.objects.filter(models.Q(user=self.request.user) | models.Q(user=None))
		ctx['selected_category'] = self.request.GET.get('category', '')
		ctx['selected_start_date'] = self.request.GET.get('start_date', '')
		ctx['selected_end_date'] = self.request.GET.get('end_date', '')
		return ctx

class ExpenseCreateView(LoginRequiredMixin, CreateView):
	model = Expense
	form_class = ExpenseForm
	template_name = 'tracker/expense_form.html'
	success_url = reverse_lazy('expense-list')

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs
	
	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)

class ExpenseUpdateView(LoginRequiredMixin, UpdateView):
	model = Expense
	form_class = ExpenseForm
	template_name = 'tracker/expense_form.html'
	success_url = reverse_lazy('expense-list')

	def get_queryset(self):
		return Expense.objects.filter(user=self.request.user)
	
	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs

class ExpenseDeleteView(LoginRequiredMixin, DeleteView):
	model = Expense
	template_name = 'tracker/expense_confirm_delete.html'
	success_url = reverse_lazy('expense-list')
	
	def get_queryset(self):
		return Expense.objects.filter(user=self.request.user)
