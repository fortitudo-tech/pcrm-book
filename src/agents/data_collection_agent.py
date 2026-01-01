"""
Data Collection Agent for financial data gathering and management.

This agent handles the collection, validation, and storage of financial
market data from various sources including Yahoo Finance.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Union
import yfinance as yf

from .base_agent import BaseAgent


class DataCollectionAgent(BaseAgent):
    """
    Agent specialized in collecting and managing financial market data.

    This agent can:
    - Download historical price data
    - Retrieve fundamental data
    - Collect dividend and split information
    - Fetch multiple securities simultaneously
    - Handle data validation and cleaning
    """

    def __init__(self, **kwargs):
        """Initialize the Data Collection Agent."""
        super().__init__(
            name="DataCollectionAgent",
            description="Collects and manages financial market data",
            **kwargs
        )
        self.cache = {}

    def execute(
        self,
        tickers: Union[str, List[str]],
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        period: str = "1y",
        interval: str = "1d",
        **kwargs
    ) -> pd.DataFrame:
        """
        Execute data collection for specified tickers.

        Args:
            tickers: Single ticker or list of tickers
            start_date: Start date (YYYY-MM-DD format)
            end_date: End date (YYYY-MM-DD format)
            period: Period to download (e.g., '1d', '5d', '1mo', '1y', 'max')
            interval: Data interval (e.g., '1m', '5m', '1h', '1d', '1wk', '1mo')
            **kwargs: Additional parameters for yfinance

        Returns:
            DataFrame with price data
        """
        self.logger.info(f"Collecting data for: {tickers}")

        if isinstance(tickers, str):
            tickers = [tickers]

        try:
            data = yf.download(
                tickers=tickers,
                start=start_date,
                end=end_date,
                period=period,
                interval=interval,
                group_by='ticker',
                auto_adjust=False,
                progress=False,
                **kwargs
            )

            self.logger.info(f"Successfully collected {len(data)} rows of data")
            return data

        except Exception as e:
            self.logger.error(f"Error collecting data: {str(e)}")
            raise

    def get_ticker_info(self, ticker: str) -> Dict:
        """
        Get detailed information about a ticker.

        Args:
            ticker: Ticker symbol

        Returns:
            Dictionary containing ticker information
        """
        self.logger.info(f"Fetching info for {ticker}")

        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            self.logger.info(f"Successfully retrieved info for {ticker}")
            return info

        except Exception as e:
            self.logger.error(f"Error fetching info for {ticker}: {str(e)}")
            raise

    def get_dividends(self, ticker: str) -> pd.Series:
        """
        Get dividend history for a ticker.

        Args:
            ticker: Ticker symbol

        Returns:
            Series containing dividend history
        """
        self.logger.info(f"Fetching dividends for {ticker}")

        try:
            stock = yf.Ticker(ticker)
            dividends = stock.dividends
            self.logger.info(f"Retrieved {len(dividends)} dividend records")
            return dividends

        except Exception as e:
            self.logger.error(f"Error fetching dividends: {str(e)}")
            raise

    def get_splits(self, ticker: str) -> pd.Series:
        """
        Get stock split history for a ticker.

        Args:
            ticker: Ticker symbol

        Returns:
            Series containing split history
        """
        self.logger.info(f"Fetching splits for {ticker}")

        try:
            stock = yf.Ticker(ticker)
            splits = stock.splits
            self.logger.info(f"Retrieved {len(splits)} split records")
            return splits

        except Exception as e:
            self.logger.error(f"Error fetching splits: {str(e)}")
            raise

    def get_financial_statements(
        self,
        ticker: str,
        statement_type: str = "income"
    ) -> pd.DataFrame:
        """
        Get financial statements for a ticker.

        Args:
            ticker: Ticker symbol
            statement_type: Type of statement ('income', 'balance', 'cashflow')

        Returns:
            DataFrame containing financial statements
        """
        self.logger.info(f"Fetching {statement_type} statement for {ticker}")

        try:
            stock = yf.Ticker(ticker)

            if statement_type == "income":
                data = stock.financials
            elif statement_type == "balance":
                data = stock.balance_sheet
            elif statement_type == "cashflow":
                data = stock.cashflow
            else:
                raise ValueError(f"Invalid statement type: {statement_type}")

            self.logger.info(f"Successfully retrieved {statement_type} statement")
            return data

        except Exception as e:
            self.logger.error(f"Error fetching financial statements: {str(e)}")
            raise

    def calculate_returns(
        self,
        prices: pd.DataFrame,
        method: str = "simple"
    ) -> pd.DataFrame:
        """
        Calculate returns from price data.

        Args:
            prices: DataFrame with price data
            method: 'simple' or 'log' returns

        Returns:
            DataFrame with calculated returns
        """
        self.logger.info(f"Calculating {method} returns")

        try:
            if method == "simple":
                returns = prices.pct_change()
            elif method == "log":
                returns = np.log(prices / prices.shift(1))
            else:
                raise ValueError(f"Invalid method: {method}")

            self.logger.info("Returns calculated successfully")
            return returns

        except Exception as e:
            self.logger.error(f"Error calculating returns: {str(e)}")
            raise

    def validate_data(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Validate collected data and report issues.

        Args:
            data: DataFrame to validate

        Returns:
            Dictionary with validation results
        """
        self.logger.info("Validating data")

        validation_report = {
            'total_rows': len(data),
            'missing_values': data.isnull().sum().to_dict(),
            'date_range': {
                'start': data.index.min() if len(data) > 0 else None,
                'end': data.index.max() if len(data) > 0 else None
            },
            'columns': list(data.columns),
            'duplicates': data.index.duplicated().sum()
        }

        self.logger.info("Validation complete")
        return validation_report
