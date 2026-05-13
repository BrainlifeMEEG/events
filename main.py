"""
Extract events from MEG/EEG raw data using MNE-Python.

This app finds events from a stimulus channel in a raw .fif file,
optionally combines or filters event IDs, and exports the results as
a BIDS-compatible events.tsv file along with an MNE report.

Inputs:
    - mne: Path to MNE raw .fif file

Outputs:
    - out_dir/events.tsv: BIDS-compatible events file
    - out_report/report.html: MNE report with event visualization
    - product.json: Metadata for Brainlife.io interface
"""

# Copyright (c) 2026 brainlife.io
#
# Extract events from MEG/EEG raw data.
#
# Authors:
# - Saeed Zahran (https://github.com/zahransa)
# - Maximilien Chaumon (https://github.com/dnacombo)

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'brainlife_utils'))

import numpy as np
import mne
import re
from mne_bids.write import _events_tsv

from brainlife_utils import (
    load_config,
    setup_matplotlib_backend,
    ensure_output_dirs,
    create_product_json,
    add_image_to_product,
    add_info_to_product,
)

setup_matplotlib_backend()

ensure_output_dirs('out_dir', 'out_report')

config = load_config()

# == LOAD DATA ==
data_file = config['mne']
raw = mne.io.read_raw_fif(data_file, verbose=False)

# == FIND EVENTS ==
events = mne.find_events(raw,
                         stim_channel=config['stim_channel'],
                         output=config['output'],
                         consecutive=config['consecutive'],
                         min_duration=config['min_duration'],
                         shortest_event=config['shortest_event'],
                         mask=config['mask'],
                         uint_cast=config['uint_cast'],
                         mask_type=config['mask_type'],
                         initial_event=config['initial_event'])

sfreq = raw.info['sfreq']

events = mne.pick_events(events, include=config['include'], exclude=config['exclude'])

# Combine event IDs if specified (syntax: "1,2,3 -> 100" per line)
if config['event_id_combine']:
    event_id_combine = config['event_id_combine'].split('\n')
    event_id_combine = [re.split(r' *, *| *: *', ids) for ids in event_id_combine]
    event_id_combine = [[int(id) for id in event] for event in event_id_combine]
    event_to = [id.pop() for id in event_id_combine]
    for ids, to in zip(event_id_combine, event_to):
        events = mne.merge_events(events, ids=ids, new_id=to)

if config['event_id_condition']:
    event_id_condition = config['event_id_condition'].replace('\n', '')
    event_id = eval('{' + event_id_condition + '}')

    id_list = list(event_id.values())
    # keep only those events named in event_id_condition that are present in raw
    id_list = [id for id in id_list if id in events[:, 2]]
    event_id = {key: val for key, val in event_id.items() if val in id_list}
else:
    event_id = None
    id_list = None

events = mne.pick_events(events, include=id_list)

# == SAVE EVENTS TSV ==
_events_tsv(events, np.repeat(0., events.shape[0]), raw, 'out_dir/events.tsv', trial_type=None, overwrite=True)

# == GENERATE REPORT ==
report = mne.Report(title='Events')
report.add_events(events=events, title='Events', sfreq=sfreq, event_id=event_id)
report.save('out_report/report.html', overwrite=True)

# == CREATE PRODUCT ==
product_items = []
add_info_to_product(product_items, f'Found {len(events)} events')
fig = mne.viz.plot_events(events, sfreq=sfreq, event_id=event_id, show=False)
fig.savefig('out_dir/events_plot.png')
add_image_to_product(product_items, 'Events', filepath='out_dir/events_plot.png')
create_product_json(product_items)
