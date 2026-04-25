# THz Biomedical Signal Denoising with XAI

A simulation-based study on denoising sub-THz spectroscopy signals for non-invasive glucose sensing, using classical signal processing and a 1D Convolutional Autoencoder with SHAP-based explainability.

---

## Motivation

Non-invasive glucose monitoring using sub-THz waves is an active research area in biomedical engineering. THz signals passing through biological tissue are highly susceptible to noise from detector electronics, photon shot noise, and environmental drift. Effective denoising is a critical preprocessing step before any glucose estimation can occur.

This project simulates realistic THz signals using the **double-Debye dielectric model** of biological tissue, adds three types of realistic noise, and compares classical vs deep learning denoising approaches — with an XAI layer to interpret what the model learns.

---

## Project Structure
```
thz_denoising/
├── data/
│   ├── simulated_clean/       # Generated clean THz signals
│   ├── simulated_noisy/       # Noisy versions
│   └── processed/             # Denoised outputs
├── notebooks/
│   ├── 01_signal_simulation.ipynb
│   ├── 02_noise_addition.ipynb
│   ├── 03_classical_denoising.ipynb
│   ├── 04_autoencoder_denoising.ipynb
│   ├── 05_evaluation.ipynb
│   └── 06_xai_shap.ipynb
├── src/
│   ├── signal_generator.py
│   └── noise_utils.py
├── models/
│   └── autoencoder_best.pt
├── results/
│   ├── figures/
│   └── metrics_summary.csv
├── config.yaml
└── requirements.txt
```

---

## Methods

### Signal Simulation
THz transmission signals are simulated using the double-Debye model of biological tissue permittivity, with glucose-dependent parameter shifts based on published experimental data. 1000 signals are generated across a glucose range of 70–300 mg/dL.
<img width="2100" height="600" alt="02_clean_vs_noisy" src="https://github.com/user-attachments/assets/da57a3c7-8550-4667-89b1-66e9996e32c6" />


### Noise Model
Three realistic noise types are applied:
- **Gaussian noise** — thermal detector noise
- **Shot noise** — photon arrival randomness
- **Baseline drift** — slow environmental variation

### Denoising Methods
| Method | Description |
|---|---|
| Savitzky-Golay | Polynomial smoothing filter |
| Wavelet | Soft thresholding with db4 wavelet |
| 1D Conv Autoencoder | Deep learning encoder-decoder trained on noisy→clean pairs |
<img width="2700" height="600" alt="03_classical_denoising" src="https://github.com/user-attachments/assets/ebe8421f-887d-4c30-9dea-547e47890aea" />


### XAI — SHAP Analysis
SHAP (SHapley Additive exPlanations) is applied to the trained autoencoder to identify which frequency bands contribute most to signal reconstruction.
<img width="1800" height="600" alt="06_shap_top_frequencies" src="https://github.com/user-attachments/assets/3ede31cd-92d2-4743-8c20-767249b2b7c2" />
<img width="1800" height="1200" alt="06_shap_frequency" src="https://github.com/user-attachments/assets/ddae53b2-21e4-4e93-b6b8-22ed42d8a408" />
<img width="2700" height="600" alt="04_autoencoder_denoising" src="https://github.com/user-attachments/assets/f3587c2a-e0ac-44b6-b224-ab63c00e442b" />


---

## Results

| Method | SNR (dB) | RMSE |
|---|---|---|
| Noisy baseline | 26.72 ± 0.25 | 0.0615 ± 0.0018 |
| Savitzky-Golay | 30.17 ± 0.44 | 0.0413 ± 0.0021 |
| Wavelet | 32.43 ± 0.79 | 0.0320 ± 0.0029 |
| **1D Conv Autoencoder** | **36.40 ± 0.74** | **0.0202 ± 0.0017** |

The autoencoder achieves **3.97 dB higher SNR** than the best classical method (Wavelet), with RMSE reduced by 36.9%.
<img width="1800" height="750" alt="05_metrics_comparison" src="https://github.com/user-attachments/assets/7e6f7976-cb64-4c89-b6da-982284da87bc" />

### SHAP Findings
Top contributing frequency bands: **0.1–0.43 THz** — consistent with the dominant dielectric relaxation region of biological tissue predicted by the double-Debye model.

---

## Setup
```bash
git clone https://github.com/Kritika-bme/thz-biomedical-denoising
cd thz-biomedical-denoising
pip install -r requirements.txt
```

Run notebooks in order: `01` → `02` → `03` → `04` → `05` → `06`

---

## References

- Kaurav, P. et al. — Non-invasive glucose measurement using sub-THz sensor, IEEE Sensors Journal
- Kaurav, P. et al. — AI-Enabled Sub-THz Systems for Biomedical Applications, Springer
- Lundberg, S. & Lee, S.I. — A unified approach to interpreting model predictions, NeurIPS 2017

---

## Author

**Kritika** — B.Tech Biomedical Engineering, SGSITS Indore  

