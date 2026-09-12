# Rheology — oscillatory amplitude sweep

An amplitude sweep applies a small, oscillating shear deformation to the sample and measures how
much of the resulting stress is elastic (**storage modulus, G′** — energy stored and recoverable,
"solid-like") versus viscous (**loss modulus, G′′** — energy dissipated as friction, "liquid-like").
At low deformation, a gel's structure stays intact and G′/G′′ sit on a flat plateau — the **linear
viscoelastic range (LVER)**. Push the deformation past the LVER limit and the network starts to
break down: G′ drops and G′′ often rises before the two curves cross, marking the point where the
sample behaves more like a liquid than a solid.

**Protocol.** Oleogel discs (2%, 4%, 6%, 8% RBX) were rested 24h, then measured at 25°C with a
parallel-plate geometry, sweeping shear strain logarithmically from 0.001% to 10% at 1Hz. The LVER
limit was taken as the strain where G′ first deviates more than 5% from its plateau value.

## Results

| | 2% RBX | 4% RBX | 6% RBX | 8% RBX |
|---|---|---|---|---|
| G′ plateau (Pa) | ≈4.8 × 10⁴ | ≈2.5 × 10⁵ | ≈3.6 × 10⁵ | ≈4.7 × 10⁵ |
| LVER limit (% strain) | ≈0.028 | ≈0.009 | ≈0.009 | ≈0.006 |

## What this tells us

The 2% oleogel is markedly less elastic than the others, consistent with the DSC and TPA results —
it's the outlier at every concentration below 4%. From 4% RBX upward, G′ keeps rising with wax
content but by smaller increments each time, suggesting the crystalline network's elastic
contribution saturates well before 8%. The LVER narrows as RBX% increases: more wax makes a stiffer
gel, but one that starts to break down at a smaller deformation — a stiffness/fragility trade-off.

**A caveat from the thesis itself:** this method wasn't fully optimized given time constraints. A
flat-plate (rather than cone-plate) probe geometry may have let a thin oil film form between probe
and sample, causing slippage that shortens the apparent LVER; and the sweep's starting strain
(0.001%) may not have been low enough to fully resolve the plateau at its lower end. Treat the LVER
values above as indicative of a trend across concentrations, not as precisely calibrated absolutes.
