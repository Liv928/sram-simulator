import os
import subprocess
import math 

def conv_mapping():
    return 0

def linear_mapping():
    return 0

def run_net( dbwmu_w=128,
             dbwmu_per_wmau=4,
             num_wmau=9,
             topology_file = './topologies/vgg16.csv',
             net_name='vgg16'
            ):

    #fname = net_name + ".csv"
    param_file = open(topology_file, 'r')

    # Used to skip the first line
    # first = True 
    
    for row in param_file:
        """
        if first:
            first = False
            continue
        """    
        elems = row.strip().split(',')
        print("row: " + elems[0])
        
        # Do not continue if incomplete line
        if len(elems) < 10:
            continue

        name = elems[0]
        print("")
        print("Commencing run for " + name)

        ifmap_h = int(elems[1])
        ifmap_w = int(elems[2])

        filt_h = int(elems[3])
        filt_w = int(elems[4])

        num_channels = int(elems[5])
        num_filters = int(elems[6])

        padding = int(elems[7])
        strides = int(elems[8])

        is_conv = int(elems[9])

        if is_conv :
            conv_mapping()
        else:
            linear_mapping()

    param_file.close()

#if __name__ == "__main__":
#    sweep_parameter_space_fast()    

