# TAEMO
T Tauri Accretion Ejection Models

Short comment, may update this at a later point:

Included in this repository are as of now the wind package (wind_git), a number of python scripts to create the cell grid and to pass on the parameters, and a shell script with which to call the relevant scripts and the mcfost installation (both in the "execution" folder).
The principal workflow here is as follows:


run_modelgrid.sh > test_wind.py > scriptgen.py, gridgen.py, wind_git package

However, in theory only the shell script needs to be executed, the rest should run automatically. You may have to edit the test_wind.py if you want to change attributes of the cell grid or similar things. You only need to edit the package if you want to change the models for MA and wind themselves.
You will have to adjust file paths in at least the run_modelgrid.sh and test_wind.py as they were defined in absolute. I added some basic commentary to the shell script so that the general idea should be understandable. I hope with this and some parsing of the files you will be able to work with it, otherwise send me a message and I will try to explain if I have time. There are some things I do not recall myself in detail unfortunately, especially when it comes to the size of fov/physical size of the region as defined in test_wind.py. I remember that there was a point why I set it to those numbers specifically, but that's it unfortunately.

I also uploaded the model files used in my 2024 paper here: https://mega.nz/folder/VJcERDRI#bNZ6bFb2DEqrdttSsNCf3w
Hopefully it is accessible to you.

The file names include the model paramters, which is not so elegant but useful to navigate large amounts of files on sight. However, you may run into technical issues due to the length of the file names at some point. For example, I could not upload them to my google drive, as the folder names are too long. 
For my purposes it was still ok, but for the future you may want to look into a better solution if you have the time to dedicate to this.

The naming conventions should be apparent from the definition in run_modelgrid.sh. Generally you will find a shorthand for one of the paramters followed by the numerical value used (in units which you can look up in the test_wind.py, although usually they are obvious).
There will be some additional letters to designate the category of the model, but I did not handle this consistently.  You need not worry about it too much at the moment. 
One example:

HybridModel_2 includes 3 files/folders. The first is named "HSMAGDC+TM8600+RMI7+RMO2+MD23e-08+Inc20+RI9.1+RO3+WA0.7+WB0.05+ZC0.02+ML12e-8+FP15+DDR13+OB0+RS2.5+MS0.8+TS4050+PS7+AZ-90+COMP0"

Prefix: HSMAGDC -> In this case it stands for Hybrid model, Strong MAGnetosphere, DeComposition

TM -> Magnetospheric temperature
RMI -> Inner Magnetospheric Radius
RMO -> Outer Magnetospheric Radius
MD -> Mdot, the mass accretion rate
Inc -> Inclination
RI -> Inner Wind Radius (the inconsistency with RMI is for "historical reasons")
RO -> Actually the width of the wind rather than the outer radius (so the true RO is actually RI+RO), again historical reasons
WA -> Alpha parameter of the Knigge wind model
WB -> Beta parameter of the Knigge wind model
ZC -> Z cutoff of the wind, see the paper for explanation
ML -> Mass Loss rate of the wind
FP -> Focal Point distance, see paper
DDR -> Dark Disk Radius, the distance to which the midplane of the midplane of the disk is transparent for the radiative transfer
RS, MS, TS, PS -> Stellar radius, mass, temperature, period
AZ -> Azimuth angle (we use only one inclination and azimuth per file)

Suffix: COMP0, in this case it indicates that the three files are a decomposition. File 0 is the full hybrid model, Files 1 and 2 you get when you turn off the magnetosphere and wind respectively. So one file is the full model, one file is the wind component only, one file is the magnetospheric component only.

I hope this is sufficient to get you started. All the information is in principle there in the files I think, you just may have to dig a bit. If there are questions, feel free to reach out.
