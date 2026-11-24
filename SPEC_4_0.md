# SPEC_4_0.md — Addendum to the SHADEWARD 4.0 TDD

The full specification is the PDF "SHADEWARD 4.0 — AI-Native TDD, Agent Rules, & Step-by-Step Build Prompts". The formulas below exist only as images in that PDF (they are lost by text extraction), so they are transcribed here for Phase 3.

## 4.1 Matchmaking latency signal
```
latencySignalScore = 1 - min(100, Δping_ms) / 100
```
`max_relevant_difference = 100 ms`, weighted highest among MatchmakingService signals.

## 4.2 Multi-team Glicko-2
- Pairwise decomposition: 4-team Duos -> 3 pairwise outcomes per team, each weighted `w = 0.5` (1.5 effective duels). 8p Solo FFA: `w = 2/7`.
- Constants: `SCALE = 173.7178`, `tau = 0.5`, `epsilon = 1e-6`, `R0 = 1500`, `RD0 = 350`, `sigma0 = 0.06`, `RD_min = 45`.

```
g(phi_j)        = 1 / sqrt(1 + 3 * phi_j^2 / pi^2)
E(mu, mu_j, phi_j) = 1 / (1 + exp(-g(phi_j) * (mu - mu_j)))

v     = [ sum_{j=1..N-1} w * g(phi_j)^2 * E_j * (1 - E_j) ]^-1
Delta = v * sum_{j=1..N-1} w * g(phi_j) * (s_j - E_j)
```
- Solve new volatility `sigma'` via Illinois root-finding (standard Glicko-2 step 5).
- Squad MMR: `0.65 * max(MMR) + 0.35 * min(MMR)`.
- Season soft reset (every 8 weeks, 25% mean compression):
```
R_new  = 1500 + 0.75 * (R_old - 1500)
RD_new = max(RD_old, 130)
```

## Unit-test fixtures (RD = 80, vol = 0.06), tolerance 0.15 MMR
- Duos even (1500 lobby): #1 +25.3, #2 +8.4, #3 -8.4, #4 -25.3 (RD -> 77.8).
- Duos underdog (1300 vs 1600 lobby): #1 +44.1, #2 +26.6, #3 +9.2, #4 -8.3.
- Solo 8p FFA even (1500): #1 +33.0 to #8 -33.0 (RD -> 76.9).
- Smurf calibration (1500, RD = 350, 5 consecutive #1 wins): 1711.3 -> 1844.8 -> 1942.6 -> 2019.8 -> 2083.7 (RD -> 124.1).
