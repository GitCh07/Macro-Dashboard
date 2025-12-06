"""
Custom Options Strategy Template
Use this template to build and analyze your own option strategies
"""

from black_scholes_calculator import BlackScholesCalculator
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt


class OptionPosition:
    """Represents a single option position (long or short)."""
    
    def __init__(self, option_type, strike, position_type, quantity=1):
        """
        Args:
            option_type: 'call' or 'put'
            strike: Strike price
            position_type: 'long' or 'short'
            quantity: Number of contracts (default 1)
        """
        self.option_type = option_type.lower()
        self.strike = strike
        self.position_type = position_type.lower()
        self.quantity = quantity
        self.multiplier = 1 if position_type == 'long' else -1
        
    def __repr__(self):
        direction = "Long" if self.position_type == 'long' else "Short"
        return f"{direction} {self.quantity} x ${self.strike} {self.option_type.upper()}"


class OptionStrategy:
    """Build and analyze custom multi-leg option strategies."""
    
    def __init__(self, stock_price, time_to_exp, risk_free_rate=0.05, 
                 volatility=0.35, dividend_yield=0.0):
        """
        Initialize strategy builder.
        
        Args:
            stock_price: Current stock price
            time_to_exp: Days to expiration
            risk_free_rate: Annual risk-free rate
            volatility: Implied volatility
            dividend_yield: Annual dividend yield
        """
        self.stock_price = stock_price
        self.time_to_exp = time_to_exp / 365.0
        self.risk_free_rate = risk_free_rate
        self.volatility = volatility
        self.dividend_yield = dividend_yield
        self.positions = []
        
    def add_option(self, option_type, strike, position_type, quantity=1):
        """Add an option leg to the strategy."""
        position = OptionPosition(option_type, strike, position_type, quantity)
        self.positions.append(position)
        return self
    
    def add_stock(self, quantity):
        """Add long/short stock position (use negative for short)."""
        self.stock_position = quantity
        return self
    
    def calculate_strategy_price(self):
        """Calculate total cost/credit of the strategy."""
        total_cost = 0
        
        for pos in self.positions:
            bs = BlackScholesCalculator(
                S=self.stock_price,
                K=pos.strike,
                T=self.time_to_exp,
                r=self.risk_free_rate,
                sigma=self.volatility,
                q=self.dividend_yield
            )
            
            if pos.option_type == 'call':
                option_price = bs.call_price()
            else:
                option_price = bs.put_price()
            
            # Long = pay premium (positive cost), Short = receive premium (negative cost)
            cost = pos.multiplier * option_price * pos.quantity * 100
            total_cost += cost
        
        return total_cost
    
    def calculate_greeks(self):
        """Calculate aggregate Greeks for the entire strategy."""
        total_delta = 0
        total_gamma = 0
        total_theta = 0
        total_vega = 0
        total_rho = 0
        
        for pos in self.positions:
            bs = BlackScholesCalculator(
                S=self.stock_price,
                K=pos.strike,
                T=self.time_to_exp,
                r=self.risk_free_rate,
                sigma=self.volatility,
                q=self.dividend_yield
            )
            
            if pos.option_type == 'call':
                delta = bs.call_delta()
                theta = bs.call_theta()
                rho = bs.call_rho()
            else:
                delta = bs.put_delta()
                theta = bs.put_theta()
                rho = bs.put_rho()
            
            gamma = bs.gamma()
            vega = bs.vega()
            
            # Multiply by position direction and quantity
            multiplier = pos.multiplier * pos.quantity * 100
            total_delta += delta * multiplier
            total_gamma += gamma * multiplier
            total_theta += theta * multiplier
            total_vega += vega * multiplier
            total_rho += rho * multiplier
        
        return {
            'delta': total_delta,
            'gamma': total_gamma,
            'theta': total_theta,
            'vega': total_vega,
            'rho': total_rho
        }
    
    def payoff_at_expiration(self, stock_prices):
        """
        Calculate strategy P&L at expiration for range of stock prices.
        
        Args:
            stock_prices: Array of stock prices to evaluate
            
        Returns:
            Array of P&L values
        """
        payoffs = np.zeros_like(stock_prices)
        
        for pos in self.positions:
            for i, price in enumerate(stock_prices):
                if pos.option_type == 'call':
                    intrinsic = max(0, price - pos.strike)
                else:
                    intrinsic = max(0, pos.strike - price)
                
                # Long = receive intrinsic, Short = pay intrinsic
                payoff = pos.multiplier * intrinsic * pos.quantity * 100
                payoffs[i] += payoff
        
        # Subtract initial cost (negative if credit received)
        initial_cost = self.calculate_strategy_price()
        payoffs -= initial_cost
        
        return payoffs
    
    def plot_payoff_diagram(self, price_range_pct=0.3, filename='strategy_payoff.png'):
        """
        Create payoff diagram showing P&L at expiration.
        
        Args:
            price_range_pct: % range around current price to plot
            filename: Output filename for the plot
        """
        # Generate stock price range
        lower = self.stock_price * (1 - price_range_pct)
        upper = self.stock_price * (1 + price_range_pct)
        stock_prices = np.linspace(lower, upper, 200)
        
        # Calculate payoffs
        payoffs = self.payoff_at_expiration(stock_prices)
        
        # Create plot
        plt.figure(figsize=(12, 7))
        plt.plot(stock_prices, payoffs, 'b-', linewidth=2, label='Strategy P&L')
        plt.axhline(y=0, color='k', linestyle='--', alpha=0.3)
        plt.axvline(x=self.stock_price, color='r', linestyle='--', 
                   alpha=0.5, label=f'Current Price: ${self.stock_price:.2f}')
        
        # Mark breakeven points
        breakevens = []
        for i in range(len(payoffs)-1):
            if (payoffs[i] <= 0 and payoffs[i+1] > 0) or (payoffs[i] >= 0 and payoffs[i+1] < 0):
                breakevens.append(stock_prices[i])
        
        for be in breakevens:
            plt.axvline(x=be, color='g', linestyle=':', alpha=0.5)
            plt.text(be, plt.ylim()[1]*0.9, f'BE: ${be:.2f}', 
                    rotation=90, va='top', ha='right')
        
        # Formatting
        plt.xlabel('Stock Price at Expiration', fontsize=12)
        plt.ylabel('Profit / Loss ($)', fontsize=12)
        plt.title('Option Strategy Payoff Diagram', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        # Add max profit/loss annotations
        max_profit = np.max(payoffs)
        max_loss = np.min(payoffs)
        plt.text(0.02, 0.98, f'Max Profit: ${max_profit:,.2f}\nMax Loss: ${max_loss:,.2f}', 
                transform=plt.gca().transAxes, fontsize=10,
                verticalalignment='top', bbox=dict(boxstyle='round', 
                facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        plt.savefig(f'/mnt/user-data/outputs/{filename}', dpi=150, bbox_inches='tight')
        plt.close()
        
        return f'/mnt/user-data/outputs/{filename}'
    
    def analyze(self, print_details=True):
        """Complete strategy analysis."""
        cost = self.calculate_strategy_price()
        greeks = self.calculate_greeks()
        
        # Generate price range for analysis
        prices = np.linspace(self.stock_price * 0.7, self.stock_price * 1.3, 200)
        payoffs = self.payoff_at_expiration(prices)
        
        max_profit = np.max(payoffs)
        max_loss = np.min(payoffs)
        
        # Find breakeven points
        breakevens = []
        for i in range(len(payoffs)-1):
            if (payoffs[i] <= 0 and payoffs[i+1] > 0) or (payoffs[i] >= 0 and payoffs[i+1] < 0):
                breakevens.append(prices[i])
        
        if print_details:
            print(f"\n{'='*70}")
            print(f"CUSTOM STRATEGY ANALYSIS")
            print(f"{'='*70}")
            
            print(f"\nStrategy Legs:")
            for i, pos in enumerate(self.positions, 1):
                print(f"  {i}. {pos}")
            
            print(f"\nStrategy Pricing:")
            if cost > 0:
                print(f"  Net Debit: ${cost:,.2f} (paid)")
            else:
                print(f"  Net Credit: ${abs(cost):,.2f} (received)")
            
            print(f"\nRisk/Reward:")
            print(f"  Max Profit: ${max_profit:,.2f}")
            print(f"  Max Loss: ${max_loss:,.2f}")
            if max_loss != 0:
                print(f"  Risk/Reward Ratio: {abs(max_profit/max_loss):.2f}:1")
            
            if breakevens:
                print(f"\nBreakeven Points:")
                for be in breakevens:
                    print(f"  ${be:.2f} ({(be/self.stock_price - 1)*100:+.1f}% from current)")
            
            print(f"\nPortfolio Greeks:")
            print(f"  Delta: {greeks['delta']:.2f}")
            print(f"  Gamma: {greeks['gamma']:.4f}")
            print(f"  Theta: ${greeks['theta']:.2f}/day")
            print(f"  Vega: ${greeks['vega']:.2f} per 1% vol")
            
            print(f"\nCharacteristics:")
            if abs(greeks['delta']) < 50:
                print(f"  • Delta neutral (±{abs(greeks['delta']):.0f})")
            elif greeks['delta'] > 0:
                print(f"  • Bullish bias (delta: +{greeks['delta']:.0f})")
            else:
                print(f"  • Bearish bias (delta: {greeks['delta']:.0f})")
            
            if greeks['theta'] > 0:
                print(f"  • Positive theta: earning ${greeks['theta']:.2f}/day from time decay")
            else:
                print(f"  • Negative theta: losing ${abs(greeks['theta']):.2f}/day to time decay")
            
            if greeks['vega'] > 0:
                print(f"  • Long volatility: gains if IV increases")
            else:
                print(f"  • Short volatility: gains if IV decreases")
        
        return {
            'cost': cost,
            'max_profit': max_profit,
            'max_loss': max_loss,
            'breakevens': breakevens,
            'greeks': greeks
        }


# ==============================================================================
# PRE-BUILT COMMON STRATEGIES
# ==============================================================================

def iron_condor(stock_price, days_to_exp, vol=0.35):
    """
    Iron Condor: Sell OTM put spread + sell OTM call spread
    Profits from low volatility / sideways movement
    """
    strategy = OptionStrategy(stock_price, days_to_exp, volatility=vol)
    
    # Sell put spread
    strategy.add_option('put', stock_price * 0.95, 'short')  # Sell put
    strategy.add_option('put', stock_price * 0.90, 'long')   # Buy put (protection)
    
    # Sell call spread
    strategy.add_option('call', stock_price * 1.05, 'short')  # Sell call
    strategy.add_option('call', stock_price * 1.10, 'long')   # Buy call (protection)
    
    return strategy


def bull_put_spread(stock_price, days_to_exp, vol=0.35):
    """
    Bull Put Spread: Sell higher strike put, buy lower strike put
    Bullish strategy with defined risk
    """
    strategy = OptionStrategy(stock_price, days_to_exp, volatility=vol)
    
    strategy.add_option('put', stock_price * 0.95, 'short')  # Sell higher put
    strategy.add_option('put', stock_price * 0.90, 'long')   # Buy lower put
    
    return strategy


def straddle(stock_price, days_to_exp, vol=0.35, position='long'):
    """
    Straddle: Buy/sell ATM call + ATM put
    Long = bet on big move, Short = bet on no move
    """
    strategy = OptionStrategy(stock_price, days_to_exp, volatility=vol)
    
    strategy.add_option('call', stock_price, position)
    strategy.add_option('put', stock_price, position)
    
    return strategy


def butterfly(stock_price, days_to_exp, vol=0.35):
    """
    Butterfly: Buy 1 lower, Sell 2 middle, Buy 1 higher
    Profits if price stays near middle strike
    """
    strategy = OptionStrategy(stock_price, days_to_exp, volatility=vol)
    
    lower = stock_price * 0.95
    middle = stock_price
    upper = stock_price * 1.05
    
    strategy.add_option('call', lower, 'long', 1)
    strategy.add_option('call', middle, 'short', 2)
    strategy.add_option('call', upper, 'long', 1)
    
    return strategy


def covered_call(stock_price, days_to_exp, vol=0.35):
    """
    Covered Call: Own stock + sell OTM call
    Generate income on stock position
    """
    strategy = OptionStrategy(stock_price, days_to_exp, volatility=vol)
    
    strategy.add_stock(100)  # Own 100 shares
    strategy.add_option('call', stock_price * 1.05, 'short')  # Sell OTM call
    
    return strategy


# ==============================================================================
# EXAMPLE USAGE
# ==============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("CUSTOM STRATEGY BUILDER - EXAMPLES")
    print("="*70)
    
    # Example 1: Custom Bull Call Spread
    print("\n### Example 1: Bull Call Spread ###")
    strategy1 = OptionStrategy(
        stock_price=150,
        time_to_exp=45,
        volatility=0.35
    )
    strategy1.add_option('call', 150, 'long')   # Buy ATM call
    strategy1.add_option('call', 160, 'short')  # Sell OTM call
    
    results1 = strategy1.analyze()
    plot1 = strategy1.plot_payoff_diagram(filename='bull_call_spread.png')
    print(f"\n📊 Payoff diagram saved: {plot1}")
    
    # Example 2: Iron Condor (pre-built)
    print("\n### Example 2: Iron Condor ###")
    strategy2 = iron_condor(stock_price=200, days_to_exp=30, vol=0.40)
    results2 = strategy2.analyze()
    plot2 = strategy2.plot_payoff_diagram(filename='iron_condor.png')
    print(f"\n📊 Payoff diagram saved: {plot2}")
    
    # Example 3: Long Straddle for Earnings
    print("\n### Example 3: Long Straddle (Volatility Play) ###")
    strategy3 = straddle(stock_price=175, days_to_exp=7, vol=0.55, position='long')
    results3 = strategy3.analyze()
    plot3 = strategy3.plot_payoff_diagram(filename='long_straddle.png')
    print(f"\n📊 Payoff diagram saved: {plot3}")
    
    # Example 4: Custom 3-leg strategy
    print("\n### Example 4: Custom Ratio Spread ###")
    strategy4 = OptionStrategy(stock_price=100, time_to_exp=30, volatility=0.30)
    strategy4.add_option('call', 100, 'long', 1)   # Buy 1 ATM
    strategy4.add_option('call', 105, 'short', 2)  # Sell 2 OTM
    
    results4 = strategy4.analyze()
    plot4 = strategy4.plot_payoff_diagram(filename='ratio_spread.png')
    print(f"\n📊 Payoff diagram saved: {plot4}")
    
    print("\n" + "="*70)
    print("BUILD YOUR OWN:")
    print("="*70)
    print("""
# Create custom strategy
my_strategy = OptionStrategy(
    stock_price=150,
    time_to_exp=30,
    volatility=0.40
)

# Add legs
my_strategy.add_option('call', 150, 'long')
my_strategy.add_option('call', 160, 'short')
my_strategy.add_option('put', 140, 'long')

# Analyze
results = my_strategy.analyze()
my_strategy.plot_payoff_diagram('my_strategy.png')
    """)
