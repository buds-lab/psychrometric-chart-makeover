import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import datetime
import seaborn #Seaborn is a a stats plotting library that sits on matplotlib

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import matplotlib.patches as mpatches

#Flask related imports
import io
import base64

#plt.rc('text', usetex=True)
plt.rc('font', family='sanserif')

def plot_psychro(temp_air_init = np.arange(10, 35, .5), 
				RH_psy_init = np.arange(0,100,1)/100, 
				MR = 69.8,
				w=0.06,
				v=.1,
				dep = 0,
				E=0.98):


	#Stephan Botlztmans constant
	o = 0.00000005670367

	Ar_Ad = 0.7

	LR = 16.5
	#define psychrometric temp bounds
	temperature = np.arange(5, 35, 0.1)

	#redefine temp anr RH arrays
	temp_air = np.tile(np.array(temp_air_init),(len(RH_psy_init),1)).transpose()
	RH_psy = np.tile(np.array(RH_psy_init),(len(temp_air_init),1))

	#clausius-clapyron constants
	a=17.08
	b=234.18
	saturation = 1000*0.62198*np.exp(77.345+0.0057*(temperature+273.15)-7235/(temperature+273.15))/(101325*np.power((temperature+273.15),8.2)-np.exp(77.345+0.0057*(temperature+273.15)-7235/(temperature+273.15)))


	#for an arbitrary fixed comfort zone box calculation
	#Mapped everything from relative humidity to absolute humidity
	#BL = Bottom Left ...
	BL = 0.3*1000*0.62198*np.exp(77.345+0.0057*(21+273.15)-7235/(21+273.15))/(101325*np.power((21+273.15),8.2)-np.exp(77.345+0.0057*(21+273.15)-7235/(21+273.15)))
	TL = 0.6*1000*0.62198*np.exp(77.345+0.0057*(21+273.15)-7235/(21+273.15))/(101325*np.power((21+273.15),8.2)-np.exp(77.345+0.0057*(21+273.15)-7235/(21+273.15)))
	BR = 0.3*1000*0.62198*np.exp(77.345+0.0057*(27+273.15)-7235/(27+273.15))/(101325*np.power((27+273.15),8.2)-np.exp(77.345+0.0057*(27+273.15)-7235/(27+273.15)))
	TR = 0.6*1000*0.62198*np.exp(77.345+0.0057*(27+273.15)-7235/(27+273.15))/(101325*np.power((27+273.15),8.2)-np.exp(77.345+0.0057*(27+273.15)-7235/(27+273.15)))
	comfort = np.arange(21, 27, 0.1)

	def f(t):
		return 1000*0.62198*np.exp(77.345+0.0057*(t+273.15)-7235/(t+273.15))/(101325*np.power((t+273.15),8.2)-np.exp(77.345+0.0057*(t+273.15)-7235/(t+273.15)))
	

	#skin temp calculation
	temp_skin = temp_air*.3812+22.406

	#DEFINITIONS

	#vapor pressure of water on skin's surface
	P_sat_skin_psy = np.power(2.718,(77.3450+0.0057*(temp_skin+273.15)-7235/(temp_skin+273.15)))/(np.power((temp_skin+273.15),8.2))/1000
	dim1 = len(RH_psy)
	dim2 = len(temp_air)
	P_sat_air_psy = np.zeros((dim2, dim1))
	Q_conv_free_psy = np.zeros((dim2, dim1))
	Q_evap_free_psy = np.zeros((dim2, dim1))
	T_MRT_psy = np.zeros((dim2, dim1))
	Q_conv_forced_psy = np.zeros((dim2, dim1))
	Q_evap_forced_psy = np.zeros((dim2, dim1))
	T_MRT_forced_psy = np.zeros((dim2, dim1))
	psy_sat = np.zeros((dim2, dim1))
	temp_MRT = temp_air - dep
	Q_rad_forced_v = np.zeros((dim2, dim1)) 
	v_forced_v = np.zeros((dim2, dim1))


	P_sat_air_psy = np.power(2.718,(77.3450+0.0057*(temp_air+273.15)-7235/(temp_air+273.15)))/(np.power((temp_air+273.15),8.2))/1000*RH_psy
	h_c_free_psy = 0.78*np.power(np.absolute(temp_skin-temp_air),0.56)
	Q_conv_free_psy = h_c_free_psy*(temp_skin-temp_air)    
	h_e_free_psy = h_c_free_psy*LR
	Q_evap_free_psy = h_e_free_psy*w*(P_sat_skin_psy-P_sat_air_psy)
	T_MRT_psy = np.power(np.power((temp_skin+273.15),4)-((MR-Q_evap_free_psy-Q_conv_free_psy)/E/o/Ar_Ad),0.25)-273.15
	h_c_forced_psy = 10.1*np.power(v,0.61)
	Q_conv_forced_psy = h_c_forced_psy*(temp_skin-temp_air)      
	h_e_forced_psy = h_c_forced_psy*LR
	Q_evap_forced_psy = h_e_forced_psy*w*(P_sat_skin_psy-P_sat_air_psy)
	T_MRT_forced_psy = np.power(np.power((temp_skin+273.15),4)-((MR-Q_evap_forced_psy-Q_conv_forced_psy)/E/o/Ar_Ad),0.25)-273.15
	psy_sat = 1000*0.62198*np.exp(77.345+0.0057*(temp_air+273.15)-7235/(temp_air+273.15))/(101325*np.power((temp_air+273.15),8.2)-np.exp(77.345+0.0057*(temp_air+273.15)-7235/(temp_air+273.15)))*RH_psy
	h_r_forced_v = 4*E*o*Ar_Ad*np.power((273.15+(temp_skin+temp_MRT)/2),3)
	Q_rad_forced_v = h_r_forced_v*E*(temp_skin-temp_MRT)
	v_forced_v = np.power(((MR-Q_rad_forced_v)/(10.1*(LR*w*(P_sat_skin_psy-P_sat_air_psy)+(temp_skin-temp_air)))),(1/0.61))

	#print(T_MRT_forced_psy)
			

	#Define flask image
	img = io.BytesIO()

	#print T_MRT_psy
	plt.figure(figsize=(15,10))
	X,Y = np.meshgrid(RH_psy_init, temp_air_init)


	textsize = 20

	a=17.08
	b=234.18
	saturation_psy = 1000*0.62198*np.exp(77.345+0.0057*(temp_air+273.15)-7235/(temp_air+273.15))/(101325*np.power((temp_air+273.15),8.2)-np.exp(77.345+0.0057*(temp_air+273.15)-7235/(temp_air+273.15)))

	alph = 0.6
	plt.plot(temperature, saturation, 'k-', linewidth = 1, alpha = 1)
	plt.plot(temperature, saturation*.9, 'k-', linewidth = 1 , alpha = alph)
	plt.plot(temperature, saturation*.8, 'k-', linewidth = 1, alpha = alph)
	plt.plot(temperature, saturation*.7, 'k-', linewidth = 1,alpha = alph)
	plt.plot(temperature, saturation*.6, 'k-', linewidth = 1,alpha = alph)
	plt.plot(temperature, saturation*.5, 'k-', linewidth = 1,alpha = alph)
	plt.plot(temperature, saturation*.4, 'k-', linewidth = 1,alpha = alph)
	plt.plot(temperature, saturation*.3, 'k-', linewidth = 1,alpha = alph)
	plt.plot(temperature, saturation*.2, 'k-', linewidth = 1,alpha = alph)
	plt.plot(temperature, saturation*.1, 'k-', linewidth = 1,alpha = alph)

	if dep != 0:

		levels_contour = np.linspace(0.1, 2, 150)
		CS3=plt.contourf(Y, psy_sat, v_forced_v, cmap = 'jet', levels=levels_contour,interpolation='sinc', fontsize = 20, dpi = 1200, alpha = 0.6)
		cbar = plt.colorbar(CS3, orientation='vertical', format="%.1f")
		plt.text(38.5,-1.75,"m/s", size=textsize)
	
	elif v < 0.2:
		levels_contour = np.linspace(np.amin(T_MRT_psy), np.amax(T_MRT_psy), 15)
		CS3=plt.contourf(Y, psy_sat, T_MRT_psy, cmap = 'jet', levels=levels_contour,interpolation='sinc', fontsize = 20, dpi = 1200, alpha = 0.6)
		CS = plt.contour(Y, psy_sat, T_MRT_psy, 13, colors='k', alpha = 1)
		plt.clabel(CS, inline=3, fmt='%1.1f', fontsize=textsize)
		cbar = plt.colorbar(CS3, orientation='vertical', format="%.1f")
		plt.text(38.5,-1.75,"MRT $^\circ$C", size=textsize)
	else:
		#Forced Convection Plots. 
		levels_contour = np.linspace(np.amin(T_MRT_forced_psy), np.amax(T_MRT_forced_psy), 15)
		CS3=plt.contourf(Y, psy_sat, T_MRT_forced_psy, cmap = 'jet', levels=levels_contour,interpolation='sinc', fontsize = 20, dpi = 1200, alpha = 0.6)
		CS = plt.contour(Y, psy_sat, T_MRT_forced_psy, 20, colors='k', alpha = 1)
		plt.clabel(CS, inline=3, fmt='%1.1f', fontsize=textsize)
		cbar = plt.colorbar(CS3, orientation='vertical', format="%.1f")
		plt.text(38.5,-1.75,"MRT $^\circ$C", size=textsize)

	plt.text(35.5, 2.7, '10%',size=textsize)
	plt.text(35.5, 6.8, '20%',size=textsize)
	plt.text(35.5, 10.5, '30%',size=textsize)
	plt.text(35.5, 14.1, '40%',size=textsize)
	plt.text(35.5, 18, '50%',size=textsize)
	plt.text(35.5, 21.5, '60%',size=textsize)
	plt.text(35.5, 25.2, '70%',size=textsize)
	plt.text(34, 28.1, '80%',size=textsize)
	plt.text(30.8, 28.1, '90%',size=textsize)
	plt.text(27, 27, '100%',size=textsize)


	plt.xlabel("Air Temperature $^\circ$C", size=textsize)
	plt.ylabel("Humidity Ratio (g water/kg dry air)",size=textsize)

	axes=plt.gca()
	axes.set_ylim([0,28])


	plt.tick_params(axis='both', labelsize=textsize)
	cbar.ax.tick_params(labelsize=textsize) 

	plt.savefig(img, format='png')
	img.seek(0)
	graph_url = base64.b64encode(img.getvalue()).decode()
	img=0 #I think I need to do this to prevent the memory from overflowing
	#plt.show()
	plt.close()
	return 'data:image/png;base64,{}'.format(graph_url), T_MRT_forced_psy




if __name__ == '__main__':
	plot_psychro()
