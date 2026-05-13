# Events

Brainlife App to extract events from MEG/EEG raw data using MNE-Python [`mne.find_events`](https://mne.tools/stable/generated/mne.find_events.html).

## Description

This app finds events from a stimulus channel in a raw `.fif` file, optionally combines or filters event IDs, and exports the results as a BIDS-compatible `events.tsv` file along with an MNE report visualization.

## Inputs

- `mne`: MEG/EEG raw data file in `.fif` format

## Outputs

- `out_dir/events.tsv`: BIDS-compatible events file
- `out_report/report.html`: MNE report with event visualization
- `product.json`: Metadata for Brainlife.io interface

## Configuration Parameters

- `stim_channel`: `None` | `str` | list of `str` — Name of the stimulus channel(s)
- `output`: `'onset'` | `'offset'` | `'step'` — Type of event to detect
- `consecutive`: `bool` | `'increasing'` — How to handle consecutive events without returning to zero
- `min_duration`: `float` — Minimum duration (in seconds) of a change in the events channel to be considered an event
- `shortest_event`: `int` — Minimum number of samples an event must last
- `mask`: `int` | `None` — Bitmask applied to the trigger channel
- `mask_type`: `'and'` | `'not_and'` — Operation between mask and trigger
- `uint_cast`: `bool` — Cast trigger channel to unsigned integer before processing
- `initial_event`: `bool` — Whether to add an event at the start of the recording
- `include`: `int` | list of `int` | `None` — Event IDs to include
- `exclude`: `int` | list of `int` | `None` — Event IDs to exclude
- `event_id_combine`: `str` — Combine event IDs (one rule per line, e.g. `"1,2,3 -> 100"`)
- `event_id_condition`: `str` — Mapping of condition names to event IDs (e.g. `"'face': 5, 'scrambled': 17"`)

## Usage

Clone the repository and update the `config.json` file with input file paths and parameters. Run via:

```bash
./main
```

## Technical Details

Events are detected using [`mne.find_events`](https://mne.tools/stable/generated/mne.find_events.html) and filtered with [`mne.pick_events`](https://mne.tools/stable/generated/mne.pick_events.html). Event IDs can be merged using [`mne.merge_events`](https://mne.tools/stable/generated/mne.merge_events.html). The output TSV file follows BIDS specification.

## Authors

- Saeed Zahran (https://github.com/saeedzahranutc)
- Maximilien Chaumon (https://github.com/dnacombo)

## Citations

Hayashi, S., Caron, B.A., Heinsfeld, A.S. et al. brainlife.io: a decentralized and open-source cloud platform to support neuroscience research. Nat Methods 21, 809–813 (2024). https://doi.org/10.1038/s41592-024-02237-2

## Funding

[![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1734853)
[![NSF-BCS-1636893](https://img.shields.io/badge/NSF_BCS-1636893-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1636893)
[![NSF-ACI-1916518](https://img.shields.io/badge/NSF_ACI-1916518-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1916518)
[![NSF-IIS-1912270](https://img.shields.io/badge/NSF_IIS-1912270-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1912270)
[![NIH-NIBIB-R01EB029272](https://img.shields.io/badge/NIH_NIBIB-R01EB029272-green.svg)](https://grantome.com/grant/NIH/R01-EB029272-01)
