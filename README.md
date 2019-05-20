# Design with Comfort:  Enhancing the psychrometric chart with radiation and convection dimensions

A paper submitted by Eric Teitelbaum, Clayton Miller and Forrest Meggers to the journal [Science and Technology for the Built Environment](https://www.ashrae.org/technical-resources/science-and-technology-for-the-built-environment)

## Abstract

This paper presents a makeover of the psychrometric chart using a new color-shading  method  that  allows  the  whole  chart  to  be  considered  comfortablebased on the variation of non-air related comfort parameters such as meanradiant temperature,  air movement,  and the transitional behavior of occu-pants.  These representations allow forthinking outside the thermal comfortboxwith the use of innovative system types and comfort feedback for occu-pants.  The new chart representations are then applied on several real-worldscenario data-sets to illustrate the value in practice.  An open-source repos-itory  is  available  for  other  researchers  to  reproduce  the  charts  and  color-shading for their own projects using Python and the matplotlib visualizationlibrary.



### Run App Locally

1) Pull the repo `git@github.com:buds-lab/psychrometric-chart-makeover.git`, and `cd psychrometric-chart-makeover`

2) Start the virtual environment `source v_env/bin/activate`

3) `cd app`: Here you can find three files, `application.py` runs the flask web server, `calculate_cart.py` is the core calculation script, `templates/graphs.html` is the html template that renders the website.

4) Run the app locally

From the route folder, in terminal, run

`export FLASK_APP=application.py`
`flask run`

You may need to `pip3 install flask` first

The app shoudld be locally hosted at http://127.0.0.1:5000/

### Deploy to AWS

1) Install the Elastic Beanstalk CLI https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3.html

2) Run `eb deploy`

if it doesn't work, check out the wiki, talk to PJ or see the elastic beanstalk-flask documentaiton which is a buit sucky https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-flask.html