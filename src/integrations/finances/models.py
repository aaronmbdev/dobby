from dataclasses import dataclass


@dataclass(frozen=True)
class Account:
    id: str
    name: str
    description: str
    latestBalance: float
    latestBalanceDate: str


@dataclass(frozen=True)
class Stock:
    id: str
    latestDate: str
    latestPriceEur: float
    latestShares: float
    name: str
    ticker: str


@dataclass(frozen=True)
class Fund:
    id: str
    isin: str
    latestDate: str
    latestPriceEur: float
    latestShares: float
    name: str
    yahooTicker: str


@dataclass(frozen=True)
class NetWorthSnapshot:
    date: str
    accountsTotal: float
    fundsTotal: float
    stocksTotal: float
    total: float


@dataclass(frozen=True)
class FinanceHealthMetrics:
    averageMonthlyIncome: float
    essentialMonthlyBurn: float
    totalAccountBalance: float
    totalMonthlyBurn: float
    debtToIncome: dict
    emergencyFund: dict
    expenseDistribution: list[dict]
    expenseGrowthRate: dict
    fixedVsVariable: dict
    housingRatio: dict
    investmentRatio: dict
    savingsRate: dict


@dataclass(frozen=True)
class ReportExpense:
    date: str
    period: str
    description: str
    category: str
    amount: float


@dataclass(frozen=True)
class ReportIncome:
    liquido: float

    def __init__(self, liquido: float, **kwargs):
        object.__setattr__(self, 'liquido', liquido)


@dataclass(frozen=True)
class ReportOverview:
    balance: float
    monthlyExpenses: float
    monthlyIncome: float


@dataclass(frozen=True)
class MonthlyReport:
    categories: dict[str, float]
    expenses: list[ReportExpense]
    income: list[ReportIncome]
    overview: ReportOverview