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

def plot_psychro(temp_air = np.arange(10, 35, .2), 
				RH_psy = np.arange(0,100,.2)/100, 
				MR = 69.8,
				w=0.06,
				v=.1,
				Ar_Ad = 0.7,
				E=0.98):


	#Stephan Botlztmans constant
	o = 0.00000005670367

	LR = 16.5
	#define psychrometric temp bounds
	temperature = np.arange(5, 35, 0.1)

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

	#vapor pressure of water on skin's surface
	P_sat_skin_psy = np.power(2.718,(77.3450+0.0057*(temp_skin+273.15)-7235/(temp_skin+273.15)))/(np.power((temp_skin+273.15),8.2))/1000
	P_sat_air_psy = [[0 for x in range(len(RH_psy))] for x in range(len(temp_air))]
	for i in range(len(temp_air)):
		for k in range(len(RH_psy)):
			P_sat_air_psy[i][k] = np.power(2.718,(77.3450+0.0057*(temp_air[i]+273.15)-7235/(temp_air[i]+273.15)))/(np.power((temp_air[i]+273.15),8.2))/1000*RH_psy[k]

	Q_conv_free_psy = [[0 for x in range(len(RH_psy))] for x in range(len(temp_air))]
	for i in range(len(temp_air)):
		for k in range(len(RH_psy)):
			h_c_free_psy = 0.78*np.power(np.absolute(temp_skin[i]-temp_air[i]),0.56)
			Q_conv_free_psy[i][k] = h_c_free_psy*(temp_skin[i]-temp_air[i])
			

	Q_evap_free_psy = [[0 for x in range(len(RH_psy))] for x in range(len(temp_air))]
	for i in range(len(temp_air)):
		for k in range(len(RH_psy)):
			h_c_free_psy = 0.78*np.power(np.absolute(temp_skin[i]-temp_air[i]),0.56)       
			h_e_free_psy = h_c_free_psy*LR
			Q_evap_free_psy[i][k] = h_e_free_psy*w*(P_sat_skin_psy[i]-P_sat_air_psy[i][k])
			
	#print Q_evap_free_psy
			
	T_MRT_psy = [[0 for x in range(len(RH_psy))] for x in range(len(temp_air))]
	for i in range(len(temp_air)):
		for k in range(len(RH_psy)):
			T_MRT_psy[i][k] = np.power(np.power((temp_skin[i]+273.15),4)-((MR-Q_evap_free_psy[i][k]-Q_conv_free_psy[i][k])/E/o/0.7),0.25)-273.15
			
			
	equivalent = [[0 for x in range(len(RH_psy))] for x in range(len(temp_air))]
	for i in range(len(temp_air)):
		for k in range(len(RH_psy)):
			equivalent[i][k] = T_MRT_psy[i][k]-temp_air[i]



	Q_conv_forced_psy = [[0 for x in range(len(RH_psy))] for x in range(len(temp_air))]
	for i in range(len(temp_air)):
		for k in range(len(RH_psy)):
			h_c_forced_psy = 10.1*np.power(v,0.61)
			Q_conv_forced_psy[i][k] = h_c_forced_psy*(temp_skin[i]-temp_air[i])
			
	Q_evap_forced_psy = [[0 for x in range(len(RH_psy))] for x in range(len(temp_air))]
	for i in range(len(temp_air)):
		for k in range(len(RH_psy)):
			h_c_forced_psy = 10.1*np.power(v,0.61)       
			h_e_forced_psy = h_c_forced_psy*LR
			Q_evap_forced_psy[i][k] = h_e_free_psy*w*(P_sat_skin_psy[i]-P_sat_air_psy[i][k])
			
	#print Q_evap_free_psy
			
	T_MRT_forced_psy = [[0 for x in range(len(RH_psy))] for x in range(len(temp_air))]
	for i in range(len(temp_air)):
		for k in range(len(RH_psy)):
			T_MRT_forced_psy[i][k] = np.power(np.power((temp_skin[i]+273.15),4)-((MR-Q_evap_forced_psy[i][k]-Q_conv_forced_psy[i][k])/E/o/0.7),0.25)-273.15
			
			
	equivalent_forced = [[0 for x in range(len(RH_psy))] for x in range(len(temp_air))]
	for i in range(len(temp_air)):
		for k in range(len(RH_psy)):
			equivalent_forced[i][k] = T_MRT_forced_psy[i][k]-temp_air[i]


	psy_sat = [[0 for x in range(len(RH_psy))] for x in range(len(temp_air))]
	for i in range(len(temp_air)):
		for k in range(len(RH_psy)):
			psy_sat[i][k] = f(temp_air[i])*RH_psy[k]
			
	wet_bulb_compare_forced = [[0 for x in range(len(RH_psy))] for x in range(len(temp_air))]
	for i in range(len(temp_air)):
		for k in range(len(RH_psy)):
			wet_bulb_compare_forced[i][k]=(temp_air[i]*np.arctan(0.151977*np.power((RH_psy[k]*100+8.313659),0.5))+np.arctan(temp_air[i]+RH_psy[k]*100)-np.arctan(RH_psy[k]*100-1.676331)+0.00391838*np.power(RH_psy[k]*100,1.5)*np.arctan(0.023101*RH_psy[k]*100)-4.686035)-T_MRT_forced_psy[i][k]

	dew_point_compare_forced = [[0 for x in range(len(RH_psy))] for x in range(len(temp_air))]
	for i in range(len(temp_air)):
		for k in range(len(RH_psy)):
			dew_point_compare_forced[i][k]=243.04*(np.log(RH_psy[k])+((17.625*temp_air[i])/(243.04+temp_air[i])))/(17.625-np.log(RH_psy[k])-((17.625*temp_air[i])/(243.04+temp_air[i])))-T_MRT_forced_psy[i][k]
			
	Q_comp_rat_forced = [[0 for x in range(len(RH_psy))] for x in range(len(temp_air))]
	for i in range(len(temp_air)):
		for k in range(len(RH_psy)):
			Q_comp_rat_forced[i][k] = (E*o*(np.power((temp_skin[i]+273.15),4)-np.power((T_MRT_forced_psy[i][k]+273.15),4)))/(Q_evap_forced_psy[i][k] + Q_conv_forced_psy[i][k])

	#MRT = air temperature - this could be modified later
	temp_MRT = temp_air   


	Q_rad_forced_v = [[0 for x in range(len(RH_psy))] for x in range(len(temp_air))]
	for i in range(len(temp_air)):
		for k in range(len(RH_psy)):
			h_r_forced_v = 4*E*o*Ar_Ad*np.power((273.15+(temp_skin[i]+temp_MRT[i])/2),3)
			Q_rad_forced_v[i][k] = h_r_forced_v*E*(temp_skin[i]-temp_MRT[i])
			

	v_forced_v = [[0 for x in range(len(RH_psy))] for x in range(len(temp_air))]
	for i in range(len(temp_air)):
		for k in range(len(RH_psy)):
			v_forced_v[i][k] = np.power(((MR-Q_rad_forced_v[i][k])/(10.1*(LR*w*(P_sat_skin_psy[i]-P_sat_air_psy[i][k])+(temp_skin[i]-temp_air[i])))),(1/0.61))
			

	#Define flask image
	img = io.BytesIO()

	#print T_MRT_psy
	plt.figure(figsize=(15,10))
	X,Y = np.meshgrid(RH_psy, temp_air)
	levels_one = np.linspace(1,1.01,2)
	levels_half = np.linspace(0.5,0.505,2)
	levels_two = np.linspace(2,2.01,2)
	levels_three = np.linspace(3,3.02,2)
	levels_four = np.linspace(4,4.04,2)
	levels_six = np.linspace(6,6.06,2)

	textsize = 20

	a=17.08
	b=234.18
	saturation_psy = 1000*0.62198*np.exp(77.345+0.0057*(temp_air+273.15)-7235/(temp_air+273.15))/(101325*np.power((temp_air+273.15),8.2)-np.exp(77.345+0.0057*(temp_air+273.15)-7235/(temp_air+273.15)))

	alph = 0.6
	plt.plot(temperature, saturation, 'k-', linewidth = 1, alpha = 1)
	plt.plot(temperature, saturation*.9, 'k-', linewidth = 1 , alpha = 1)
	plt.plot(temperature, saturation*.8, 'k-', linewidth = 1, alpha = alph)
	plt.plot(temperature, saturation*.7, 'k-', linewidth = 1,alpha = alph)
	plt.plot(temperature, saturation*.6, 'k-', linewidth = 1,alpha = alph)
	plt.plot(temperature, saturation*.5, 'k-', linewidth = 1,alpha = alph)
	plt.plot(temperature, saturation*.4, 'k-', linewidth = 1,alpha = alph)
	plt.plot(temperature, saturation*.3, 'k-', linewidth = 1,alpha = alph)
	plt.plot(temperature, saturation*.2, 'k-', linewidth = 1,alpha = alph)
	plt.plot(temperature, saturation*.1, 'k-', linewidth = 1,alpha = 1)

	#Forced Convection Plots. 
	levels_psy_forced = np.linspace(np.amin(T_MRT_forced_psy), np.amax(T_MRT_forced_psy), 15)
	levels_wb_forced = np.linspace(-0.01,0.01,2)
	CS3=plt.contourf(Y, psy_sat, T_MRT_forced_psy, cmap = 'jet', levels=levels_psy_forced,interpolation='sinc', fontsize = 20, dpi = 1200, alpha = 1)
	CS = plt.contour(Y, psy_sat, T_MRT_forced_psy, 20, colors='k', alpha = 1)
	plt.clabel(CS, inline=3, fmt='%1.1f', fontsize=textsize)
	plt.contour(Y, psy_sat, wet_bulb_compare_forced, cmap = 'ocean', levels=levels_wb_forced, interpolation='sinc', fontsize = 20, dpi = 1200)
	plt.contour(Y, psy_sat, equivalent_forced, cmap = 'ocean', levels=levels_wb_forced, interpolation='sinc', fontsize = 20, dpi = 600)
	plt.contour(Y, psy_sat, dew_point_compare_forced, cmap = 'ocean', levels=levels_wb_forced, interpolation='sinc', fontsize = 20, dpi = 600)
	#plt.contourf(Y, psy_sat, Q_comp_rat, cmap = 'ocean', levels=levels_one, interpolation='sinc', fontsize = 20, dpi = 600)
	#plt.contourf(Y, psy_sat, Q_comp_rat, cmap = 'ocean', levels=levels_half, interpolation='sinc', fontsize = 20, dpi = 600)
	#plt.contourf(Y, psy_sat, Q_comp_rat, cmap = 'ocean', levels=levels_two, interpolation='sinc', fontsize = 20, dpi = 600)
	#plt.contourf(Y, psy_sat, Q_comp_rat, cmap = 'ocean', levels=levels_three, interpolation='sinc', fontsize = 20, dpi = 600)
	#plt.contourf(Y, psy_sat, Q_comp_rat, cmap = 'ocean', levels=levels_four, interpolation='sinc', fontsize = 20, dpi = 600)
	#plt.contourf(Y, psy_sat, Q_comp_rat, cmap = 'ocean', levels=levels_six, interpolation='sinc', fontsize = 20, dpi = 600)
	cbar = plt.colorbar(CS3, orientation='vertical', format="%.1f")


	plt.text(35.5, 2.7, '10\%',size=textsize)
	plt.text(35.5, 6.8, '20\%',size=textsize)
	plt.text(35.5, 10.5, '30\%',size=textsize)
	plt.text(35.5, 14.1, '40\%',size=textsize)
	plt.text(35.5, 18, '50\%',size=textsize)
	plt.text(35.5, 21.5, '60\%',size=textsize)
	plt.text(35.5, 25.2, '70\%',size=textsize)
	plt.text(34, 28.1, '80\%',size=textsize)
	plt.text(31.8, 28.1, '90\%',size=textsize)
	plt.text(27, 27, '100\%',size=textsize)



	#plt.text(10, 10.5, 'Q$rad$/Q$conv$ = 0.5')
	#plt.text(16, 12, '1')
	#plt.text(19.5, 15.5, '2')
	#plt.text(22.7, 18.3, '4')

	plt.text(43.5,-1.75,"MRT $^\circ$C", size=textsize)

	#plt.text(21,14,"Dehumidification with", fontsize=textsize)
	#plt.text(22,12.5,"M-Cycle EC", fontsize=textsize)
	#plt.text(20,2,"Wet-bulb EC", fontsize=textsize)
	#plt.text(23.5,8,"M-Cycle EC", fontsize=textsize)

	#plt.title("Forced Convection")
	plt.xlabel("Air Temperature $^\circ$C", size=textsize)
	plt.ylabel("Humidity Ratio (g water/kg dry air)",size=textsize)

	axes=plt.gca()
	axes.set_ylim([0,28])


	plt.tick_params(axis='both', labelsize=textsize)
	cbar.ax.tick_params(labelsize=textsize) 

	plt.savefig(img, format='png')
	img.seek(0)
	graph_url = base64.b64encode(img.getvalue()).decode()

	#plt.show()
	plt.close()
	return 'data:image/png;base64,{}'.format(graph_url), T_MRT_forced_psy




if __name__ == '__main__':
	plot_psychro2()
