from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    ROLE_CHOICES = [
        ('TEACHER', 'Teacher'),
        ('CUSTOMER', 'Customer'),
        ('TEAM', 'Team'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='CUSTOMER')
    class_name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"


class Wallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user.username} wallet - {self.balance}"


@receiver(post_save, sender=User)
def create_wallet_for_user(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)


class Transaction(models.Model):
    from_wallet = models.ForeignKey(
        Wallet, related_name='sent_transactions', on_delete=models.CASCADE
    )
    to_wallet = models.ForeignKey(
        Wallet, related_name='received_transactions', on_delete=models.CASCADE
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_wallet.user} -> {self.to_wallet.user}: {self.amount}"
