
#Web framework related imports
from flask import Flask, request, render_template
from flask import Response
import io

#Calculation related imports
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

#Import user defined modules
#from calculate_chart import plot_psychro
from calculate_chart import plot_psychro

#To be reviewed and deleted prior to release
import random
import base64
matplotlib.use('agg')

app = Flask(__name__)


@app.route('/')
def graphs():
    graph1_url = plot_psychro();
 
    return render_template('graphs.html', graph1=graph1_url)

@app.route('/', methods=['POST'])
def my_form_post():
    MR = request.form['mr']

    MR = float(MR)
    print("number taken and converted to float")
    print(MR)
    graph1_url = plot_psychro(MR = MR);
    return render_template('graphs.html', graph1=graph1_url)


if __name__ == '__main__':
	app.run(port=5000, debug=True)