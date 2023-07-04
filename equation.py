import math 
from tqdm import tqdm

def get_feature_info(feature):
    in_c = feature.in_channels   # the number of input channels
    in_h = feature.in_h          # the width of the input matrix 
    in_w = feature.in_w          # the height of the input matrix
    k_h = feature.k_h
    k_w = feature. k_w
    out_c = feature.out_channels
    s = feature.stride
    p = feature.padding
    b = feature.batch
    return in_c, in_h, in_w, k_h, k_w, out_c, s, p, b
    

def conv_mapping(feature, sram_config):
   
    in_c, in_h, in_w, k_h, k_w, out_c, s, p, b = get_feature_info(feature)

    out_h = (in_h + 2*p - k_h)/s + 1
    out_w = (in_w + 2*p - k_w)/s + 1

    if (feature.in_channels < 128):
        rounds = out_h * out_w * (out_c/4) * b
    else:
        rounds = out_h * out_w * (out_c/4) * (math.ceil(in_c / 128)) * b

    return rounds


def linear_mapping(feature, sram_config):
    in_c, in_h, in_w, k_h, k_w, out_c, s, p, b = get_feature_info(feature)

    w_size = in_c * out_c         # the size of weight matrix = in_channels * out_channels

    rounds = math.ceil(in_c/4608)*out_c

    return rounds


