# Storages description

This section discusses the crucial topic about data storage. 
If choose the wrong way to store data, it can become a critical bottleneck for the entire service.
Therefore, on this page we suggest to explore in detail what kind of storage is worth using in different cases.

## Files as local storages

Let's start with a very simple example. You can use regular files! 
Sometimes you don't need to complicate things. Especially during the first
stages of development, when it is carried out locally on the developers' laptops.

The following options can be used to access storage files in wiredflow:

- `json` - save data into JSON file (good for variable structure data)
- `csv` - save data into CSV file (good for data with fixed structure)

JSON in this case can be considered as a very simplified analogue of MongoDB. 
And csv is an example of a relational database, such as PostgreSQL.

<img src="https://raw.githubusercontent.com/wiredhut/wiredflow/main/docs/media/local_storages.png" width="800"/>

Warning! 
Please do not use the files as storage for data for "production ready" solutions! 
Storing data in files is convenient only in the first stages of service development. 
Then switch to using a suitable database.

### Usage examples 

### Customization 

## Databases

### Usage examples 

### Customization 
