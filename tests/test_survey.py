#!/usr/bin/env python
"""
Generic python script.
"""
__author__ = "Alex Drlica-Wagner"

import os
import glob
import json

import numpy as np

from obztak.survey import Survey
from obztak.maglites import MaglitesSurvey
from obztak.bliss import BlissSurvey
from obztak.utils.testing import call, make_options
from obztak.utils import fileio

def test_prepare_windows():
    nights = [['2017/2/21', 'full'],
              ['2017/2/22', 'second'],
              ['2017/2/23', 'first']]

    survey = Survey()
    windows = survey.prepare_windows(nights)

    assert windows['UTC_START'][0] == '2017/02/22 00:29:35'
    assert windows['UTC_END'][0] == '2017/02/22 09:24:12'
    assert windows['UTC_START'][1] == '2017/02/23 05:06:45'
    assert windows['UTC_END'][1] == '2017/02/23 09:25:06'
    assert windows['UTC_START'][2] == '2017/02/24 00:27:14'
    assert windows['UTC_END'][2] == '2017/02/24 04:46:37'

def test_maglites_prepare_fields():
    survey = MaglitesSurvey()
    fields = survey.prepare_fields(plot=False)

    assert len(fields) == 4478

    idx = [17,583,3389]
    test=fields[idx]

    np.testing.assert_equal(test['HEX'],[2042,4947,2207])
    np.testing.assert_equal(test['TILING'],[1,1,4])
    np.testing.assert_allclose(test['RA'],[358.03, 104.729, 342.55892077])
    np.testing.assert_allclose(test['DEC'],[-70.2678, -65.2038, -68.50739044])

def test_survey_prepare():
    kwargs = dict(fields='test_target_fields.csv',windows='test_windows.csv')
    opts = make_options(kwargs)
    cmd = 'survey_prepare %s'%(opts)
    call(cmd,shell=True)

    fields = fileio.csv2rec(kwargs['fields'])
    windows = fileio.csv2rec(kwargs['windows'])

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    args = parser.parse_args()
