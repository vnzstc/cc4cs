<p align="center">
  <img src="/framework/img/logo.png">
</p>

## Motivation 

During the initial design phases of an embedded system, the ability to support designers using a metric, obtained through a preliminary analysis, is of fundamental importance. Knowing which initial parameters of the embedded system (HW or SW) influence this metric is even more important. The execution time of an embedded software is an important metric to estimate system performance at design time.

The  goal of this project is to  analyze the usefulness and the  meaningfulness  of  an  innovative  performance metric that is concurrently “Off the Shelf”, “HW/SW Unifying”, and  “Statement  Level”. In fact, to overcome existing metrics limitations, the idea is to consider to measure the number of clock cycles needed to a specific  processor to execute a generic C statement. The proposed metric is called CC4CS (Clock Cycles for C Statement) and is defined as the ration between the number of clock cycles and the executed C statements.

## Framework 
A framework has been developed to calculate the metric. It gives the possibility to execute a C function using processors Instruction Set Simulators (ISS). The framework has been developed in Python and includes a simple benchmark composed by 10 well-know algorithms to calculate the value of CC4CS. The source code of the algorithms is contained in /framework/benchmark directory. 
The framework is structured in three modules: the InputsGenerator, Parser, and the CommandsManager. 

The InputsGenerator (semi)automatically generates inputs for a function. The parameters of a function are specified in a json file contained in the same directory of the function. The InputsGenerator reads a range [x; y] that is used to generate the values of the parameters and the number of inputs to be created. Finally, for each function, different data types have been considered (i.e., int8, int16, int32, and float) to analyze the results with respect to the internal  architecture of the considered processor.

The number of executed C statements is obtained by profiling the benchmark functions using the gcov profiler for each generated input. It is worth noting that such a profiling is performed one-shot on the  host platform since it is independent of the target processor technologies. Instead, the clock cycles needed by the target processor technology to execute each function in the benchmark. Depending on the processor technology there is the need for an Instruction Set Simulator (ISS) or an HDL Simulator.

###  Screenshots 

###  Installation 
