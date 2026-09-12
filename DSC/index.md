# DSC — thermal behavior

Differential Scanning Calorimetry (DSC) heats and cools a tiny sample (2–4 mg, sealed in an
aluminum pan) alongside an empty reference pan, and measures the extra heat flow needed to keep
both at the same temperature. Melting and crystallization show up as peaks: the **onset**
temperature marks where the transition starts, the **peak** temperature is its maximum, and the
peak area gives the transition enthalpy (ΔH, in J/g) — how much energy the phase change absorbs
(melting) or releases (crystallization).

**Protocol.** Oleogel samples (2%, 4%, 6%, 8% RBX, 4 replicates each) were held at 20°C, heated to
90°C at 5°C/min, held, then cooled back to 20°C at 5°C/min. Lard was run the same way but starting
and ending at 5°C. See [`analisi.ipynb`](RBXRSO/heating/analisi) in each sub-folder for the code
that loads the raw thermograms, smooths them, and extracts these peak values.

## Results

**Heating (melting):**

| | 2% RBX | 4% RBX | 6% RBX | 8% RBX | Lard |
|---|---|---|---|---|---|
| Onset (°C) | 48.7 ± 4.4 | 56.6 ± 8.9 | 56.1 ± 10.7 | 66.3 ± 2.8 | ≈25 (1st of 3 peaks) |
| Peak (°C) | 63.9 ± 0.5 | 67.3 ± 0.4 | 68.6 ± 0.4 | 70.4 ± 0.5 | 34.0 / 36.7 / 49.1 |
| ΔH (J/g) | 6.4 ± 0.9 | 7.6 ± 1.5 | 12.8 ± 1.4 | 18.1 ± 1.9 | 22.7 (1st peak) |

**Cooling (crystallization):**

| | 2% RBX | 4% RBX | 6% RBX | 8% RBX | Lard |
|---|---|---|---|---|---|
| Onset (°C) | 57.3 ± 0.8 | 61.8 ± 0.5 | 64.0 ± 0.2 | 66.4 ± 0.6 | ≈26 / ≈22 |
| Peak (°C) | 55.7 ± 1.0 | 60.2 ± 0.4 | 62.6 ± 0.5 | 64.8 ± 0.3 | 24.5 / 23.6 |
| ΔH (J/g) | −2.1 ± 1.2 | −6.4 ± 3.3 | −7.7 ± 2.3 | −12.2 ± 2.3 | −3.5 / −28.8 |

Values are mean ± SD of 4 replicates; differences between RBX concentrations are statistically
significant (Tukey HSD, p<0.05) for onset, peak, and ΔH.

## What this tells us

More wax means a higher, later, and more energetic melting/crystallization transition — but the
effect isn't perfectly linear, and at higher RBX% the peaks broaden and get closer together rather
than continuing to spread out. All four oleogels melt at a *higher* temperature than lard, and in a
much narrower window: lard shows multiple peaks starting near 25°C because it's a mix of many
different triglycerides, while the wax-oil gel has a simpler, more uniform crystal population.

Practically: every oleogel's melting point is still well below the 100°C the sausage reaches during
cooking, so the crystal network set up when the gel was made doesn't survive that heat treatment —
it re-forms from scratch as the sausage cools. In a product with a milder heat treatment, though,
these onset/peak values would define the safe operating range before the gel's structure changes.
