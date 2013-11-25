from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from telemeta.models import *
import datetime, time, calendar, itertools
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_pdf import PdfPages


SECOND = 1
MINUTE = SECOND * 60
HOUR = MINUTE * 60
DAY = HOUR * 24
MONTH = DAY * 30


class Command(BaseCommand):
    help = "export MediaItem revisions vs. dates to a matplotlib PDF file"
    """ info :
    http://www.geophysique.be/2012/06/14/matplotlib-datetimes-tutorial-03-grouping-sparse-data/
    http://matplotlib.org/examples/pylab_examples/date_demo2.html
    http://matplotlib.org/examples/api/date_demo.html
    """

    binning = 7*DAY
    limit_date = datetime.datetime(2011, 6, 30)

    def group(self, di):
        return int(calendar.timegm(di.timetuple()))/self.binning

    def handle(self, *args, **options):
        years    = mdates.YearLocator()
        months    = mdates.MonthLocator(range(1,13), bymonthday=1, interval=3)
        mondays   = mdates.WeekdayLocator(mdates.MONDAY)
        monthsFmt = mdates.DateFormatter("%b '%y")
        yearsFmt = mdates.DateFormatter('%Y')

        revisions = Revision.objects.filter(time__gte=self.limit_date)

        # dates
        list_of_dates = [r.time for r in revisions]
        grouped_dates = [[datetime.datetime(*time.gmtime(d*self.binning)[:6]), len(list(g))] \
                            for d,g in itertools.groupby(list_of_dates, self.group)]
        grouped_dates = zip(*grouped_dates)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot_date(grouped_dates[0], grouped_dates[1] , '-')
        ax.xaxis.set_major_locator(months)
        ax.xaxis.set_major_formatter(monthsFmt)
        ax.xaxis.set_minor_locator(mondays)
        ax.autoscale_view()
        ax.grid(True)
        fig.autofmt_xdate()

        plt.savefig('/tmp/crem-revisions.png')
        plt.savefig('/tmp/crem-revisions.pdf')

        plt.show()

        # means
        revs = np.array(grouped_dates[1])
        print np.mean(revs)

