from django.urls import path

from app.forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from django.contrib import admin


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('category/<slug:val>', views.CategoryView.as_view(), name= 'category'),
    path('category-title/<val>', views.CategoryTitle.as_view(), name= 'category-title'),
    path('product-detail/<int:pk>', views.ProductDetail.as_view(), name= 'product_detail'),
    path('profile/', views.ProfileView.as_view(), name = 'profile'),
    path('address/', views.address, name = 'address'),
    path('updateAddress/<int:pk>', views.UpdateAddressView.as_view(), name = 'updateAddress'),

    path('add-to-cart/', views.add_to_cart, name = 'add_to_cart'),
    path('cart/', views.show_cart, name = 'show_cart'),
    path('checkout/', views.Checkout.as_view(), name = 'checkout'),
    path('payment-done', views.payment_done, name = 'payment_done'),
    path('orders', views.orders, name = 'orders'),

    path('plus-cart/', views.plus_cart, name = "plus_cart"),
    path('minus-cart/', views.minus_cart, name = "minus_cart"),
    path('remove-cart', views.remove_cart, name = "remove_cart"),

    path('search/', views.search, name = 'search'),

    #login and registration
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('account/login', auth_view.LoginView.as_view(template_name = 'app/login.html',
    authentication_form = LoginForm), name = 'login'),
    path('password-change', auth_view.PasswordChangeView.as_view(template_name = 'app/password_change.html',
    form_class = MyPasswordChangeForm, success_url = 'password-change-done'), name = 'password_change'),
    path('password-change-done', auth_view.PasswordChangeDoneView.as_view(template_name = 'app/password_change_done.html'), 
    name = 'password_change_done'),
    path('logout', auth_view.LogoutView.as_view(next_page = 'login'), name= 'logout'),

    path('password-reset', auth_view.PasswordResetView.as_view(template_name = 'app/password_reset.html',
    form_class = MyPasswordResetForm), name = 'password_reset'),
    path('password-reset/done', auth_view.PasswordResetDoneView.as_view(template_name = 'app/password_reset_done.html'),
    name = 'password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(
        template_name = 'app/password_reset_confirm.html', form_class = MySetPasswordForm), name = 'password_reset_confirm'),
    path('password-reset-complete', auth_view.PasswordResetCompleteView.as_view(template_name = 
    'app/password_reset_complete.html'), name = 'password_reset_complete'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Neel Dairy"
admin.site.site_title = "Neel Dairy"
admin.site.site_index_title = "Neel Dairy"