# Quick start

Welcome to the wiredflow documentation section exploring use cases! 

Below, we take a look at what **ETL** (Extract, Transform, Load) services, 
detailing at each step what we're doing and why are, write our own services 
to solve toy tasks, and configure advanced services. 

The only skill required to begin studying is the ability to use Python. 
All other technologies will be covered when necessary. 
We'll go step by step, detailing at each step what we're doing and why.

## What are ETL services and why are they needed?

**ETL** pipelines are needed when it is necessary to automatically retrieve data 
from somewhere (extract), do something with it (transform), 
and then save it to a new place (load), and sometimes repeat this task (schedule).
Feel free to skip some steps - for examples just extract and load data is also ok. - You are still need ETL framework.

ETL tasks are similar to backend logic. 
Except that when the backend maintains a website, 
it usually runs tasks at the user's request (event based). 
Classic ETL pipelines usually use a fixed schedule. 
Obviously, when processing data from sensors, ETL services are also configured to run tasks according to events 
(but let's reserve that topic for future sections). 

There are many things that can be done with ETL pipelines - gathering data to 
train machine learning models, running background processes to synchronize databases, 
send alerts and messages to users at particular time of the day and much more. 
Usually these are processes that no one sees. But, nevertheless, many services cannot manage without them.

Since such processes are critical, developers quite often have to write ETL-related services.
Therefore, there are many tools that can automate the launch of such services, speed up their development and simplify monitoring.
There is a short list with such a tools:

- [luigi](https://github.com/spotify/luigi)
- [bonobo](https://github.com/python-bonobo/bonobo) 
- [Apache Airflow](https://github.com/apache/airflow)
- [prefect](https://github.com/PrefectHQ/prefect)

And, definitely, [wiredflow](https://github.com/wiredhut/wiredflow)

## What is Application Programming Interface (API)

First, let's review the mechanisms that allow services to "communicate" with each other. 

## How to use wiredflow for ETL construction

Start with installation - it is pretty easy:

```
pip install wiredflow
```

Then, ...