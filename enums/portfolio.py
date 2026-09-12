from enum import StrEnum

class PortfolioType(StrEnum):
    ETF = "etf"
    CRYPTO = "crypto"
    STOCKS = "stocks"
    MIXED = "mixed"
    RETIREMENT = "retirement"

class Currency(StrEnum):
    USD = "usd"
    EUR = "eur"
    CZK = "czk"
