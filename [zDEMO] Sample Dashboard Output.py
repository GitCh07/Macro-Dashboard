"""
MACRO DASHBOARD - DEMO OUTPUT
This shows what the dashboard looks like with real data
"""

print("""
================================================================================
                         MACRO ECONOMIC DASHBOARD
                            Updated: 2025-12-02 14:30
================================================================================

MARKET REGIME:       🔴 RISK_OFF
Risk Level:          LOW
--------------------------------------------------------------------------------

📊 INTEREST RATES & FED POLICY
--------------------------------------------------------------------------------
10Y Treasury:             4.35%  (+0.28% 1M)
2Y Treasury:              4.68%  (+0.35% 1M)
Yield Curve (10Y-2Y):     -0.33%  ⚠️ INVERTED
Fed Funds Rate:           5.50%

📈 INFLATION INDICATORS
--------------------------------------------------------------------------------
CPI (YoY):                3.2%  ↘️ Falling
Core CPI (YoY):           4.0%  ↘️ Falling

💹 MARKET CONDITIONS
--------------------------------------------------------------------------------
S&P 500:                  4,567.23  (-4.2% 1M)
VIX:                      28.5  (High volatility)
Unemployment Rate:        3.8%

🌍 CROSS-ASSET MARKETS
--------------------------------------------------------------------------------
Dollar Index (DXY):       106.8  (Strong)
Gold:                     $2,048.50  (+5.2% 1M)
Oil (WTI):                $78.45  (-2.1% 1M)

💳 CREDIT MARKETS
--------------------------------------------------------------------------------
HY Spreads (OAS):         512 bps  ⚠️ Widening
IG Spreads (OAS):         148 bps

🔄 SECTOR ROTATION (1-Month Performance)
--------------------------------------------------------------------------------
Utilities (XLU)                 +2.8%  ██
Consumer Staples (XLP)          +1.5%  █
Healthcare (XLV)                +0.9%  
Financials (XLF)                -1.2%  ⬛
Energy (XLE)                    -2.5%  ⬛⬛
Consumer Discretionary (XLY)    -4.8%  ⬛⬛⬛
Technology (XLK)                -5.2%  ⬛⬛⬛

Signal:                   🛡️ DEFENSIVE ROTATION

================================================================================
🎯 TRADING IMPLICATIONS
================================================================================

Positioning:         Defensive - Reduce risk, increase hedges
Options Strategy:    Buy protective puts, long volatility strategies
Equity Strategy:     Rotate to defensives (utilities, staples, healthcare)

Volatility Note:     High VIX = Fear. Good for buying options/protection.
Credit Note:         ⚠️ Credit stress elevated - reduce risk exposure

Overweight Sectors:  Utilities, Consumer Staples, Healthcare
Underweight Sectors: Technology, Consumer Discretionary, Small Caps

================================================================================
💡 Use this dashboard to inform your options and equity strategies!
================================================================================


================================================================================
EXAMPLE: RISK-ON REGIME
================================================================================

MARKET REGIME:       🟢 RISK_ON
Risk Level:          MODERATE TO HIGH
--------------------------------------------------------------------------------

📊 KEY METRICS
--------------------------------------------------------------------------------
10Y Treasury:             4.10%  (-0.15% 1M)
Yield Curve:              +0.25%  ✓ Normal
VIX:                      12.8  (Low volatility)
S&P 500:                  4,785.45  (+5.8% 1M)
Dollar Index:             103.2  (Weakening)
HY Spreads:               285 bps  ✓ Tightening

🔄 SECTOR ROTATION
--------------------------------------------------------------------------------
Technology (XLK)                +8.2%  ████████
Consumer Discretionary (XLY)    +6.5%  ██████
Financials (XLF)                +4.2%  ████
Energy (XLE)                    +3.1%  ███
Healthcare (XLV)                +1.8%  ██
Consumer Staples (XLP)          +0.5%  
Utilities (XLU)                 -0.8%  ⬛

Signal:                   🚀 GROWTH ROTATION

🎯 TRADING IMPLICATIONS
--------------------------------------------------------------------------------
Positioning:         Offensive - Increase equity exposure
Options Strategy:    Sell puts on quality names, bull put spreads
Equity Strategy:     Overweight growth/tech, high beta stocks

Volatility Note:     Low VIX = Complacency. Consider selling premium cautiously.
Credit Note:         ✓ Credit markets healthy - risk appetite supported

Overweight Sectors:  Technology, Consumer Discretionary, Communication Services
Underweight Sectors: Utilities, Consumer Staples


================================================================================
HOW TO USE FOR YOUR OPTIONS TRADING
================================================================================

RISK-OFF REGIME (Current example above):
✓ BUY protective puts on your long stock positions
✓ LONG straddles/strangles (high VIX = expensive but protects)
✓ AVOID selling naked options (gamma risk too high)
✓ Consider defensive sector calls (XLU, XLP, XLV)
✗ Don't fight the trend with bullish plays

RISK-ON REGIME:
✓ SELL cash-secured puts on quality growth stocks
✓ BULL put spreads for defined risk premium collection
✓ Covered calls on existing positions
✓ Tech sector calls (XLK, QQQ)
✗ Avoid buying expensive puts for hedging

NEUTRAL REGIME:
✓ Iron condors (profit from low volatility)
✓ Credit spreads (collect premium)
✓ Covered call writing (income)
✓ Dividend aristocrat holdings
✗ Avoid directional bets

TRANSITIONING REGIME:
✓ REDUCE position sizes across the board
✓ Close winning trades early
✓ Build cash reserves
✓ Use spreads instead of naked positions
✗ Avoid opening large new positions


================================================================================
REAL-WORLD EXAMPLE: December 2025
================================================================================

Based on today's data (hypothetical but realistic):

SCENARIO: Fed pauses rate hikes, inflation cooling, but recession fears rising

Current State:
- Inverted yield curve (-33 bps) = Recession warning
- High VIX (28.5) = Market fear elevated
- Widening credit spreads (512 bps) = Credit stress
- Defensive sectors outperforming = Flight to safety
- Strong dollar = Risk-off behavior

→ REGIME: RISK_OFF

YOUR ACTION PLAN:
1. Portfolio: Reduce exposure to 60% from 80%
2. Options: Buy SPY $440 puts (3 months out) for 5% of portfolio
3. Equity: Rotate 20% of tech holdings → utilities/staples
4. Sectors: Overweight XLU, XLP, XLV | Underweight XLK, XLY
5. Cash: Build to 20% of portfolio
6. Volatility: AVOID selling premium until VIX < 20

Expected Outcome:
- Protected downside with puts if market drops 10-15%
- Defensive sectors hold value better
- High cash position lets you buy dips
- Avoided selling premium into high volatility (would get hurt)


================================================================================
INTEGRATION WITH YOUR BLACK-SCHOLES CALCULATOR
================================================================================

Use macro regime to inform your options strategy selection:

RISK-OFF REGIME:
from black_scholes_calculator import BlackScholesCalculator
from macro_dashboard import quick_regime_check

regime = quick_regime_check()  # Returns 'RISK_OFF'

# Buy protective puts
bs = BlackScholesCalculator(S=450, K=440, T=60/365, r=0.05, sigma=0.35)
put_price = bs.put_price()  # $12.50
put_delta = bs.put_delta()  # -0.38

# For 500 shares, need: 500 / (100 * 0.38) = 13 contracts
print(f"Buy 13 put contracts @ ${put_price:.2f} = ${put_price * 13 * 100:,.0f}")

RISK-ON REGIME:
# Sell cash-secured puts
bs = BlackScholesCalculator(S=450, K=440, T=30/365, r=0.05, sigma=0.25)
put_price = bs.put_price()  # $3.20
put_delta = bs.put_delta()  # -0.22
prob_itm = bs.probability_itm('put')  # 22% chance of assignment

print(f"Sell 5 put contracts @ ${put_price:.2f}")
print(f"Premium collected: ${put_price * 5 * 100:,.0f}")
print(f"Probability of keeping premium: {(1-prob_itm)*100:.0f}%")


================================================================================
""")
