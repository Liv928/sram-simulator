## Getting Started

### 30 seconds to SRAM simulator!

Getting started is simple! SCALE-Sim is completely written in python. At the moment, it has dependencies on the following python packages. Make sure you have them in your environment.

* os
* subprocess
* math
* configparser
* tqdm


### Custom Experiment

* Fill in the config file, 9_wmau.cfg with proper values. 
* Run the command: ```python scale.py```
* Wait for the run to finish

The config file 9_wmau.cfg contains one section, achitecture presets  
Here is sample of the config file.  
![sample config](https://github.com/Liv928/sram-simulator/blob/main/images/9_wmau.png "sample config")    
Architecture presets are the variable parameters for SCALE-Sim, like array size, memory etc.  
  
The simulator accepts topology csv in the format shown below.  
![vgg16 topology](https://github.com/Liv928/sram-simulator/blob/main/images/vgg16.png "vgg16.csv")

Since this simulator is a CNN simulator please do not provide any layers other than convolutional or fully connected in the csv.
You can take a look at 
[vgg16.csv](https://github.com/Liv928/sram-simulator/blob/mainr/topologies/vgg16.csv)
for your reference.

### Output

Here is an example output dumped to stdout when running vgg16 (whose configuration is in vgg16.csv):
![sample output](https://github.com/Liv928/sram-simulator/blob/main/images/sample_output.png "sample output")



## Detailed Documentation
For detailed insights on using SCALE-Sim, you can refer to this [paper](https://arxiv.org/abs/1811.02883)
