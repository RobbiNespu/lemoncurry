from django.contrib import admin
from otp_agents.decorators import otp_required


admin.site.login = otp_required(admin.site.login, accept_trusted_agent=True)
