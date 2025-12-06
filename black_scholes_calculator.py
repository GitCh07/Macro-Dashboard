"""
Black-Scholes Options Pricing Calculator with Greeks
Built for real-world options trading analysis and risk management
"""

import numpy as np
from scipy.stats import norm
from datetime import datetime, timedelta
from typing import Dict, Tuple


class BlackScholesCalculator:
    """
    Complete Black-Scholes pricing engine with Greeks calculation.
    
    Attributes:
        S: Current stock price
        K: Strike price
        T: Time to expiration (in years)
        r: Risk-free interest rate (annualized)
        sigma: Volatility (annualized standard deviation)
        q: Dividend yield (annualized, continuous)
    """
    
    def __init__(self, S: float, K: float, T: float, r: float, sigma: float, q: float = 0.0):
        """
        Initialize Black-Scholes calculator with option parameters.
        
        Args:
            S: Current stock price
            K: Strike price
            T: Time to expiration in years (e.g., 30 days = 30/365)
            r: Risk-free rate (e.g., 0.05 for 5%)
            sigma: Implied volatility (e.g., 0.25 for 25%)
            q: Dividend yield (default 0.0)
        """
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.q = q
        
        # Calculate d1 and d2 (core B-S components)
        self.d1 = self._calculate_d1()
        self.d2 = self._calculate_d2()
    
    def _calculate_d1(self) -> float:
        """Calculate d1 component of Black-Scholes formula."""
        numerator = np.log(self.S / self.K) + (self.r - self.q + 0.5 * self.sigma**2) * self.T
        denominator = self.sigma * np.sqrt(self.T)
        return numerator / denominator if denominator != 0 else 0
    
    def _calculate_d2(self) -> float:
        """Calculate d2 component of Black-Scholes formula."""
        return self.d1 - self.sigma * np.sqrt(self.T)
    
    def call_price(self) -> float:
        """
        Calculate European call option price.
        
        Returns:
            Theoretical call option price
        """
        call = (self.S * np.exp(-self.q * self.T) * norm.cdf(self.d1) - 
                self.K * np.exp(-self.r * self.T) * norm.cdf(self.d2))
        return call
    
    def put_price(self) -> float:
        """
        Calculate European put option price.
        
        Returns:
            Theoretical put option price
        """
        put = (self.K * np.exp(-self.r * self.T) * norm.cdf(-self.d2) - 
               self.S * np.exp(-self.q * self.T) * norm.cdf(-self.d1))
        return put
    
    def call_delta(self) -> float:
        """
        Calculate call option Delta.
        Delta measures the rate of change of option price with respect to stock price.
        
        Returns:
            Call delta (range: 0 to 1)
        """
        return np.exp(-self.q * self.T) * norm.cdf(self.d1)
    
    def put_delta(self) -> float:
        """
        Calculate put option Delta.
        
        Returns:
            Put delta (range: -1 to 0)
        """
        return np.exp(-self.q * self.T) * (norm.cdf(self.d1) - 1)
    
    def gamma(self) -> float:
        """
        Calculate Gamma (same for calls and puts).
        Gamma measures the rate of change of Delta with respect to stock price.
        
        Returns:
            Gamma value
        """
        numerator = np.exp(-self.q * self.T) * norm.pdf(self.d1)
        denominator = self.S * self.sigma * np.sqrt(self.T)
        return numerator / denominator if denominator != 0 else 0
    
    def vega(self) -> float:
        """
        Calculate Vega (same for calls and puts).
        Vega measures sensitivity to volatility changes.
        
        Returns:
            Vega value (typically divided by 100 for 1% vol change)
        """
        vega = self.S * np.exp(-self.q * self.T) * norm.pdf(self.d1) * np.sqrt(self.T)
        return vega / 100  # Per 1% change in volatility
    
    def call_theta(self) -> float:
        """
        Calculate call option Theta.
        Theta measures time decay (negative for long positions).
        
        Returns:
            Call theta (per day, divide by 365)
        """
        term1 = -(self.S * norm.pdf(self.d1) * self.sigma * np.exp(-self.q * self.T)) / (2 * np.sqrt(self.T))
        term2 = self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(self.d2)
        term3 = self.q * self.S * np.exp(-self.q * self.T) * norm.cdf(self.d1)
        
        theta = term1 - term2 + term3
        return theta / 365  # Convert to per-day theta
    
    def put_theta(self) -> float:
        """
        Calculate put option Theta.
        
        Returns:
            Put theta (per day)
        """
        term1 = -(self.S * norm.pdf(self.d1) * self.sigma * np.exp(-self.q * self.T)) / (2 * np.sqrt(self.T))
        term2 = self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(-self.d2)
        term3 = self.q * self.S * np.exp(-self.q * self.T) * norm.cdf(-self.d1)
        
        theta = term1 + term2 - term3
        return theta / 365  # Convert to per-day theta
    
    def call_rho(self) -> float:
        """
        Calculate call option Rho.
        Rho measures sensitivity to interest rate changes.
        
        Returns:
            Call rho (per 1% change in interest rate)
        """
        rho = self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(self.d2)
        return rho / 100  # Per 1% change in interest rate
    
    def put_rho(self) -> float:
        """
        Calculate put option Rho.
        
        Returns:
            Put rho (per 1% change in interest rate)
        """
        rho = -self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(-self.d2)
        return rho / 100  # Per 1% change in interest rate
    
    def get_all_greeks(self, option_type: str = 'call') -> Dict[str, float]:
        """
        Get all Greeks for specified option type.
        
        Args:
            option_type: 'call' or 'put'
            
        Returns:
            Dictionary containing all Greeks
        """
        if option_type.lower() == 'call':
            return {
                'price': self.call_price(),
                'delta': self.call_delta(),
                'gamma': self.gamma(),
                'theta': self.call_theta(),
                'vega': self.vega(),
                'rho': self.call_rho()
            }
        else:
            return {
                'price': self.put_price(),
                'delta': self.put_delta(),
                'gamma': self.gamma(),
                'theta': self.put_theta(),
                'vega': self.vega(),
                'rho': self.put_rho()
            }
    
    def intrinsic_value(self, option_type: str = 'call') -> float:
        """Calculate intrinsic value of option."""
        if option_type.lower() == 'call':
            return max(0, self.S - self.K)
        else:
            return max(0, self.K - self.S)
    
    def time_value(self, option_type: str = 'call') -> float:
        """Calculate time value (extrinsic value) of option."""
        if option_type.lower() == 'call':
            return self.call_price() - self.intrinsic_value('call')
        else:
            return self.put_price() - self.intrinsic_value('put')
    
    def probability_itm(self, option_type: str = 'call') -> float:
        """
        Calculate probability of option finishing in-the-money.
        
        Args:
            option_type: 'call' or 'put'
            
        Returns:
            Probability (0 to 1)
        """
        if option_type.lower() == 'call':
            return norm.cdf(self.d2)
        else:
            return norm.cdf(-self.d2)


def days_to_expiration(expiration_date: str) -> float:
    """
    Convert expiration date to years for Black-Scholes.
    
    Args:
        expiration_date: Date string in 'YYYY-MM-DD' format
        
    Returns:
        Time to expiration in years
    """
    exp_date = datetime.strptime(expiration_date, '%Y-%m-%d')
    today = datetime.now()
    days = (exp_date - today).days
    return max(days / 365.0, 0.0001)  # Avoid division by zero


def implied_volatility(market_price: float, S: float, K: float, T: float, 
                       r: float, option_type: str = 'call', q: float = 0.0,
                       max_iterations: int = 100, tolerance: float = 0.0001) -> float:
    """
    Calculate implied volatility using Newton-Raphson method.
    
    Args:
        market_price: Observed market price of option
        S: Current stock price
        K: Strike price
        T: Time to expiration (years)
        r: Risk-free rate
        option_type: 'call' or 'put'
        q: Dividend yield
        max_iterations: Maximum number of iterations
        tolerance: Convergence tolerance
        
    Returns:
        Implied volatility (annualized)
    """
    # Initial guess
    sigma = 0.3
    
    for i in range(max_iterations):
        bs = BlackScholesCalculator(S, K, T, r, sigma, q)
        
        # Get theoretical price and vega
        if option_type.lower() == 'call':
            theo_price = bs.call_price()
        else:
            theo_price = bs.put_price()
        
        vega = bs.vega() * 100  # Convert back to per 1.0 change
        
        # Price difference
        price_diff = theo_price - market_price
        
        # Check convergence
        if abs(price_diff) < tolerance:
            return sigma
        
        # Newton-Raphson update
        if vega != 0:
            sigma = sigma - price_diff / vega
            sigma = max(0.0001, sigma)  # Ensure positive volatility
        else:
            break
    
    return sigma  # Return best estimate even if not converged


def print_option_analysis(bs: BlackScholesCalculator, option_type: str = 'call'):
    """
    Print formatted analysis of option pricing and Greeks.
    
    Args:
        bs: BlackScholesCalculator instance
        option_type: 'call' or 'put'
    """
    greeks = bs.get_all_greeks(option_type)
    
    print(f"\n{'='*60}")
    print(f"BLACK-SCHOLES {option_type.upper()} OPTION ANALYSIS")
    print(f"{'='*60}")
    print(f"\nUnderlying Parameters:")
    print(f"  Stock Price (S):        ${bs.S:.2f}")
    print(f"  Strike Price (K):       ${bs.K:.2f}")
    print(f"  Time to Expiration:     {bs.T:.4f} years ({bs.T*365:.0f} days)")
    print(f"  Volatility (σ):         {bs.sigma*100:.2f}%")
    print(f"  Risk-Free Rate (r):     {bs.r*100:.2f}%")
    print(f"  Dividend Yield (q):     {bs.q*100:.2f}%")
    
    print(f"\n{option_type.upper()} Option Pricing:")
    print(f"  Theoretical Price:      ${greeks['price']:.4f}")
    print(f"  Intrinsic Value:        ${bs.intrinsic_value(option_type):.4f}")
    print(f"  Time Value:             ${bs.time_value(option_type):.4f}")
    print(f"  Probability ITM:        {bs.probability_itm(option_type)*100:.2f}%")
    
    print(f"\nThe Greeks:")
    print(f"  Delta (Δ):              {greeks['delta']:.4f}")
    print(f"  Gamma (Γ):              {greeks['gamma']:.6f}")
    print(f"  Theta (Θ):              ${greeks['theta']:.4f} per day")
    print(f"  Vega (ν):               ${greeks['vega']:.4f} per 1% vol change")
    print(f"  Rho (ρ):                ${greeks['rho']:.4f} per 1% rate change")
    
    print(f"\nTrading Insights:")
    print(f"  • For every $1 move in stock, {option_type} changes by ${abs(greeks['delta']):.2f}")
    print(f"  • Daily time decay is ${abs(greeks['theta']):.2f}")
    print(f"  • 1% volatility increase adds ${greeks['vega']:.2f} to price")
    print(f"{'='*60}\n")


# Example usage and testing
if __name__ == "__main__":
    # Example 1: Basic call option analysis
    print("\nEXAMPLE 1: NVIDIA CALL OPTION")
    nvda_call = BlackScholesCalculator(
        S=140.00,      # NVDA trading at $140
        K=145.00,      # $145 strike call
        T=30/365,      # 30 days to expiration
        r=0.05,        # 5% risk-free rate
        sigma=0.45,    # 45% implied volatility
        q=0.0          # No dividend
    )
    print_option_analysis(nvda_call, 'call')
    
    # Example 2: Put option with dividend
    print("\nEXAMPLE 2: APPLE PUT OPTION")
    aapl_put = BlackScholesCalculator(
        S=185.00,      # AAPL at $185
        K=180.00,      # $180 strike put
        T=45/365,      # 45 days to expiration
        r=0.05,        # 5% risk-free rate
        sigma=0.30,    # 30% implied volatility
        q=0.005        # 0.5% dividend yield
    )
    print_option_analysis(aapl_put, 'put')
    
    # Example 3: Implied volatility calculation
    print("\nEXAMPLE 3: IMPLIED VOLATILITY CALCULATION")
    market_call_price = 8.50
    iv = implied_volatility(
        market_price=market_call_price,
        S=150.00,
        K=155.00,
        T=60/365,
        r=0.05,
        option_type='call'
    )
    print(f"Market Price: ${market_call_price:.2f}")
    print(f"Implied Volatility: {iv*100:.2f}%")
    
    # Example 4: Compare multiple strikes (volatility smile analysis)
    print("\nEXAMPLE 4: STRIKE COMPARISON")
    print(f"{'Strike':<10}{'Call Price':<15}{'Delta':<12}{'Theta':<12}{'Prob ITM'}")
    print("-" * 60)
    
    stock_price = 100
    strikes = [90, 95, 100, 105, 110]
    
    for strike in strikes:
        bs = BlackScholesCalculator(
            S=stock_price,
            K=strike,
            T=30/365,
            r=0.05,
            sigma=0.35
        )
        greeks = bs.get_all_greeks('call')
        prob = bs.probability_itm('call')
        
        print(f"${strike:<9.0f}${greeks['price']:<14.2f}{greeks['delta']:<12.3f}"
              f"${greeks['theta']:<11.2f}{prob*100:.1f}%")
