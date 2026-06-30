# Ammeter Emulators

This project provides emulators for different types of ammeters: Greenlee, ENTES, and CIRCUTOR. Each ammeter emulator runs on a separate thread and can respond to current measurement requests.

## Project Structure

- `main.py`: Main script to start the ammeter emulators and request current measurements.
- `Ammeters/`  
  - `Circutor_Ammeter.py`: Emulator for the CIRCUTOR ammeter.
  - `Entes_Ammeter.py`: Emulator for the ENTES ammeter.
  - `Greenlee_Ammeter.py`: Emulator for the Greenlee ammeter.
  - `base_ammeter.py`: Base class for all ammeter emulators.
  - `client.py`: Client to request current measurements from the ammeter emulators.
- `config/`
  - `config.yaml`: Configuration file for the ammeter emulators.
- `examples/`
  - `test_circutor.py`: Test for circutor.
  - `test_entes.py`: Test for entes ammeter.
  - `test_greenlee.py`: Test for greenlee.
- `src/`
  - `testing/`
    - `test_framework.py`: Class to test the ammeter emulators.
  - `utils/`
    - `config.py`: Configuration settings.
    - `logger.py`: Logging setup.
    - `Utils.py`: Utility functions, including `generate_random_float`.

## Usage

To make tests in "examples/ run, do the following:

1. download (or clone) the repo:

2. cd into "eb_ammeters"

3. create a venv with command "python3 -m venv venv"

4. activate venv with command "source venv/bin/activate" on Linux / Mac. For windows use "venv\scripts\activate".

5. add pyaml library with "pip install pyaml" (this is te only library added)

6. run a test with command "python3 -m examples.test_entes" (without .py)

7. a results/logs directory should be created with and log file "timestamp_test_entes.log" for example.

8. the log file has 3 different loglevels - warning, error, debug and info level which has statistics of the entire run.

9. the test duration, sample frequency and occurances are configured in .yaml file in config/config.yaml.

10. in future tests, pytest library will be used and test date can be displayed in plot charts (pytest and matplot libraries).

# Ammeter Emulators

## Greenlee Ammeter
!!! Port 5000 is used on mac devices by some important proccess, so for greenlee, 5001 is used !!!
- **Port**: 5001
- **Command**: `MEASURE_GREENLEE -get_measurement`
- **Measurement Logic**: Calculates current using voltage (1V - 10V) and (0.1Ω - 100Ω).
- **Measurement method** : Ohm's Law: I = V / R

## ENTES Ammeter
!!! Since greenlee is with 5001, entes is 5002
- **Port**: 5002
- **Command**: `MEASURE_ENTES -get_data`
- **Measurement Logic**: Calculates current using magnetic field strength (0.01T - 0.1T) and calibration factor (500 - 2000).
- **Measurement method** : Hall Effect: I = B * K

## CIRCUTOR Ammeter

- **Port**: 5003
- **Command**: `MEASURE_CIRCUTOR -get_measurement`
- **Measurement Logic**: Calculates current using voltage values (0.1V - 1.0V) over a number of samples and a random time step (0.001s - 0.01s).
- **Measurement method** : Rogowski Coil Integration: I = ∫V dt

To start the ammeter emulators and request current measurements, run the `main.py` script:
```sh
python main.py
```
THe script runs for all 3 ammeters simmoultanously when configuring "itterations" and "sleep_time"