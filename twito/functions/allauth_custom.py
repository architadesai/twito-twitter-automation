from allauth.account.adapter import DefaultAccountAdapter


class AccountAdapter(DefaultAccountAdapter):
    # Redirect URL after successful login
    def get_login_redirect_url(self, request):
        return '/dashboard/'
