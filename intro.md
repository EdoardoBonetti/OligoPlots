# OligoPlots

This book documents the experimental data behind a master's thesis on formulating an **oleogel**
from **rice bran wax (RBX)** in **canola oil (RSO)**, and using it to replace the fat fraction of a
**vegan Lyoner-type sausage**.

## Background

Saturated fats (like lard) and industrially hydrogenated or interesterified oils give food its
structure, texture and mouthfeel, but their link to cardiovascular disease has driven regulation
(the EU caps industrial trans fats at 2g/100g of total fat) and consumer demand for alternatives.
**Oleogelation** is a comparatively new structuring approach: a small amount of a gelling agent —
here, rice bran wax — is dissolved into a liquid oil at high temperature. On cooling, the wax
crystallizes into a three-dimensional network that physically traps the liquid oil, producing a
semi-solid, thermoreversible gel *without* changing the oil's chemistry. That makes oleogels an
attractive solid-fat substitute wherever a recipe currently relies on lard, butter, or hydrogenated
fat for its texture.

## The experiment, in short

1. **Formulate** the oleogel at four wax concentrations — 2%, 4%, 6%, 8% RBX (w/w) in canola oil —
   and characterize it against pork lard as the animal-fat baseline.
2. **Characterize structure and behavior**: melting/crystallization by DSC, firmness by
   single-compression penetration testing, and viscoelasticity by oscillatory rheology
   (amplitude sweep). The thesis additionally used optical and confocal microscopy to image the
   wax crystal network directly — informative context, but not part of this repo's data/code.
3. **Apply it**: replace the fat in a vegan Lyoner-type sausage recipe with the oleogel — added
   either liquid (straight after preparation) or pre-frozen at −20°C — and compare the resulting
   sausage's texture (TPA) against versions made with margarine, plain canola oil, or lard.

## How this book is organized

- **DSC** — thermal behavior of the oleogel and lard: does wax concentration shift the melting and
  crystallization temperatures, and by how much?
- **TPA** — mechanical firmness, first of the pure oleogel on its own, then ([in the `SAUSAGES`
  sub-section](TPA/SAUSAGES/index)) of the finished sausage made with it.
- **Rheology** — how elastic vs. viscous the oleogel is under small oscillating deformations, and
  where it stops behaving like an intact solid (its linear viscoelastic range).

Each part opens with a short page summarizing the method and the headline numbers, before linking
to the notebook that actually loads, cleans, and plots the raw instrument data.

## What we learned

Wax concentration raises the oleogel's melting point and firmness, but with diminishing returns
above ~4% RBX. In the sausage, the oleogel doesn't fully replicate lard or margarine's firmness,
but clearly outperforms using plain liquid oil — and *how* it's incorporated (liquid vs. frozen)
measurably affects the outcome. See each section for the numbers, and the thesis itself for the
full discussion, statistics, and the microscopy work that isn't reproduced here.
