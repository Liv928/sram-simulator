import os
import subprocess
import math 
import xlwt
import latency_calc as latency
import energy_calc as energy
import latency_calc_updated as latency_updated
import energy_calc_updated as energy_updated


def run_net(ary_w, ary_h, topology_file):

    net_name = topology_file.split('/')[-1].split('.')[0]
    wfname  = net_name + "_energy_2.xls"

    # create workbook
    workbook = xlwt.Workbook(encoding= 'ascii')
    worksheet = workbook.add_sheet(net_name)
    
    param_file = open(topology_file, 'r')

    row_idx=0
    first = True
    for row in param_file:

        if first:
            first = False
            continue

        col_idx=0
        elems = row.strip().split(',')
        
        # skip if incomplete line
        if len(elems) < 13:
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
        batch = int(elems[10])

        # conv layer
        if is_conv==1:
            ws_calc = energy_updated.conv_ws(ary_w, ary_h, ifmap_h, ifmap_w, filt_h,  filt_w, num_channels, num_filters,padding, strides, batch)
            is_calc = energy_updated.conv_is(ary_w, ary_h, ifmap_h, ifmap_w, filt_h,  filt_w, num_channels, num_filters,padding, strides, batch, 128)
            recon_calc = ws_calc if  ws_calc < is_calc else is_calc
                
            worksheet.write(row_idx, col_idx, ws_calc)
            col_idx+=1
            worksheet.write(row_idx, col_idx, is_calc)
            col_idx+=1
            worksheet.write(row_idx, col_idx, recon_calc)
        # linear layer
        elif is_conv==0:
            ws_calc = energy_updated.linear_ws(ary_w, ary_h, ifmap_h, ifmap_w, filt_h,  filt_w, num_channels, num_filters,padding, strides, batch)
            is_calc = energy_updated.linear_is(ary_w, ary_h, ifmap_h, ifmap_w, filt_h,  filt_w, num_channels, num_filters,padding, strides, batch)
            recon_calc = ws_calc if  ws_calc < is_calc else is_calc

            worksheet.write(row_idx, col_idx, ws_calc)
            col_idx+=1
            worksheet.write(row_idx, col_idx, is_calc)
            col_idx+=1
            worksheet.write(row_idx, col_idx, recon_calc)
        # depthwise
        else:
            ws_calc = energy_updated.depthwise_ws(ary_w, ary_h, ifmap_h, ifmap_w, filt_h,  filt_w, num_channels, num_filters,padding, strides, batch)
            is_calc =  energy_updated.depthwise_is(ary_w, ary_h, ifmap_h, ifmap_w, filt_h,  filt_w, num_channels, num_filters,padding, strides, batch)
            recon_calc = ws_calc if  ws_calc < is_calc else is_calc
               
            worksheet.write(row_idx, col_idx, ws_calc)
            col_idx+=1
            worksheet.write(row_idx, col_idx, is_calc)
            col_idx+=1
            worksheet.write(row_idx, col_idx, recon_calc)
        
        row_idx+=1
       
    workbook.save(wfname)
    param_file.close()


# =============================== calculate for fixed batch size e.g. [1, 16, 64, 256, 1024, 4096] =====================================
def run_net_batchset( ary_w,
             ary_h,
             topology_file
            ):
    #fname = net_name + ".csv"
    net_name = topology_file.split('/')[-1].split('.')[0]
    wfname  = net_name + "_latency.xls"

    # create new workbook
    workbook = xlwt.Workbook(encoding= 'ascii')

    # create new sheet
    worksheet = workbook.add_sheet(net_name)

    row_idx=0
    
    
    batches = [1,4,16,64,256,1024,4096]

    param_file = open(topology_file, 'r')

    # Used to skip the first line
    # first = True 
   
    for row in param_file:
        """
        if first:
            first = False
            continue
        """ 
        col_idx=0
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
       
        for b in batches:
            print("!!calculate for batch size: "+ str(b))
            # convolutional layer
            if is_conv==1:
                ws_latency = latency.conv_ws(ary_w, ary_h, ifmap_h, ifmap_w, filt_h,  filt_w, num_channels, num_filters,padding, strides, b)
                is_latency = latency.conv_is(ary_w, ary_h, ifmap_h, ifmap_w, filt_h,  filt_w, num_channels, num_filters,padding, strides, b, 128)
                recon_latency = ws_latency if  ws_latency < is_latency else is_latency
                
                worksheet.write(row_idx, col_idx, ws_latency)
                col_idx+=1
                worksheet.write(row_idx, col_idx, is_latency)
                col_idx+=1
                worksheet.write(row_idx, col_idx, recon_latency)
            # linear layer
            elif is_conv==0:
                ws_latency = latency.linear_ws(ary_w, ary_h, ifmap_h, ifmap_w, filt_h,  filt_w, num_channels, num_filters,padding, strides, b)
                is_latency = latency.linear_is(ary_w, ary_h, ifmap_h, ifmap_w, filt_h,  filt_w, num_channels, num_filters,padding, strides, b)
                recon_latency = ws_latency if  ws_latency < is_latency else is_latency

                worksheet.write(row_idx, col_idx, ws_latency)
                col_idx+=1
                worksheet.write(row_idx, col_idx, is_latency)
                col_idx+=1
                worksheet.write(row_idx, col_idx, recon_latency)
            # depthwise
            else:
                ws_latency = latency.depthwise_ws(ary_w, ary_h, ifmap_h, ifmap_w, filt_h,  filt_w, num_channels, num_filters,padding, strides, b)
                is_latency =  latency.depthwise_is(ary_w, ary_h, ifmap_h, ifmap_w, filt_h,  filt_w, num_channels, num_filters,padding, strides, b)
                recon_latency = ws_latency if  ws_latency < is_latency else is_latency
               
                worksheet.write(row_idx, col_idx, ws_latency)
                col_idx+=1
                worksheet.write(row_idx, col_idx, is_latency)
                col_idx+=1
                worksheet.write(row_idx, col_idx, recon_latency)
            col_idx+=2
        row_idx +=1

    workbook.save(wfname)
    param_file.close()



