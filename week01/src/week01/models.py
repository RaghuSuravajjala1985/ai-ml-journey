"""Day 3 - classes, properties, classmethods, dunders, ABC vs Protocol, dataclasses."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field, replace
from typing import Protocol, override


class BankAccount:
    """A plain class, written by hand, to see what dataclasses later generate for you."""

    interest_rate: float = 0.02  # class attribute, like a static field

    def __init__(self, owner: str, balance: float = 0.0) -> None:
        self.owner = owner
        self._balance = balance  # "private" by convention

    @property
    def balance(self) -> float:
        return self._balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("amount must be positive")
        self._balance += amount

    def withdraw(self, amount: float) -> None:
        if amount > self._balance:
            raise ValueError("insufficient funds")
        self._balance -= amount

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> BankAccount:
        """Alternate constructor, like a static factory method."""
        return cls(owner=str(data["owner"]), balance=float(data.get("balance", 0.0)))

    def __repr__(self) -> str:
        return f"BankAccount(owner={self.owner!r}, balance={self._balance:.2f})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BankAccount):
            return NotImplemented
        return (self.owner, self._balance) == (other.owner, other._balance)

    __hash__ = None  # mutable object with custom __eq__: deliberately unhashable


class SavingsAccount(BankAccount):
    interest_rate = 0.045  # overrides the class attribute

    @override
    def withdraw(self, amount: float) -> None:
        if amount > 1_000:
            raise ValueError("savings withdrawals are limited to 1,000")
        super().withdraw(amount)  # like base.Withdraw(amount)


# --- ABC: nominal typing, like an abstract base class -----------------------
class Notifier(ABC):
    @abstractmethod
    def send(self, to: str, message: str) -> str: ...


class EmailNotifier(Notifier):
    @override
    def send(self, to: str, message: str) -> str:
        return f"email to {to}: {message}"


# --- Protocol: structural typing, an interface satisfied implicitly --------
class SupportsSend(Protocol):
    def send(self, to: str, message: str) -> str: ...


class SmsGateway:  # does NOT inherit anything, but has a matching send()
    def send(self, to: str, message: str) -> str:
        return f"sms to {to}: {message}"


def broadcast(notifier: SupportsSend, recipients: list[str], message: str) -> list[str]:
    return [notifier.send(r, message) for r in recipients]


# --- Dataclasses: Python's records ------------------------------------------
@dataclass(frozen=True, slots=True)
class Money:
    amount: float
    currency: str = "USD"

    def __post_init__(self) -> None:  # validation, runs after generated __init__
        if self.amount < 0:
            raise ValueError("amount cannot be negative")
        if len(self.currency) != 3:
            raise ValueError("currency must be a 3-letter ISO code")

    def __add__(self, other: Money) -> Money:  # operator +
        if self.currency != other.currency:
            raise ValueError("currency mismatch")
        return Money(self.amount + other.amount, self.currency)


@dataclass(kw_only=True)
class ExperimentRun:
    """The kind of record you'll keep for every ML experiment from week 3 onward."""

    name: str
    learning_rate: float = 1e-3
    epochs: int = 10
    tags: list[str] = field(default_factory=list)
    metrics: dict[str, float] = field(default_factory=dict)

    def best_metric(self) -> tuple[str, float] | None:
        if not self.metrics:
            return None
        return max(self.metrics.items(), key=lambda kv: kv[1])


if __name__ == "__main__":
    acct = BankAccount.from_dict({"owner": "Raghu", "balance": 100})
    acct.deposit(50)
    print(acct, acct.balance)

    savings = SavingsAccount("Raghu", 5_000)
    print(savings.interest_rate, BankAccount.interest_rate)

    print(broadcast(EmailNotifier(), ["a@x.com"], "deploy done"))
    print(broadcast(SmsGateway(), ["+1555"], "deploy done"))  # no inheritance needed

    price = Money(19.99)
    print(price + Money(5.01), price == Money(19.99))  # value equality
    print(replace(price, currency="EUR"))  # like 'price with { Currency = "EUR" }'

    run = ExperimentRun(name="baseline", tags=["week1"])
    run.metrics["accuracy"] = 0.91
    run.metrics["f1"] = 0.88
    print(run)
    print(run.best_metric())