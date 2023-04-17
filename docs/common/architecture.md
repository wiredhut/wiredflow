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

<img src="https://raw.githubusercontent.com/wiredhut/wiredflow/main/docs/media/arc_user_view.png" width="800"/>

Thus, the user can compile services with a variety of such blocks.
All the user needs to know - what blocks there are and how they should be configured correctly.
This is the end of the abstractions with which the user interacts.

## How the developer sees wiredflow

Wiredflow uses a classic approach - multi-layer architecture: 

<span style="color:orange">In progress</span>

## Key abstraction layers

<span style="color:orange">In progress</span>

### Pipeline and templates

<span style="color:orange">In progress</span>

### Actions

<span style="color:orange">In progress</span>

### Stages

<span style="color:orange">In progress</span>
