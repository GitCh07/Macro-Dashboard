"""
Professional Macro Economic Dashboard
Real-time tracking of key economic indicators, market conditions, and regime analysis
"""

import yfinance as yf
import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")


class MacroDashboard:
    """
    Comprehensive macro economic dashboard for trading decisions.
    Tracks rates, inflation, growth, sentiment, and cross-asset relationships.
    """
    
    def __init__(self, fred_api_key):
        """
        Initialize the macro dashboard.
        
        Args:
            fred_api_key: FRED API key for economic data
        """
        self.fred_api_key = fred_api_key
        self.fred_base_url = "https://api.stlouisfed.org/fred/series/observations"
        self.data = {}
        self.regime = None
        
    def _fetch_fred_data(self, series_id, lookback_days=365):
        """Fetch data from FRED API."""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=lookback_days)
            
            params = {
                'series_id': series_id,
                'api_key': self.fred_api_key,
                'file_type': 'json',
                'observation_start': start_date.strftime('%Y-%m-%d'),
                'observation_end': end_date.strftime('%Y-%m-%d')
            }
            
            response = requests.get(self.fred_base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            observations = data.get('observations', [])
            
            if not observations:
                return None
            
            # Convert to pandas Series
            df = pd.DataFrame(observations)
            df['date'] = pd.to_datetime(df['date'])
            df['value'] = pd.to_numeric(df['value'], errors='coerce')
            df = df.dropna()
            df.set_index('date', inplace=True)
            
            return df['value']
            
        except Exception as e:
            print(f"Error fetching {series_id}: {e}")
            return None
    
    def _fetch_yfinance_data(self, ticker, period='1y'):
        """Fetch data from Yahoo Finance."""
        try:
            data = yf.download(ticker, period=period, progress=False)
            if data.empty:
                return None
            return data['Close']
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")
            return None
    
    def collect_all_data(self):
        """Collect all macro data from various sources."""
        print("📊 Collecting macro economic data...")
        
        # ============= INTEREST RATES & FED POLICY =============
        print("  → Interest rates & Fed policy...")
        self.data['10Y_treasury'] = self._fetch_fred_data('DGS10')
        self.data['2Y_treasury'] = self._fetch_fred_data('DGS2')
        self.data['fed_funds'] = self._fetch_fred_data('FEDFUNDS')
        self.data['30Y_mortgage'] = self._fetch_fred_data('MORTGAGE30US')
        
        # ============= INFLATION =============
        print("  → Inflation indicators...")
        self.data['cpi'] = self._fetch_fred_data('CPIAUCSL', lookback_days=1095)  # 3 years
        self.data['core_cpi'] = self._fetch_fred_data('CPILFESL', lookback_days=1095)
        self.data['pce'] = self._fetch_fred_data('PCEPI', lookback_days=1095)
        self.data['ppi'] = self._fetch_fred_data('PPIACO', lookback_days=1095)
        
        # ============= ECONOMIC GROWTH =============
        print("  → Economic growth metrics...")
        self.data['gdp'] = self._fetch_fred_data('GDP', lookback_days=3650)  # 10 years
        self.data['unemployment'] = self._fetch_fred_data('UNRATE')
        self.data['retail_sales'] = self._fetch_fred_data('RSXFS')
        self.data['industrial_production'] = self._fetch_fred_data('INDPRO')
        self.data['housing_starts'] = self._fetch_fred_data('HOUST')
        
        # ============= CREDIT MARKETS =============
        print("  → Credit market conditions...")
        self.data['hy_spread'] = self._fetch_fred_data('BAMLH0A0HYM2')  # High Yield OAS
        self.data['ig_spread'] = self._fetch_fred_data('BAMLC0A0CM')  # IG Corporate OAS
        self.data['ted_spread'] = self._fetch_fred_data('TEDRATE')
        
        # ============= MARKET DATA (Yahoo Finance) =============
        print("  → Market prices & indices...")
        self.data['spy'] = self._fetch_yfinance_data('^GSPC')
        self.data['vix'] = self._fetch_yfinance_data('^VIX')
        self.data['dxy'] = self._fetch_yfinance_data('DX-Y.NYB')  # Dollar Index
        self.data['gold'] = self._fetch_yfinance_data('GC=F')
        self.data['oil'] = self._fetch_yfinance_data('CL=F')
        self.data['copper'] = self._fetch_yfinance_data('HG=F')
        
        # ============= SECTOR PERFORMANCE =============
        print("  → Sector rotation data...")
        self.data['xlk'] = self._fetch_yfinance_data('XLK')  # Technology
        self.data['xle'] = self._fetch_yfinance_data('XLE')  # Energy
        self.data['xlf'] = self._fetch_yfinance_data('XLF')  # Financials
        self.data['xlu'] = self._fetch_yfinance_data('XLU')  # Utilities
        self.data['xlv'] = self._fetch_yfinance_data('XLV')  # Healthcare
        self.data['xlp'] = self._fetch_yfinance_data('XLP')  # Consumer Staples
        self.data['xly'] = self._fetch_yfinance_data('XLY')  # Consumer Discretionary
        
        print("✅ Data collection complete!\n")
        
        return self.data
    
    def calculate_current_values(self):
        """Calculate current values and recent changes."""
        metrics = {}
        
        # Helper function to get latest value and change
        def get_metrics(series, name):
            if series is None or series.empty:
                return None
            
            latest = series.iloc[-1]
            
            # Get 1 month ago value
            month_ago_idx = max(0, len(series) - 22)  # ~1 month of trading days
            month_ago = series.iloc[month_ago_idx]
            
            change_1m = latest - month_ago
            change_1m_pct = (latest / month_ago - 1) * 100 if month_ago != 0 else 0
            
            return {
                'current': latest,
                'change_1m': change_1m,
                'change_1m_pct': change_1m_pct
            }
        
        # Interest Rates
        metrics['10Y'] = get_metrics(self.data.get('10Y_treasury'), '10Y Treasury')
        metrics['2Y'] = get_metrics(self.data.get('2Y_treasury'), '2Y Treasury')
        metrics['fed_funds'] = get_metrics(self.data.get('fed_funds'), 'Fed Funds')
        
        # Calculate yield curve
        if metrics['10Y'] and metrics['2Y']:
            metrics['yield_curve'] = {
                'current': metrics['10Y']['current'] - metrics['2Y']['current'],
                'inverted': metrics['10Y']['current'] < metrics['2Y']['current']
            }
        
        # Inflation
        metrics['cpi_yoy'] = self._calculate_yoy_change(self.data.get('cpi'))
        metrics['core_cpi_yoy'] = self._calculate_yoy_change(self.data.get('core_cpi'))
        
        # Market metrics
        metrics['vix'] = get_metrics(self.data.get('vix'), 'VIX')
        metrics['spy'] = get_metrics(self.data.get('spy'), 'S&P 500')
        metrics['dxy'] = get_metrics(self.data.get('dxy'), 'Dollar Index')
        metrics['gold'] = get_metrics(self.data.get('gold'), 'Gold')
        metrics['oil'] = get_metrics(self.data.get('oil'), 'Oil')
        
        # Credit spreads
        metrics['hy_spread'] = get_metrics(self.data.get('hy_spread'), 'HY Spread')
        metrics['ig_spread'] = get_metrics(self.data.get('ig_spread'), 'IG Spread')
        
        # Unemployment
        metrics['unemployment'] = get_metrics(self.data.get('unemployment'), 'Unemployment')
        
        return metrics
    
    def _calculate_yoy_change(self, series):
        """Calculate year-over-year percentage change."""
        if series is None or series.empty or len(series) < 252:
            return None
        
        latest = series.iloc[-1]
        year_ago = series.iloc[-252]
        
        yoy_pct = ((latest / year_ago) - 1) * 100
        
        # Determine trend
        if len(series) >= 22:
            month_ago = series.iloc[-22]
            trend = 'rising' if latest > month_ago else 'falling'
        else:
            trend = 'stable'
        
        return {
            'current': yoy_pct,
            'trend': trend
        }
    
    def calculate_sector_rotation(self):
        """Calculate 1-month sector performance for rotation analysis."""
        sectors = {
            'Technology (XLK)': self.data.get('xlk'),
            'Energy (XLE)': self.data.get('xle'),
            'Financials (XLF)': self.data.get('xlf'),
            'Utilities (XLU)': self.data.get('xlu'),
            'Healthcare (XLV)': self.data.get('xlv'),
            'Consumer Staples (XLP)': self.data.get('xlp'),
            'Consumer Discretionary (XLY)': self.data.get('xly')
        }
        
        performance = {}
        
        for name, data in sectors.items():
            if data is None or data.empty or len(data) < 22:
                continue
            
            latest = data.iloc[-1]
            month_ago = data.iloc[-22]
            
            return_1m = ((latest / month_ago) - 1) * 100
            performance[name] = return_1m
        
        # Sort by performance
        performance = dict(sorted(performance.items(), key=lambda x: x[1], reverse=True))
        
        return performance
    
    def detect_regime(self, metrics):
        """
        Detect current market regime based on macro conditions.
        
        Returns: 'RISK_ON', 'RISK_OFF', 'NEUTRAL', or 'TRANSITIONING'
        """
        risk_on_signals = 0
        risk_off_signals = 0
        
        # VIX analysis
        if metrics.get('vix'):
            vix_level = metrics['vix']['current']
            if vix_level < 15:
                risk_on_signals += 2
            elif vix_level > 25:
                risk_off_signals += 2
            elif vix_level > 20:
                risk_off_signals += 1
        
        # Credit spreads
        if metrics.get('hy_spread'):
            hy_change = metrics['hy_spread'].get('change_1m', 0)
            if hy_change > 20:  # Widening spreads
                risk_off_signals += 2
            elif hy_change < -10:  # Tightening spreads
                risk_on_signals += 1
        
        # Equity market
        if metrics.get('spy'):
            spy_return = metrics['spy'].get('change_1m_pct', 0)
            if spy_return > 3:
                risk_on_signals += 1
            elif spy_return < -3:
                risk_off_signals += 1
        
        # Dollar strength
        if metrics.get('dxy'):
            dxy_change = metrics['dxy'].get('change_1m_pct', 0)
            if dxy_change > 2:  # Strong dollar = risk off
                risk_off_signals += 1
            elif dxy_change < -2:
                risk_on_signals += 1
        
        # Gold (safe haven)
        if metrics.get('gold'):
            gold_return = metrics['gold'].get('change_1m_pct', 0)
            if gold_return > 5:  # Flight to safety
                risk_off_signals += 1
        
        # Yield curve
        if metrics.get('yield_curve'):
            if metrics['yield_curve']['inverted']:
                risk_off_signals += 1
        
        # Determine regime
        signal_diff = risk_on_signals - risk_off_signals
        
        if signal_diff >= 3:
            return 'RISK_ON'
        elif signal_diff <= -3:
            return 'RISK_OFF'
        elif abs(signal_diff) <= 1:
            return 'NEUTRAL'
        else:
            return 'TRANSITIONING'
    
    def generate_trading_implications(self, regime, metrics, sector_rotation):
        """Generate specific trading recommendations based on regime."""
        implications = {
            'regime': regime,
            'positioning': '',
            'options_strategy': '',
            'equity_strategy': '',
            'sectors': {},
            'risk_level': ''
        }
        
        # Get top and bottom performing sectors
        sectors_list = list(sector_rotation.items())
        top_sectors = sectors_list[:2] if len(sectors_list) >= 2 else sectors_list
        bottom_sectors = sectors_list[-2:] if len(sectors_list) >= 2 else []
        
        if regime == 'RISK_ON':
            implications['positioning'] = 'Offensive - Increase equity exposure'
            implications['options_strategy'] = 'Sell puts on quality names, bull put spreads'
            implications['equity_strategy'] = 'Overweight growth/tech, high beta stocks'
            implications['risk_level'] = 'MODERATE TO HIGH'
            implications['sectors'] = {
                'overweight': ['Technology', 'Consumer Discretionary', 'Communication Services'],
                'underweight': ['Utilities', 'Consumer Staples']
            }
            
        elif regime == 'RISK_OFF':
            implications['positioning'] = 'Defensive - Reduce risk, increase hedges'
            implications['options_strategy'] = 'Buy protective puts, long volatility strategies'
            implications['equity_strategy'] = 'Rotate to defensives (utilities, staples, healthcare)'
            implications['risk_level'] = 'LOW'
            implications['sectors'] = {
                'overweight': ['Utilities', 'Consumer Staples', 'Healthcare'],
                'underweight': ['Technology', 'Consumer Discretionary', 'Small Caps']
            }
            
        elif regime == 'NEUTRAL':
            implications['positioning'] = 'Balanced - Maintain diversified exposure'
            implications['options_strategy'] = 'Income strategies (covered calls, iron condors)'
            implications['equity_strategy'] = 'Quality dividend payers, market-weight allocation'
            implications['risk_level'] = 'MODERATE'
            implications['sectors'] = {
                'overweight': ['Quality names across sectors'],
                'underweight': ['Speculative/unprofitable companies']
            }
            
        else:  # TRANSITIONING
            implications['positioning'] = 'Cautious - Wait for clearer signals'
            implications['options_strategy'] = 'Reduce position sizes, favor spreads over naked'
            implications['equity_strategy'] = 'Trim winners, build cash, stay flexible'
            implications['risk_level'] = 'LOW TO MODERATE'
            implications['sectors'] = {
                'overweight': ['Cash/short duration bonds'],
                'underweight': ['Avoid large new positions']
            }
        
        # Add VIX-specific guidance
        if metrics.get('vix'):
            vix_level = metrics['vix']['current']
            if vix_level < 15:
                implications['volatility_note'] = 'Low VIX = Complacency. Consider selling premium cautiously.'
            elif vix_level > 25:
                implications['volatility_note'] = 'High VIX = Fear. Good for buying options/protection.'
            else:
                implications['volatility_note'] = 'Normal VIX levels. Standard strategies apply.'
        
        # Add credit market note
        if metrics.get('hy_spread'):
            hy_current = metrics['hy_spread']['current']
            if hy_current > 500:
                implications['credit_note'] = '⚠️ Credit stress elevated - reduce risk exposure'
            elif hy_current < 300:
                implications['credit_note'] = '✓ Credit markets healthy - risk appetite supported'
        
        return implications
    
    def print_dashboard(self):
        """Print formatted dashboard to console."""
        # Collect and calculate all metrics
        self.collect_all_data()
        metrics = self.calculate_current_values()
        sector_rotation = self.calculate_sector_rotation()
        regime = self.detect_regime(metrics)
        implications = self.generate_trading_implications(regime, metrics, sector_rotation)
        
        # Print header
        print("\n" + "="*80)
        print(" " * 25 + "MACRO ECONOMIC DASHBOARD")
        print(" " * 28 + f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print("="*80)
        
        # Market Regime
        regime_emoji = {
            'RISK_ON': '🟢',
            'RISK_OFF': '🔴',
            'NEUTRAL': '🟡',
            'TRANSITIONING': '🟠'
        }
        
        print(f"\n{'MARKET REGIME:':<20} {regime_emoji.get(regime, '')} {regime}")
        print(f"{'Risk Level:':<20} {implications['risk_level']}")
        print("-" * 80)
        
        # Rates & Policy
        print("\n📊 INTEREST RATES & FED POLICY")
        print("-" * 80)
        
        if metrics.get('10Y'):
            m = metrics['10Y']
            print(f"{'10Y Treasury:':<25} {m['current']:.2f}%  "
                  f"{'(+' if m['change_1m'] > 0 else '('}{m['change_1m']:.2f}% 1M)")
        
        if metrics.get('2Y'):
            m = metrics['2Y']
            print(f"{'2Y Treasury:':<25} {m['current']:.2f}%  "
                  f"{'(+' if m['change_1m'] > 0 else '('}{m['change_1m']:.2f}% 1M)")
        
        if metrics.get('yield_curve'):
            curve = metrics['yield_curve']
            status = "⚠️ INVERTED" if curve['inverted'] else "✓ Normal"
            print(f"{'Yield Curve (10Y-2Y):':<25} {curve['current']:.2f}%  {status}")
        
        if metrics.get('fed_funds'):
            m = metrics['fed_funds']
            print(f"{'Fed Funds Rate:':<25} {m['current']:.2f}%")
        
        # Inflation
        print("\n📈 INFLATION INDICATORS")
        print("-" * 80)
        
        if metrics.get('cpi_yoy'):
            m = metrics['cpi_yoy']
            trend_arrow = '↗️' if m['trend'] == 'rising' else '↘️' if m['trend'] == 'falling' else '➡️'
            print(f"{'CPI (YoY):':<25} {m['current']:.1f}%  {trend_arrow} {m['trend'].title()}")
        
        if metrics.get('core_cpi_yoy'):
            m = metrics['core_cpi_yoy']
            trend_arrow = '↗️' if m['trend'] == 'rising' else '↘️' if m['trend'] == 'falling' else '➡️'
            print(f"{'Core CPI (YoY):':<25} {m['current']:.1f}%  {trend_arrow} {m['trend'].title()}")
        
        # Market Conditions
        print("\n💹 MARKET CONDITIONS")
        print("-" * 80)
        
        if metrics.get('spy'):
            m = metrics['spy']
            print(f"{'S&P 500:':<25} {m['current']:.2f}  "
                  f"({'+'if m['change_1m_pct'] > 0 else ''}{m['change_1m_pct']:.1f}% 1M)")
        
        if metrics.get('vix'):
            m = metrics['vix']
            level = 'Low' if m['current'] < 15 else 'High' if m['current'] > 25 else 'Normal'
            print(f"{'VIX:':<25} {m['current']:.2f}  ({level} volatility)")
        
        if metrics.get('unemployment'):
            m = metrics['unemployment']
            print(f"{'Unemployment Rate:':<25} {m['current']:.1f}%")
        
        # Cross-Assets
        print("\n🌍 CROSS-ASSET MARKETS")
        print("-" * 80)
        
        if metrics.get('dxy'):
            m = metrics['dxy']
            strength = 'Strong' if m['change_1m_pct'] > 2 else 'Weak' if m['change_1m_pct'] < -2 else 'Neutral'
            print(f"{'Dollar Index (DXY):':<25} {m['current']:.2f}  ({strength})")
        
        if metrics.get('gold'):
            m = metrics['gold']
            print(f"{'Gold:':<25} ${m['current']:.2f}  "
                  f"({'+'if m['change_1m_pct'] > 0 else ''}{m['change_1m_pct']:.1f}% 1M)")
        
        if metrics.get('oil'):
            m = metrics['oil']
            print(f"{'Oil (WTI):':<25} ${m['current']:.2f}  "
                  f"({'+'if m['change_1m_pct'] > 0 else ''}{m['change_1m_pct']:.1f}% 1M)")
        
        # Credit Markets
        print("\n💳 CREDIT MARKETS")
        print("-" * 80)
        
        if metrics.get('hy_spread'):
            m = metrics['hy_spread']
            status = '⚠️ Widening' if m['change_1m'] > 20 else '✓ Stable' if abs(m['change_1m']) < 10 else 'Tightening'
            print(f"{'HY Spreads (OAS):':<25} {m['current']:.0f} bps  {status}")
        
        if metrics.get('ig_spread'):
            m = metrics['ig_spread']
            print(f"{'IG Spreads (OAS):':<25} {m['current']:.0f} bps")
        
        # Sector Rotation
        print("\n🔄 SECTOR ROTATION (1-Month Performance)")
        print("-" * 80)
        
        for sector, perf in sector_rotation.items():
            bars = '█' * int(abs(perf) / 2) if abs(perf) > 0 else ''
            color = '' if perf > 0 else '⬛'
            print(f"{sector:<30} {perf:>6.1f}%  {bars}")
        
        # Determine rotation signal
        top_sector = list(sector_rotation.keys())[0] if sector_rotation else ''
        if 'Utilities' in top_sector or 'Staples' in top_sector:
            rotation_signal = '🛡️ DEFENSIVE ROTATION'
        elif 'Technology' in top_sector or 'Discretionary' in top_sector:
            rotation_signal = '🚀 GROWTH ROTATION'
        elif 'Energy' in top_sector:
            rotation_signal = '⚡ COMMODITY ROTATION'
        else:
            rotation_signal = '➡️ MIXED SIGNALS'
        
        print(f"\n{'Signal:':<25} {rotation_signal}")
        
        # Trading Implications
        print("\n" + "="*80)
        print("🎯 TRADING IMPLICATIONS")
        print("="*80)
        
        print(f"\n{'Positioning:':<20} {implications['positioning']}")
        print(f"{'Options Strategy:':<20} {implications['options_strategy']}")
        print(f"{'Equity Strategy:':<20} {implications['equity_strategy']}")
        
        if implications.get('volatility_note'):
            print(f"\n{'Volatility Note:':<20} {implications['volatility_note']}")
        
        if implications.get('credit_note'):
            print(f"{'Credit Note:':<20} {implications['credit_note']}")
        
        print(f"\n{'Overweight Sectors:':<20} {', '.join(implications['sectors'].get('overweight', []))}")
        print(f"{'Underweight Sectors:':<20} {', '.join(implications['sectors'].get('underweight', []))}")
        
        print("\n" + "="*80)
        print("💡 Use this dashboard to inform your options and equity strategies!")
        print("="*80 + "\n")
        
        return {
            'metrics': metrics,
            'regime': regime,
            'sector_rotation': sector_rotation,
            'implications': implications
        }


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def create_dashboard(fred_api_key='de51fa06a63378ccba191279d347d569'):
    """Create and display macro dashboard."""
    dashboard = MacroDashboard(fred_api_key)
    return dashboard.print_dashboard()


def quick_regime_check(fred_api_key='de51fa06a63378ccba191279d347d569'):
    """Quick check of current market regime."""
    dashboard = MacroDashboard(fred_api_key)
    dashboard.collect_all_data()
    metrics = dashboard.calculate_current_values()
    regime = dashboard.detect_regime(metrics)
    
    regime_descriptions = {
        'RISK_ON': 'Market in risk-seeking mode. Favor growth/tech, sell volatility.',
        'RISK_OFF': 'Market in risk-aversion mode. Defensive positioning, buy protection.',
        'NEUTRAL': 'Balanced market conditions. Income strategies work well.',
        'TRANSITIONING': 'Mixed signals. Stay cautious, reduce position sizes.'
    }
    
    print(f"\n🎯 Current Market Regime: {regime}")
    print(f"   {regime_descriptions.get(regime, '')}\n")
    
    return regime


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*80)
    print("MACRO DASHBOARD - Example Usage")
    print("="*80)
    
    # Create and display full dashboard
    results = create_dashboard()
    
    print("\n\n" + "="*80)
    print("QUICK REFERENCE:")
    print("="*80)
    print("""
# Display full dashboard
from macro_dashboard import create_dashboard
results = create_dashboard()

# Quick regime check
from macro_dashboard import quick_regime_check
regime = quick_regime_check()

# Access the dashboard object for custom analysis
from macro_dashboard import MacroDashboard
dashboard = MacroDashboard('your_fred_api_key')
dashboard.collect_all_data()
metrics = dashboard.calculate_current_values()
    """)
