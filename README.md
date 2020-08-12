# XPy-50

Data analysis and auto generation of patches for the Roland XP-50 synthesizer.
Very much a Work In Progress, current focus is on data analysis.

## Overview
Inspired by similar work targeting the DX-7 synth, the core idea is to take a
synthesizer that has a powerful sound engine but somewhat unweildly programming 
interface and autogenerate patches for it based on a training set of patches. 

Initial data analysis on training data is [here](src/stats/README.md).
Training data was found [here](https://www.polynominal.com/site/studio/gear/synth/Roland-xp50/Roland-xp50.html).

## TODOs:
- [ ] Parse remainder of params from sysex files
- [ ] Determine how many patches are duplicates of "INIT PATCH" and remove 
- [ ] Add dir for processed data set
- [ ] Data cleaning and augmentation based
- [ ] To/from one-hot functions
- [ ] Actual patch generation!

