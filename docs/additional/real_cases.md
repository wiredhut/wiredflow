# Real use cases

This section contains some examples of cases where wiredflow was 
(or currently is) used in commercial development on real-world projects.
This page will show how the functionality of the library can be used with certain examples. 

NB: You can add your own example of using wiredflow to this page. 
If you want to do so, follow [these instructions](contributing.md).
We would be happy to hear about your scenarios using wiredflow.

## Database replication

- **Customer**: Anonymous case
- **Year of realisation**: 2023
- **Artifacts**: Not available

The library was used to create a service that produces a replica of the database. 
Connection to the database was done using the REST API. 
The endpoint allowed getting data using SQL and select queries. 
The database should have been updated once a day. 
Using wiredflow, a service was configured in which each pipeline is responsible for its own entity for replication

## Sensor processing system

<span style="color:orange">In progress</span>