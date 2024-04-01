# rhigo

This program implements communication between two instruments: Rohde&Schwarz Signal Generator R&S®SMB100A and Rigol RSA3000 Series Real-time Spectrum Analyzer.
The Rohde&Schwarz instrument sends signal of given frequency and amplitude, the signal traverses some obstacle and the Rigol instruments reads the signal and checks its attenuation.

## Installation
- Install Python 3
- Install all dependencies by running:
  ```
  python -m pip install -r requirements.txt
  ```

## Running
From the project directory run:
```
python main.py
```
The program:
1. Detects connected Rohde&Scharz and Rigol instruments.
1. Read input data from `input.csv` file.
  The file has two comma separated columns without any header. The first columnis a frequency in Hz and the second an amplitude level in dBm.
1. Performs measurement.
1. Writes the result to a `.csv` file which name is based of the time of the measurement start.
  The file has four comma separated columns: input frequency, input amplitude level, output frequency and output amplitude level.
