from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str

    def __post_init__(self) -> None:
        if not isinstance(self.amount, Decimal):
            object.__setattr__(self, "amount", Decimal(str(self.amount)))
        if self.amount < Decimal("0"):
            raise ValueError("Money amount cannot be negative.")
        if not self.currency or not self.currency.strip():
            raise ValueError("Currency cannot be empty.")

    def add(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError(
                f"Cannot add money with different currencies: "
                f"{self.currency} vs {other.currency}"
            )
        return Money(self.amount + other.amount, self.currency)

    def multiply(self, factor: int) -> "Money":
        if factor < 0:
            raise ValueError("Multiplication factor cannot be negative.")
        return Money(self.amount * Decimal(factor), self.currency)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return False
        return self.amount == other.amount and self.currency == other.currency

    def __repr__(self) -> str:
        return f"Money(amount={self.amount}, currency={self.currency!r})"