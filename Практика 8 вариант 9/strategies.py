# Паттерн STRATEGY: разные способы расчёта цены.
# Стратегию можно менять на лету, не трогая остальной код.

from abc import ABC, abstractmethod


# Абстрактная стратегия
class PricingStrategy(ABC):
    @abstractmethod
    def calculate(self, base):
        ...


# Стандартная цена (без изменений)
class StandardPricing(PricingStrategy):
    def calculate(self, base):
        return base


# Сезонная цена (наценка 20%)
class SeasonalPricing(PricingStrategy):
    def calculate(self, base):
        return base * 1.2


# Динамическая цена: чем больше продано мест, тем дороже
class DynamicPricing(PricingStrategy):
    def __init__(self, sold, capacity):
        self.sold = sold
        self.capacity = capacity

    def calculate(self, base):
        if self.capacity == 0:
            return base
        factor = 1 + self.sold / self.capacity   # от x1 до x2
        return base * factor
