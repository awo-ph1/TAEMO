#!/bin/bash
#file_dir="/home/awo/SWS/IDAT/IDATneu/TWHyaExpanded/WindTestFiles/RULupWindMagSeptDDR/Run27/WindKnigge+TM8600+RMI7+RMO2+MD23e-08+Inc20+RI9.1+RO3+WA0.7+WB0.05+ZC0.02+ML12e-08+FP15+DDR13/"
dest_dir="/home/awo/SWS/IDAT/IDATneu/TWHyaExpanded/WindTestFiles/RULupWindMagSeptDDR/WindParamterVari2/"

# The following are fixed parameters that are baseline parameters that will be passed on to the model unless overwritten during the loop. If you don't explicitly redefine one of these values during the loop, the value in this list will be used.
r_mag_in=6
constant=0.1
constant2=1
r_wind_width=6
wbeta=0.05
walpha=0.7
fp=15
zc=0.02
magtemp=8600
obliq=0
inc=20
r_mag_width=1
mloss=1e-08
star_temp=4050
star_radius=2.5
star_mass=0.8
dark_disk_radius=13
macc=23e-08
star_period=7

# Perform addition with bc



# Example for a function that will create the grid files for an individual model and then will run mcfost on it. The function is called during the loops below. It will also generate a log file for the mcfost run.
# As it is written, I don't think this shell script needs to be in a specific place to run, but you may have to experiment. The paths for the files and for mcfost are specific and need to be adjusted for your PC.
# Refer to the test_wind.py script to understand the parameters to call the function. 
Create_files6(){



mkdir -p $dest_dir/$1
cd $dest_dir/$1
echo test_wind.py $1 -rmi $r_mag_in -rmo $r_mag_width -tmag $magtemp -m $macc -b $obliq -inc $inc -so "Custom" -pxs 0.03 -dw -ml $mloss -z $zc -wb $wbeta -ro $r_wind_width -wa $walpha -ri $r_wind_i -fp $fp -ms $star_mass -rs $star_radius -ps $star_period -ts $star_temp -dd -ddr $dark_disk_radius
test_wind.py $1 -rmi $r_mag_in -rmo $r_mag_width -tmag $magtemp -m $macc -b $obliq -inc $inc -so "Custom" -pxs 0.03 -dw -ml $mloss -z $zc -wb $wbeta -ro $r_wind_width -wa $walpha -ri $r_wind_i -fp $fp -ms $star_mass -rs $star_radius -ps $star_period -ts $star_temp -dd -ddr $dark_disk_radius
wait
/home/awo/mcfost/src/./mcfost $1.para +disk_struct -atom -sphere_mesh $1.s -iterate_ne 1 -Nrays_mc_step 1000  | tee $1+Processing24Cores.txt

}

# This is an example for a variant function which will "regrid" an existing model fits without recomputing the non-LTE population files. This is useful if you want to recompute the image for different inclinations, azimuths etc, for which the population does not change. 
# Note that this is assuming you use one model file per inclination, which is what we did for technical reasons. You can also include multiple inclinations in a single model fits from the start, then you will likely not need this.
# test_wind_aztest.py is just a slightly modified version of the regular script which computes a grid with more than one azimuthal point. It also keeps the secondary columns from the magnetspheric accretion region. 
# You could fold that into the regular test_wind.py easily, I was just lazy and needed something quick.
Create_files7(){

cd $file_dir 

model_dir=$file_dir

mkdir -p $dest_dir/$1
cd $dest_dir/$1
echo test_wind_aztest.py $1 -acc -rmi $r_mag_in -rmo $r_mag_width -tmag $magtemp -m $macc -b $obliq -inc $inc -so "Custom" -pxs 0.03  -ml $mloss -z $zc -wb $wbeta -ro $r_wind_width -wa $walpha -ri $r_wind_i -fp $fp -ms $star_mass -rs $star_radius -ps $star_period -ts $star_temp -dd -ddr $dark_disk_radius

test_wind_aztest.py $1 -acc -rmi $r_mag_in -rmo $r_mag_width -tmag $magtemp -m $macc -b $obliq -inc $inc -so "Custom" -pxs 0.03  -ml $mloss -z $zc -wb $wbeta -ro $r_wind_width -wa $walpha -ri $r_wind_i -fp $fp -ms $star_mass -rs $star_radius -ps $star_period -ts $star_temp  -lte
cp $model_dir/H.fits.gz ./
cp $model_dir/ne.fits.gz ./
wait
sed -i 's|0			#initial solution, 0 LTE, 1 old pops|1			#initial solution, 0 LTE, 1 old pops|' $1.para 
wait  
# The idea is that you will copy the H.fits.gz and ne.fits.gz from your reference model to the folder where you save the new model and then replace the "initial solution" line in the model para file so that it uses the existing population files.
/home/awo/mcfost/src/./mcfost $1.para +disk_struct -atom -sphere_mesh $1.s -iterate_ne 1 -Nrays_mc_step 1000 | tee $1+Processing24Cores.txt

}



# This is an example for the way I automated the computation of many model files. The loop will define a queue of function calls at different parameters. In the first example below, only the stellar mass ("star_mass") has more than one parameter value.
# So this loop would compute 2 models, one at 0.6 M_sol and one at 1.2 M_sol with the other parameters as defined below. The units you may have to parse from the test_wind.py where not obvious. Usually it is what you would expect. I think zc (the vertical cutoff of the wind) is in au.
for fp in 15;
do
for dark_disk_radius in 14.5;
do
for mloss in 51e-09;
do
for star_period in 7; 
do
for star_mass in 0.6 1.2;
do
    for r_mag_in in 6;
    do 
        for walpha in 0.4;
        do
            for star_radius in 2.5;
            do 
                for zc in 0.05157;
                do 
                    for star_temp in 4050;
                    do
                        for r_wind_width in 5; 
                        do
                            for wbeta in 0.62;  
                            do
                            r_wind_i=$(echo "$r_mag_in + $r_mag_width + $constant" | bc -l) # This is to tie the inner radius of the wind to the outer radius of the magnetosphere dynamically, so that you dont create overlap of you forget to change one of them.
                            Create_files6 MAG+RLC+TM$magtemp+RMI$r_mag_in+RMO$r_mag_width+MD$macc+Inc$inc+RI$r_wind_i+RO$r_wind_width+WA$walpha+WB$wbeta+ZC$zc+ML$mloss+FP$fp+DDR$dark_disk_radius+OB$obliq+RS$star_radius+MS$star_mass+TS$star_temp+PS$star_period 
                            # Note that this is where the file name convention is defined. All the model parameters are passed to the file/directory name in order to see what model is what at a glance. I do not recall that I had issues with the filename length at any point, but
                            # if you do you could also switch to a running index to designate the model file and then try to store the info in the fits header somehow or just as a txt file inside the folder.
                            done
                        done
                    done
                done
            done
        done
    done 
done
done
done
done
done

# Multiple loops in sequence are for when you want to vary a single parameter from a reference model at a time rather than do a full multidimensional grid. In the examples below, we use the same reference point, but vary the stellar period by two steps. 
# After that the stellar radius, then the temperature. So in total you would compute 8 models rather than 3^4.
for fp in 15;
do
for dark_disk_radius in 14.5;
do
for mloss in 51e-09;
do
for star_period in 3.7 10; 
do
for star_mass in 0.8;
do
    for r_mag_in in 6;
    do 
        for walpha in 0.4;
        do
            for star_radius in 2.5;
            do 
                for zc in 0.05157;
                do 
                    for star_temp in 4050;
                    do
                        for r_wind_width in 5; 
                        do
                            for wbeta in 0.62;  
                            do
                            r_wind_i=$(echo "$r_mag_in + $r_mag_width + $constant" | bc -l)
                            Create_files6 MAG+RLC+TM$magtemp+RMI$r_mag_in+RMO$r_mag_width+MD$macc+Inc$inc+RI$r_wind_i+RO$r_wind_width+WA$walpha+WB$wbeta+ZC$zc+ML$mloss+FP$fp+DDR$dark_disk_radius+OB$obliq+RS$star_radius+MS$star_mass+TS$star_temp+PS$star_period 
                            done
                        done
                    done
                done
            done
        done
    done 
done
done
done
done
done


for fp in 15;
do
for dark_disk_radius in 14.5;
do
for mloss in 51e-09;
do
for star_period in 7; 
do
for star_mass in 0.8;
do
    for r_mag_in in 6;
    do 
        for walpha in 0.4;
        do
            for star_radius in 1.6 2.8;
            do 
                for zc in 0.05157;
                do 
                    for star_temp in 4050;
                    do
                        for r_wind_width in 5; 
                        do
                            for wbeta in 0.62;  
                            do
                            r_wind_i=$(echo "$r_mag_in + $r_mag_width + $constant" | bc -l)
                            Create_files6 MAG+RLC+TM$magtemp+RMI$r_mag_in+RMO$r_mag_width+MD$macc+Inc$inc+RI$r_wind_i+RO$r_wind_width+WA$walpha+WB$wbeta+ZC$zc+ML$mloss+FP$fp+DDR$dark_disk_radius+OB$obliq+RS$star_radius+MS$star_mass+TS$star_temp+PS$star_period 
                            done
                        done
                    done
                done
            done
        done
    done 
done
done
done
done
done


for fp in 15;
do
for dark_disk_radius in 14.5;
do
for mloss in 51e-09;
do
for star_period in 7; 
do
for star_mass in 0.8;
do
    for r_mag_in in 6;
    do 
        for walpha in 0.4;
        do
            for star_radius in 2.5;
            do 
                for zc in 0.05157;
                do 
                    for star_temp in 3850 4250;
                    do
                        for r_wind_width in 5; 
                        do
                            for wbeta in 0.62;  
                            do
                            r_wind_i=$(echo "$r_mag_in + $r_mag_width + $constant" | bc -l)
                            Create_files6 MAG+RLC+TM$magtemp+RMI$r_mag_in+RMO$r_mag_width+MD$macc+Inc$inc+RI$r_wind_i+RO$r_wind_width+WA$walpha+WB$wbeta+ZC$zc+ML$mloss+FP$fp+DDR$dark_disk_radius+OB$obliq+RS$star_radius+MS$star_mass+TS$star_temp+PS$star_period 
                            done
                        done
                    done
                done
            done
        done
    done 
done
done
done
done
done


