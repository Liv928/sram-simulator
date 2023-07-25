import os
import subprocess
import math 
import xlwt


def conv_ws(ary_w,
            ary_h,
            ifmap_h,
            ifmap_w,
            filt_h,
            filt_w,
            num_channels,
            num_filters,
            padding,
            strides,
            batch):
    ofmap_h = math.floor(((ifmap_h - filt_h + 2*padding) / strides)) + 1
    ofmap_w = math.floor(((ifmap_w - filt_w + 2*padding) / strides)) + 1 

    num_rounds = ofmap_h * ofmap_w
   
    num_write = math.ceil(num_channels / ary_w) * math.ceil((filt_h * filt_w * num_filters)/ary_h)
  
    conv_ws_latency = num_rounds * num_write * 2 * batch

    print("conv ws latency: " + str(conv_ws_latency))
    return conv_ws_latency

def conv_is(ary_w,
            ary_h,
            ifmap_h,
            ifmap_w,
            filt_h,
            filt_w,
            num_channels,
            num_filters,
            padding,
            strides,
            batch,
            batch_per_write):
    ofmap_h = math.floor(((ifmap_h - filt_h + 2*padding) / strides)) + 1
    ofmap_w = math.floor(((ifmap_w - filt_w + 2*padding) / strides)) + 1 

    output_sz = ofmap_h * ofmap_w

    conv_is_latency = math.ceil(num_channels / ary_w) * output_sz * num_filters * math.ceil(batch/batch_per_write) + num_filters
  
    print("conv is latency: " + str(conv_is_latency))
    return conv_is_latency

def linear_ws(ary_w,
            ary_h,
            ifmap_h,
            ifmap_w,
            filt_h,
            filt_w,
            num_channels,
            num_filters,
            padding,
            strides,
            batch):
    ofmap_h = math.floor(((ifmap_h - filt_h + 2*padding) / strides)) + 1
    ofmap_w = math.floor(((ifmap_w - filt_w + 2*padding) / strides)) + 1 

    rows_per_vector = math.ceil(num_channels/ary_w)
    num_writes = math.ceil((rows_per_vector * num_filters)/ary_h)
    
    num_input_reads = math.ceil(num_channels/(ary_h*ary_w))

    linear_ws_latency = (num_writes + num_input_reads) * batch

    print("linear ws latency: " + str(linear_ws_latency))
    return linear_ws_latency

def linear_is(ary_w,
            ary_h,
            ifmap_h,
            ifmap_w,
            filt_h,
            filt_w,
            num_channels,
            num_filters,
            padding,
            strides,
            batch):
    ofmap_h = math.floor(((ifmap_h - filt_h + 2*padding) / strides)) + 1
    ofmap_w = math.floor(((ifmap_w - filt_w + 2*padding) / strides)) + 1 

    rows_per_vector = math.ceil(num_channels/ary_w)
    
    num_writes = math.ceil(rows_per_vector*(batch/ary_h))
    
    linear_is_latency = num_writes * num_filters * 2

    print("linear is latency: " + str(linear_is_latency))
    return linear_is_latency

def depthwise_ws(ary_w,
            ary_h,
            ifmap_h,
            ifmap_w,
            filt_h,
            filt_w,
            num_channels,
            num_filters,
            padding,
            strides,
            batch):
    ofmap_h = math.floor(((ifmap_h - filt_h + 2*padding) / strides)) + 1
    ofmap_w = math.floor(((ifmap_w - filt_w + 2*padding) / strides)) + 1 
   
    depthwise_ws_latency = math.ceil((filt_h*filt_w)/ary_w) * math.ceil(num_filters/ary_h) * ofmap_h * ofmap_w * 2 * batch
    
    print("depthwise ws latency: " + str(depthwise_ws_latency))
    return depthwise_ws_latency

def depthwise_is(ary_w,
            ary_h,
            ifmap_h,
            ifmap_w,
            filt_h,
            filt_w,
            num_channels,
            num_filters,
            padding,
            strides,
            batch):
    ofmap_h = math.floor(((ifmap_h - filt_h + 2*padding) / strides)) + 1
    ofmap_w = math.floor(((ifmap_w - filt_w + 2*padding) / strides)) + 1 
    
    depthwise_is_latency = math.ceil((ifmap_h*ifmap_w)/ary_w) * math.ceil((num_channels*batch)/ary_h) * ofmap_h *  ofmap_w + 1
    
    print("depthwise is latency: " + str(depthwise_is_latency))
    return depthwise_is_latency


    
def run_net( ary_w,
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
           
            if is_conv==1:
                ws_latency = conv_ws(ary_w, ary_h, ifmap_h, ifmap_w, filt_h,  filt_w, num_channels, num_filters,padding, strides, b)
                is_latency = conv_is(ary_w, ary_h, ifmap_h, ifmap_w, filt_h,  filt_w, num_channels, num_filters,padding, strides, b, 128)
                recon_latency = ws_latency if  ws_latency < is_latency else is_latency
                
                worksheet.write(row_idx, col_idx, ws_latency)
                col_idx+=1
                worksheet.write(row_idx, col_idx, is_latency)
                col_idx+=1
                worksheet.write(row_idx, col_idx, recon_latency)
            elif is_conv==0:
                ws_latency = linear_ws(ary_w, ary_h, ifmap_h, ifmap_w, filt_h,  filt_w, num_channels, num_filters,padding, strides, b)
                is_latency = linear_is(ary_w, ary_h, ifmap_h, ifmap_w, filt_h,  filt_w, num_channels, num_filters,padding, strides, b)
                recon_latency = ws_latency if  ws_latency < is_latency else is_latency

                worksheet.write(row_idx, col_idx, ws_latency)
                col_idx+=1
                worksheet.write(row_idx, col_idx, is_latency)
                col_idx+=1
                worksheet.write(row_idx, col_idx, recon_latency)
            else:
                ws_latency = depthwise_ws(ary_w, ary_h, ifmap_h, ifmap_w, filt_h,  filt_w, num_channels, num_filters,padding, strides, b)
                is_latency =  depthwise_is(ary_w, ary_h, ifmap_h, ifmap_w, filt_h,  filt_w, num_channels, num_filters,padding, strides, b)
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



