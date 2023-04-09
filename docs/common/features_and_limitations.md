# Features and limitations

In this section we will take a closer look at the basic concepts that are used in Wiredflow. 
It is known fact that each approach is likely to have advantages and disadvantages. We are here to investigate them.

NB: It is worth noting that the restrictions described below (mostly related to 
scalability) can be overcome by using tips from [Scalability issues page](./scalability.md).

## Brief introduction 

First, a short section on terms. Services in wiredflow are called **Flow** or **Service**. 
A **service** can consist of one or more **pipelines**. 
**Pipelines** can consist of individual operations (**stages**). 

That's it - move on!

## Each pipeline in an individual thread (or process)

<img src="https://raw.githubusercontent.com/wiredhut/wiredflow/main/docs/media/pipeline_thread.png" width="800"/>

NB: Threads and processes are not the same abstractions! Follow the guide below to figure out the difference. 

We should start the discussion with a fundamental concept: "all pipelines in wiredflow run in separate threads (or processes)".
This means that if there are defined 30 pipelines in `Flow` (e.g. Service), the Python interpreter will use the `threading` module and run 30 threads.
It is worth noting that threads in Python do not run in parallel. 
This means that the interpreter is only computing one thread at a given moment in time.

By default, threads are using. If you want the pipelines to be executed in parallel, wiredflow can also run the pipelines in separate processes. 
It might then be reasonable to limit the number of pipelines to the number of CPU cores. 

### Pros

- Architecture with threads allows to effectively involve input and output (IO) operations;
- Launch through threads allows to configure single service with one entry point. This makes it easy to control the execution process. 
It is relatively easy to share messages between threads. This allows all threads to terminate if at least one 
of them crashes with an error (natively supported be the library);
- Load balancing - only one task is calculated at a single time. So the processor will not be as heavily utilized as 
it could have been if the processes used;
- Native ability to use "threads" and "processes" mode.

### Cons

- Threads and processes in Python may slow computationally intensive tasks. 
So it won't be very effective if, for example, you fit different large machine learning models in pipelines. Сan be resolved through
remote launch usage and through flow tokenization. 
  Check [efficiency issues resolving guide](scalability.md) for more information;
- Threads and processes sometimes needs synchronization. Wiredflow supports thread synchronization, but if you 
write custom functions and want to synchronize threads, then it is necessary to use a special decorator (in progress). 
  This is not complicated, but it is easy just to forget about it.

## All pipelines may be in one service

<img src="https://raw.githubusercontent.com/wiredhut/wiredflow/main/docs/media/single_service.png" width="800"/>

As it was mentioned above, using Wiredflow it is possible to configure the whole service (with different pipelines) in one 
python (`.py`) file (entry point). So, all the business logic will be described in one place.

### Pros

- A single entry point significantly simplifies the management of the execution processes;
- Easy to test and deploy. Easy to onboard new developers and integrate into current project because of local development 
process simplicity.

### Cons

- The limited resources of a single virtual machine, on which the service is executed, may not be enough. Сan be resolved through
remote launch usage and through flow tokenization. Check [efficiency issues resolving guide](scalability.md) for more information. 

## Construct service through builder 

<img src="https://raw.githubusercontent.com/wiredhut/wiredflow/main/docs/media/wiredflow_builder.png" width="800"/>

Builder is a highly beneficial software design pattern. It allows to configure both simple linear and complex services in a very flexible way.
However, when the number of parameters in it is pretty large, the amount of code to be written to properly configure the service will be large too.
Wiredflow allows building services based only on Builder.

### Pros

- Provide flexible instrument for service customization. 

### Cons

- Requires code writing. Sometimes, a lot of. On the other hand, sometimes implementing custom logic will require writing a lot 
of specialized code. And then it's better if the tool can natively assimilate it (Wiredflow can).

## Customizations through functions 

<img src="https://raw.githubusercontent.com/wiredhut/wiredflow/main/docs/media/simplicity.png" width="800"/>

As it was mentioned in [customization](customization.md) section, any stage of data processing can be set in a custom way. 
For example, if you don't like the default connectors, it is possible to implement own one through a simple Python function. 
Follow [these instructions](customization.md) for more information about how to write custom functions. 

### Pros

- Easy to integrate custom logic into service. There is no need to worry about 
inheritance, abstract methods, and much more. Feel free to organize your custom software solution 
architecture as you want to, but the entry point into service will be as simple as standard Python function. 

### Cons

- Does not allow to keep the state of objects (in contrast to the class usage). 