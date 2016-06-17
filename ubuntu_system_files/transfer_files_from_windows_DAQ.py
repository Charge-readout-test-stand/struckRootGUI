#!/usr/bin/env python

"""
this script transfers data from the windows DAQ and logs the output to a file in the 
home directory, rsync_log.out

finding the newest file isn't really working, since the open file and the last
closed file have the same timestamp in windows. Should change this to find the
open file based on file name. 
"""

import os
import glob
import commands


#---------------------------------------------------------------
# options:
#---------------------------------------------------------------

exclude_newest = False

# directory on DAQ PC:
#source_dir = "2015_12_02_testing" 
#source_dir = "2015_12_03_testing" 
#source_dir = "2015_12_07_6thLXe" 
#source_dir = "2016_02_26_PMT" 
source_dir = "2016_03_07_7thLXe" 

# directory on linux DAQ:
target_dir = source_dir

# rsync options
options = [ 
    #"-n", # dry run, for debugging...
    #"--exclude=vacuum_HFE_1200VPMT_0Vcath_amplified_2015-12-05_18-04-59.dat", 
    #"--exclude=vacuum*.dat",
    #"--exclude=*thre_*.dat",
    #"--include=*thre_*12-08_09-3*.dat",
    #"--include=*12-08_07-*.dat",
    #"--include=*integrator*.dat",
    #"--include=vacuum*.dat",
    #"--include=PMT_and_charge_Test_InDewar_InHFE_LED_2016*.dat",
    #"--exclude=*.dat",
    #"--bwlimit=1m", # limit bandwidth use
    #"--bwlimit=0.5m", # limit bandwidth use
    "--progress", # print progress
    #"--remove-source-files", # delete from DAQ PC when done
    #"--exclude-from=/home/xenon/rsync_excludes",
    "-avzh", # archive mode, verbose, compression, human readable
    #"-e ssh", # use ssh
    "-e 'ssh -i /home/test-stand/.ssh/id_rsa'", # use ssh
]

# host & file path at target
#target_path = "alexis4@rhel6-64.slac.stanford.edu:/afs/slac.stanford.edu/u/xo/alexis4/test-stand"
target_path = "/home/test-stand/windows_data"

# path on the DAQ PC:
daq_path = "xenon@171.64.56.127:/cygdrive/d/Struck_data"

# log file:
log_file = "/home/test-stand/rsync_log.out"

is_6th_LXe = False
if source_dir == "2015_12_07_6thLXe":
    is_6th_LXe = True

#---------------------------------------------------------------

if exclude_newest:

    # find most recent file:

    path = "%s/%s/*.dat" % (daq_path, source_dir)
    if is_6th_LXe:
        path = "%s/%s/tier0/*.dat" % (daq_path, source_dir) # for 6th LXe
    print "path:", path
    files = glob.glob(path)
    #print "files:"
    #print files



    print files[0]
    newest = max(files, key=os.path.getctime)
    #newest =  os.path.basename(newest)
    print "newest:", newest
    # exclude the newest file (this needs to be at the front of the exclude/include
    # arguments):
    #options.insert(0, "--exclude=%s" % newest)

    files.remove(newest)
    #files.remove("%s/%s" % (path, newest))
    newest = max(files, key=os.path.getctime)
    print "newest:", newest
    # exclude the newest file (this needs to be at the front of the exclude/include
    # arguments):
    #options.insert(0, "--exclude=%s" % newest)


    #for i_file in files:
    #    print "file:", i_file
    #    start_time = i_file


# concatenate options list:
rsync_options = " ".join(options)

# this command is for the testing data, which has no tier0 subdirectory:
cmd = "rsync %(rsync_options)s %(daq_path)s/%(source_dir)s/ %(target_path)s/%(target_dir)s/tier0/ &> %(log_file)s"

# trying to make this work as cron job...
#cmd = "/home/test-stand/ssh_setup.sh; rsync %(rsync_options)s %(daq_path)s/%(source_dir)s/ %(target_path)s/%(target_dir)s/tier0/ &> %(log_file)s"

if is_6th_LXe:
    cmd = "rsync %(rsync_options)s %(daq_path)s/%(source_dir)s/ %(target_path)s/%(target_dir)s/ &> %(log_file)s"
    

# this cmd is for 6th LXe data:
cmd = cmd % {
    "rsync_options": rsync_options,
    "daq_path": daq_path,
    "source_dir": source_dir,
    "target_path": target_path,
    "target_dir": target_dir,
    "log_file": log_file,
}

print "command:"
#print "\n".join(cmd.split(" "))
print cmd
output = commands.getstatusoutput(cmd)
print output[1]
if output[0] != 0: print output[1]

# print the rsync output
cmd = "cat %s" % log_file
output = commands.getstatusoutput(cmd)
if output[0] != 0: print output[1]
print output[1]


