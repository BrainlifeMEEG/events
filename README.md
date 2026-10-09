# Extract Events from MEG/EEG Data

[![Run on Brainlife.io](https://img.shields.io/badge/Brainlife-bl.app.666-blue.svg)](https://doi.org/10.25663/brainlife.app.666)

## Description

This app finds events from a stimulus channel in a raw MEG/EEG `.fif` file using
[`mne.find_events`](https://mne.tools/stable/generated/mne.find_events.html). Detected events can
be restricted to a subset of IDs with
[`mne.pick_events`](https://mne.tools/stable/generated/mne.pick_events.html) and merged into new
IDs with [`mne.merge_events`](https://mne.tools/stable/generated/mne.merge_events.html).

The app generates:
- a BIDS-compatible `events.tsv` file
- a sanity-check plot of the detected events (`mne.viz.plot_events`)
- an MNE report visualizing the events

## Inputs

- **`mne`** (`neuro/meeg/mne/raw`): continuous MEG/EEG raw data to extract events from (required)

## Outputs

- **`out_dir/events.tsv`** (`neuro/meg/fif-override`, tag `events`): BIDS-compatible events file
- **`out_figs/events_plot.png`**: sanity-check plot of the detected events, embedded in `product.json`
- **`out_report/report.html`** (`report/html`): MNE report with event visualization
- **`product.json`**: metadata for the Brainlife.io interface

## Configuration Parameters

| key | type | default | description |
|---|---|---|---|
| `stim_channel` | string | `""` | Name of the stimulus channel(s) to read triggers from, passed to `mne.find_events(stim_channel=...)`. Empty falls back to MNE's auto-detection (`MNE_STIM_CHANNEL*` config vars, then `"STI 014"`, then the first `stim`-type channel). |
| `output` | string | `"onset"` | Whether to report event `"onset"`, `"offset"`, or `"step"` (both), passed to `mne.find_events(output=...)`. |
| `consecutive` | string | `"increasing"` | How to handle consecutive events without returning to zero: `"true"`, `"false"`, or `"increasing"` (adjacent events counted only when the code increases), passed to `mne.find_events(consecutive=...)`. |
| `min_duration` | float | `0.005` | Minimum duration (seconds) of a change on the stim channel to count as an event, passed to `mne.find_events(min_duration=...)`. |
| `shortest_event` | int | `2` | Minimum number of samples an event must last, passed to `mne.find_events(shortest_event=...)`. |
| `mask` | int \| null | `null` | Bitmask applied to the trigger channel values before detecting events, passed to `mne.find_events(mask=...)`. `null` disables masking. |
| `mask_type` | string | `"and"` | Operation between `mask` and the trigger channel: `"and"` or `"not_and"`, passed to `mne.find_events(mask_type=...)`. |
| `uint_cast` | boolean | `false` | If `true`, cast the stim channel to `uint16` before detecting events (works around a Neuromag STI101/STI014 sign issue), passed to `mne.find_events(uint_cast=...)`. |
| `initial_event` | boolean | `false` | If `true`, create an event at the first sample when the stim channel is non-zero there, passed to `mne.find_events(initial_event=...)`. |
| `include` | int \| list of int \| null | `null` | Event ID(s) to keep, passed to `mne.pick_events(include=...)`. `null`/empty keeps all events; takes precedence over `exclude` when both are set. |
| `exclude` | int \| list of int \| null | `null` | Event ID(s) to drop, passed to `mne.pick_events(exclude=...)`. Ignored when `include` is set. |
| `event_id_combine` | string | `""` | Rules for merging event IDs with `mne.merge_events()`, one rule per line: comma-separated source IDs followed by the destination ID, e.g. `"1,2,3 -> 100"`. |
| `event_id_condition` | string | `""` | Mapping from condition names to event IDs, e.g. `"'face': 5, 'scrambled': 17"`, used to label the output report/figure and restrict events to those IDs. |

## Usage

### Running on Brainlife.io

1. Select a MEG/EEG raw data file (`.fif`) as the `mne` input.
2. Set `stim_channel` and the other detection parameters, or keep the defaults.
3. Optionally set `event_id_combine` and/or `event_id_condition` to merge or label event IDs.
4. Submit the task.
5. Review the resulting `events.tsv`, the events plot, and the HTML report in the output viewer.

### Local Testing

```bash
# Clone the repository and update config.json with your input file path and parameters
./main
```

## Technical Details

Events are detected using [`mne.find_events`](https://mne.tools/stable/generated/mne.find_events.html)
and filtered with [`mne.pick_events`](https://mne.tools/stable/generated/mne.pick_events.html). Event
IDs can be merged using [`mne.merge_events`](https://mne.tools/stable/generated/mne.merge_events.html).
The output TSV file follows the BIDS specification.

## Authors

- Saeed Zahran (https://github.com/saeedzahranutc)
- Maximilien Chaumon (https://github.com/dnacombo)

## Citations

- Hayashi, S., Caron, B.A., Heinsfeld, A.S. et al. brainlife.io: a decentralized and open-source cloud platform to support neuroscience research. Nat Methods 21, 809–813 (2024). https://doi.org/10.1038/s41592-024-02237-2
- Gramfort, A. et al. MEG and EEG data analysis with MNE-Python. Front. Neurosci. 7, 267 (2013). https://doi.org/10.3389/fnins.2013.00267

## Funding Acknowledgement

brainlife.io is publicly funded. We kindly ask that you acknowledge the funding below in your code and publications.

[![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1734853)
[![NSF-BCS-1636893](https://img.shields.io/badge/NSF_BCS-1636893-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1636893)
[![NSF-ACI-1916518](https://img.shields.io/badge/NSF_ACI-1916518-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1916518)
[![NSF-IIS-1912270](https://img.shields.io/badge/NSF_IIS-1912270-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1912270)
[![NIH-NIBIB-R01EB029272](https://img.shields.io/badge/NIH_NIBIB-R01EB029272-green.svg)](https://grantome.com/grant/NIH/R01-EB029272-01)
[![NIH-NIBIB-R01EB030896](https://img.shields.io/badge/NIH_NIBIB-R01EB030896-green.svg)](https://grantome.com/grant/NIH/R01-EB030896-01)

## License

Copyright (c) 2026 MEEG Brainlife team. Licensed under AGPL-3.0, see [license.txt](license.txt).
