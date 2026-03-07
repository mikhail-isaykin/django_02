"""
apps/payments/services.py
NowPayments API — ООП-сервис + dataclass-маппинг ответов.
Принципы: Single Responsibility, type hints, безопасность (HMAC).
"""
from __future__ import annotations

import hashlib
import hmac
import json
from dataclasses import dataclass
from typing import Any

import requests
from django.conf import settings


# ── Dataclass-маппинг API-ответов ─────────────────────────────

@dataclass(frozen=True)
class PaymentInvoice:
    """Маппинг ответа POST /v1/payment от NowPayments."""
    payment_id:     str
    payment_status: str
    pay_address:    str
    price_amount:   float
    price_currency: str
    pay_amount:     float
    pay_currency:   str
    invoice_url:    str

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "PaymentInvoice":
        return cls(
            payment_id     = str(data["payment_id"]),
            payment_status = data["payment_status"],
            pay_address    = data["pay_address"],
            price_amount   = float(data["price_amount"]),
            price_currency = data["price_currency"],
            pay_amount     = float(data["pay_amount"]),
            pay_currency   = data["pay_currency"],
            invoice_url    = data.get("invoice_url", ""),
        )


@dataclass(frozen=True)
class WebhookPayload:
    """Маппинг IPN-уведомления от NowPayments."""
    payment_id:     str
    payment_status: str
    order_id:       str
    price_amount:   float
    actually_paid:  float

    @classmethod
    def from_request(cls, data: dict[str, Any]) -> "WebhookPayload":
        return cls(
            payment_id     = str(data["payment_id"]),
            payment_status = data["payment_status"],
            order_id       = str(data.get("order_id", "")),
            price_amount   = float(data.get("price_amount", 0)),
            actually_paid  = float(data.get("actually_paid", 0)),
        )


# ── Сервисный класс ───────────────────────────────────────────

class NowPaymentsService:
    """
    Обёртка над NowPayments REST API.
    Документация: https://documenter.getpostman.com/view/7907941/2s93JqTRWN
    """

    BASE_URL = "https://api.nowpayments.io/v1"
    SANDBOX_URL = "https://api-sandbox.nowpayments.io/v1"

    def __init__(self) -> None:
        self.api_key    = settings.NOWPAYMENTS_API_KEY
        self.ipn_secret = settings.NOWPAYMENTS_IPN_SECRET
        self.sandbox    = getattr(settings, "NOWPAYMENTS_SANDBOX", False)
        self._base      = self.SANDBOX_URL if self.sandbox else self.BASE_URL

    def _headers(self) -> dict[str, str]:
        return {
            "x-api-key":   self.api_key,
            "Content-Type": "application/json",
        }

    def create_payment(
        self,
        order_id:       int | str,
        amount:         float,
        currency_from:  str = "usd",
        currency_to:    str = "btc",
        success_url:    str = "",
        cancel_url:     str = "",
    ) -> PaymentInvoice:
        """Создаёт платёжный инвойс и возвращает маппированный объект."""
        payload = {
            "price_amount":    amount,
            "price_currency":  currency_from,
            "pay_currency":    currency_to,
            "order_id":        str(order_id),
            "success_url":     success_url,
            "cancel_url":      cancel_url,
        }
        response = requests.post(
            f"{self._base}/payment",
            json=payload,
            headers=self._headers(),
            timeout=15,
        )
        response.raise_for_status()
        return PaymentInvoice.from_api(response.json())

    def verify_webhook(self, payload_bytes: bytes, signature: str) -> bool:
        """
        Верифицирует подпись IPN-уведомления через HMAC-SHA512.
        Документация: https://nowpayments.io/help/what-is-the-ipn
        """
        computed = hmac.new(
            self.ipn_secret.encode(),
            payload_bytes,
            hashlib.sha512,
        ).hexdigest()
        return hmac.compare_digest(computed, signature.lower())

    def get_payment_status(self, payment_id: str) -> str:
        """Проверяет текущий статус платежа."""
        response = requests.get(
            f"{self._base}/payment/{payment_id}",
            headers=self._headers(),
            timeout=10,
        )
        response.raise_for_status()
        return response.json().get("payment_status", "unknown")
