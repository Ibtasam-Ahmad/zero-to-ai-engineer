# AI with Sensors: Signals, IMU, Radar, LiDAR and Sensor Fusion

Most AI courses start from data that is already clean: a table, a folder of images, a text corpus. In the real world a lot of data comes from **sensors**: the accelerometer in a watch, the radar in a car bumper, the LiDAR on a robot, the vibration sensor on a factory motor. That data arrives as noisy streams of numbers with sampling rates, units, drift and timing problems. This track teaches you to turn those streams into reliable AI systems, from the basics of signals and the FFT to fall detection, radar processing, 3-D point clouds, Kalman filters and the new wave of sensor foundation models. Every notebook starts from zero, explains each term the first time it appears, runs on a laptop CPU, and uses synthetic data so nothing needs to be downloaded.

**Who needs it.**
- **Students and beginners** who have done some NumPy and classical ML and want a practical, physical application area.
- **ML engineers and data scientists** moving into wearables, health tech, automotive, robotics, IoT or industrial AI.
- **Embedded and electronics engineers** who know the hardware and want the ML side (features, evaluation, edge models).
- **Interview preparation** for roles that mention "sensor data", "signal processing", "ADAS", "perception", "HAR" or "predictive maintenance".

**How it complements the rest of the repo.** Other modules teach the general tools. This track applies them to sensor data and adds the signal-processing and physics knowledge you need on top:

| Module | What it already teaches | What this track adds |
|---|---|---|
| [`04_Forecasting`](../04_Forecasting/) | time series, trends, seasonality, forecasting, [time-series anomaly detection](../04_Forecasting/10_ts_anomaly_detection.ipynb) | high-rate sensor signals: sampling, aliasing, FFT, filters, spectrograms, windowed classification |
| [`06_Computer_Vision`](../06_Computer_Vision/) | images, CNNs, detection, [3-D vision](../06_Computer_Vision/09_3d_vision.ipynb) | the *other* perception sensors: IMU, radar, LiDAR, and how they compare with cameras |
| [`03_Machine_Learning`](../03_Machine_Learning/) | models, metrics, cross-validation, [anomaly detection](../03_Machine_Learning/08_anomaly_detection/) | subject-wise evaluation (leave-one-subject-out), rare-event metrics such as false alarms per day |
| [`05_Deep_Learning`](../05_Deep_Learning/) | CNNs, RNNs, transformers, [model compression](../05_Deep_Learning/08_model_compression.ipynb) | which network suits which sensor, and when hand-made features still win |
| [`16_Deployment`](../16_Deployment/) | [edge deployment](../16_Deployment/04_edge_deployment.ipynb) | on-device limits of wearables (battery, latency, int8 quantization, cascades) |
| [`19_AI_Ethics_and_Safety`](../19_AI_Ethics_and_Safety/) | [privacy](../19_AI_Ethics_and_Safety/03_privacy.ipynb), regulation | privacy of radar/WiFi sensing vs cameras, medical-device and safety-system concerns |
| [`25_Quantum_AI`](../25_Quantum_AI/) | quantum computing and quantum ML | [05 - quantum ML on sensor data](../25_Quantum_AI/05_quantum_ml_on_sensor_data_fall_detection.ipynb) applies quantum ML to the fall-detection features built in notebook 02 of this track |

**When to take it** (see [LEARNING_PATH.md](../LEARNING_PATH.md)):

```
 Stage 3 Data analysis (NumPy) --> Stage 4 Maths --> Stage 5 Classical ML
                                                         |
                                       EARLIEST START ---+
                                                         v
                     26_Sensor_AI 01 -> 02 -> 03 -> 04 -> 05 -> 06
                                                         |
              helpful in parallel: 04_Forecasting, 05_Deep_Learning, 06_Computer_Vision
```

- **Earliest:** right after classical machine learning, once you can train and cross-validate a scikit-learn model.
- **Notebook 01 is the foundation** for everything else: sampling, FFT, filters, spectrograms and features.
- Notebook 06 (generative and foundation models for sensor data) is easier after [05_Deep_Learning](../05_Deep_Learning/).

---

## The whole topic explained simply

A **sensor** measures something physical (motion, distance, sound, radio echoes) and turns it into numbers. A **signal** is how those numbers change over time. Sensor AI is a pipeline: **measure -> clean -> describe -> decide**. You sample the signal fast enough (or fake frequencies appear), remove noise and bias, describe each short window with useful numbers (or let a neural network learn them), and then a model classifies, detects or tracks. A single sensor is often not enough, so systems **fuse** several sensors, each covering the others' weaknesses: radar sees speed in fog, cameras see colour, LiDAR sees precise 3-D shape, an IMU feels motion even in the dark.

**Tiny worked example.** A watch samples its accelerometer 50 times per second. Someone falls. In about one second the watch sees the total acceleration **drop** from about 1 g to about 0.3 g (free fall), then **jump** to about 4 g (impact), then stay near 1 g but pointing sideways (lying still). A rule like "dip below 0.6 g, then a spike above 2.5 g" catches many falls, but it also fires when someone jumps. Adding "and afterwards the person is lying and still" removes most of those false alarms, but now it misses falls that end sitting. Notebook 02 shows how ML combines all of these clues, and why "accuracy" is the wrong way to judge it when falls are about 1 window in 100 (or far fewer in real life).

---

## Who is this for, prerequisites and time

| | |
|---|---|
| **Who** | beginners with NumPy and basic ML; ML engineers moving into wearables, automotive, robotics, health or industrial IoT; embedded engineers learning the ML side |
| **Must know first** | [NumPy](../02_Data_Analysis/02_numpy.ipynb), [your first ML model](../03_Machine_Learning/00_start_here_your_first_ml_model.ipynb) |
| **Helpful** | [linear algebra](../14_Mathematics/01_linear_algebra.ipynb) (vectors, rotations, dot products; needed most in 04 and 05), [time series basics](../04_Forecasting/01_time_series_basics.ipynb), [probability](../14_Mathematics/03_probability.ipynb) (for Kalman filters in 05), [PyTorch from zero](../05_Deep_Learning/00_start_here_pytorch_from_zero.ipynb) (for 06) |
| **Time needed** | about 2-3 hours per notebook to read and experiment, 12-18 hours for the whole track |
| **Runs on** | CPU only, no API key, no internet. All data is synthetic (generated inside each notebook), so every number is illustrative |

---

## Study order

| # | Notebook | In one sentence |
|---|---|---|
| 01 | [Signals, frequency and sensor basics](01_signals_frequency_and_sensor_basics.ipynb) | Sampling, Nyquist and aliasing, ADC bits, noise and calibration, FFT, windowing, spectrograms, filters, resampling, wavelets, features, and a healthy-vs-faulty machine vibration classifier |
| 02 | [IMU activity recognition and fall detection](02_imu_activity_recognition_and_fall_detection.ipynb) | Accelerometer and gyroscope basics, a realistic synthetic IMU generator, threshold vs tree models vs a small neural net, leave-one-subject-out evaluation, false alarms per day, imbalance, edge constraints and safe deployment |
| 03 | [Radar: FMCW, range-Doppler and micro-Doppler](03_radar_fmcw_range_doppler_and_micro_doppler.ipynb) | How FMCW radar measures range, speed and angle, CA-CFAR detection, DBSCAN clustering, micro-Doppler activity and fall classification, breathing from radar phase |
| 04 | [LiDAR point clouds from zero](04_lidar_point_clouds_from_zero.ipynb) | How LiDAR builds 3-D point clouds; cropping and voxel downsampling, RANSAC ground removal, DBSCAN clustering, bounding boxes, bird's-eye-view maps, ICP registration and a simple cluster classifier |
| 05 | [Sensor fusion, Kalman filters and tracking](05_sensor_fusion_kalman_filters_and_tracking.ipynb) | Why and how to fuse sensors: calibration and coordinate frames, LiDAR-to-camera projection, time sync, Kalman and extended Kalman filters, the complementary filter, multi-object tracking and a particle-filter teaser |
| 06 | [Sensor data for generative and foundation models](06_sensor_data_for_generative_and_foundation_models.ipynb) | The data engine, augmentation, simulation and the sim-to-real gap, generative models for sensor data, sensor and time-series foundation models, self-supervised pretraining, sensor-language models, privacy and digital twins |

---

## The notebooks one by one

### 01 · Signals, frequency and sensor basics

*Explained simply.* A digital sensor takes snapshots of a continuous world. Take them too slowly and fast things look slow (like a car wheel spinning backwards in a film). The FFT is a recipe-reader that tells you which "notes" (frequencies) a signal is made of; filters keep the notes you want; a spectrogram is sheet music showing which notes play when.

*Tiny example.* A 9 Hz vibration sampled at 10 Hz produces exactly the same samples as a (flipped) 1 Hz vibration. After sampling, nothing can tell them apart. That is aliasing, and it is why devices filter before they sample.

*You will learn:*
- sensors, transducers and ADCs; analog vs digital; sampling rate, the **Nyquist** rule and **aliasing**;
- **quantization** and ADC bits (about 6 dB per bit), **noise types** (white, bias, drift) and why integrating a gyroscope drifts;
- units and two-point **calibration**;
- the **FFT** from intuition, frequency resolution `df = 1 / T`, **Hann windowing** and leakage, the **spectrogram (STFT)**;
- **filters**: moving average and Butterworth low/high/band-pass, zero-phase vs causal; safe **resampling** and aligning sensors;
- **wavelets** (a Haar transform by hand), **features** for ML (time and frequency domain, the **MFCC** idea);
- a project: **healthy vs faulty machine** from vibration (imbalance, misalignment, bearing fault), evaluated on unseen machines, plus **envelope analysis**.

*Key takeaway:* most sensor problems become much easier in the frequency domain, but only if the signal was sampled and windowed correctly.

### 02 · IMU activity recognition and fall detection

*Explained simply.* An accelerometer always feels gravity, so it knows which way is down; in free fall that feeling disappears. A fall is "lighter, then a hard hit, then lying still". The hard part is not detecting falls; it is detecting falls **without** ringing every time someone jumps or drops into a chair.

*Tiny example.* In the notebook's synthetic data about 1.2% of windows contain a fall. A model that always answers "no fall" is about 99% accurate and catches nothing. That is why the notebook reports sensitivity, specificity, precision, PR curves and false alarms per day instead.

*You will learn:*
- accelerometer and gyroscope axes, **g** units, gravity and **tilt**;
- a synthetic multi-subject IMU generator with activities, **look-alike** movements and falls;
- **windowing** with overlap and motion **features**;
- a **threshold detector** vs **random forest / gradient boosting** vs a small **MLP on raw windows**;
- **leave-one-subject-out** cross-validation, and why random splits are optimistic;
- rare-event metrics, **class imbalance**, threshold choice;
- **edge** constraints: model size, latency, **int8 quantization**, a gate-then-model **cascade**;
- other fall sensors (camera, radar, WiFi CSI, floor vibration) and privacy; **deployment**: confirmation countdown, escalation, medical-device rules.

*Key takeaway:* evaluate on new people and report false alarms per day; a fall detector is a safety system, not just a classifier.

### 03 · Radar: FMCW, range-Doppler and micro-Doppler

*Explained simply.* Radar shouts with radio waves and listens for echoes. An FMCW radar "sings" a rising note; the echo comes back slightly lower, and the difference tells the distance. Tiny phase changes from chirp to chirp tell the speed; differences between antennas tell the direction. Moving arms and legs leave a "micro-Doppler" fingerprint that reveals walking, sitting or falling, without a camera.

*Tiny example.* At 60 GHz the wavelength is 5 mm, so a 1 mm chest movement changes the echo phase by about 2.5 radians. That is why radar can measure breathing from across a room.

*You will learn:*
- radar basics, the **radar equation** (power falls as 1/R^4), wavelength and **mmWave** bands (24, 60, 77 GHz);
- **pulse vs FMCW**, the **chirp**, **beat frequency** and the **range FFT**; range resolution `c / 2B`;
- **Doppler** across chirps and the **range-Doppler map**; **angle of arrival** and the **MIMO virtual array**;
- **CA-CFAR** detection (1-D and 2-D, implemented by hand), masking, **DBSCAN** clustering, a **tracking** teaser;
- **micro-Doppler** simulation of walking, sitting, bending and **falls**, and a classifier on spectrogram features;
- **vital signs** (breathing from phase), **gesture sensing**, in-cabin **child presence detection**;
- radar vs camera vs LiDAR, and industry applications.

*Key takeaway:* radar measures speed directly and works in the dark and in bad weather, with good privacy; its weakness is coarse angular resolution and little semantic detail.

### 04 · LiDAR point clouds from zero

LiDAR measures distance with laser pulses and builds a 3-D **point cloud** of the scene. This notebook covers how LiDAR works and the classic pipeline from raw points to objects: preprocessing, RANSAC ground removal, DBSCAN clustering, bounding boxes, bird's-eye-view maps, ICP registration, the idea of SLAM, and deep learning on point clouds. It connects to the radar point cloud built in notebook 03 and to [3-D vision](../06_Computer_Vision/09_3d_vision.ipynb).

### 05 · Sensor fusion, Kalman filters and tracking

No single sensor is perfect. This notebook shows how to combine measurements (for example IMU + GPS, or radar + camera) into a better estimate, using **Kalman filters** (including the extended Kalman filter and the simple complementary filter), and how to **track** several objects over time. It also covers the practical glue: calibration, coordinate frames and time synchronisation. It continues the IMU drift problem from notebook 01 and the radar tracking teaser from notebook 03.

### 06 · Sensor data for generative and foundation models

Real sensor data is expensive to label, and rare events (falls, crashes, machine failures) are hard to collect. This notebook covers the **data engine** that feeds models, **augmentation**, **synthetic sensor data and simulation**, the **sim-to-real** gap, **generative models** for sensor data, **sensor and time-series foundation models** with **self-supervised pretraining**, multimodal **sensor-language models**, privacy and **digital twins**, as of late 2026.

---

## Sensor cheat-sheet

| Sensor | What it measures | Strengths | Weaknesses | Typical AI uses |
|---|---|---|---|---|
| **Camera** (RGB, also depth/stereo) | light intensity and colour per pixel | rich detail, reads signs and text, cheap | needs light, struggles with glare, fog and rain; poor direct distance; **privacy** | object detection, segmentation, pose estimation, OCR, visual inspection ([06_Computer_Vision](../06_Computer_Vision/)) |
| **Accelerometer** (IMU) | linear acceleration on 3 axes, including gravity (g or m/s²) | tiny, cheap, low power; gives tilt from gravity; detects impacts | noise and bias; position from double integration drifts quickly | activity recognition, step counting, fall detection, vibration monitoring (notebooks 01, 02) |
| **Gyroscope** (IMU) | rotation speed on 3 axes (deg/s) | smooth, fast orientation changes | bias drift: integrated angle error grows over time | orientation tracking, gesture recognition, stabilisation, fall detection (02, 05) |
| **Magnetometer** (IMU) | Earth's magnetic field (µT) | absolute heading (compass) | disturbed by metal and electronics indoors | heading for navigation, fused with gyro and accelerometer (05) |
| **Radar** (mmWave) | range, radial velocity, angle from radio echoes | measures speed directly; works in dark, fog, dust; sees through thin materials; good privacy | coarse angular resolution, little semantic detail, multipath ghosts | ADAS, presence and fall detection, vital signs, gesture sensing (03) |
| **LiDAR** | distance by laser time of flight -> 3-D point cloud | precise 3-D geometry, works in the dark | cost, degraded by heavy rain/fog/snow, no colour | 3-D object detection, mapping and localisation (SLAM), robotics (04) |
| **Ultrasonic** | distance by sound echo | very cheap, simple | short range, wide beam, affected by temperature and soft surfaces | parking sensors, robot obstacle avoidance, liquid level |
| **Thermal camera** (infrared) | surface temperature / heat radiation | works in total darkness; people stand out; less identifying than RGB | low resolution, cost; glass blocks it | people detection at night, fever screening, electrical and building inspection |
| **Microphone** | sound pressure | cheap, hears events out of sight | background noise, **speech privacy** | speech recognition, sound event detection, machine sound monitoring (MFCC in 01) |
| **GPS / GNSS** | global position and time from satellites | absolute position outdoors, accurate time | does not work indoors; urban canyons and multipath; about metre-level accuracy for consumer devices | navigation, fleet tracking, fused with IMU for smooth position (05) |
| **WiFi sensing (CSI)** | changes in the WiFi **channel state information** caused by people moving | uses existing routers; no camera; through walls | sensitive to room and furniture changes; still maturing for reliability | presence, activity and fall detection, people counting (02) |
| **ECG / PPG wearables** | heart electrical activity (ECG) or blood volume changes by light (PPG) | continuous health signals | motion artefacts, skin tone and fit effects on PPG; medical-grade claims need regulation | heart rate, arrhythmia screening, sleep and stress tracking |

---

## Real-world application areas

| Area | Sensors | What the AI does |
|---|---|---|
| **Self-driving and driver assistance** | camera, radar, LiDAR, IMU, GPS | detect and track vehicles and people, estimate free space, fuse sensors, plan safe motion |
| **Robotics** | LiDAR, depth cameras, IMU, wheel encoders, force sensors | mapping and localisation (SLAM), obstacle avoidance, grasping |
| **Health and elder care** | wearables (IMU, PPG, ECG), radar, WiFi | fall detection, activity and sleep monitoring, vital signs, early warning |
| **Smart homes and buildings** | radar, PIR motion sensors, thermal, microphones, WiFi | presence detection for lights and heating, occupancy counting, security |
| **Industry and predictive maintenance** | vibration (accelerometers), acoustic, temperature, current | detect bearing, imbalance and misalignment faults before breakdown; quality control |
| **Wearables and fitness** | IMU, PPG, GPS, barometer | step counting, activity recognition, workout tracking, heart rate, gesture control |

---

## Privacy notes: radar and WiFi sensing vs cameras

- **Cameras** capture faces, bodies and surroundings. In homes, bathrooms, bedrooms and care facilities this is often unacceptable to the people being monitored, and it creates sensitive data that can leak.
- **Radar and WiFi sensing** do not produce recognisable images, so they are often preferred for in-home monitoring and fall detection. They are **not privacy-free**: presence, routines, breathing and activity patterns are still personal (and sometimes health) data, and WiFi sensing can work through walls, so people may not know they are being sensed.
- **Wearables** collect continuous motion and health data tied to one person.
- Good practice for all of them: process on the device where possible, send only alerts or summaries, collect the minimum, get clear consent, and follow data-protection law (for example the GDPR for health data). See [privacy](../19_AI_Ethics_and_Safety/03_privacy.ipynb) and [AI regulation](../19_AI_Ethics_and_Safety/05_ai_regulation_compliance.ipynb).

---

## Install

The whole track needs only four libraries (all already in the repo's [requirements](../requirements.txt)):

```bash
pip install numpy scipy scikit-learn matplotlib
```

No GPU, no API key and no dataset downloads are needed. Real datasets (for example UCI HAR, SisFall or the CWRU bearing data) are named in each notebook's Further reading section if you want to practise on real recordings afterwards.

---

## Common beginner mistakes

- **Splitting windows randomly** instead of by person, machine or device. Overlapping windows from the same recording leak into the test set and inflate scores.
- **Reporting accuracy for rare events** such as falls or machine failures. Report sensitivity, precision, PR curves and false alarms per day (or per machine-month).
- **Downsampling with `x[::k]`** without a low-pass filter first, which creates aliases.
- **Mixing units** (g vs m/s², degrees vs radians, deg/s vs rad/s) or ignoring timestamps when combining sensors.
- **Using zero-phase filters (`filtfilt`) in a real-time design**: they need future samples. On a device, use causal filters and account for the delay.
- **Integrating a gyroscope or accelerometer for a long time without correction**: bias makes the result drift. Fuse with another sensor.
- **Trusting lab data**: simulated or lab falls, clean test benches and young volunteers differ from real users and real machines.

---

## Exam / interview quick revision

| Question | Short answer |
|---|---|
| What is the Nyquist frequency? | Half the sampling rate; anything above it aliases to a lower frequency. |
| What sets FFT frequency resolution? | The window length: `df = 1 / T`. |
| Why use a Hann window? | To reduce spectral leakage from cutting the signal into a window. |
| What does an accelerometer read in free fall? | About 0 g; at rest it reads 1 g pointing up. |
| How to evaluate a wearable model honestly? | Leave-one-subject-out (or GroupKFold by subject). |
| How does FMCW radar get range? | The beat frequency between transmitted and received chirps: `f_b = 2SR/c`. |
| Range and velocity resolution of FMCW? | `c / 2B` and `lambda / (2 N_c T_c)`. |
| What is CFAR? | A detector with a local, adaptive threshold that keeps the false-alarm rate constant. |
| What is micro-Doppler? | Extra Doppler shifts from moving parts (limbs); its spectrogram identifies activities. |
| Radar vs LiDAR vs camera in one line each? | Radar: speed and bad weather. LiDAR: precise 3-D shape. Camera: rich semantics. |

---

## Further reading

- Steven W. Smith, *The Scientist and Engineer's Guide to Digital Signal Processing* (free online at dspguide.com).
- Andreas Bulling, Ulf Blanke and Bernt Schiele, "A tutorial on human activity recognition using body-worn inertial sensors", *ACM Computing Surveys*, 2014.
- Sandeep Rao, "Introduction to mmWave Sensing: FMCW Radars", Texas Instruments training material.
- Mark A. Richards, *Fundamentals of Radar Signal Processing*, McGraw-Hill.
- Sebastian Thrun, Wolfram Burgard and Dieter Fox, *Probabilistic Robotics*, MIT Press (Kalman filters, localisation and mapping).
- Each notebook ends with its own detailed Further reading list.

Study notes for the whole track: [notes/26_Sensor_AI.md](notes/26_Sensor_AI.md).
