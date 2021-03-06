from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime


class WeekDaysFiller(object):
    '''Bar Filler to add missing calendar days to trading days'''
    # kickstart value for date comparisons
    lastdt = datetime.datetime.max.toordinal()

    def __init__(self, data, fillclose=False):
        self.fillclose = fillclose
        self.voidbar = [float('Nan')] * data.size()  # init a void bar

    def __call__(self, data):
        '''Empty bars (NaN) or with last close price are added for weekdays with no
        data

        Params:
          - data: the data source to filter/process

        Returns:
          - True (always): bars are removed (even if put back on the stack)

        '''
        dt = data.datetime.dt()  # current date in int format
        lastdt = self.lastdt + 1  # move the last seen data once forward

        while lastdt < dt:  # loop over gap bars
            if datetime.date.fromordinal(lastdt).isoweekday() < 6:  # Mon-Fri
                # Fill in date and add new bar to the stack
                if self.fillclose:
                    self.voidbar = [self.lastclose] * data.size()
                self.voidbar[-1] = float(lastdt) + data.sessionend
                data._add2stack(self.voidbar[:])

            lastdt += 1  # move lastdt forward

        self.lastdt = dt  # keep a record of the last seen date

        self.lastclose = data.close[0]
        data._save2stack(erase=True)  # dt bar to the stack and out of stream
        return True  # bars are on the stack (new and original)
