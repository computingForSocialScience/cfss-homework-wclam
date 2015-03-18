from flask import Flask, render_template, request, redirect, url_for
from downloadscript import *

app = Flask(__name__)

@app.route('/')
def make_index_resp():
    #db.ping()
    # this function just renders templates/index.html when
    # someone goes to http://127.0.0.1:5000/
    return(render_template('index.html'))

#comparison code

from bokeh.plotting import figure, output_file, show
import numpy as np
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html, components
from pandas.stats.api import ols

@app.route("/compare?state=<FIPSCode>&col1=<columnId1>&col2=<columnId2>")
def show_plot(FIPSCode, col1, col2):
     x=col1
     y=col2

     cur = db.cursor()
     cur.execute('''select ____ from _____;''') 

     p = figure(title="___", plot_height =, plot_width=)
     p.line(x,y)
     p.xaxis.axis_label = ""
     p.yaxix.axis_label = ""
     figJS, figDiv = components(p,CDN)

     rendered = render_template('comparison.html', FIPSCode= , col1= , col2= , figJS=figJS, figDiv=figDiv, plotPag=plotPag)
     return(rendered)

if __name__ == '__main__':
    app.debug=True
    app.run()