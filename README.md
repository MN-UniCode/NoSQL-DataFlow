# NoSQL-DataFlow

## About this Project
This project was developed as part of the **"Advanced Data Management"** course at the **University of Genoa**, within the Master's program in **Computer Engineering - Artificial Intelligence and Human-Centered Computing**.

## Overview
This project uses Docker Compose to set up a multi-node Cassandra cluster and integrates with Neo4j for graph-based data storage. 
Python scripts are used to extract data from the Hardcover API and load them into the respective databases.
To follow all the steps that we have done during this project and also replicate our queries and commands inside Cassandra and Neo4j you can examin our detailed [report](./ADM_Project.pdf).

## Requirements
- Docker & Docker Compose
- Python 3.x
- Neo4j Aura (Free Instance)

## Getting Started

### Clone the Repository
```bash
git clone [https://github.com/MN-UniCode/ADM-Project.git](https://github.com/MN-UniCode/NoSQL-DataFlow.git)
cd /path/NoSQL-DataFlow
```

### API-KEY to extract data
Extracting data from Hardcover API requires an API-KEY that you can find [here](https://hardcover.app/account/api) after logging in.
You need to create a folder `config` inside the main directory of the project and put it inside a file `config.py` with you API-KEY.

Here the steps:
```bash
cd NoSQL-DataFlow
mkdir config
nano config.py
```

```python
# config.py
API_KEY = "your api-key"
```

---
### Cassandra

#### Start the Cassandra Cluster
```bash
docker-compose up -d
```
This will start a **three-node Cassandra cluster** with the following containers:
- `cassandra-1` (seed node, port 9042)
- `cassandra-2` (port 9043)
- `cassandra-3` (port 9044)

#### Enter into the Node & Check Cluster Status
Run the following command to check the cluster status:
```bash
docker exec -it cassandra-1 bash
nodetool status
```
Use cassandra-x, x = {1, 2, 3} to choose in which node to connect to.

#### Access Cassandra Shell
To open CQL Shell (cqlsh):
```bash
cqlsh
```

#### Stopping & Removing Containers
To stop the cluster:
```bash
docker-compose down
```

To remove all data volumes:
```bash
docker-compose down -v
```

#### Extract more data
Python scripts in the `Cassandra/pyScript` folder are used to fetch data from the Hardcover API:
```bash
python3 -m Cassandra.pyScript.main
```
These scripts will process and save the data for use in Cassandra.

### Notes
- Data is **persisted** using Docker volumes.
- The cluster uses **GossipingPropertyFileSnitch** for topology awareness.
- The replication factor is set to **3** for fault tolerance.

---
### Neo4j

#### Load Data into Neo4j
For Neo4j, use the free instance of [Neo4j Aura](https://neo4j.com/cloud/aura/) and execute Cypher queries to insert data or use the *import* feature that allows you to import easily CSV files into the instance.

### Extract more data
Python scripts in the `Neo4j/pyScript` folder are used to fetch data from the Hardcover API:
```bash
python3 -m Neo4j.pyScript.main
```
These scripts will process and save the data for use in Neo4j.
