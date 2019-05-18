
#Web framework related imports
from flask import Flask
from flask import render_template
from flask import Response
import io

#Calculation related imports
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

#To be reviewed and deleted prior to release
import random

app = Flask(__name__)


@app.route('/')
def index(name=None):
    return render_template('hello.html', name=name)

@app.route('/plot.png')
def plot(name=None):
    fig = plot_graph()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')



def plot_graph():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig




	# results = plotGraph()
	# return render_template('hello.html', name=name, results = results)






# def plotGraph():
# 	plt.figure()
# 	t = np.arange(0.0, 2.0, 0.01)
# 	s = np.sin(2 * np.pi * t)

# 	plt.plot(t, s)

# 	plt.title("test plot")

# 	#for flaskign the plot
# 	figfile = BytesIO()
# 	plt.savefig(figfile, format='png')
# 	figfile.seek(0)  # rewind to beginning of file
# 	figdata_png = figfile.getvalue()  # extract string (stream of bytes)
# 	figdata_png = base64.b64encode(figdata_png) #Convert to base 64. whatever that is

# 	return figdata_png


if __name__ == '__main__':
	app.run(port=5000, debug=True)