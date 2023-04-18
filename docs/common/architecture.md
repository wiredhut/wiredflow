# Architecture of wiredflow (for developers)

Sometimes, in order to know a tool, it's worth finding out how it's arranged internally. 
This section will help to make sense of it. 
This section was prepared by the developers for developers. 

We have tried to organize the text, diagrams and specifications so that the reader 
can understand the internals of wiredflow as quickly as possible and be able to start modifying the source code.

## How the user sees wiredflow

The user works with wiredflow as a tool for constructing services. That is, 
the framework in this case is considered from the functional point of view.
To construct services, it is necessary to use one of the suggested entities:

<img src="https://raw.githubusercontent.com/wiredhut/wiredflow/main/docs/media/arc_user_view.png" width="900"/>

Thus, the user can compile services with a variety of such blocks.
All the user needs to know - what blocks there are and how they should be configured correctly.
This is the end of the abstractions with which the user interacts.

## How the developer sees wiredflow

Wiredflow uses a classic approach - multi-layer architecture.
A brief description of the abstraction layers and their functions:

- **Builder** - builder pattern. Is used to create services (flows) by sequentially adding stages and pipelines to the flow structure;
  - **Flow** - service with pipelines. Runs pipelines in threads or processes;
    - **Pipeline** - storage container for stages. Provides methods to modify its structure;
    - **PipelineTemplate** - transforms a pipeline (defines structures) into an executable object - Action. Action type defined based on stages and their order in the pipeline;
      - **Action** - provides a single interface for launching both individual stages and their sequences. Responsible for the correct sequential execution of the stages;
        - **ProxyStage** - wrapper over the stages, - provides transferring and merging arguments in stages and single interface for invoking different stage implementations; 
        - **Stages** - low-level abstraction, which consists of a single operation (just load data, just transform it or load into database);

- **Scheduler** & **Timer** - internal scheduler and timer, measures the execution time of various tasks and stops execution if the time limit is exceeded. Follow defined scheduling during execution;

Failures managers: 
- **FailuresCheck** (threads) - singleton for sharing messages about errors during execution of a pipelines, when pipelines are running in threads;
- multiprocessing **Manager** (processes) - sharing messages about errors during execution of a pipelines, when pipelines are running in processes;

## Key abstraction layers

<span style="color:orange">In progress</span>

### Pipeline and templates

<span style="color:orange">In progress</span>

### Actions

<span style="color:orange">In progress</span>

### Stages

<span style="color:orange">In progress</span>
