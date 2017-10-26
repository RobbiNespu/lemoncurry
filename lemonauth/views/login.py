import django.contrib.auth.views
from otp_agents.forms import OTPAuthenticationForm
from lemoncurry import breadcrumbs

breadcrumbs.add(route='lemonauth:login', label='log in', parent='home:index')

login = django.contrib.auth.views.LoginView.as_view(
    authentication_form=OTPAuthenticationForm,
    extra_context={'title': 'log in'},
    template_name='lemonauth/login.html',
    redirect_authenticated_user=True,
)
