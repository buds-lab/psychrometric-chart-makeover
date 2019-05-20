
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





#Define flask name. Note for elastic beanstalk this must be called application, not app
application = Flask(__name__)

#Load Base version of the graph with default values
@application.route('/')
def graphs():
	matplotlib.use('agg') #Matplotlib needs to be in this format for web compatibility
	form_values ={"MR": 69.8, "w": 0.06, "v": 0.1, "Ar_Ad": 0.7, "E": 0.98}
	graph1_url, T_MRT_forced_psy = plot_psychro();
	#graph1_url, x1 = build_graph()
	return render_template('graphs.html', graph1=graph1_url, form_values = form_values)


#Post Method: When someone submits new values
@application.route('/', methods=['POST'])
def my_form_post():
	matplotlib.use('agg') #Matplotlib needs to be in this format for web compatibility
	#Collect data from form submission and convert to floats
	MR = float(request.form['mr'])
	w = float(request.form['w'])
	v = float(request.form['v'])
	Ar_Ad = float(request.form['Ar_Ad'])
	E = float(request.form['E'])

	#Update form values for subsequent render of page
	form_values ={"MR": MR, "w": w, "v": v, "Ar_Ad": Ar_Ad, "E": E}

	#Plot graph with new form values
	graph1_url, T_MRT_forced_psy = plot_psychro(temp_air = np.arange(10, 35, .2), 
				RH_psy = np.arange(0,100,.2)/100, 
				MR = MR,
				w=w,
				v=v,
				Ar_Ad = Ar_Ad,
				E=E);
	#graph1_url, x1 = build_graph() # For AWS debugging
	return render_template('graphs.html', graph1=graph1_url, form_values = form_values)

# A simple plotting function for AWS server side debugging independent of calc_cart.py
def build_graph():
	x1 = [0, 1, 2, 3, 4]
	y1 = [10, 30, 40, 5, 50]
	img = io.BytesIO()
	plt.plot(x1, y1)
	plt.savefig(img, format='png')
	img.seek(0)
	graph_url = base64.b64encode(img.getvalue()).decode()
	img=0 #I think I need to do this to prevent the memory from overflowing
	plt.close()
	return 'data:image/png;base64,{}'.format(graph_url), x1

if __name__ == '__main__':
	#Running the application, both locally and via WSGI
	#Debug must be False in production mode to prevent memeory overloads
	application.run(debug=False)
