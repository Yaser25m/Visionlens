from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Review, ReviewHelpful
from products.models import Product


class AddReviewView(LoginRequiredMixin, CreateView):
    """إضافة تقييم للمنتج"""
    model = Review
    template_name = 'reviews/add.html'
    fields = ['rating', 'title', 'comment']

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.product = get_object_or_404(Product, id=self.kwargs['product_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('products:detail', kwargs={'pk': self.kwargs['product_id']})


class EditReviewView(LoginRequiredMixin, UpdateView):
    """تعديل التقييم"""
    model = Review
    template_name = 'reviews/edit.html'
    fields = ['rating', 'title', 'comment']

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('products:detail', kwargs={'pk': self.object.product.pk})


class DeleteReviewView(LoginRequiredMixin, DeleteView):
    """حذف التقييم"""
    model = Review
    template_name = 'reviews/delete.html'

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('products:detail', kwargs={'pk': self.object.product.pk})


class MarkHelpfulView(LoginRequiredMixin, View):
    """تقييم التقييم كمفيد"""
    def post(self, request, pk):
        review = get_object_or_404(Review, id=pk)
        is_helpful = request.POST.get('is_helpful') == 'true'

        helpful, created = ReviewHelpful.objects.get_or_create(
            user=request.user,
            review=review,
            defaults={'is_helpful': is_helpful}
        )

        if not created:
            helpful.is_helpful = is_helpful
            helpful.save()

        return JsonResponse({'success': True})
