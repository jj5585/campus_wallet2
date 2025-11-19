from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import views as auth_views
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db import transaction as db_transaction
from django.contrib.auth import logout as auth_logout

from .models import Wallet, Transaction
from .forms import TopUpForm, PaymentForm

User = get_user_model()


def is_teacher(user):
    return user.is_authenticated and user.role == 'TEACHER'


@login_required
def dashboard(request):
    user = request.user
    wallet = Wallet.objects.get(user=user)

    if user.role == 'TEACHER':
        teams = User.objects.filter(role='TEAM')
        leaderboard = []
        for team in teams:
            twallet = Wallet.objects.get(user=team)
            total_received = Transaction.objects.filter(to_wallet=twallet)
            total_amount = sum(t.amount for t in total_received)
            leaderboard.append({
                'team': team,
                'wallet': twallet,
                'total_amount': total_amount,
            })

        leaderboard.sort(key=lambda x: x['total_amount'], reverse=True)

        context = {'wallet': wallet, 'leaderboard': leaderboard}
        template_name = 'core/teacher_dashboard.html'

    elif user.role == 'CUSTOMER':
        sent = Transaction.objects.filter(from_wallet=wallet).order_by('-created_at')
        context = {
            'wallet': wallet,
            'sent_transactions': sent,
        }
        template_name = 'core/customer_dashboard.html'

    else:  # TEAM
        received = Transaction.objects.filter(to_wallet=wallet).order_by('-created_at')
        qr_url = request.build_absolute_uri(f"/pay/?team={user.username}")
        context = {
            'wallet': wallet,
            'received_transactions': received,
            'qr_url': qr_url,
        }
        template_name = 'core/team_dashboard.html'

    return render(request, template_name, context)


@login_required
@user_passes_test(is_teacher)
def topup_view(request):
    if request.method == 'POST':
        form = TopUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['student_username']
            amount = form.cleaned_data['amount']

            try:
                student = User.objects.get(username=username, role='CUSTOMER')
            except User.DoesNotExist:
                messages.error(request, "No customer with that username.")
                return redirect('topup')

            wallet = Wallet.objects.get(user=student)
            wallet.balance += amount
            wallet.save()

            messages.success(request, f"Added {amount} credits to {student.username}'s wallet.")
            return redirect('dashboard')
    else:
        form = TopUpForm()

    return render(request, 'core/topup.html', {'form': form})


@login_required
def pay_view(request):
    user = request.user
    if user.role != 'CUSTOMER':
        messages.error(request, "Only customers can make payments.")
        return redirect('dashboard')

    from_wallet = Wallet.objects.get(user=user)

    # Pre-fill team from QR link if present
    team_param = request.GET.get('team')
    if request.method == 'GET':
        if team_param:
            form = PaymentForm(initial={'team_username': team_param})
        else:
            form = PaymentForm()
    else:
        form = PaymentForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            team_username = form.cleaned_data['team_username']
            amount = form.cleaned_data['amount']
            description = form.cleaned_data['description']

            try:
                team = User.objects.get(username=team_username, role='TEAM')
            except User.DoesNotExist:
                messages.error(request, "No team with that username.")
                return redirect('pay')

            to_wallet = Wallet.objects.get(user=team)

            if from_wallet.balance < amount:
                messages.error(request, "Not enough balance.")
                return redirect('pay')

            with db_transaction.atomic():
                from_wallet.balance -= amount
                from_wallet.save()

                to_wallet.balance += amount
                to_wallet.save()

                Transaction.objects.create(
                    from_wallet=from_wallet,
                    to_wallet=to_wallet,
                    amount=amount,
                    description=description,
                )

            messages.success(request, f"Paid {amount} credits to {team.username}.")
            return redirect('dashboard')

    return render(request, 'core/pay.html', {'form': form, 'balance': from_wallet.balance})


class LoginView(auth_views.LoginView):
    template_name = 'core/login.html'
    redirect_authenticated_user = True


@login_required
def logout_view(request):
    """Simple logout view that works with GET and redirects to login."""
    auth_logout(request)
    return redirect('login')
