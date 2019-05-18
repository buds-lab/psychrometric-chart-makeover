
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


# @app.route('/')
# def index(name=None):
#     return render_template('hello.html', name=name)

@app.route('/')
def graphs():
    #These coordinates could be stored in DB

 
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

# @app.route('/plot.png')
# def plot(name=None):
#     #fig = plot_psychro()
#     fig = plot_graph()
#     output = io.BytesIO()
#     FigureCanvas(fig).print_png(output)
#     return Response(output.getvalue(), mimetype='image/png')



# def plot_graph():
#     fig = Figure()
#     axis = fig.add_subplot(1, 1, 1)
#     xs = range(100)
#     ys = [random.randint(1, 50) for x in xs]
#     axis.plot(xs, ys)
#     return fig


# def build_graph():
    # x1 = [0, 1, 2, 3, 4]
    # y1 = [10, 30, 40, 5, 50]
#     img = io.BytesIO()
#     plt.plot(x_coordinates, y_coordinates)
#     plt.savefig(img, format='png')
#     img.seek(0)
#     graph_url = base64.b64encode(img.getvalue()).decode()
#     plt.close()
#     return 'data:image/png;base64,{}'.format(graph_url)





if __name__ == '__main__':
	app.run(port=5000, debug=True)