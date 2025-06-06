from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.urls import reverse_lazy
from .models import UserProfile, Address


class RegisterView(CreateView):
    """تسجيل مستخدم جديد"""
    model = User
    form_class = UserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'تم إنشاء الحساب بنجاح! يمكنك الآن تسجيل الدخول.')
        return response


class ProfileView(LoginRequiredMixin, UpdateView):
    """عرض وتعديل الملف الشخصي"""
    model = UserProfile
    template_name = 'accounts/profile.html'
    fields = ['phone', 'birth_date', 'gender', 'avatar', 'preferred_language', 'newsletter_subscription']
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user.userprofile


class EditProfileView(LoginRequiredMixin, UpdateView):
    """تعديل الملف الشخصي"""
    model = UserProfile
    template_name = 'accounts/edit_profile.html'
    fields = ['phone', 'birth_date', 'gender', 'avatar', 'preferred_language', 'newsletter_subscription']
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user.userprofile


class AddressListView(LoginRequiredMixin, ListView):
    """عرض قائمة العناوين"""
    model = Address
    template_name = 'accounts/addresses.html'
    context_object_name = 'addresses'

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)


class AddAddressView(LoginRequiredMixin, CreateView):
    """إضافة عنوان جديد"""
    model = Address
    template_name = 'accounts/add_address.html'
    fields = ['title', 'full_name', 'phone', 'address_line_1', 'address_line_2', 'city', 'state', 'postal_code', 'country', 'is_default']
    success_url = reverse_lazy('accounts:addresses')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EditAddressView(LoginRequiredMixin, UpdateView):
    """تعديل عنوان"""
    model = Address
    template_name = 'accounts/edit_address.html'
    fields = ['title', 'full_name', 'phone', 'address_line_1', 'address_line_2', 'city', 'state', 'postal_code', 'country', 'is_default']
    success_url = reverse_lazy('accounts:addresses')

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)


class DeleteAddressView(LoginRequiredMixin, DeleteView):
    """حذف عنوان"""
    model = Address
    template_name = 'accounts/delete_address.html'
    success_url = reverse_lazy('accounts:addresses')

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
