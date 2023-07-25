import os
import subprocess
import math 

def tops_calc_wsis(
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
    ofmap_h = ((ifmap_h - filt_h + 2*padding) / strides) + 1 # output matrices 
    ofmap_w = ((ifmap_w - filt_w + 2*padding) / strides) + 1 

    # WS
    num_activated_dbwmu = dbwmu_per_wmau * num_wmau
    if num_channels < dbwmu_w:
        tops_ws = num_activated_dbwmu * num_channels * 2
    else:
        tops_ws = num_activated_dbwmu * dbwmu_w *2
    print("WS tops: " + str(tops_ws))

    # IS
    num_activated_dbwmu = filt_h*filt_w
    if num_channels < dbwmu_w:
        tops_is = num_activated_dbwmu * num_channels * 2
    else:
        tops_is = num_activated_dbwmu * dbwmu_w *2
    print("IS tops: " + str(tops_is))

def tops_calc_config(
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
    ofmap_h = ((ifmap_h - filt_h + 2*padding) / strides) + 1 # output matrices 
    ofmap_w = ((ifmap_w - filt_w + 2*padding) / strides) + 1 

    # num_rounds WS
    if num_channels < dbwmu_w :
        num_rounds_ws = (ofmap_h * ofmap_w / dbwmu_per_wmau) * num_filters
    else:
        rounds_per_channel_wise = math.ceil(num_channels / dbwmu_w)
        num_rounds_ws = ofmap_h * ofmap_w * (num_filters / dbwmu_per_wmau) * rounds_per_channel_wise
    #print("WS num_rounds: " + str(num_rounds_ws))

     # num_rounds IS
    if num_channels <= dbwmu_w :
        num_rounds_is = ofmap_h * ofmap_w * num_filters
    else:
        rounds_per_channel_wise = math.ceil(num_channels / dbwmu_w)
        num_rounds_is = ofmap_h * ofmap_w * num_filters * rounds_per_channel_wise
    #print("IS num_rounds: " + str(num_rounds_is))

    # num DBWMU WS
    total_w = filt_h * filt_w * num_filters
    temp = math.ceil(num_channels / dbwmu_w)
    num_dbwmu_ws = total_w * temp
    #print("WS num_DBWMU: " + str(num_dbwmu_ws))

    # num DBWMU IS
    num_ins = ifmap_h * ifmap_w 
    temp = math.ceil(num_channels / dbwmu_w) 
    num_dbwmu_is = num_ins * temp
    #print("IS num_DBWMU: " + str(num_dbwmu_is))

    ws_eff = num_rounds_ws * num_dbwmu_ws
    is_eff = num_rounds_is * num_dbwmu_is
    compare = ws_eff / is_eff

    if compare<1:
        num_win_per_rounds = math.floor(1024/ (filt_h*filt_w)) 
        num_activated_dbwmu = num_win_per_rounds * filt_h*filt_w
        if num_channels < dbwmu_w:
            tops = num_activated_dbwmu * num_channels * 2
        else:
            tops = num_activated_dbwmu * dbwmu_w *2
    else:
        num_activated_dbwmu = filt_h*filt_w
        if num_channels < dbwmu_w:
            tops = num_activated_dbwmu * num_channels * 2
        else:
            tops = num_activated_dbwmu * dbwmu_w *2
    print("tops: "+str(tops))

def num_rounds_ws_calc(
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
    ofmap_h = ((ifmap_h - filt_h + 2*padding) / strides) + 1 # output matrices 
    ofmap_w = ((ifmap_w - filt_w + 2*padding) / strides) + 1 

    rounds_per_win = math.ceil((filt_h*filt_w)/num_wmau)
    temp = math.ceil(num_channels/dbwmu_w)
    output_per_rounds = dbwmu_per_wmau
    print("rounds_per_win: "+str(rounds_per_win)+" temp: "+str(temp)+" output_per_rounds: "+str(output_per_rounds))
    num_rounds = ((ofmap_h*ofmap_w*num_filters) / output_per_rounds) * rounds_per_win * temp
    print("num rounds: " + str(num_rounds)) 
     
    
def configurable_calc(
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
    
    ofmap_h = ((ifmap_h - filt_h + 2*padding) / strides) + 1 # output matrices 
    ofmap_w = ((ifmap_w - filt_w + 2*padding) / strides) + 1 

    # num_rounds WS
    if num_channels < dbwmu_w :
        num_rounds_ws = (ofmap_h * ofmap_w / dbwmu_per_wmau) * num_filters
    else:
        rounds_per_channel_wise = math.ceil(num_channels / dbwmu_w)
        num_rounds_ws = ofmap_h * ofmap_w * (num_filters / dbwmu_per_wmau) * rounds_per_channel_wise
    #print("WS num_rounds: " + str(num_rounds_ws))

     # num_rounds IS
    if num_channels <= dbwmu_w :
        num_rounds_is = ofmap_h * ofmap_w * num_filters
    else:
        rounds_per_channel_wise = math.ceil(num_channels / dbwmu_w)
        num_rounds_is = ofmap_h * ofmap_w * num_filters * rounds_per_channel_wise
    #print("IS num_rounds: " + str(num_rounds_is))

    # num DBWMU WS
    total_w = filt_h * filt_w * num_filters
    temp = math.ceil(num_channels / dbwmu_w)
    num_dbwmu_ws = total_w * temp
    #print("WS num_DBWMU: " + str(num_dbwmu_ws))

    # num DBWMU IS
    num_ins = ifmap_h * ifmap_w 
    temp = math.ceil(num_channels / dbwmu_w) 
    num_dbwmu_is = num_ins * temp
    #print("IS num_DBWMU: " + str(num_dbwmu_is))

    ws_eff = num_rounds_ws * num_dbwmu_ws
    is_eff = num_rounds_is * num_dbwmu_is
    compare = ws_eff / is_eff
 
   
def mapping_calc(dbwmu_w,
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
    
    ofmap_h = ((ifmap_h - filt_h + 2*padding) / strides) + 1 # output matrices 
    ofmap_w = ((ifmap_w - filt_w + 2*padding) / strides) + 1 

    # num_rounds WS
    if num_channels < dbwmu_w :
        num_rounds_ws = (ofmap_h * ofmap_w / dbwmu_per_wmau) * num_filters
    else:
        rounds_per_channel_wise = math.ceil(num_channels / dbwmu_w)
        num_rounds_ws = ofmap_h * ofmap_w * (num_filters / dbwmu_per_wmau) * rounds_per_channel_wise
    print("WS num_rounds: " + str(num_rounds_ws))

     # num_rounds IS
    if num_channels <= 128 :
        num_rounds_is = ofmap_h * ofmap_w * num_filters
    else:
        rounds_per_channel_wise = math.ceil(num_channels / dbwmu_w)
        num_rounds_is = ofmap_h * ofmap_w * num_filters * rounds_per_channel_wise
    print("IS num_rounds: " + str(num_rounds_is))

    # num DBWMU WS
    total_w = filt_h * filt_w * num_filters
    temp = math.ceil(num_channels / dbwmu_w)
    num_dbwmu_ws = total_w * temp
    print("WS num_DBWMU: " + str(num_dbwmu_ws))

    # num DBWMU IS
    num_ins = ifmap_h * ifmap_w 
    temp = math.ceil(num_channels / dbwmu_w) 
    num_dbwmu_is = num_ins * temp
    print("IS num_DBWMU: " + str(num_dbwmu_is))

def get_num_w(dbwmu_w,
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
    num_weights = filt_h * filt_w * num_channels * num_filters
    print("WS num writes: " + str(num_weights))
    num_inputs = ifmap_h * ifmap_w * num_channels
    print("IS num writes: " + str(num_inputs))


def conv_mapping_is_flex(
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
    print("=== Calculating is mapping for customer config SRAM ===")
    ofmap_h = ((ifmap_h - filt_h + 2*padding) / strides) + 1
    ofmap_w = ((ifmap_w - filt_w + 2*padding) / strides) + 1
    
    # calculate the number of rounds
    if num_channels <= 128 :
        num_rounds = ofmap_h * ofmap_w * num_filters
    else:
        rounds_per_channel_wise = math.ceil(num_channels / dbwmu_w)
        num_rounds = ofmap_h * ofmap_w * num_filters * rounds_per_channel_wise
    print("The number of rounds needed: " + str(num_rounds))

    # calculate the number of DBWMU needed
    num_ins = ifmap_h * ifmap_w
    temp = math.ceil(num_channels / dbwmu_w)
    num_dbwmu = num_ins * temp
    print("The number of DBWMU needed: " + str(num_dbwmu))

    # calculate the 9-WMAU SRAM occupancy
    if num_channels > 128:
        sram_ocp = 1
    else:
        sram_ocp = num_channels / 128
    print("The DBCells utilization: " + str(sram_ocp*100) + "%")

def conv_mapping_ws(dbwmu_w,
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
    print("")
    print("===  Calculating ws mapping for 9-WMAU ===")
    ofmap_h = ((ifmap_h - filt_h + 2*padding) / strides) + 1
    ofmap_w = ((ifmap_w - filt_w + 2*padding) / strides) + 1

    macro_sz = dbwmu_w * dbwmu_per_wmau * num_wmau * 8

    # calculate the number of rounds
    if num_channels < dbwmu_w :
        num_rounds = (ofmap_h * ofmap_w / dbwmu_per_wmau) * num_filters
    else:
        rounds_per_channel_wise = math.ceil(num_channels / dbwmu_w)
        num_rounds = ofmap_h * ofmap_w * (num_filters / dbwmu_per_wmau) * rounds_per_channel_wise
    print("The number of rounds needed: " + str(num_rounds))

    # calculate the number of 9-WMAU SRAM needed
    total_w = filt_h * filt_w * num_filters
    temp = math.ceil(num_channels / dbwmu_w)
    num_dbwmu = total_w * temp
    print("The number of DBWMU needed: " + str(num_dbwmu))

    # calculate the 9-WMAU SRAM occupancy
    if num_channels > dbwmu_w:
        sram_ocp = 1
    else:
        sram_ocp = num_channels / dbwmu_w
    print("The DBCells utilization: " + str(sram_ocp*100) + "%")
    

def linear_mapping_ws(dbwmu_w,
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
             net_name='vgg16',
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
            #get_num_w(dbwmu_w, dbwmu_per_wmau, num_wmau, ifmap_h, ifmap_w, filt_h, filt_w, num_channels, num_filters, padding, strides)
             tops_calc_wsis(dbwmu_w, dbwmu_per_wmau, num_wmau, ifmap_h, ifmap_w, filt_h, filt_w, num_channels, num_filters, padding, strides)

            #linear_mapping_ws(dbwmu_w, dbwmu_per_wmau, num_wmau, ifmap_h, ifmap_w, filt_h, filt_w, num_channels, num_filters, padding, strides)
    
    param_file.close()



