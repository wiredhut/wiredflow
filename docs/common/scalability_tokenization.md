# Tokenization

This document details the features of tokenization of wiredflow services. 
The goal of tokenization is to improve service performance. This can be achieved by decomposing tasks on three levels:

- Stage into stages;
- Pipeline into pipelines; 
- Flow into flows.

## Stage into stages

The first thing worth paying attention to is how the code is organized. 
Tasks should be decomposed into the simplest actions, which are placed in wiredflow stages. 

If any tasks run very slowly, consist of a lot of code and use 
complex multi-step logic, it may be worth to divide these tasks 
into smaller ones. 

## Pipeline into pipelines

In progress 

## Flow into flows

In progress 
