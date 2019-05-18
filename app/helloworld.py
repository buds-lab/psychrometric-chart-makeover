
#Web framework related imports
from flask import Flask, request, render_template
from flask import Response
import io
import base64

#Calculation related imports
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

#Import user defined modules
from calculate_chart import plot_psychro


#Matplotlib needs to be in this format for web compatibility
matplotlib.use('agg')

#Define flask name
app = Flask(__name__)

#Load Base version of the graph with default values
@app.route('/')
def graphs():
    form_values ={"MR": 69.8, "w": 0.06, "v": 0.1, "Ar_Ad": 0.7, "E": 0.98}
    graph1_url = plot_psychro();
    return render_template('graphs.html', graph1=graph1_url, form_values = form_values)


#Post Method: When someone submits new values
@app.route('/', methods=['POST'])
def my_form_post():
    #Collect data from form submission and convert to floats
    MR = float(request.form['mr'])
    w = float(request.form['w'])
    v = float(request.form['v'])
    Ar_Ad = float(request.form['Ar_Ad'])
    E = float(request.form['E'])

    #Update form values for subsequent render of page
    form_values ={"MR": MR, "w": w, "v": v, "Ar_Ad": Ar_Ad, "E": E}

    #Plot graph with new form values
    graph1_url = plot_psychro(temp_air = np.arange(10, 35, .2), 
                RH_psy = np.arange(0,100,.2)/100, 
                MR = MR,
                w=w,
                v=v,
                Ar_Ad = Ar_Ad,
                E=E);
    return render_template('graphs.html', graph1=graph1_url, form_values = form_values)

if __name__ == '__main__':
	app.run(port=5000, debug=True)