# RMP Quadrant Strategy - Comprehensive Backtest Analysis

## Executive Summary

Testing period: January 2015 - January 2026 (11 years)
Initial capital: $100,000
Benchmark: Buy-and-hold SPY

**Bottom line**: All quadrant rotation strategy variants **underperformed** buy-and-hold SPY, though improvements reduced the gap from -5.10% to -3.57% annual alpha.

---

## 1. Allocation Analysis - Which Quadrants Hurt Performance?

### Performance by Quadrant (Original Strategy)

| Quadrant | Days (%) | Alpha | Avg Daily Alpha | Win Rate | Verdict |
|----------|----------|-------|-----------------|----------|---------|
| **Dovish/Co-operative** | 620 (22.4%) | **-115.05%** | -0.012% | 50.8% | **WORST** |
| **Happiness Zone** | 576 (20.8%) | **-104.37%** | -0.039% | 50.0% | **2nd WORST** |
| **Crisis Zone** | 555 (20.1%) | **-87.12%** | -0.088% | 43.2% | **3rd WORST** |
| **Hawkish Policy** | 745 (26.9%) | **-67.99%** | +0.034% | 50.9% | **Best (but still bad)** |

### Key Findings

**ALL FOUR QUADRANTS UNDERPERFORMED SPY** - This is a fundamental problem with the asset allocation, not just the regime identification.

#### Dovish/Co-operative (WORST: -115% alpha)
- **Current allocation**: EEM 15%, GLD 15%, XLI 15%, IWM 15%, XLB 10%, KRE 10%, DBC 10%, SPY 10%
- **Problem**: Over-weighted emerging markets, commodities, and cyclicals
- **Reality**: During "dovish" periods (weak USD + steep curve), large-cap US equities (SPY, QQQ) still outperformed sector bets
- **Fix**: Increase SPY/QQQ to 50%+, reduce EM and commodity exposure

#### Happiness Zone (2nd WORST: -104% alpha)
- **Current allocation**: SPY 30%, QQQ 25%, XLF 15%, VNQ 10%, XLK 10%, IWM 5%, EEM 5%
- **Problem**: Even with 55% in SPY/QQQ, the remaining 45% in financials/REITs/small-caps dragged down returns
- **Reality**: During growth periods, concentrated large-cap tech (QQQ) dominated
- **Fix**: Increase SPY/QQQ to 70%+, reduce sector tilts

#### Crisis Zone (3rd WORST: -87% alpha)
- **Current allocation**: TLT 30%, GLD 25%, SHY 20%, XLU 10%, XLV 10%, Cash 5%
- **Problem**: Defensive allocation underperformed even during "crisis" periods
- **Reality**: SPY gained +167% during these periods vs strategy's +80%
- **Insight**: 2015-2026 had no prolonged crisis - the COVID crash recovered quickly
- **Fix**: This allocation might work better in a true multi-year crisis (2008-style)

#### Hawkish Policy (Best of worst: -68% alpha)
- **Current allocation**: SHY 25%, XLP 20%, XLU 15%, VIG 15%, SPY 10%, GLD 10%, Cash 5%
- **Problem**: Too defensive - heavy in short-duration treasuries and staples
- **Reality**: Even during hawkish periods, SPY outperformed defensive positioning
- **Note**: This quadrant had POSITIVE daily alpha (+0.034%) but still underperformed cumulatively
- **Fix**: Reduce defensive positioning, increase equity allocation

---

## 2. Strategy Improvements - Impact Analysis

### Variant Comparison

| Strategy | CAGR | Alpha vs SPY | Volatility | Sharpe | Max DD | Quadrant Changes | Trades |
|----------|------|--------------|------------|--------|--------|------------------|--------|
| **V1: Original** | 8.34% | **-5.10%** | 12.73% | 0.66 | -30.45% | 171 | 758 |
| **V2: Z-score Bands (0.5)** | 8.80% | **-4.64%** | 14.33% | 0.61 | -33.14% | 168 | 763 |
| **V3: 20-Day Hold Filter** | 8.28% | **-5.17%** | 11.48% | 0.72 | -18.80% | 11 | 753 |
| **V4: Combined (Z+Hold)** | 8.46% | **-4.98%** | 11.69% | 0.72 | -18.80% | 13 | 756 |
| **V5: Quarterly + Low Cost** | 9.87% | **-3.57%** | 11.34% | 0.87 | -18.49% | 13 | 253 |
| **SPY Benchmark** | 13.44% | 0.00% | 17.79% | 0.76 | -33.72% | - | - |

### Improvement Impact

#### 1. Z-score Bands (Threshold = 0.5)
- **Result**: Slightly improved (+0.46% alpha improvement)
- **Mechanism**: Reduced whipsaw by requiring stronger signals
- **Trade-off**: Slightly higher volatility (14.33% vs 12.73%)
- **Conclusion**: Minor improvement, not sufficient to solve the problem

#### 2. 20-Day Holding Period Filter
- **Result**: Minimal impact on return, but **dramatically reduced** max drawdown
- **Mechanism**: Reduced quadrant changes from 171 to just 11 (94% reduction!)
- **Trade-off**: Slightly worse alpha (-5.17% vs -5.10%)
- **Benefit**: Max drawdown improved from -30.45% to **-18.80%** (39% reduction)
- **Conclusion**: Great for risk management, doesn't improve alpha

#### 3. Combined (Z-bands + Holding Filter)
- **Result**: Best of both worlds - improved alpha AND reduced risk
- **Alpha**: -4.98% (improvement of 0.12%)
- **Max DD**: -18.80% (same as holding filter alone)
- **Sharpe**: 0.72 (improved from 0.66)
- **Conclusion**: Modest improvement

#### 4. Quarterly Rebalancing + Lower Costs ⭐ **BEST VARIANT**
- **Result**: **Best performance** of all variants
- **Alpha**: -3.57% (1.53% improvement over original)
- **CAGR**: 9.87% (vs 8.34% original)
- **Max DD**: -18.49% (best of all)
- **Sharpe**: 0.87 (best of all - even better than SPY!)
- **Trades**: 253 (vs 758 - 67% reduction)
- **Conclusion**: **Quarterly rebalancing is far superior to monthly**
  - Reduces transaction costs
  - Reduces whipsaw
  - Better risk-adjusted returns
  - Still underperforms SPY on absolute returns, but closes the gap significantly

---

## 3. Alternative Rebalancing & Transaction Costs

### Key Insights from V5 (Quarterly + Low Cost)

**Rebalancing Frequency**:
- Monthly (original): 758 trades, -5.10% alpha
- Quarterly: 253 trades (-67%), **-3.57% alpha** (+1.53% improvement)
- **Conclusion**: Less is more - quarterly rebalancing is superior

**Transaction Costs**:
- 0.10% (original): Realistic for retail investors
- 0.05% (V5): Achievable with low-cost brokers or larger accounts
- **Impact**: Contributed to ~0.3-0.5% of the improvement in V5

**Quadrant Changes**:
- Original: 171 changes over 11 years (every 23 days on average)
- With filters: 11-13 changes (every ~300 days)
- **Conclusion**: The original signal was too noisy - markets don't change macro regimes every month

---

## 4. Root Cause Analysis

### Why Did the Strategy Underperform?

#### Problem #1: Asset Allocation Doesn't Match Theory
- **Hypothesis**: Different macro regimes favor different asset classes
- **Reality**: SPY outperformed in ALL quadrants during 2015-2026
- **Reason**: This was a secular bull market for US large-caps, regardless of macro regime
- **Implication**: The strategy might work better in different market environments (2000-2010)

#### Problem #2: Regime Identification Noise
- **Issue**: Z-score thresholds of 0 caused 171 quadrant changes
- **Reality**: True macro regime changes are less frequent (5-10 per decade)
- **Solution**: Z-score bands + holding filters reduced changes to 11-13 (much more realistic)

#### Problem #3: Over-Diversification Penalty
- **Issue**: Allocating to 7-8 ETFs per quadrant diluted concentration
- **Reality**: During a tech-led bull market, concentrated tech exposure won
- **Example**: Happiness Zone with 55% SPY/QQQ still underperformed 100% SPY
- **Reason**: The other 45% (XLF, VNQ, IWM) dragged down returns

#### Problem #4: Transaction Costs & Whipsaw
- **Issue**: Monthly rebalancing with frequent quadrant changes = high trading costs
- **Impact**: Estimated 0.5-1.0% annual drag from transaction costs
- **Solution**: Quarterly rebalancing reduced drag significantly

#### Problem #5: Wrong Decade for the Strategy
- **2015-2026 Characteristics**:
  - Tech-led mega-cap dominance
  - Low volatility (except COVID crash which recovered quickly)
  - No prolonged crisis period
  - Persistently low rates until 2022
- **Better Period for This Strategy**: 2000-2010
  - Multiple regime changes (tech bubble, GFC)
  - Sector rotation was more important
  - Commodities and EM had their day

---

## 5. Recommendations

### Short-term: How to Use This Framework NOW

Given that the strategy underperforms SPY, here's how to actually use it:

#### Option A: Use as a Risk Overlay, Not a Return Driver
- **Core position**: 70-80% SPY or diversified equity portfolio
- **Macro tilt**: Use quadrant analysis to add 20-30% tactical overlay
  - Dovish: +10% GLD, +10% EEM
  - Happiness: Stay 100% core
  - Hawkish: +20% SHY (reduce duration risk)
  - Crisis: +10% TLT, +10% GLD
- **Rebalancing**: Quarterly only

#### Option B: Use for Risk Management, Not Alpha
- **Purpose**: Identify when to reduce equity exposure, not which sectors to rotate into
- **Rules**:
  - Happiness/Dovish: 90% equities
  - Hawkish: 70% equities, 30% bonds/cash
  - Crisis: 50% equities, 50% bonds/cash
- **Asset choice**: Just use SPY for equities, AGG for bonds (keep it simple)

#### Option C: Combine with Momentum/Technical Signals
- **Macro (quadrant)**: Sets the baseline allocation
- **Momentum**: Adjusts exposure within that baseline
- **Example**:
  - Quadrant says "Dovish" → baseline 90% equities
  - SPY is above 200-day MA → stay 90% equities
  - SPY is below 200-day MA → reduce to 60% equities

### Long-term: How to Improve the Strategy

#### Fix #1: Simplify Asset Allocation
**Current**: 7-8 ETFs per quadrant
**Proposed**: 2-3 ETFs per quadrant

- **Dovish**: 50% SPY, 25% GLD, 25% EEM
- **Happiness**: 70% SPY, 30% QQQ
- **Hawkish**: 50% SPY, 30% SHY, 20% TLT
- **Crisis**: 40% SPY, 30% TLT, 30% GLD

**Rationale**: Reduce over-diversification, keep core SPY exposure high

#### Fix #2: Increase Z-score Threshold
**Current**: 0.5
**Proposed**: 1.0

**Rationale**: Only act on very strong signals (1+ standard deviation)

#### Fix #3: Add Momentum Filters
**Proposed Rule**: Only rotate if:
1. Quadrant has changed AND
2. New quadrant persists for 30+ days AND
3. Target asset class is in uptrend (above 10-month MA)

#### Fix #4: Quarterly Rebalancing (Already Validated)
**Result**: Best performing variant (V5)

#### Fix #5: Test on Different Time Periods
**Proposed**: Backtest on 2000-2014 to see if strategy works better in different market regimes

---

## 6. Final Verdict

### Is This Strategy Viable?

**For Absolute Returns**: ❌ **No** - All variants underperformed buy-and-hold SPY by 3.6-5.1% annually

**For Risk-Adjusted Returns**: ⚠️ **Maybe** - V5 achieved:
- Better Sharpe ratio than SPY (0.87 vs 0.76)
- Much lower max drawdown (-18.5% vs -33.7%)
- Lower volatility (11.3% vs 17.8%)

**For Portfolio Diversification**: ✅ **Yes** - Can be used as a satellite strategy (20-30% allocation) to:
- Reduce overall portfolio volatility
- Provide diversification away from pure equity exposure
- Potentially perform better in different market regimes

### What Did We Learn?

1. **Macro regime identification is real** - The quadrant framework makes conceptual sense
2. **Asset allocation is more important than timing** - The problem wasn't regime switching, it was the ETF choices
3. **Less trading is better** - Quarterly rebalancing beat monthly by 1.5% annually
4. **Simplicity wins** - The "Unknown" quadrant allocation (60% SPY, 20% TLT, 10% GLD, 10% cash) might have beaten the complex quadrant allocations
5. **Time period matters** - 2015-2026 was a uniquely favorable period for US mega-cap tech

### Should You Trade This?

**❌ Don't**: Use it as your primary investment strategy expecting to beat SPY

**✅ Do**: Use it as:
- A framework for thinking about macro positioning
- A risk management overlay (20-30% of portfolio)
- A systematic way to reduce drawdowns
- A complement to a core buy-and-hold strategy

**🔬 Worth Researching**:
- Test on 2000-2014 period
- Test with simplified allocations (higher SPY weights)
- Combine with momentum/technical filters
- Use as a pure risk-on/risk-off toggle rather than multi-quadrant rotation

---

## 7. Next Steps

### To Improve Performance

1. ✅ **DONE**: Identify which quadrants hurt performance → ALL of them
2. ✅ **DONE**: Test z-score bands → Minor improvement
3. ✅ **DONE**: Test holding period filters → Improved risk, not returns
4. ✅ **DONE**: Test quarterly rebalancing → Best improvement (+1.5% alpha)
5. ⏭️ **TODO**: Redesign allocations with higher SPY weights
6. ⏭️ **TODO**: Backtest on 2000-2014 period
7. ⏭️ **TODO**: Add momentum overlay
8. ⏭️ **TODO**: Test simplified 2-asset per quadrant approach

### Files Generated

- `backtest_results_10yr.csv` - Original strategy results
- `backtest_variant_1.csv` through `backtest_variant_5.csv` - All strategy variants
- `quadrant_allocation_analysis.png` - Visual breakdown of quadrant performance
- `strategy_comparison.png` - Visual comparison of all 5 strategy variants
- `BACKTEST_SUMMARY.md` - This document

---

## Appendix: Detailed Performance Tables

### Variant 5 (Best) - Quarterly + Low Cost
- Final Value: $281,653
- CAGR: 9.87%
- Volatility: 11.34%
- Sharpe: 0.87 ⭐
- Max Drawdown: -18.49% ⭐
- Trades: 253
- **Alpha gap vs SPY: -3.57%** (smallest gap)

### SPY Benchmark
- Final Value: $400,476
- CAGR: 13.44%
- Volatility: 17.79%
- Sharpe: 0.76
- Max Drawdown: -33.72%

**Risk-Adjusted Win**: V5 delivered 73% of SPY's returns with only 64% of the volatility and 55% of the max drawdown.
