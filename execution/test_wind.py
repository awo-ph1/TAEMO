#!/usr/bin/python3
import scriptgen
# import plutomod
import gridgen

import wind_git.ctts_env_awo.ctts_env as ctts_env
from wind_git.ctts_env_awo.ctts_env.constants import *

import numpy as np
import sys
import getopt
import os
import shutil
import argparse
# import subprocess
import matplotlib.pyplot as plt
import matplotlib


parser=argparse.ArgumentParser(description="Write Job files for mcfost",prog="BrG Wind/Magnetosphere RT File Writer",epilog="End")
parser.add_argument("filename")
parser.add_argument("-m","--macc",help="Stellar mass accretion rate in Msol/yr",required=False,default=1E-6)
parser.add_argument("-ml","--massloss",help="Knigge disk wind mass loss rate in Msol/yr",required=False,default=1E-10)
parser.add_argument("-z","--zcutoff",help="Vertical distance !in au! from the disk midplane at which the wind starts",required=False,default=0)
parser.add_argument("-acc","--accretion",help="Add a magnetosphere to the model",required=False,action="store_true")
parser.add_argument("-show","--showdensity",help="Shows a plot of the system upon execution",required=False,action="store_true")
parser.add_argument("-b","--beta_ma",help="Obliquity of the magnetosphere in deg",required=False,default=0)
parser.add_argument("-dw","--diskwind",help="Add a disk wind to the model",required=False,action="store_true")
parser.add_argument("-wm","--windmodel",help="Give a filename to specify the wind model",required=False,default="sol1143.dat")
parser.add_argument("-wb","--windbeta",help="Knigge disk wind radial velocity exponent",required=False,default=0.5)
parser.add_argument("-ro","--windradiuso",help="Outer radius of the disk wind",required=False,default=5)
parser.add_argument("-wbt","--windbetatemp",help="Temperature exponent of the disk wind",required=False,default=3)
parser.add_argument("-wa","--windalpha",help="Mass loss rate power law per unit area",required=False,default=0.5)
parser.add_argument("-inc","--inclination",help="Inclinations",required=False,default=15)
parser.add_argument("-zoR0","--zoverR0",help="z height scales over R if true",required=False,action="store_true")
parser.add_argument("-tv","--terminalvel",help="Terminal velocity of the wind in units of escape velocity",required=False,default=2)
parser.add_argument("-ri","--windradiusi",help="Inner radius of the disk wind",required=False,default=5)
parser.add_argument("-so","--stelobj",help="Determines the parameters of the star",type=str,required=False,default="HD 190073")
parser.add_argument("-rmo","--magradiuso",help="Outer radius of the magnetosphere",required=False,default=3.9)
parser.add_argument("-rmi","--magradiusi",help="Inner radius of the magnetosphere",required=False,default=3)
parser.add_argument("-tmag","--tempmag",help="Inner radius of the magnetosphere",required=False,default=7e3)
parser.add_argument("-p","--rotperiod",help="Rotational period in days.",required=False,default=25)
parser.add_argument("-fp","--focalpoint",help="Point where field lines converge, distance below the midplane in R*",required=False,default=25)
parser.add_argument("-fov","--fieldofview",help="Field of view in Rstar",required=False,default=25)
parser.add_argument("-pxs","--pixelsize",help="Size in Rstar of the individual pixel",required=False,default=0.03)
parser.add_argument("-ddr","--darkdiskradius",help="Dark disk radius",required=False,default=4)
parser.add_argument("-dd","--darkdisk",help="Add an optically thick midplane.",required=False,action="store_true")
parser.add_argument("-lte","--onlylte",help="LTE Calculations only",required=False,action="store_false")
parser.add_argument("-wt","--wind_transp",help="Wind Transparency",required=False,action="store_true")
parser.add_argument("-at","--acc_transp",help="Accretion Column Transparency",required=False,action="store_true")
parser.add_argument("-az","--azimuth",help="Azimuth angle on a 3D grid",required=False,default=-90)
parser.add_argument("-ms","--mstar",help="Stellar Mass",required=False,default=0.8)
parser.add_argument("-rs","--rstar",help="Stellar Radius",required=False,default=2.5)
parser.add_argument("-ts","--tstar",help="Stellar Temperature",required=False,default=4050)
parser.add_argument("-ps","--pstar",help="Stellar Period (in days)",required=False,default=10)
parser.add_argument("-wtmax","--windtmax",help="Wind temperature (in Kelvin)",required=False,default=1e4)

cl_args=parser.parse_args()

filename=cl_args.filename
acc=cl_args.accretion
disk=cl_args.diskwind
modelfile=cl_args.windmodel
Mdot=float(cl_args.macc)
zcutoff=float(cl_args.zcutoff)
beta_ma=float(cl_args.beta_ma)
show=cl_args.showdensity
distance = 1
MassLoss=float(cl_args.massloss)
wind_beta=float(cl_args.windbeta)
wind_radius_outer=float(cl_args.windradiuso)
windbetatemp=float(cl_args.windbetatemp)
wind_alpha=float(cl_args.windalpha)
incli=float(cl_args.inclination)
zscaling=cl_args.accretion
terminalvel=float(cl_args.terminalvel)
wind_radius_inner=float(cl_args.windradiusi)
stellar_object=cl_args.stelobj
mag_radius_outer=float(cl_args.magradiuso)
mag_radius_inner=float(cl_args.magradiusi)
temp_mag=float(cl_args.tempmag)
wind_zs=float(cl_args.focalpoint)
fov=float(cl_args.fieldofview)
pxs=float(cl_args.pixelsize)
dark_disk=cl_args.darkdisk
nlte_var=cl_args.onlylte
dark_disk_radius=float(cl_args.darkdiskradius)
wind_transp=cl_args.wind_transp
acc_transp=cl_args.acc_transp
az=float(cl_args.azimuth)
stellar_mass=float(cl_args.mstar)
stellar_radius=float(cl_args.rstar)
stellar_temperature=float(cl_args.tstar)
stellar_period=float(cl_args.pstar)
wind_temperature=float(cl_args.windtmax)




is_bb = True

if stellar_object=="RU Lup":
	Mstar = 0.8 #0.6
	Rstar = 2.5 #2.6
	Tstar = 4050 
	#Prot = 3.7 # 5 but actually 3.7!

if stellar_object=="RU Lup2":
	Mstar = 1 #0.6
	Rstar = 2 #2.6
	Tstar = 4050 
	#Prot = 3.7 # 5 but actually 3.7!
	

if stellar_object=="HD 190073":
	Mstar = 5.6 #Msol
	Rstar = 9.8 #Rsol
	Tstar = 9000 #K
	#Prot = 25 #days

if stellar_object=="Custom":
	Mstar = stellar_mass
	Rstar = stellar_radius
	Tstar = stellar_temperature
	Prot = stellar_period





job_description=(filename + ", stellar mass = "+str(Mstar)+" Msol"+", stellar radius = "+ str(Rstar)+" Rsol"+ ", eff. Temp = "+ str(Tstar) +" K"
+ ", rotational period ="+ str(Prot)+ " days" + ", accretion rate = "+str(Mdot)+" Msol/yr || " )
if acc:
	job_description+="Added accreting magnetosphere, tilt = "+str(beta_ma)+" deg || "
if disk:
	job_description+="Added disk wind, model = "+modelfile+", z cutoff = " +str(zcutoff)+ " au || "

#arguments for mcfost on dahu (mostly non-LTE)

args = "+disk_struct -atom -healpix_lorder 1 -max_err 1e-2 -iterate_ne 1 " #healpix_lorder, iterate_ne 1 or 2
args += "-safe_stop -Nrays_mc_step 100 -Ndelay_iterate_ne 4"# -split_image " #Ndelay_iterate_ne 0 to 5


## line transfer ##
nlte = nlte_var
atom_file = ['H_16.atom']
i_trans = [[4]]#[[2,4]]
j_trans = [[7]]#[[3,7]]
ladd_disc=dark_disk#True
## configuration files ##
paraf = filename+".para"

## Star ##
rmo = mag_radius_outer+mag_radius_inner#3.9#Rin * 0.99
rmi = mag_radius_inner#3#rmo*0.6#4.0#rmo - 0.4*rmo
ob_factor=(2 / (2 + np.cos(beta_ma) ** 2)) ** (1 / 3)
rco=1.01*rmo/ob_factor*Rstar*Rsun
#Prot=(2*np.pi*(rco**3/(Ggrav*Mstar*Msun))**(1/2))/(60*60*24)
print("Co-Rot: "+str(rco/(Rstar*Rsun)))
print("Rotation:"+str(Prot))
# star = ctts_env.Star(2.5,0.6,4300,Prot,3000) #Rstar,Mstar,Temperature, Rotation period,Polar Magnetic field - unused
star = ctts_env.Star(Rstar,Mstar,Tstar,Prot,3000) 		
## Magnetosphere ##
#Mdot = 1e-6 #1e-6 Msol/yr
#acc = False
Tring = 0.0; T_preshock = 0.
#beta_ma=0
## grid ##
Nr = 150; Nt = 150; Np = (64,1)[beta_ma == 0]

#wind_radius_inner=rmi*1.1
#wind_radius_outer=5
Rin = wind_radius_inner#5# / star.R_au
Ro = wind_radius_inner+wind_radius_outer#20# / star.R_au #0.3
#Rmax = 1.5*Ro#100 / star.R_au
Rmax = 3*Ro#(Ro, 3*Ro)[ladd_disc]
mapsize = 2* 2.1 * Ro * star.R_au #Physical dimension in au
Rmin = (Rin,1.001)[acc]
T_mag = temp_mag
fov=2*2.1*Ro
px=fov/pxs
## image ##
limage = True #otherwise total flux (not tested)
nx = (1,px)[limage]; ny = nx
vmax = 500 #lines expansion for image
nfreq = 101 #number of velocity points
incl = (incli,incli); Nincl = 1#(5,85); Nincl = 3
Nazim = 1#0
azim_bin = ((360 - 90 + 90))/(Nazim+1 - 1)
azim = (az,az)#(-90,360-90 - azim_bin)
print(azim, azim_bin) #last is 360 - zero. zero is -90 here. 
							  # we remove the bin to the last point because
							  # the last and the zero (first) points are the same!
print("azimuths:", np.linspace(azim[0],azim[1],Nazim))

	
scriptgen.write_oar(filename+".oar",job_description,filename+"s",paraf,args)
mapsize = 4* 2.1 * Ro * star.R_au # ??? Physical dimension in au

scriptgen.write_parafile4_atom(paraf,atom_file,i_trans,j_trans,\
			Nr,Nt,Np,Nrad_in=1,map_size=mapsize,nx=nx,ny=ny,\
			imin=incl[0],imax=incl[-1],nincl=Nincl,amin=azim[0],amax=azim[-1],naz=(1,Nazim)[Np>1],\
			distance=distance,Rmin=10,Rmax=1000,non_lte=nlte,nfreq=nfreq,vmax=vmax,\
			Teff=star.T,Mstar=star.M,Rstar=star.R,is_bb=is_bb,limage=limage)
			
			
r_lim = np.logspace(np.log10(Rmin),np.log10(Rmax), Nr+1)
t_lim = np.zeros((Nt,2*Nt)[Np>1]+1) - 99
t_lim[:Nt+1] = np.linspace(np.pi/2, 0, Nt+1)
if Np>1:#3d
	t_lim[Nt+1:] = -t_lim[:Nt][::-1]# 
# 		t_lim = np.linspace(np.pi/2, (0,-np.pi/2)[Np>1], Nt*(1,2)[Np>1] + 1)
sint_lim = np.sin(t_lim)
p_lim = np.linspace(0, 2*np.pi, (Np+1,1)[Np==1])
		
r, t, phi = gridgen.define_cells_centres(r_lim,sint_lim,p_lim) #-> theta from pi/2 to -pi/2
#r, t, phi = np.meshgrid(np.linspace(Rin, Ro, Nr), np.linspace(0, np.pi, Nt), [0])



gr = ctts_env.Grid(r,t,phi)
if acc:
	#gr.add_mag(star,rmi=rmi,rmo=rmo,Mdot=Mdot,beta=beta_ma,Tmax=T_mag,verbose=True,V0=20) #Tmax=7e3
	gr.add_magnetosphere_v1(star,rmi=rmi,rmo=rmo,Mdot=Mdot,beta=beta_ma,Tmax=T_mag,verbose=False,no_sec=True)
model = '/home/awo/SWS/IDAT/IDATneu/TWHyaExpanded/WindGen/wind_git/wind_models/'+modelfile


#wind_alpha=0.5
#wind_gamma=-0.5

wind_fesc=terminalvel

wind_ls=10
if disk:
	#gr.add_disc_wind(star, Rin=Rin,Rout=Ro,Macc=Mdot,wind_model=model,Tmax=1e4,z_limit=zcutoff/star.R_au)
	gr.add_disc_wind_knigge95(star, Rin=Rin,Rout=Ro,Tmax=wind_temperature,z_limit=zcutoff/star.R_au,Mloss=MassLoss,
			   alpha=wind_alpha,zs=wind_zs,ls=wind_ls,fesc=wind_fesc,beta=wind_beta)#,beta_temp=windbetatemp,scale_as_zoR0=zscaling)


#gr.rho[gr.regions==2]*=10**(1)

if ladd_disc:
	gr.regions[gr.regions==-1] = 0
	gr.add_dark_disc(dark_disk_radius,dwidth=abs(gr.z).min(),Td=0)

if wind_transp:
	gr.regions[gr.regions==2] = 0

if acc_transp:
	gr.regions[gr.regions==1] = 0


fig, ax = plt.subplots()
ax.pcolormesh(gr.x[:,:,0], gr.z[:,:,0], gr.rho[:,:,0])
ax.pcolormesh(gr.x[:,:,Np//2], gr.z[:,:,Np//2], gr.rho[:,:,Np//2])
#ax.colorbar
if show:
	plt.show()
plt.savefig(filename+".png")
gr.z *= star.R_au
gr.R *= star.R_au
gr.r *= star.R_au
job_desc_file=open("./"+filename+".txt","w")
job_desc_file.write(job_description)
job_desc_file.close()
gr._write(filename+".s", Thp=Tring, Tpre_shock=T_preshock,laccretion=acc,rlim_au=[Rmin*star.R_au,Rmax*star.R_au])

print(Mdot)
print(zcutoff)
