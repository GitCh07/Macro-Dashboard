# Black-Scholes Options Pricing Calculator
### Professional-Grade Options Analysis Toolkit

Built for real-world options trading, portfolio hedging, and volatility analysis.

---

##  Files Included

1. **black_scholes_calculator.py** - Core pricing engine with full Greeks
2. **trading_scenarios.py** - 6 practical trading scenarios with real examples
3. **quick_reference.py** - Usage guide and live data integration template

---

##  Quick Start

### Basic Usage
```python
from black_scholes_calculator import BlackScholesCalculator

# Price an option
bs = BlackScholesCalculator(
    S=150,      # Current stock price
    K=155,      # Strike price
    T=30/365,   # 30 days to expiration
    r=0.05,     # 5% risk-free rate
    sigma=0.40, # 40% implied volatility
    q=0.0       # No dividend
)

# Get prices
call_price = bs.call_price()  # $5.33
put_price = bs.put_price()    # $9.69

# Get Greeks
delta = bs.call_delta()       # 0.429
gamma = bs.gamma()            # 0.0217
theta = bs.call_theta()       # -$0.126/day
vega = bs.vega()              # $0.169 per 1% vol
```

### Calculate Implied Volatility
```python
from black_scholes_calculator import implied_volatility

# If a call is trading at $8.50 in the market
iv = implied_volatility(
    market_price=8.50,
    S=150,
    K=155,
    T=60/365,
    r=0.05,
    option_type='call'
)
print(f"Implied Volatility: {iv*100:.1f}%")  # 41.8%
```

---

##  Real Trading Applications

### 1. Find Mispriced Options
Compare theoretical Black-Scholes price to market price:
- **Market > Theory**: Option overpriced → Sell/write strategy
- **Market < Theory**: Option underpriced → Buy opportunity

### 2. Volatility Trading
- **Current IV < Historical Vol**: Options cheap → Buy straddles/strangles
- **Current IV > Historical Vol**: Options expensive → Sell premium

### 3. Portfolio Hedging
Use Delta to calculate exact hedge ratios:
```python
# Hedge 400 shares with puts
put_delta = -0.35
contracts_needed = 400 / (100 * abs(put_delta))  # 11.4 ≈ 11 contracts
```

### 4. Earnings Plays
Evaluate IV crush impact before buying pre-earnings options:
```python
# Pre-earnings: IV = 55%, Call = $2.53
# Post-earnings: IV drops to 35%
# Even if stock jumps 5%, IV crush can wipe out gains!
```

### 5. Spread Strategies
Price multi-leg strategies (bull spreads, iron condors):
```python
# Bull call spread: Long 100C, Short 110C
long_call = bs_long.call_price()   # $5.20
short_call = bs_short.call_price() # $1.76
net_cost = long_call - short_call  # $3.44
max_profit = 10 - 3.44            # $6.56
return_on_risk = 6.56/3.44        # 190%
```

### 6. Delta Neutral Strategies
Maintain market-neutral positions to profit from vol/theta:
```python
# Short 10 calls with 0.45 delta
position_delta = -10 * 100 * 0.45  # -450
shares_to_buy = 450  # Hedge to delta neutral
```

---

##  Output Examples

### Call Option Analysis
```
============================================================
BLACK-SCHOLES CALL OPTION ANALYSIS
============================================================

Underlying Parameters:
  Stock Price (S):        $140.00
  Strike Price (K):       $145.00
  Time to Expiration:     0.0822 years (30 days)
  Volatility (σ):         45.00%
  Risk-Free Rate (r):     5.00%

CALL Option Pricing:
  Theoretical Price:      $5.32
  Intrinsic Value:        $0.00
  Time Value:             $5.32
  Probability ITM:        38.03%

The Greeks:
  Delta (Δ):              0.4303
  Gamma (Γ):              0.021750
  Theta (Θ):              $-0.13 per day
  Vega (ν):               $0.16 per 1% vol change
  Rho (ρ):                $0.05 per 1% rate change

Trading Insights:
  • For every $1 move in stock, call changes by $0.43
  • Daily time decay is $0.13
  • 1% volatility increase adds $0.16 to price
```

---

## Practical Trading Scenarios

Run `python trading_scenarios.py` to see 6 detailed scenarios:

1. **Identifying Mispriced Options** - Find overpriced/underpriced options
2. **Volatility Trading** - Long straddle when IV < historical vol
3. **Portfolio Hedging** - Protective put strategy with exact sizing
4. **Earnings Play Analysis** - IV crush vs stock movement impact
5. **Bull Call Spread** - Defined risk directional trade
6. **Delta Neutral Trading** - Market-neutral position management

---

## 🔧 Advanced Features

### Greeks Explained

| Greek | Meaning | Trading Application |
|-------|---------|---------------------|
| **Delta** | Price change per $1 stock move | Position sizing, hedge ratios |
| **Gamma** | Delta change per $1 stock move | How quickly delta shifts |
| **Theta** | Daily time decay | Income from selling premium |
| **Vega** | Price change per 1% vol move | Volatility exposure |
| **Rho** | Price change per 1% rate move | Interest rate sensitivity |

### Key Formulas

**Call Price:**
```
C = S·e^(-q·T)·N(d1) - K·e^(-r·T)·N(d2)
```

**Put Price:**
```
P = K·e^(-r·T)·N(-d2) - S·e^(-q·T)·N(-d1)
```

Where:
```
d1 = [ln(S/K) + (r - q + σ²/2)·T] / (σ·√T)
d2 = d1 - σ·√T
```

---

## Integration with Live Market Data

### Install yfinance for real-time data:
```bash
pip install yfinance
```

### Analyze live options:
```python
from quick_reference import analyze_with_market_data

# Analyze AAPL $180 call expiring Jan 17, 2025
analyze_with_market_data('AAPL', 180, '2025-01-17', 'call')
```

Output includes:
- Real-time stock price
- Current market bid/ask
- Market implied volatility
- Black-Scholes theoretical price
- All Greeks
- Volume and open interest

### Scan for opportunities:
```python
from quick_reference import scan_volatility_opportunities

# Scan all strikes for mispriced options
scan_volatility_opportunities('NVDA', '2025-01-17')
```

---

##  Understanding Option Pricing

### Moneyness
- **In-the-Money (ITM)**: Has intrinsic value
  - Call: Stock > Strike
  - Put: Stock < Strike
- **At-the-Money (ATM)**: Stock ≈ Strike
- **Out-of-the-Money (OTM)**: No intrinsic value
  - Call: Stock < Strike
  - Put: Stock > Strike

### Time Value vs Intrinsic Value
- **Intrinsic Value**: Immediate exercise value
  - Call: max(0, S - K)
  - Put: max(0, K - S)
- **Time Value**: Premium above intrinsic value
  - Decays to zero at expiration (theta)

### Probability of Profit
Black-Scholes calculates probability of finishing ITM:
- Based on lognormal stock distribution
- N(d2) for calls, N(-d2) for puts
- NOT the same as 50% when ATM due to drift

---

##  Model Limitations & Considerations

### Black-Scholes Assumptions
1. **European exercise only** - US equity options are American (can exercise early)
2. **Constant volatility** - Reality: volatility smile/skew exists
3. **No dividends** - Use `q` parameter to adjust for dividend yield
4. **Log-normal returns** - Fat tails in reality
5. **No transaction costs** - Include in real strategy analysis

### Practical Adjustments Needed

**For Real Trading:**
- Add bid-ask spread costs
- Consider liquidity (volume, open interest)
- Use American option pricing for early exercise scenarios (binomial model)
- Adjust for volatility surface, not flat vol
- Account for earnings dates (IV spikes)
- Include margin/capital requirements

**When to Use:**
- ✅ Quick theoretical valuation
- ✅ Greeks calculation for risk management
- ✅ Relative value comparisons
- ✅ Strategy P&L estimation
- ⚠️ Always verify against market prices before trading

---

##  Next Steps for Enhancement

### Phase 2 Additions:
1. **Historical vs Implied Vol Comparison**
   - Pull historical price data
   - Calculate realized volatility
   - Compare to current IV for edge

2. **Binomial Tree for American Options**
   - Price early exercise premium
   - More accurate for ITM options
   - Handle discrete dividends

3. **Volatility Surface**
   - Interpolate IV across strikes
   - Capture volatility smile/skew
   - Better pricing accuracy

4. **Backtesting Framework**
   - Test strategies on historical data
   - Calculate Sharpe ratio, max drawdown
   - Validate edge before live trading

5. **Position Portfolio Analysis**
   - Aggregate Greeks across positions
   - Portfolio-level risk metrics
   - Scenario analysis

---

## 📚 Resources for Further Learning

### Books
- "Options, Futures, and Other Derivatives" - John Hull
- "Option Volatility and Pricing" - Sheldon Natenberg
- "Dynamic Hedging" - Nassim Taleb

### Online Resources
- CBOE Options Institute
- Tastytrade (free options education)
- QuantLib (open-source pricing library)

### Data Sources
- Yahoo Finance (yfinance) - Free historical + options data
- Interactive Brokers API - Professional-grade access
- Alpha Vantage - Free API with limitations
- CBOE DataShop - Premium options data

---

## Quick Reference Card

### Option Price
```python
bs.call_price()  # Theoretical call price
bs.put_price()   # Theoretical put price
```

### Greeks
```python
bs.call_delta()  # Call: 0 to 1
bs.put_delta()   # Put: -1 to 0
bs.gamma()       # Same for calls/puts
bs.call_theta()  # Daily decay
bs.vega()        # Vol sensitivity
```

### Analysis
```python
bs.intrinsic_value('call')    # Exercise value
bs.time_value('call')         # Extrinsic value
bs.probability_itm('call')    # P(finish ITM)
```

### Implied Vol
```python
implied_volatility(market_price, S, K, T, r, 'call')
```

---

## Trading Edge Development

### How to Find Profitable Trades

1. **Volatility Edge**
   - Compare current IV to historical realized vol
   - Buy when IV < historical (cheap options)
   - Sell when IV > historical (expensive options)

2. **Mispricing Edge**
   - Run scanner across all strikes
   - Find options with market price ≠ theoretical
   - Verify with volume/liquidity

3. **Event-Driven Edge**
   - IV spikes before earnings
   - IV crush immediately after
   - Sell premium before, avoid buying

4. **Structure Edge**
   - Use spreads to reduce capital and risk
   - Improve probability of profit vs naked options
   - Better risk/reward with defined outcomes

5. **Greek Edge**
   - Harvest theta by selling OTM options
   - Long vega before expected vol expansion
   - Delta neutral to isolate vol/time profits

---

## Risk Management Rules

1. **Never risk more than 2-5% of capital per trade**
2. **Always know your max loss before entering**
3. **Use defined risk strategies (spreads) when learning**
4. **Size positions based on Greeks, not just dollars**
5. **Have exit plan before entry (take profit + stop loss)**

---

## Support & Questions

This toolkit is designed for educational and analysis purposes. Always:
- Verify calculations with multiple sources
- Paper trade strategies before using real money
- Consult with financial advisors for personal situations
- Understand that past performance ≠ future results

**Remember**: Options are leveraged instruments with substantial risk. 
Only trade with capital you can afford to lose.

---

## Black-Scholes calculator with:
✅ Full pricing engine
✅ All Greeks calculations  
✅ Implied volatility solver
✅ 6 practical trading scenarios
✅ Live market data integration template
✅ Comprehensive documentation


