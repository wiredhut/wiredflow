# Why you should try wiredflow

As stated in the [repository readme](https://github.com/wiredhut/wiredflow), 
wiredflow is not the only library used for ETL pipelines. We can consider 
[luigi](https://github.com/spotify/luigi), [bonobo](https://github.com/python-bonobo/bonobo),
[Apache Airflow](https://github.com/apache/airflow) and [prefect](https://github.com/PrefectHQ/prefect) as analogues.
So the question may arise: "Why I should try wiredflow instead of other tools?".

## Key features of wiredflow

Start with list of key features which help to determine is wiredflow suitable for your tasks or not: 

- easy to use - almost the same as any regular python library
- suitable for creating both classic ETL pipelines (batch processing) and real-time services 
  (continuous streaming workflows)
- ability to construct complex services with both streaming and batch-processing logic in the same service (simultaneously)
- has an internal scheduler - so there is no need to configure scheduler through crontab (but it is possible if you want to use external one)
- out of box integration with HTTP and MQTT protocol
- native ability to save data into files (for local development and MVP) and databases for more production solutions
- highly customizable
- allow launching service partly in threads or processes (parallel computing) through single entry point

## Questions section

Below is a Q&A section to make it clearer 
to you how this library differs from other more well-known analogues.

> **Question**: What does "lightweight" mean?
> 
> **Response**: That means that the library only uses native Python to run. 
> Thus for basic usage there is no need to install **docker** or deal with **docker-compose**, you do 
> not need to deploy the **database** locally (or non-locally) or figuring out how perform desired actions 
> on **AWS** with full production infrastructure - you can just use your laptop and run 
> the python script as "hello_world.py". The only thing you need to know to work 
> with wiredflow is Python.

---

> **Question**: What is the advantage of such a lightweight?
> 
> **Response**: 1) Prototyping - you can quickly start listening to your MQTT 
> queues or start collecting data using HTTP requests, etc. 2) Python code 
> would be easy to build into larger projects because using wiredflow has 
> pretty low overhead. 3) Wiredflow has its own internal scheduler, allowing 
> you to run your services out of the box.

---

> **Question**: If wiredflow does not use a database, where is the data saved?
> 
> **Response**: In CSV files or in JSON files. Yes, this is not a production solution, 
> but it is very convenient to deal with data you unfamiliar with.

---

> **Question**: What if I want to use the database?
> 
> **Response**: Sure you can use a database, for example you can use a local one 
> or save (and retrieve) the data to the already configured remote one.

---

> **Question**: Can I create Python scripts that will combine data from multiple 
> sources (APIs) and store data in a storage?
>
> **Response**: Sure! That's exactly what wiredflow is for.

---

> **Question**: I saw in the documentation that the service can be subscribed to 
> multiple MQTT queues at the same time. How does it work?
> 
> **Response**: Wiredflow uses the multithreading and multiprocessing Python modules. This allows 
> effective sharing of resources between individual pipelines in your service. It is possible 
> to choose whether to use threads to launch pipelines or processes.

---

> **Question**: Many ETL tools must be managed externally (using CRON or Kubernetes above docker containers). 
> Does wiredflow have the same system?
> 
> **Response**: Wiredflow has its own internal scheduler, which allows 
> launching pipelines with different scheduling in the same service. 
> But services can be configured to run once also. 
> And then services can be orchestrated by external mechnaisms