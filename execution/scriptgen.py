"""
	Generate scripts to run a calculation on dahu

"""
wt="48:00:00"
project="spidi1"
cmd='${HOME}/mcfost/src/mcfost'
cmd_dev='${HOME}/dev_mcfost/mcfost/src/mcfost'
mailto="wojtczak@ph1.uni-koeln.de"

MCFOST_UTILS="${HOME}/mcfost/utils/"
MCFOST_INSTALL="${HOME}/mcfost/"

from os import chmod
from stat import S_IRWXU#S_IEXEC
def write_oar(filename,job_name,model,para_file,args):#,total_flx_mode=False):
	"""
		write a .oar file (job administrator) for a given model to be run on dahu cluster.
		Note: the function write strings, not interpretable commands.
			 it writes commands as they are not as they would be with their given values.
	"""
	
	f = open(filename,"w")
	f.write("#!/bin/bash\n")
	f.write("#OAR -l /nodes=1,walltime=%s\n"%wt)
	f.write("#OAR --name %s\n"%job_name)
	f.write("#OAR --project %s\n"%project)
	if mailto:
		f.write("#OAR --notify mail:%s\n"%mailto)
		
	f.write("\n")
	f.write("\n")

	f.write("sim_dir=$(basename $(pwd))\n")
	f.write('command="%s"\n'%cmd)
	#or add option to add /dev_mcfost/ if dev==True
	#uncomment in script to apply
	f.write("##########################################\n")
	f.write('#(DEV) for untested new features and debug\n')
	f.write('#command_dev="%s"\n'%cmd_dev)
	f.write('#command=${command_dev}\n')
	f.write("##########################################\n")
	f.write('parafile="%s"\n'%para_file)
	f.write("\n")
	f.write('args_mc="%s"\n'%args)

	f.write("\n")
	f.write("\n")
	
	f.write('model_ascii="%s"\n'%model)

	f.write("\n")
	f.write("\n")

	## initialize number of cores
	## Number of cores
	f.write('nbcores=`cat $OAR_NODE_FILE|wc -l`\n')
	f.write('echo "nbcores=$nbcores"\n')

	f.write("\n")
	f.write("\n")

	## Start the program
	f.write("ulimit -s unlimited\n")
	f.write('export MCFOST_UTILS="%s"\n'%MCFOST_UTILS)
	f.write('export MCFOST_INSTALL="%s"\n'%MCFOST_INSTALL)
	f.write('export OMP_STACKSIZE=100000M\n')
	f.write('export OMP_NUM_THREADS=$nbcores\n')
	f.write('export MCFOST_NO_DISCLAIMER=1\n')
	#export MCFOST_GIT=1
	f.write('export MCFOST_AUTO_UPDATE=0\n')
	#export MCFOST_NO_XGBOOST=yes
	#f.write('source ~/.nix-profile/compilers_and_libraries_2018/linux/bin/compilervars.sh intel64\n')
	f.write('source /applis/site/nix_nur.sh\n')
	f.write('source ~/.nix-profile/setvars.sh >/dev/null\n')


	f.write("\n")
	f.write("\n")
	
	
	f.write('${command} ${parafile} ${args_mc} -model_ascii -df ${model_ascii}\n')

	f.write("\n")
	f.write("\n")
	
# 	if (flatten_cube):
# 		f.write("${HOME}/./flatten_fitsimage_dahu.py\n")
# 		f.write("\n")
# 		f.write("\n")
		
# 	if total_flx_mode:
# 		f.write('mkdir total_flux\n')
# 		f.write('cd total_flux\n')
# 
# 		f.write('${command} ${parafile} ${args} -model_ascii -df ${model_ascii}\n')		
# 		f.write('cd ..\n')
	
	f.write('cd ..\n')
	f.write('tar -zcf ${sim_dir}.tar.gz ${sim_dir}\n')
	f.write('mv ${sim_dir}.tar.gz ${HOME}/${sim_dir}.tar.gz\n')
	
	f.close()
	chmod(filename,S_IRWXU)#S_IEXEC)

	return
# 		if restart:
# 		
# 		f.write('mkdir old_pops\n')
# 		f.write("cp -rf H.fits.gz ne.fits.gz *.std* old_pops/\n")
# 		f.write("~/clean.zsh\n")
# 		f.write("cp old_pops/H.fits.gz
# 		
# 		f.write("\n"); f.write("\n")
	
def write_parafile4_atom(filename,atomic_file,i_trans,j_trans,Nr,Nt,Np,Nrad_in=1,map_size=1,nx=256,ny=256,imin=0,imax=90,nincl=1,\
	amin=-45,amax=360,naz=1,distance=1.0,Rmin=1,Rmax=10,non_lte=False,nfreq=101,vmax=1000,Teff=4000,Mstar=0.8,Rstar=2.0,is_bb=True,limage=True):
	"""
		write simple .para file necessary to run a calculation with MCFOST's code, 
		for atomic line transfer.
		
		atomic_file = [file]*n_atom
		i_trans = [[i]*n_trans]*n_atom
		j_trans = [[j]*n_trans]*n_atom
		
		TO DO:
			generalisation
	"""
# 	if not hasattr(atomic_file,"__iter__"):
# 		atomic_file = [atomic_file]
	n_atom = len(atomic_file)
	
	f = open(filename,"w")
	
	f.write("4.0\n")
	f.write("\n")
	f.write("#Number of photon packages\n")
	f.write("1.28e5\n")
	f.write("1.28e3\n")
	f.write("1.28e5\n")
	f.write("\n")
	f.write("#wavelength\n")
	f.write("50  0.1 3000.0\n")
	f.write("F F T\n")
	f.write("IMLup.lambda\n")
	f.write("F T\n")
	f.write("\n")
	f.write("#grid\n")
	f.write("2\n")
	f.write("%d %d %d %d\n"%(Nr,Nt,Np,Nrad_in))
	f.write("\n")
	f.write("#Maps\n")
	f.write("%d %d %.3e\n"%(nx,ny,map_size)) # map size in au
	f.write("%lf %lf %d  F\n"%(imin,imax,nincl)) # not linear
	f.write("%lf %lf %d\n"%(amin,amax,naz)) # linear
	f.write("%.6e\n"%(distance)) # pc (impacts absolute flux, not disk to flux ratio)
	f.write("-90.0\n") # PA of model
	f.write("\n")
	f.write("#scattering\n") # disk surface scattering, not available for atomic lines
	f.write("0\n")
	f.write("1\n")
	f.write("\n")
	f.write("symmetries\n") # 
	f.write("F\n")
	f.write("F\n")
	f.write("F\n")
	f.write("\n")
	f.write("#Disc\n") # see doc
	f.write("0     0.50  1.0\n")
	f.write("F\n")
	f.write("F correct_rsub\n")
	f.write("F\n")
	f.write("F  1e-5\n")
	f.write("\n")
	f.write("#number of zone\n")
	f.write("1\n")
	f.write("\n")
	f.write("#Density\n")
	f.write("3\n") #envelope
	f.write("1.e-3    100.\n")
	f.write("0.01  0.025  2\n")
	f.write("%.4e 0.0 %.4e 0.0\n"%(Rmin,Rmax)) # not used
	f.write("1.\n")
	f.write("-0.5  0.0\n")
	f.write("\n")
	f.write("#Dust\n") # Grain properties / species
	f.write("1\n")
	f.write("Mie  1 2  0.0  1.0  0.9\n")
	f.write("Draine_Si_sUV.dat  1.0\n")
	f.write("1\n")
	f.write("0.03  1000.0 3.5 100\n")
	f.write("\n")
	
	f.write("#Molecular RT settings\n") 
	f.write("T T T 15\n")
	f.write("0.2\n")
	f.write("1\n")
	f.write("co@xpol.dat 6\n")
	f.write("1.0 20\n")
	f.write("T 1.e-6 abundance.fits.gz\n")
	f.write("T  3\n")
	f.write("1 2 3\n")
	
	f.write("\n")
	f.write("#Atoms settings / share some informations with molecules\n")
	f.write("%d				#number of atoms\n"%n_atom) #number of atomic models (only hydrogen -> 1)
	for n in range(n_atom):
		f.write("%s			#all levels treated in details\n"%atomic_file[n])
		f.write("%s 		#treated in non-LTE ?\n"%("F","T")[non_lte])
		f.write("0			#initial solution, 0 LTE, 1 old pops\n")
		f.write("%d %d		#vmax (km/s), n_points for ray-traced images\n"%(vmax,nfreq)) #linear
		n_trans = len(i_trans[n]) #number of transitions
		f.write("%s %d		#images (T) or total flux (F) ? Number of lines for images (depends on the model).\n"%(("F","T")[limage],n_trans))
		for i in range(n_trans):
			f.write("%d %d		#upper level -> lower level\n"%(j_trans[n][i],i_trans[n][i])) # Bry 7 - 4, Halpha 3 - 2
		f.write("\n")
	
	f.write("#Star properties\n")
	f.write("1 Number of stars\n")
	f.write("%.3f %.2f %.2f 0.0 0.0 0.0 %s\n"%(Teff,Rstar,Mstar,("F","T")[is_bb])) #Mstar no direct impact, Rstar in Rsol
	f.write("lte4000-3.5.NextGen.fits.gz\n")
	f.write("0.0	2.2  fUV, slope_fUV\n")
	
	f.close()

	return
	
if __name__ == "__main__":
	print("Writing test .para file v4 for atomic transfer")
	atomic_file = ["H_16.atom"]#,"H_20.atom"]
	i_trans = [[4]]#,[2,3]]
	j_trans = [[7]]#,[3,4]]
	Nr = 144
	Nt = 64
	Np = 128
	write_parafile4_atom("test.para",atomic_file,i_trans,j_trans,Nr,Nt,Np,Nrad_in=1,map_size=1,nx=256,ny=256,imin=0,imax=90,nincl=1,\
	amin=-45,amax=360,naz=1,distance=1.0,Rmin=1,Rmax=10,non_lte=False,nfreq=101,vmax=1000,Teff=4000,Mstar=0.8,Rstar=2.0)
	
	print("Writing test .oar file for dahu")
	write_oar("test.oar","toto","toto.s","test.para","-disk_struct")