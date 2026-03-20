import numpy as np
import yaml
import os


def load_config(config_path="config.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def double_debye_permittivity(freq_thz, eps_inf, eps_s1, eps_s2, tau1, tau2):
    """
    Computes complex permittivity of biological tissue using the double-Debye model.

    This tells us how much the tissue absorbs and slows THz waves at each frequency.
    Two Debye terms because biological tissue has two dominant relaxation mechanisms
    (bulk water relaxation and bound water relaxation).

    Args:
        freq_thz : array of frequencies in THz
        eps_inf  : permittivity at infinite frequency (background response)
        eps_s1   : strength of first relaxation (bulk water)
        eps_s2   : strength of second relaxation (bound water)
        tau1     : relaxation time of first mechanism (seconds)
        tau2     : relaxation time of second mechanism (seconds)

    Returns:
        Complex permittivity array (real + imaginary parts)
    """
    omega = 2 * np.pi * freq_thz * 1e12  # convert THz to rad/s

    term1 = (eps_s1 - eps_s2) / (1 + 1j * omega * tau1)
    term2 = (eps_s2 - eps_inf) / (1 + 1j * omega * tau2)

    return eps_inf + term1 + term2


def generate_thz_signal(freq_thz, glucose_level=100, add_variation=True):
    """
    Simulates a THz transmission signal through skin tissue at a given glucose level.

    Higher glucose slightly changes the dielectric relaxation parameters,
    which is the physical basis for non-invasive glucose sensing.

    Args:
        freq_thz      : frequency array in THz
        glucose_level : blood glucose in mg/dL (normal ~100, diabetic ~200+)
        add_variation : adds small random biological variation (realistic)

    Returns:
        1D array representing THz signal amplitude across frequencies
    """

    # base tissue parameters (skin, from published literature)
    eps_inf = 2.1
    eps_s1  = 8.5
    eps_s2  = 4.8
    tau1    = 9.4e-12   # ~9.4 picoseconds
    tau2    = 1.8e-12   # ~1.8 picoseconds

    # glucose shifts the permittivity slightly
    # this is a linearised approximation based on experimental studies
    glucose_factor = (glucose_level - 100) / 1000.0
    eps_s1 = eps_s1 + 0.03 * glucose_factor
    eps_s2 = eps_s2 + 0.015 * glucose_factor

    permittivity = double_debye_permittivity(
        freq_thz, eps_inf, eps_s1, eps_s2, tau1, tau2
    )

    # transmission amplitude = e^(-absorption * freq)
    absorption = np.imag(permittivity)
    signal = np.exp(-absorption * freq_thz)

    # small biological variation per sample (no two readings are identical in real life)
    if add_variation:
        signal += np.random.normal(0, 0.005, size=signal.shape)

    return signal.astype(np.float32)


def generate_dataset(config_path="config.yaml"):
    """
    Generates the full dataset of clean THz signals and saves them.
    Glucose levels are sampled uniformly between 70 and 300 mg/dL.
    """
    config = load_config(config_path)

    n        = config["signal"]["num_samples"]
    n_points = config["signal"]["num_points"]
    f_start  = config["signal"]["freq_start"]
    f_end    = config["signal"]["freq_end"]
    out_dir  = config["paths"]["clean_data"]

    os.makedirs(out_dir, exist_ok=True)

    freq_thz = np.linspace(f_start, f_end, n_points)
    glucose_levels = np.random.uniform(70, 300, size=n)

    signals = []
    for gl in glucose_levels:
        sig = generate_thz_signal(freq_thz, glucose_level=gl)
        signals.append(sig)

    signals = np.array(signals)         # shape: (1000, 512)
    labels  = glucose_levels.astype(np.float32)

    np.save(os.path.join(out_dir, "signals.npy"), signals)
    np.save(os.path.join(out_dir, "glucose_labels.npy"), labels)
    np.save(os.path.join(out_dir, "freq_axis.npy"), freq_thz)

    print(f"Generated {n} signals | shape: {signals.shape}")
    print(f"Glucose range: {labels.min():.1f} – {labels.max():.1f} mg/dL")
    print(f"Saved to: {out_dir}")

    return signals, labels, freq_thz


if __name__ == "__main__":
    generate_dataset()