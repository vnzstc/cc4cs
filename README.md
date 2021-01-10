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

### Screenshots
<p align="center">
  <img src="/framework/img/screen2.png">
</p>

###  Installation 
The installation of the framework is accomplished through a few simple steps. All that is required is to install the tools exploited by the framework at each step: Profiling, Simulation, and Static Analysis. For a deeper insight of the commands executed to perform each phase, the user can look at the /framework/cmds.json file.

The framework is implemented in Python3 and uses the csv, os, shutil, subprocess, tkinter libraries for internal operations. Thus, Python3 and the above listed libraries should be installed for the framwork to run properly. 

#### Profiling
The profiling phase requires the execution of [gcc-8](https://gcc.gnu.org/gcc-8/) and [gcov](https://gcc.gnu.org/onlinedocs/gcc/Gcov.html).

#### Static Analysis
This step requires the [frama-c](https://frama-c.com/) software analyzer.

#### Simulation 
The simulation phase involves the execution of the toolchain of each processor supported by the framework. The following is a description of each supported processor and the tools needed to get the information required to calculate CC4CS:

- Atmega328p: 
	- sed: it is needed to convert the instruction set simulator output  to a format readable by the framework parser;
	- **[perf stat](https://man7.org/linux/man-pages/man1/perf-stat.1.html)** : needed to get the clock cycles required by the execution on the Atmega328p;
	- **[simulavr](https://www.nongnu.org/simulavr/)** : the instruction set simulator of the Atmega328p;
	- **[avr-gcc](https://gcc.gnu.org/wiki/avr-gcc)** : the cross-compiler for the AVR ISA;

- Leon3: 
	- **[tsim-leon3](https://www.gaisler.com/index.php/downloads/simulators)** : the instruction set simulator for the LEON3;  
	- **[sparc-gaisler-elf-gcc](https://www.gaisler.com/index.php/downloads/compilers)** : the cross-compiler for the SPARC ISA;

- 8051:
	- **[sdcc](http://sdcc.sourceforge.net/)** : the cross-compiler for the 8051;
	- **[isasim](http://www.newit.gsu.by/resources/CPUs/i8051/VHDL/Synthesizeable%20VHDL%20Model%20of%208051.htm)** : the simulator of the 8051;


For any bug or doubt, it is possible to contact me at: [vincenzo.stoico@graduate.univaq.it](mailto:vincenzo.stoico@graduate.univaq.it)
