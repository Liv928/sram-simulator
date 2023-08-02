## Getting Started

### 30 seconds to SRAM simulator!

Getting started is simple! SCALE-Sim is completely written in python. At the moment, it has dependencies on the following python packages. Make sure you have them in your environment.

* os
* subprocess
* math
* configparser
* tqdm
* xlwt


### Custom Experiment

* Fill in the config file, config.cfg with proper values. 
* In the run_nets.py file, modify the run_net() function, make sure you are invoking the calculation formulas from the correct files
* In the scale.py file, set the network topology file
* Run the command: ```python scale.py```
* Wait for the run to finish

The config file config.cfg contains one section, achitecture presets  
Here is sample of the config file.  
![sample config](https://github.com/Liv928/sram-simulator/blob/main/images/config.png "sample config")    
Architecture presets are the variable parameters for SCALE-Sim, like array size, memory etc.  
  
The simulator accepts topology csv in the format shown below.  
![vgg16 topology](https://github.com/Liv928/sram-simulator/blob/main/images/vgg16.png "vgg16.csv")

Since this simulator is a CNN simulator please do not provide any layers other than convolutional or fully connected in the csv.
You can take a look at 
[vgg16.csv](https://github.com/Liv928/sram-simulator/blob/mainr/topologies/vgg16.csv)
for your reference.


### Formula files
As shown in the picture, these four files contain the calculation formulas of Latency and Energy. The files 
with "_updated" suffix contain formulas for 2-parallelism calculation.
![formula files](https://github.com/Liv928/sram-simulator/blob/main/images/formula.png "formula file")


