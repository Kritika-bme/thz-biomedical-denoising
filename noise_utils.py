import numpy as np
import yaml


def load_config(config_path="config.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def add_gaussian_noise(signal, std=0.05):
    noise = np.random.normal(0, std, size=signal.shape)
    return signal + noise


def add_shot_noise(signal, scale=0.02):
    noise = np.random.poisson(np.abs(signal) * 100) / 100 * scale
    return signal + noise.astype(np.float32)


def add_baseline_drift(signal, freq_thz, amplitude=0.03):
    drift = amplitude * np.sin(2 * np.pi * freq_thz / freq_thz[-1])
    return signal + drift.astype(np.float32)


def add_all_noise(signal, freq_thz, config):
    noisy = add_gaussian_noise(signal, std=config["noise"]["gaussian_std"])
    noisy = add_shot_noise(noisy, scale=config["noise"]["shot_scale"])
    noisy = add_baseline_drift(noisy, freq_thz, amplitude=config["noise"]["drift_amplitude"])
    return noisy.astype(np.float32)


def generate_noisy_dataset(config_path="config.yaml"):
    import os
    config  = load_config(config_path)
    clean   = np.load(config["paths"]["clean_data"] + "signals.npy")
    freq    = np.load(config["paths"]["clean_data"] + "freq_axis.npy")
    out_dir = config["paths"]["noisy_data"]

    os.makedirs(out_dir, exist_ok=True)

    noisy_signals = np.array([
        add_all_noise(sig, freq, config) for sig in clean
    ])

    np.save(out_dir + "signals_noisy.npy", noisy_signals)
    print(f"Noisy signals shape : {noisy_signals.shape}")
    print(f"Saved to            : {out_dir}")

    return noisy_signals, freq


if __name__ == "__main__":
    generate_noisy_dataset()