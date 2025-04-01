#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import mne
import numpy as np
import matplotlib.pyplot as plt
from specparam import SpectralGroupModel
from scipy.stats import ttest_rel
import os

#File_paths
file_ec = os.path.join(os.environ['SYNOLOGY_ROOT'],r"EEG_student_5G\Blessing\data_proc\Blessing_sample_cleaned\GOLIAT_NF1X_001_S1_b04_EC.vhdr")
file_eo = os.path.join(os.environ['SYNOLOGY_ROOT'],r"EEG_student_5G\Blessing\data_proc\Blessing_sample_cleaned\GOLIAT_NF1X_001_S1_b04_EO.vhdr")

#Load_EEG_Data
raw_ec = mne.io.read_raw_brainvision(file_ec, preload=True)
raw_eo = mne.io.read_raw_brainvision(file_eo, preload=True)

#To_Pick_ Channel
raw_ec.pick(['O2'])
raw_eo.pick(['O2'])

#PSD_Parameters
fmin, fmax = 1, 50  # Frequency range
n_fft = 1024
n_overlap = 512

#To_Compute_PSD
psd_ec, freqs = mne.time_frequency.psd_array_welch(
    raw_ec.get_data(), sfreq=raw_ec.info['sfreq'],
    fmin=fmin, fmax=fmax, n_fft=n_fft, n_overlap=n_overlap
)

psd_eo, _ = mne.time_frequency.psd_array_welch(
    raw_eo.get_data(), sfreq=raw_eo.info['sfreq'],
    fmin=fmin, fmax=fmax, n_fft=n_fft, n_overlap=n_overlap
)


psd_ec, psd_eo = np.squeeze(psd_ec), np.squeeze(psd_eo)
psd_ec, psd_eo = psd_ec[np.newaxis, :] if psd_ec.ndim == 1 else psd_ec, psd_eo[np.newaxis, :] if psd_eo.ndim == 1 else psd_eo

#Fitting_Models
fg_ec = SpectralGroupModel(min_peak_height=0.1, verbose=False)
fg_eo = SpectralGroupModel(min_peak_height=0.1, verbose=False)

fg_ec.fit(freqs, psd_ec)
fg_eo.fit(freqs, psd_eo)

#Extract_Aperiodic_Parameters
aperiodic_params_ec = fg_ec.get_params('aperiodic_params')[0]
aperiodic_params_eo = fg_eo.get_params('aperiodic_params')[0]

#Extracting_Alpha_Power_(8-12 Hz)
def extract_alpha_power(fg_model):
    peaks = fg_model.get_params('peak_params')
    alpha_power = [peak[1] for peak in peaks if 8 <= peak[0] <= 12]
    return alpha_power[0] if alpha_power else np.nan

alpha_power_ec = extract_alpha_power(fg_ec)
alpha_power_eo = extract_alpha_power(fg_eo)

#Statistical_Comparisons
t_alpha, p_alpha = ttest_rel([alpha_power_ec], [alpha_power_eo])
t_aperiodic, p_aperiodic = ttest_rel([aperiodic_params_ec[1]], [aperiodic_params_eo[1]])

#Plotting_PSD
plt.figure(figsize=(8, 5))
plt.plot(freqs, np.log10(psd_ec.T), label='Eyes Closed', alpha=0.7)
plt.plot(freqs, np.log10(psd_eo.T), label='Eyes Open', alpha=0.7)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Log Power Spectral Density')
plt.legend()
plt.title('PSD Comparison: Eyes Open vs. Eyes Closed')
plt.show()

#Results
print(f"Aperiodic Parameters (EC): {aperiodic_params_ec}")
print(f"Aperiodic Parameters (EO): {aperiodic_params_eo}")
print(f"Alpha Power (EC): {alpha_power_ec}")
print(f"Alpha Power (EO): {alpha_power_eo}")

print(f"\nPaired t-test for Alpha Power: t = {t_alpha:.4f}, p = {p_alpha:.4f}")
print(f"Paired t-test for Aperiodic Exponent: t = {t_aperiodic:.4f}, p = {p_aperiodic:.4f}")

