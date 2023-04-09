# Remote launch

This document discusses the remote launch capabilities of wiredflow.
Remote launch is an instruction to execute a program on a remote server. 
For example, with this mechanism it is possible to run 9 tasks on one virtual machine with 16 GB RAM, and 1 task on a machine with 64 GB RAM.
This is very convenient when one of the tasks requires a lot of resources and executed infrequently.

## Problem localization

The first thing to start with is to determine which task is too slow. 
For example, if the service consists of two pipelines, then first you should determine which 
pipeline are not effective enough. Then it is worth defining the stage, which is the "bottleneck".
Once you have decided about the stage - it's time to configure remote launch for it.

## Custom remote launcher implementation

In progress