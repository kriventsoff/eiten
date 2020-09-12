# Basic libraries
import os
import sys
import math
import scipy
import random
import collections
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

# Styling for plots
plt.style.use('seaborn-white')
plt.rc('grid', linestyle="dotted", color='#a0a0a0')
plt.rcParams['axes.edgecolor'] = "#04383F"


class BackTester:
    """
    Backtester module that does both backward and forward testing for our portfolios.
    """

    def __init__(self):
        print("\n--# Backtester has been initialized")

    def price_delta(self, prices):
        """
        Percentage change
        """

        return ((prices - prices.shift()) * 100 / prices.shift())[1:]

    def portfolio_weight_manager(self, weight, is_long_only):
        """
        Manage portfolio weights. If portfolio is long only, 
        set the negative weights to zero.
        """
        if is_long_only == 1:
            weight = max(weight, 0)
        else:
            weight = weight
        return weight

    def back_test(self, p_weights, data, market_data, long_only: bool,
                  market_chart: bool, strategy_name: str):
        """
        Main backtest function. Takes in the portfolio weights and compares 
        the portfolio returns with a market index of your choice.
        """
        historical_data = market_data
        # Get market returns during the backtesting time
        symbol_names = list(p_weights.keys())
        historical_prices = historical_data["historical"]["Close"]
        market_returns = self.price_delta(historical_prices)
        market_returns_cumulative = np.cumsum(market_returns)

        # Get invidiual returns for each stock in our portfolio
        normal_returns_matrix = []
        for symbol in symbol_names:
            symbol_historical_prices = data[symbol]["historical"]["Close"]
            symbol_historical_returns = self.price_delta(
                symbol_historical_prices)
            normal_returns_matrix.append(symbol_historical_returns)

        # Get portfolio returns
        normal_returns_matrix = np.array(normal_returns_matrix).transpose()
        portfolio_weights_vector = np.array([self.portfolio_weight_manager(
            p_weights[symbol], long_only) for symbol in p_weights]).transpose()
        portfolio_returns = np.dot(
            normal_returns_matrix, portfolio_weights_vector)
        portfolio_returns_cumulative = np.cumsum(portfolio_returns)

        # Plot returns
        x = np.arange(len(portfolio_returns_cumulative))
        plt.plot(x, portfolio_returns_cumulative,
                 linewidth=2.0, label=strategy_name)
        plt.axhline(y=0, linestyle='dotted', alpha=0.3, color='black')
        if market_chart:
            x = np.arange(len(market_returns_cumulative))
            plt.plot(x, market_returns_cumulative, linewidth=2.0,
                     color='#282828', label='Market Index', linestyle='--')

        # Plotting styles
        plt.title("Backtest Results", fontsize=14)
        plt.xlabel("Bars (Time Sorted)", fontsize=14)
        plt.ylabel("Cumulative Percentage Return", fontsize=14)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)

    def future_test(self, p_weights, data, market_data, long_only: bool,
                    market_chart: bool, strategy_name: str):
        """
        Main future test function. If future data is available i.e is_test
        is set to 1 and future_bars set to > 0, this takes in the portfolio
        weights and compares the portfolio returns with a market index of1
        your choice in the future.
        """
        symbol_names = list(p_weights.keys())
        #future_data = data_dict[symbol]["future"].Close

        # Get future prices
        future_price_market = market_data["future"].Close
        market_returns = self.price_delta(future_price_market)
        market_returns_cumulative = np.cumsum(market_returns)

        # Get invidiual returns for each stock in our portfolio
        normal_returns_matrix = []
        for symbol in symbol_names:
            symbol_historical_prices = data[symbol]["future"].Close
            symbol_historical_returns = self.price_delta(
                symbol_historical_prices)
            normal_returns_matrix.append(symbol_historical_returns)

        # Get portfolio returns
        normal_returns_matrix = np.array(normal_returns_matrix).transpose()
        portfolio_weights_vector = np.array([self.portfolio_weight_manager(
            p_weights[symbol], long_only) for symbol in p_weights]).transpose()
        portfolio_returns = np.dot(
            normal_returns_matrix, portfolio_weights_vector)
        portfolio_returns_cumulative = np.cumsum(portfolio_returns)

        # Plot
        x = np.arange(len(portfolio_returns_cumulative))
        plt.axhline(y=0, linestyle='dotted', alpha=0.3, color='black')
        plt.plot(x, portfolio_returns_cumulative,
                 linewidth=2.0, label=strategy_name)
        if market_chart:
            x = np.arange(len(market_returns_cumulative))
            plt.plot(x, market_returns_cumulative, linewidth=2.0,
                     color='#282828', label='Market Index', linestyle='--')

        # Plotting styles
        plt.title("Future Test Results", fontsize=14)
        plt.xlabel("Bars (Time Sorted)", fontsize=14)
        plt.ylabel("Cumulative Percentage Return", fontsize=14)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
