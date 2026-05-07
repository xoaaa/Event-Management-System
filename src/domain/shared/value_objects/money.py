from dataclasses import dataclass


@dataclass(frozen=True)
class Money:
    amount: float
    currency: str = "IDR"

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Money amount cannot be negative")
        if not self.currency:
            raise ValueError("Currency is required")

    def add(self, other: "Money") -> "Money":
        self._assert_same_currency(other)
        return Money(self.amount + other.amount, self.currency)

    def multiply(self, factor: float) -> "Money":
        if factor < 0:
            raise ValueError("Factor cannot be negative")
        return Money(self.amount * factor, self.currency)

    def _assert_same_currency(self, other: "Money") -> None:
        if self.currency != other.currency:
            raise ValueError("Cannot operate on different currencies")
