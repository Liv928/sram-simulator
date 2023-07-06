import os
import subprocess
import math 

def conv_mapping(
                dbwmu_w,
                dbwmu_per_wmau,
                num_wmau,
                ifmap_h,
                ifmap_w,
                filt_h,
                filt_w,
                num_channels,
                num_filters,
                padding,
                strides):
    ofmap_h = ((ifmap_h - filt_h + 2*padding) / strides) + 1
    ofmap_w = ((ifmap_w - filt_w + 2*padding) / strides) + 1

    macro_sz = dbwmu_w * dbwmu_per_wmau * num_wmau * 8

    # calculate the number of rounds
    if num_channels < dbwmu_w :
        num_rounds = ofmap_h * ofmap_w * (num_filters / dbwmu_per_wmau)
    else:
        rounds_per_channel_wise = math.ceil(num_channels / dbwmu_w)
        num_rounds = ofmap_h * ofmap_w * (num_filters / dbwmu_per_wmau) * rounds_per_channel_wise
    print("The numerber of rounds needed: " + str(num_rounds))

    # calculate the number of 9-WMAU SRAM needed
    total_w_bits = filt_h * filt_w * num_channels * num_filters * 8
    num_macro = math.ceil(total_w_bits / macro_sz)
    print("The numerber of 9-WMAU SRAM needed: " + str(num_macro))

    # calculate the 9-WMAU SRAM occupancy
    if num_channels > dbwmu_w:
        sram_ocp = 1
    else:
        sram_ocp = num_channels / dbwmu_w
    print("The DBCells occupancy: " + str(sram_ocp*100) + "%")
    

def linear_mapping(
                dbwmu_w,
                dbwmu_per_wmau,
                num_wmau,
                    ifmap_h,
                    ifmap_w,
                    filt_h,
                    filt_w,
                    num_channels,
                    num_filters,
                    padding,
                    strides):
    total_mac = dbwmu_w * dbwmu_per_wmau * num_wmau
    macro_sz = dbwmu_w * dbwmu_per_wmau * num_wmau * 8

    # calculate the number of rounds needed
    num_rounds = math.ceil(num_channels / total_mac) * num_filters
    print("The numerber of rounds needed: " + str(num_rounds))

    # calculate the number of 9-WMAU SRAM needed
    total_w_bits = num_filters * num_channels * 8
    num_macro = math.ceil(total_w_bits / macro_sz)
    print("The numerber of 9-WMAU SRAM needed: " + str(num_macro))

    # calculate the 9-WMAU SRAM occupancy
    sram_ocp = num_channels / total_mac
    if sram_ocp > 1:
        sram_ocp =1
    sram_ocp = round(sram_ocp,4)
    print("The DBCells occupancy: " + str(sram_ocp*100) + "%")
    
def run_net( dbwmu_w=128,
             dbwmu_per_wmau=4,
             num_wmau=9,
             topology_file = './topologies/vgg16.csv',
             net_name='vgg16'
            ):

    #fname = net_name + ".csv"
    param_file = open(topology_file, 'r')

    # conv
    macro_sz = 8 * dbwmu_w * dbwmu_per_wmau * num_wmau
    # linear
    total_mac = dbwmu_w * dbwmu_per_wmau * num_wmau

    # Used to skip the first line
    # first = True 
    
    for row in param_file:
        """
        if first:
            first = False
            continue
        """    
        elems = row.strip().split(',')
        
        # Do not continue if incomplete line
        if len(elems) < 10:
            continue

        name = elems[0]
        print("")
        print("Commencing run for " + name)

        ifmap_h = int(elems[1])
        ifmap_w = int(elems[2])

        filt_h = int(elems[4])
        filt_w = int(elems[5])

        num_channels = int(elems[3])
        num_filters = int(elems[6])

        padding = int(elems[7])
        strides = int(elems[8])

        is_conv = int(elems[9])

        if is_conv :
            conv_mapping(dbwmu_w, dbwmu_per_wmau, num_wmau, ifmap_h, ifmap_w, filt_h, filt_w, num_channels, num_filters, padding, strides)
        else:
            linear_mapping(dbwmu_w, dbwmu_per_wmau, num_wmau, ifmap_h, ifmap_w, filt_h, filt_w, num_channels, num_filters, padding, strides)

    param_file.close()

#if __name__ == "__main__":
#    sweep_parameter_space_fast()    

