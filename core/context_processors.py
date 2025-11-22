from django.utils import timezone

from .models import User, Wallet, Transaction


def dashboard_stats(request):
    """
    Extra stats for the admin dashboard.
    """
    today = timezone.now().date()

    return {
        "dashboard_total_users": User.objects.count(),
        "dashboard_total_wallets": Wallet.objects.count(),
        "dashboard_total_transactions": Transaction.objects.count(),
        "dashboard_transactions_today": Transaction.objects.filter(
            created_at__date=today
        ).count(),
    }
