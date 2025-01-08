from django.urls import path

from wallet.views import (
    WalletView, RechargesView,
    VerifyRecharge, FundAccountsView,
    WithdrawalsView, RazorpayWebhookView,
    RechargeView
)

urlpatterns = [
    path('', WalletView.as_view(), name='wallet'),
    path('recharges', RechargesView.as_view(), name='recharges'),
    path('recharges/<str:recharge_id>/verify', VerifyRecharge.as_view(), name='verify_recharge'),
    path('fund-accounts', FundAccountsView.as_view(), name='wallet_fund_accounts'),
    path('withdrawals', WithdrawalsView.as_view(), name='withdrawals'),
    path('webhook', RazorpayWebhookView.as_view(), name='razorpay_webhook'),
    path('recharges/<str:recharge_id>', RechargeView.as_view(), name='recharge'),
]