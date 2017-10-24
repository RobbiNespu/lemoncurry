from django.contrib.auth import views as auth_views
from django_otp.forms import OTPAuthenticationForm
from lemoncurry import breadcrumbs

breadcrumbs.add(route='lemonauth:login', label='log in', parent='home:index')

login = auth_views.LoginView.as_view(
    authentication_form=OTPAuthenticationForm,
    template_name='lemonauth/login.html',
    redirect_authenticated_user=True,
)
logout = auth_views.LogoutView.as_view()
