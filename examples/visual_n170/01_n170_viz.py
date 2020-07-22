"""
N170 Load and Visualize Data
===============================

This notebook runs only the data analysis part of N170 notebook.

Look at the notes to see how this can be run on the web with binder or google collab.

All of the additional notes are removed; only the code cells are kept.

"""

###################################################################################################

# Imports
from muselsl import stream, list_muses, view, record
from multiprocessing import Process
from mne import Epochs, find_events
from time import time, strftime, gmtime
import os
#from stimulus_presentation import n170
#from eegnb.experiments.visual_n170 import n170
from eegnb.datasets import datasets
from eegnb.analysis import utils
from collections import OrderedDict
import warnings
warnings.filterwarnings('ignore')

# sphinx_gallery_thumbnail_number = 3

###################################################################################################  
# Skipping these steps 
# ---------------------  
#  
# Step 1: Connect to an EEG Device
# Step 2: Apply the EEG Device and Wait for Signal Quality to Stabilize
# Step 3: Run the Experiment

###################################################################################################
# Load Data
# ---------------------
#
# We will use the
# `MNE sample dataset <https://mne.tools/stable/overview/datasets_index.html?#sample>`_
# which is a combined MEG/EEG recording with an audiovisual task.
#
# First we will load the dataset from MNE, have a quick look at the data,
# and extract the EEG data that we will use for this example.
#
# Note that if you are running this locally, the following cell will download
# the example dataset, if you do not already have it.
#

###################################################################################################

eegnb_data_path = os.path.join(os.path.expanduser('~/'),'.eegnb', 'data')    
n170_data_path = os.path.join(eegnb_data_path, 'visual-N170', 'eegnb_examples')

# If dataset hasn't been downloaded yet, download it 
if not os.path.isdir(n170_data_path):
  datasets.fetch_dataset(data_dir=eegnb_data_path, experiment='visual-N170', site='eegnb_examples')        


subject = 1
session = 1

raw = utils.load_data(n170_data_path, sfreq=256., 
                              subject_nb=subject, session_nb=session)

###################################################################################################
# Visualize the power spectrum
# ----------------------------

#%matplotlib inline
raw.plot_psd()

###################################################################################################
# Filteriing
# ----------------------------

raw.filter(1,30, method='iir')
raw.plot_psd(fmin=1, fmax=30);

###################################################################################################
# Epoching
# ----------------------------

# Create an array containing the timestamps and type of each stimulus (i.e. face or house)
events = find_events(raw)
event_id = {'House': 1, 'Face': 2}

# Create an MNE Epochs object representing all the epochs around stimulus presentation
epochs = Epochs(raw, events=events, event_id=event_id, 
                        tmin=-0.1, tmax=0.8, baseline=None,
                                        reject={'eeg': 75e-6}, preload=True, 
                                                        verbose=False, picks=[0,1,2,3])
print('sample drop %: ', (1 - len(epochs.events)/len(events)) * 100)
epochs

###################################################################################################
# Epoch average
# ----------------------------

#%matplotlib inline
conditions = OrderedDict()
conditions['House'] = [1]
conditions['Face'] = [2]

fig, ax = utils.plot_conditions(epochs, conditions=conditions, 
                                        ci=97.5, n_boot=1000, title='',
                                                                        diff_waveform=(1, 2))

###################################################################################################
# Conclusions
# ----------------------------

# Blah

