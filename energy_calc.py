import os
import subprocess
import math 

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
    print("energy updated with rewrites")
    ofmap_h = math.floor(((ifmap_h - filt_h + 2*padding) / strides)) + 1
    ofmap_w = math.floor(((ifmap_w - filt_w + 2*padding) / strides)) + 1 

    num_rounds = ofmap_h * ofmap_w
   
    num_writes = math.ceil(num_channels / ary_w) * math.ceil((filt_h * filt_w * num_filters)/ary_h)
  
    conv_ws_latency = num_rounds * num_writes * batch * 2 + num_writes
    conv_ws_energy =  conv_ws_latency * 3.84

    print("conv ws energy: " + str(conv_ws_energy))
    return conv_ws_energy

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

    conv_w = math.floor((math.sqrt(ary_h/batch_per_write) - filt_w)/strides)+1
    conv_h = math.floor((math.sqrt(ary_h/batch_per_write) - filt_h)/strides)+1
    
    num_writes = math.ceil(num_channels / ary_w) * math.ceil(batch/batch_per_write) * (output_sz/ (conv_h*conv_w))

    conv_is_latency = math.ceil(num_channels / ary_w) * output_sz * num_filters * math.ceil(batch/batch_per_write) +num_writes + num_filters
    conv_is_energy = conv_is_latency * 3.84
    
    print("conv is energy: " + str(conv_is_energy))
    return conv_is_energy

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

    num_reads = math.ceil(num_channels / (ary_h*ary_w))

    linear_ws_latency = (num_writes + num_reads) * batch + num_writes
    linear_ws_energy =  linear_ws_latency * 3.84

    print("linear ws energy: " + str(linear_ws_energy))
    return linear_ws_energy

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
    
    num_writes = math.ceil(rows_per_vector * (batch/ary_h))
    
    linear_is_latency = num_writes * num_filters * 2 + num_writes
    linear_is_energy = linear_is_latency * 3.84

    print("linear is energy: " + str(linear_is_energy))
    return linear_is_energy

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

    num_writes =  math.ceil((filt_h*filt_w)/ary_w) * math.ceil(num_filters/ary_h)
    num_rounds = ofmap_h * ofmap_w
    
    depthwise_ws_latency = math.ceil((filt_h*filt_w)/ary_w) * math.ceil(num_filters/ary_h) * num_rounds * batch * 2 + num_writes
    depthwise_ws_energy = depthwise_ws_latency * 3.84
    
    print("depthwise ws energy: " + str(depthwise_ws_energy))
    return depthwise_ws_energy

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

    num_writes = math.ceil((ifmap_h*ifmap_w)/ary_w) * math.ceil((num_channels*batch)/ary_h)
    depthwise_is_latency = math.ceil((ifmap_h*ifmap_w)/ary_w) * math.ceil((num_channels*batch)/ary_h) * ofmap_h *  ofmap_w + num_writes +1
    depthwise_is_energy = depthwise_is_latency * 3.84
    
    print("depthwise is energy: " + str(depthwise_is_energy))
    return depthwise_is_energy

