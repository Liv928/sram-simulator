import os
import time
import configparser as cp
import run_nets as r
from absl import flags
from absl import app

FLAGS = flags.FLAGS
#name of flag | default | explanation
flags.DEFINE_string("arch_config","./configs/9_wmau.cfg","file where we are getting our architechture from")
flags.DEFINE_string("network","./topologies/vgg16.csv","topology that we are reading")


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
        ## The number of DBCells per DBWMU
        dbwmu_w = config.get(arch_sec, 'DBWMUWidth').split(',')
        self.dbwmu_w = dbwmu_w[0].strip()
        print("dbwmu: " + self.dbwmu_w)
        
        ## The number of DBWMU per WMAU
        dbwmu_per_wmau = config.get(arch_sec, 'DBWMUPerWMAU').split(',')
        self.dbwmu_per_wmau = dbwmu_per_wmau[0].strip()
        print("dbwmu_per_wmau: " + self.dbwmu_per_wmau)

        ## The number of WMAU per Macro
        num_wmau = config.get(arch_sec, 'NumOfWMAU').split(',')
        self.num_wmau = num_wmau[0].strip()
        print("num_wmau: " + self.num_wmau)

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
        print("******************* SCALE SIM **********************")
        print("====================================================")
        print("DBWMU Width: \t" + str(self.dbwmu_w))
        print("DBWMU per WMAU: \t" + str(self.dbwmu_per_wmau))
        print("Number of WMAU: \t" + str(self.num_wmau))
        print("====================================================")

        net_name = self.topology_file.split('/')[-1].split('.')[0]
        print("Net name = " + net_name)

        r.run_net(  dbwmu_w  = int(self.dbwmu_w),
                    dbwmu_per_wmau = int(self.dbwmu_per_wmau),
                    num_wmau = int(self.num_wmau),
                    net_name = net_name,
                    topology_file = self.topology_file   
                )
        print("************ SCALE SIM Run Complete ****************")


def main(argv):
    s = scale()
    s.run_scale()

if __name__ == '__main__':
  app.run(main)

