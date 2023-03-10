# Features and limitations

In this section we will take a closer look at the basic concepts that are used in Wiredflow. 
It is known fact that each approach is likely to have advantages and disadvantages. We are here to investigate them.

NB: It is worth noting that the restrictions described below (mostly related to scalability) can be overcome by dividing the 
service into several smaller ones (perform tokenization). However, tokenization, while an effective 
way to scale, can make service management much more difficult. If you want to know more about concept of tokenization,
follow this [link](./scalability_tokenization.md). Or [implementation with remote launches](scalability_remote.md) can be applied to solve efficiency and scalability issues.

## Each pipeline in individual thread

TODO add picture 

We should start the discussion with a fundamental concept: "all pipelines in wiredflow run in separate threads".
This means that if there are defined 30 pipelines in `Flow` (e.g. Service), the Python interpreter will use the `threading` module and run 30 threads.
It is worth noting that threads in Python do not run in parallel. 
This means that the interpreter is only computing one thread at a given moment in time.

### Pros

- Architecture with threads allows to effectively involve input and output (IO) operations;
- Launch through threads allows to configure single service with one entry point. This makes it easy to control the execution process. 
It is relatively easy to share messages between threads. This allows all threads to terminate if at least one 
of them crashes with an error (natively supported be the library);
- Load balancing - only one task is calculated at a single time. So the processor will not be as heavily utilized as 
it could have been if the processes used 

### Cons

- Threads in Python will slow computationally intensive tasks (which would be better executed using the processes). 
So it won't be very effective if, for example, you fit different machine learning models in pipelines. Сan be resolved through
remote launch usage and through flow tokenization. Check [efficiency issues resolving guide](scalability.md) for more information. 
- Threads sometimes needs synchronization. Wiredflow supports thread synchronization, but if you 
write custom functions and want to synchronize threads, then it is necessary to use a special decorator. This is not complicated, but it is easy just to forget about it

## All pipelines may be in one service

TODO add picture 

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

TODO add picture 

Builder is a highly beneficial software design pattern. It allows to configure both simple linear and complex services in a very flexible way.
However, when the number of parameters in it is pretty large, the amount of code to be written to properly configure the service will be large too.
Wiredflow allows building services based only on Builder.

### Pros

- Provide flexible instrument for service customization. 

### Cons

- Requires code writing. Sometimes, a lot of. On the other hand, sometimes implementing custom logic will require writing a lot 
of specialized code. And then it's better if the tool can natively assimilate it (Wiredflow can).

## Customizations through functions 

TODO add picture 

As it was mentioned in [customization](customization.md) section, any stage of data processing can be set in a custom way. 
For example, if you don't like the default connectors, it is possible to implement own one through a simple Python function. 
Follow [these instructions](customization.md) for more information about how to write custom functions. 

### Pros

- Easy to integrate custom logic into service. There is no need to worry about 
inheritance, abstract methods, and much more. Feel free to organize your custom software solution 
architecture as you want to, but the entry point into service will be as simple as standard Python function. 

### Cons

- Does not allow to keep the state of objects (in contrast to the class usage). 