import httpx

from src.config.settings import settings
from src.integrations.finances.exceptions import FinanceIntegrationError
from src.integrations.finances.models import Account, Stock, Fund, NetWorthSnapshot, FinanceHealthMetrics, \
    MonthlyReport, ReportOverview, ReportIncome, ReportExpense


class FinancesAppClient:

    def __init__(self):

        self.client = httpx.Client(
            base_url=settings.finances_url,
            headers={
                "Content-Type": "application/json",
            },
            follow_redirects=True,
        )


    def get_accounts(self) -> list[Account]:
        try:
            data = self._make_get_request("/api/v1/accounts")
            return [Account(**item) for item in data]
        except httpx.HTTPError as e:
            raise FinanceIntegrationError(f"Error fetching accounts: {e}") from e


    def get_stocks(self) -> list[Stock]:
        try:
            data = self._make_get_request("/api/v1/investments/stocks")
            return [Stock(**item) for item in data]
        except httpx.HTTPError as e:
            raise FinanceIntegrationError(f"Error fetching stocks: {e}") from e


    def get_investment_funds(self) -> list[Fund]:
        try:
            data = self._make_get_request("/api/v1/investments/funds")
            return [Fund(**item) for item in data]
        except httpx.HTTPError as e:
            raise FinanceIntegrationError(f"Error fetching investment funds: {e}") from e


    def get_net_worth_history(self) -> list[NetWorthSnapshot]:
        try:
            data = self._make_get_request("/api/v1/networth/history")
            return [NetWorthSnapshot(**item) for item in data]
        except httpx.HTTPError as e:
            raise FinanceIntegrationError(f"Error fetching net worth history: {e}") from e


    def get_health_metrics(self) -> FinanceHealthMetrics:
        try:
            data = self._make_get_request("/api/v1/health-metrics")
            return FinanceHealthMetrics(**data)
        except httpx.HTTPError as e:
            raise FinanceIntegrationError(f"Error fetching health metrics: {e}") from e


    def get_report_by_month(self, date: str):
        try:
            data = self._make_get_request(f"/api/v1/report", params={"date": date})
            if not data.get("hasData"):
                raise FinanceIntegrationError(f"No report data available for {date}")
            result = data.get("data")
            return MonthlyReport(
                categories=result["categories"],
                expenses=[
                    ReportExpense(**expense)
                    for expense in result["expenses"]
                ],
                income=[
                    ReportIncome(**income)
                    for income in result["income"]
                ],
                overview=ReportOverview(**result["overview"]),
            )
        except httpx.HTTPError as e:
            raise FinanceIntegrationError(f"Error fetching report for {date}: {e}") from e


    def _make_get_request(self, endpoint: str, params: dict = None) -> dict:
        response = self.client.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()