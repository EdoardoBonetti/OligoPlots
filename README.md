# OligoPlots

Data, notebooks, and plots behind a master's thesis on **rice-bran-wax oleogels** and their use as
a fat replacer in a **vegan Lyoner-type sausage**.

> **Thesis:** *Formulazione di un oleogel a base di cera di crusca di riso e suo impiego nella
> formulazione di salsicce vegane tipo Lyoner*
> Daniele Tateo — Corso di Laurea Magistrale in Scienze e Tecnologie Alimentari,
> Dipartimento di Scienze e Tecnologie Agro-Alimentari, Università di Bologna (AY 2023/2024).
> Advisor: Prof.ssa Maria Teresa Rodriguez Estrada. Co-advisors: Prof. Jochen Weiss,
> Dott. Sebastian Mannweiler, Dott. Dario Mercatante. Lab work carried out at the Department of
> Food Technology, University of Hohenheim, Germany.

## Why this project

Saturated and trans fats (lard, hydrogenated/interesterified oils) give food its texture, mouthfeel
and structure, but their health effects have pushed regulators and manufacturers to look for
substitutes. **Oleogelation** turns a liquid oil into a semi-solid gel using only a small amount of
a structuring agent — no hydrogenation, no interesterification, no trans fats — by trapping the
liquid oil in a 3D crystalline network. This project formulates such a gel from **rice bran wax
(RBX)** dissolved in **canola oil (RSO)** at 2/4/6/8% w/w, characterizes it, and then tests it as a
drop-in replacement for the fat in a vegan sausage.

## What's in this repo

The repo is organized by measurement technique. Each top-level folder holds the raw instrument
output plus the notebook that cleans, plots, and (where relevant) statistically compares it.

| Folder | Technique | What it measures |
|---|---|---|
| [`DSC/`](DSC/index.md) | Differential Scanning Calorimetry | Melting/crystallization temperature and enthalpy of the oleogel (2/4/6/8% RBX) and of pork lard, for comparison |
| [`TPA/`](TPA/index.md) | Texture analysis (single-compression penetration) | How firm the pure oleogel is, on its own, versus lard |
| [`TPA/SAUSAGES/`](TPA/SAUSAGES/index.md) | Texture Profile Analysis | Hardness/springiness of the finished vegan sausage, made with the oleogel (added liquid or frozen), plain oil, margarine, or lard |
| [`REHO/`](REHO/index.md) | Oscillatory rheology (amplitude sweep) | Elastic (G′) vs. viscous (G′′) behavior of the oleogel and its linear viscoelastic range |

Each folder's `index.md`/`intro` page (viewable as part of the [Jupyter Book](#browsing-the-book))
explains the method in plain language and summarizes the actual results before you get to the raw
notebook. The thesis also covers optical and confocal laser scanning microscopy (CLSM) of the wax
crystal network — those images motivate the story but aren't reproduced here, since this repo only
tracks the data/code for DSC, TPA, and rheology.

## Key takeaways

- **Melting point scales with wax content, but plateaus.** Oleogel onset melting temperature rises
  from ≈49°C (2% RBX) to ≈66°C (8% RBX) — all comfortably below the 100°C the sausage reaches
  during cooking, meaning the crystal network doesn't survive the cook and re-forms on cooling.
- **Firmness saturates above ~4% RBX.** Below that, at 2% RBX, the oleogel is noticeably softer and
  easier to penetrate; from 4% up, penetration resistance and elastic modulus (G′) change much less
  with concentration.
- **In the sausage, the oleogel lands between plain oil and animal fat.** Sausages made with the
  oleogel don't reach the hardness of lard- or margarine-based sausages, but adding it *liquid*
  (rather than pre-frozen at −20°C) makes the sausage significantly firmer than using plain canola
  oil — so how the oleogel is incorporated matters as much as its concentration.
- **The rheology method needs more work.** The amplitude-sweep protocol (plate geometry, starting
  strain) wasn't fully optimized in the time available, so its linear viscoelastic range (LVER)
  estimates should be read as indicative, not definitive — see the thesis conclusions.

## Browsing the book

`_config.yml`/`_toc.yml` wire this repo up as a [Jupyter Book](https://jupyterbook.org/). To build
it locally:

```bash
pip install -r requirements.txt
jupyter-book build .
```

or open any `analisi.ipynb` directly in Jupyter to rerun the plotting/statistics code
(in [`lab.py`](lab.py)) against the raw data.

## Repo scope and limitations

This repo captures the DSC, TPA, and rheology work only — it does not include the sensory or
oxidative-stability analyses the thesis flags as necessary follow-ups, nor the microscopy imaging.
For the full picture (materials, protocols, statistics, and discussion), see the thesis itself.
