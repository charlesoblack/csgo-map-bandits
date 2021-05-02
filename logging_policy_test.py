import pandas as pd
import numpy as np
from context_engineering_functions import *
from logging_policy import LoggingPolicy
import os

data_directory = '../data/clean/'
map_pick_context = create_basic_triples(data_directory)

# Compare p(a|x) for LoggingPolicy.get_pa_x(context) to manual calculation.
# Prints "Good" if the probabilities are equal

context_cols = ['de_dust2_is_available', 'de_inferno_is_available',
       'de_mirage_is_available', 'de_nuke_is_available',
       'de_overpass_is_available', 'de_train_is_available',
       'de_vertigo_is_available', 'DecisionTeamId', 'OtherTeamId',
       'DecisionOrder']
full_context = map_pick_context[context_cols]
full_action = map_pick_context['X_Action']

lp = LoggingPolicy(map_pick_context,map_pick_context['X_Action'])

print("\n**********************************\nTest 1: Compare predict_proba to manual calculation for Team ID in the dataset")
context = full_context.loc[100]
full_pa_x = lp.pa_x_dict[context['DecisionTeamId']]
# Calculate probability distributions
from_lp = lp.predict_proba(context)[0]
manual = full_pa_x[0]/(1-full_pa_x[3]-full_pa_x[4])

print("predict_proba: ",from_lp)
print("manual calculation: ",manual)

if from_lp == manual:
    print("Good")
else:
	print("Test Failed")


print("\n**********************************\nTest 2: Compare predict_proba to manual calculation for Team ID NOT in the dataset")

# What error comes up when teamid isn't in lp.pa_x_dict?
context_fake = full_context.loc[100]
# Use fake Team ID
context_fake['DecisionTeamId'] = 123456
full_pa_x = lp.pa_x_dict['default']
manual = full_pa_x[0]/(1-full_pa_x[3]-full_pa_x[4])
from_lp = lp.predict_proba(context_fake)[0]
print("predict_proba: ",from_lp)
print("manual calculation: ",manual)

if from_lp == manual:
    print("Good")
else:
	print("Test Failed")
