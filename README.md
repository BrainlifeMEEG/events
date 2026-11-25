# Extract Events from MEG/EEG Data

<!-- brainlife-app:begin (generated from the App manifest; edit the manifest, not this block) -->

> **Detects events on the stimulus channel of raw MEG/EEG data with MNE-Python find_events, optionally picks and merges event IDs, and outputs a BIDS events.tsv, an events plot and an HTML report.**

Runs mne.find_events with the given detection options, restricts events with mne.pick_events (include/exclude), merges IDs with mne.merge_events (event_id_combine) and labels conditions (event_id_condition). Use it to create the events file needed for epoching when events are coded on a trigger channel. It needs raw .fif data with a stimulus channel.

| | |
|---|---|
| 📥 **Inputs** | `neuro/meeg/mne/raw` |
| 📤 **Outputs** | `report/html` · `neuro/meg/fif-override` |
| 🐳 **Container** | `brainlifemeeg/mne:1.12.1` |
| ⚙️ **Resources** | 8 CPUs · 32 GB memory · 2 h walltime |
| 🔗 **Run it** | [doi.org/10.25663/brainlife.app.666](https://doi.org/10.25663/brainlife.app.666) |

#### 📥 Inputs

| Input | Datatype | Required | Description |
|---|---|---|---|
| `fif` | `neuro/meeg/mne/raw` | yes | Continuous MEG/EEG data in MNE raw .fif format containing a stimulus (trigger) channel. |

#### 📤 Outputs

| Output | Datatype | Description |
|---|---|---|
| `out_dir_report` | `report/html` | MNE HTML report visualizing the detected events. |
| `out_dir` | `neuro/meg/fif-override` | BIDS-compatible events.tsv with the detected (and merged) events. |

<details>
<summary><b>⚙️ Parameters</b> (13)</summary>

| Parameter | Type | Default | Description |
|---|---|---|---|
| `stim_channel` | string |  | Name of the stim channel or all the stim channels affected by triggers. If None, the config variables ‘MNE_STIM_CHANNEL’, ‘MNE_STIM_CHANNEL_1’, ‘MNE_STIM_CHANNEL_2’, etc. are read. If these are not found, it will fall back to ‘STI 014’ if present, then fall back to the first channel of type ‘stim’, if present. If multiple channels are provided then the returned events are the union of all the events extracted from individual stim channels. |
| `event_id_combine` | string |  | Events to be combined. Several IDs separated by commas, followed by ":" and the new ID or condition name of the merged events. 1,2 : 1 3,4 : 2 Note: These values need to be integers. This triggers repeated calls to mne.merge_events in the order provided. |
| `event_id_condition` | string |  | dict \| None Descriptions or names describing the event codes, if you passed events. The descriptions will be written to the trial_type column in *_events.tsv. The dictionary keys correspond to the event description,s and the values to the event codes. You must specify a description for all event codes appearing in events. If your data contains Annotations, you can use this parameter to assign event codes to each unique annotation description (mapping from description to event code). Note: this is run after combining events listed in (event_id_combine). |
| `consecutive` | string | `increasing` | If True, consider instances where the value of the events channel changes without first returning to zero as multiple events. If False, report only instances where the value of the events channel changes from/to zero. If ‘increasing’, report adjacent events only when the second event code is greater than the first. |
| `mask` | number |  | The value of the digital mask to apply to the stim channel values. If None (default), no masking is performed. |
| `uint_cast` | boolean | `false` | If True (default False), do a cast to uint16 on the channel data. This can be used to fix a bug with STI101 and STI014 in Neuromag acquisition setups that use channel STI016 (channel 16 turns data into e.g. -32768), similar to mne_fix_stim14 --32 in MNE-C. |
| `mask_type` | string | `and` | The type of operation between the mask and the trigger. Choose ‘and’ (default) for MNE-C masking behavior. |
| `initial_event` | boolean | `false` | If True (default False), an event is created if the stim channel has a value different from 0 as its first sample. This is useful if an event at t=0s is present. |
| `min_duration` | number | `0.005` | The minimum duration of a change in the events channel required to consider it as an event (in seconds). |
| `include` | string |  | A event id to include or a list of them. If None all events are included. |
| `exclude` | string |  | A event id to exclude or a list of them. If None no event is excluded. If include is not None the exclude parameter is ignored. |
| `shortest_event` | number | `2` | int Minimum number of samples an event must last (default is 2). If the duration is less than this an exception will be raised. |
| `output` | string | `onset` | ‘onset’ \| ‘offset’ \| ‘step’ Whether to report when events start, when events end, or both. |

</details>

📚 **References used by this App:**
- Hayashi S, Caron BA, Heinsfeld AS, et al. brainlife.io: a decentralized and open-source cloud platform to support neuroscience research. Nat Methods 21:809-813 (2024). [doi:10.1038/s41592-024-02237-2](https://doi.org/10.1038/s41592-024-02237-2)
- Gramfort A, et al. MEG and EEG data analysis with MNE-Python. Front Neurosci 7:267 (2013). [doi:10.3389/fnins.2013.00267](https://doi.org/10.3389/fnins.2013.00267)

<!-- brainlife-app:end -->

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
| `event_id_combine` | string | `""` | Rules for merging event IDs with `mne.merge_events()`, one rule per line: comma- or colon-separated source IDs followed by the destination ID, e.g. `"1,2,3:100"` merges events `1`, `2`, `3` into new ID `100`. |
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
