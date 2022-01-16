# -*- coding: utf-8 -*-
# @author: Antoine Allard <antoineallard.info>

# Computes the a priori score (i.e. with no prior information) for each word in the dataset.
# The execution of this code is quite long (each ordered pair of word must be considered).

from wordle_solver import wordle_solver


ws = wordle_solver()
words, scores = ws.get_compatible_word_scores()

