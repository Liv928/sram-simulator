import os
import time
import configparser as cp
import run_nets as r
from absl import flags
from absl import app


FLAGS = flags.FLAGS
#name of flag | default | explanation
flags.DEFINE_string("arch_config","./configs/hw_config.cfg","file where we are getting our architechture from")
flags.DEFINE_string("network","./topologies/resnet18.csv","topology that we are reading")


class scale:

    def parse_config(self):
        arch_sec = 'architecture_presets'

        # hardware configuration file
        config_filename = FLAGS.arch_config
        print("Using Architechture from ",config_filename)

        # parse the configuration file
        config = cp.ConfigParser()
        config.read(config_filename)

        ## Read the architecture_presets

        ## The number of cells per row
        ary_w = config.get(arch_sec, 'arrayWidth').split(',')
        self.ary_w = ary_w[0].strip()
        
        ## The number of rows per macro
        ary_h = config.get(arch_sec, 'arrayHeight').split(',')
        self.ary_h = ary_h[0].strip()
       

        ## Read network_presets
        ## For now that is just the topology csv filename
        #topology_file = config.get(net_sec, 'TopologyCsvLoc')
        #self.topology_file = topology_file.split('"')[1]     #Config reads the quotes as wells
        self.topology_file= FLAGS.network


    def run_scale(self):
        self.parse_config()
        self.run_once()


    def run_once(self):

        print("====================================================")
        print("******************* SRAM SIM **********************")
        print("====================================================")
        print("Array Width   : \t" + str(self.ary_w))
        print("Array Height  : \t" + str(self.ary_h))
        print("====================================================")

        net_name = self.topology_file.split('/')[-1].split('.')[0]
        print("Net name = " + net_name)
   
        r.run_net(  ary_w = int(self.ary_w),
                    ary_h = int(self.ary_h),
                    topology_file = self.topology_file
                )
        print("************ SRAM SIM Run Complete ****************")


def main(argv):
    s = scale()
    s.run_scale()

if __name__ == '__main__':
  app.run(main)

