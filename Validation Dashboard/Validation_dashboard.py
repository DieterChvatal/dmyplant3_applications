#Version 1.2

from bokeh.io import push_notebook, show, output_notebook, save
from bokeh.plotting import figure, output_file, show
from bokeh.models import LinearAxis, Range1d, HoverTool
from bokeh.layouts import column, row, gridplot, layout
from bokeh.models import ColumnDataSource, Div
from bokeh.models.widgets import Panel, Tabs
import bokeh

from itertools import cycle
import dmyplant2
from dmyplant2.dPlot import bokeh_chart, datastr_to_dict, expand_cylinder, shrink_cylinder, load_pltcfg_from_excel,show_val_stats
import arrow
import pandas as pd
import numpy as np
import math
import traceback
import matplotlib
import sys
import warnings
import logging
import datetime
import pytz
import os

os.chdir(os.path.dirname(sys.argv[0]))
#dir_path = os.path.dirname(os.path.realpath(__file__))

warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)

logging.basicConfig(
    filename='dmyplant.log',
    filemode='w',
    format='%(asctime)s %(levelname)s, %(message)s',
    level=logging.INFO
)
logging.captureWarnings(True)

dmyplant2.cred()
mp = dmyplant2.MyPlant(0)
# from urllib3.exceptions import NewConnectionError
# import urllib
# import socket

try:
    class myEngine(dmyplant2.Engine):
        @ property
        def dash(self):
            _dash = dict()
            _dash['Name'] = self['Name']
            _dash['serialNumber'] = self['serialNumber'] #self.serialNumber
            _dash['Site'] = self['IB Site Name'] #self.get_property('IB Site Name') 
            _dash['Engine ID'] = self['Engine ID'] #self.get_property('Engine ID')
            _dash['Design Number'] = self['Design Number'] #self.get_property('Design Number')
            _dash['Engine Type'] = self['Engine Type'] #self.get_property('Engine Type')
            _dash['Engine Version'] = self['Engine Version'] #self.get_property('Engine Version')
            _dash['Gas type'] = self['Gas Type'] #self.get_property('Gas Type')
            _dash['Country'] = self['Country'] #self.get_property('Country')
            _dash['OPH Engine'] = self['Count_OpHour'] #self.Count_OpHour
            _dash['OPH Validation'] = self['oph_parts'] #self.oph_parts
            _dash['P_nom'] = self.Pmech_nominal
            _dash['BMEP'] = self.BMEP
            _dash['LOC'] = self.get_dataItem(
                'RMD_ListBuffMAvgOilConsume_OilConsumption')
            return _dash

    dval=dmyplant2.Validation.load_def_excel('Input_validation_dashboard.xlsx', 'Engines', mp) #Loading of validation engine data from excel
    vl = dmyplant2.Validation(mp, dval, lengine=myEngine, cui_log=True)
    logging.info('Engine properties loaded')

    vd = dmyplant2.ValidationDashboard('Input_validation_dashboard.xlsx')
    vd.all_code(vl)

except Exception as e:
    print(e)
    if str(e)=="'Engine' object has no attribute 'asset'":
        print ('Possible cause: No internet connection')
    traceback.print_tb(e.__traceback__)
    sys.exit(1)