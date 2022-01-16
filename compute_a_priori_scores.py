# -*- coding: utf-8 -*-
# @author: Antoine Allard <antoineallard.info>

# Computes the a priori score (i.e. with no prior information) for each word in the dataset.
# The execution of this code is quite long (each ordered pair of word must be considered).

import pandas
from wordle_solver import wordle_solver


ws = wordle_solver()
df = ws.get_compatible_word_scores()

with open('data/a_priori_scores.txt', 'w') as ofile:

    header = '# {:4s} {:>8s} {:>8s}\n'.format('Word', 'SumScore', 'AvgScore')
    ofile.write(header)

    fmt_str = '%6s %8d %8.3f'
    np.savetxt(ofile, df.values, fmt=fmt_str)