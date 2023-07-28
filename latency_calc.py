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
    print("updated with rewrites")
    ofmap_h = math.floor(((ifmap_h - filt_h + 2*padding) / strides)) + 1
    ofmap_w = math.floor(((ifmap_w - filt_w + 2*padding) / strides)) + 1 

    num_rounds = ofmap_h * ofmap_w
   
    num_writes = math.ceil(num_channels / ary_w) * math.ceil((filt_h * filt_w * num_filters)/ary_h)
  
    conv_ws_latency = num_rounds * num_writes * batch + num_writes

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

    conv_w = math.floor((math.sqrt(ary_h/batch_per_write) - filt_w)/strides)+1
    conv_h = math.floor((math.sqrt(ary_h/batch_per_write) - filt_h)/strides)+1
    
    num_writes = math.ceil(num_channels / ary_w) * math.ceil(batch/batch_per_write) * (output_sz/ (conv_h*conv_w))

    conv_is_latency = math.ceil(num_channels / ary_w) * output_sz * num_filters * math.ceil(batch/batch_per_write) +num_writes
  
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

    linear_ws_latency = num_writes * batch + num_writes

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
    
    num_writes = math.ceil(rows_per_vector * (batch/ary_h))
    
    linear_is_latency = num_writes * num_filters + num_writes

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

    num_writes =  math.ceil((filt_h*filt_w)/ary_w) * math.ceil(num_filters/ary_h)
   
    depthwise_ws_latency = math.ceil((filt_h*filt_w)/ary_w) * math.ceil(num_filters/ary_h) * ofmap_h * ofmap_w * batch + num_writes
    
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

    num_writes = math.ceil((ifmap_h*ifmap_w)/ary_w) * math.ceil((num_channels*batch)/ary_h)
    depthwise_is_latency = math.ceil((ifmap_h*ifmap_w)/ary_w) * math.ceil((num_channels*batch)/ary_h) * ofmap_h *  ofmap_w + num_writes
    
    print("depthwise is latency: " + str(depthwise_is_latency))
    return depthwise_is_latency

