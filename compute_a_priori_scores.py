# -*- coding: utf-8 -*-
# @author: Antoine Allard <antoineallard.info>

# Computes the a priori score (i.e. with no prior information) for each word in the dataset.
# The execution of this code is quite long (each ordered pair of word must be considered).

import pandas
import numpy
from wordle_solver import wordle_solver


ws = wordle_solver()
df = ws.get_compatible_word_scores().reset_index()
with open('data/a_priori_scores.txt', 'w') as ofile:

    header = '# {:4s} {:>8s} {:>8s}\n'.format('Word', 'SumScore', 'AvgScore')
    ofile.write(header)

    fmt_str = '%6s %8d %8.3f'
    numpy.savetxt(ofile, df.values, fmt=fmt_str)