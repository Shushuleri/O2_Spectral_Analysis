#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import mne
import numpy as np
import matplotlib.pyplot as plt
from specparam import SpectralModel
from scipy.stats import ttest_rel
import os

#File_paths
file_ec = os.path.join(os.environ['SYNOLOGY_ROOT'],r"EEG_student_5G\Blessing\data_proc\Blessing_sample_cleaned\GOLIAT_NF1X_001_S1_b04_EC.vhdr")
file_eo = os.path.join(os.environ['SYNOLOGY_ROOT'],r"EEG_student_5G\Blessing\data_proc\Blessing_sample_cleaned\GOLIAT_NF1X_001_S1_b04_EO.vhdr")

#Load_EEG_Data
raw_ec = mne.io.read_raw_brainvision(file_ec, preload=True)
raw_eo = mne.io.read_raw_brainvision(file_eo, preload=True)

ch_name='O2'

#To_Pick_ Channel
# raw_ec.pick(ch_name)
# raw_eo.pick(ch_name)

#Compute_PSD
psd_ec = raw_ec.compute_psd(method="welch", fmin=1, fmax=50, n_fft=2048, n_overlap=1024, picks=[ch_name])
psd_eo = raw_eo.compute_psd(method="welch", fmin=1, fmax=50, n_fft=2048, n_overlap=1024, picks=[ch_name])


freqs = psd_ec.freqs

power_ec = psd_ec.get_data()[0]
power_eo = psd_eo.get_data()[0]

#Fitting_SpecParam_models
fg_ec = SpectralModel(min_peak_height=0.1, peak_width_limits=[1, 8], aperiodic_mode="fixed")
fg_eo = SpectralModel(min_peak_height=0.1, peak_width_limits=[1, 8], aperiodic_mode="fixed")

fg_ec.fit(freqs, power_ec)
fg_eo.fit(freqs, power_eo)

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


# Plot 1: Power Spectrum for EC vs. EO
plt.figure(figsize=(8, 5))
plt.plot(freqs, np.log10(power_ec), label="EC - Power Spectrum", color="blue")
plt.plot(freqs, np.log10(power_eo), label="EO - Power Spectrum", color="red", linestyle="dashed")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Power Spectral Density (PSD)")
plt.title("Power Spectrum - O2 Channel")
plt.legend()
plt.show()

# Plot 2: Aperiodic Component
plt.figure(figsize=(8, 5))
plt.plot(freqs, fg_ec._ap_fit, label="EC - Aperiodic Fit", color="blue")
plt.plot(freqs, fg_eo._ap_fit, label="EO - Aperiodic Fit", color="red", linestyle="dashed")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Aperiodic Fit")
plt.title("Aperiodic Component (Steepness of Slope) - O2 Channel")
plt.legend()
plt.show()

#Results
print(f"Aperiodic Parameters (EC): {aperiodic_params_ec}")
print(f"Aperiodic Parameters (EO): {aperiodic_params_eo}")
print(f"Alpha Power (EC): {alpha_power_ec}")
print(f"Alpha Power (EO): {alpha_power_eo}")


fg_ec.report()
fg_eo.report()

