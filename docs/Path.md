# Generic Execution Engine (GEE)

## Vision

Generic Execution Engine (GEE) is a high-performance gRPC-based execution layer built on top of PostgreSQL.

The goal is to provide a single, generic, scalable execution interface capable of:

* Executing arbitrary SQL statements
* Executing PostgreSQL functions
* Executing PostgreSQL procedures
* Streaming large input datasets
* Streaming large query/function result sets
* Minimizing network traffic using Apache Arrow
* Supporting large engineering datasets
* Supporting tens of thousands of client connections through an asynchronous architecture

The engine is intentionally designed to remain generic so that PostgreSQL is only the first backend implementation. Future backends may include:

* PostgreSQL
* OpeCore
* SQL Server
* Oracle
* MySQL
* Other data platforms

***

# V1 Scope

## Included

### SQL Execution

```sql
SELECT * FROM employee;
```

```sql
UPDATE employee
SET salary = 1000
WHERE id = 1;
```

```sql
DELETE FROM employee
WHERE id = 1;
```

Any valid SQL statement can be executed.

***

### Function Execution

Example:

```sql
SELECT *
FROM public.get_employee(100);
```

The execution engine will execute PostgreSQL functions and stream returned data.

***

### Procedure Execution

Example:

```sql
CALL public.import_data(...);
```

The execution engine will execute PostgreSQL procedures.

***

### Streaming Input

Large datasets should not be transferred as a single payload.

Client sends:

```text
Chunk 1
Chunk 2
Chunk 3
Chunk 4
...
```

using gRPC streaming.

The server receives chunks and stores them into a temporary dataset for processing.

***

### Streaming Output

Large result sets are returned incrementally.

Instead of:

```text
50 million rows
↓
single response
```

the engine returns:

```text
Arrow Batch #1
Arrow Batch #2
Arrow Batch #3
...
```

through a gRPC stream.

Memory remains stable regardless of result size.

***

### Apache Arrow Data Transfer

All large data transfers use Apache Arrow.

Reasons:

* Compact binary format
* Much smaller than JSON
* Faster serialization
* Faster deserialization
* Language independent
* Designed for high-volume analytical workloads

***

# Not Included In V1

The following features are intentionally excluded.

They may be introduced later if required.

## Job Manager

Not implemented.

No:

```text
QUEUED
RUNNING
FAILED
COMPLETED
```

tracking.

All executions are synchronous from the execution engine perspective.

***

## Progress Notifications

Not implemented.

***

## Redis

Not implemented.

***

## CDC

Not implemented.

***

## LISTEN / NOTIFY

Not implemented.

***

## Security Layer

Not implemented.

***

## RBAC

Not implemented.

***

## Audit Framework

Not implemented.

***

## Metadata Discovery

Not implemented.

***

## Multi-Tenant Support

Not implemented.

***

## Multi-Database Routing

Not implemented.

***

# High Level Architecture

```text
+--------------------+
|      Client        |
+--------------------+
          |
          |
          v
+--------------------+
|   gRPC Gateway     |
|  Execution Engine  |
+--------------------+
          |
          |
          v
+--------------------+
|     PgBouncer      |
+--------------------+
          |
          |
          v
+--------------------+
|    PostgreSQL      |
+--------------------+
```

***

# Core Design Principles

## 1. Async First

Everything should be asynchronous.

Avoid:

```text
Thread Per Request
```

Use:

```text
Async IO
```

for maximum client scalability.

***

## 2. Streaming First

The primary communication model is:

```text
Client Stream
Server Stream
Bidirectional Stream
```

We do not optimize around request-response patterns.

***

## 3. Stateless Services

The execution engine should remain stateless.

Any engine instance should process any request.

Example:

```text
Gateway #1
Gateway #2
Gateway #3
```

all behave identically.

***

## 4. Backend Agnostic

Execution Engine should never become tightly coupled to PostgreSQL.

The command model should remain generic enough for future adapters.

***

# Supported Execution Modes

## SQL

### Input

```sql
SELECT * FROM employee;
```

### Output

```text
Arrow Stream
```

### Streaming

```text
Input  : Optional
Output : Yes
```

***

## Function

### Input

Parameters

### Output

Function result set

### Streaming

```text
Input  : Optional
Output : Yes
```

Functions returning tables are streamed exactly like SQL queries.

***

## Procedure

### Input

Parameters

or

Streamed Dataset

### Output

Final execution result

### Streaming

```text
Input  : Yes
Output : No (V1)
```

Procedures execute to completion and then return a final response.

***

# Procedure Streaming Model

Large datasets are transferred separately.

Example:

```text
Create Session
       |
       v

Upload Chunks
       |
       v

Execute Procedure
       |
       v

Final Result
```

Procedure receives a temporary dataset reference.

Example:

```sql
CALL process_data(
    'temp_dataset_123'
);
```

The procedure reads data from the temporary dataset.

This avoids passing millions of rows as procedure parameters.

***

# Apache Arrow Workflow

## Query Export

```text
PostgreSQL
    |
    v
Rows
    |
    v
Arrow Table
    |
    v
Arrow Batches
    |
    v
gRPC Stream
    |
    v
Client
```

***

## Data Import

```text
Client
    |
    v
Arrow Batches
    |
    v
gRPC Stream
    |
    v
Execution Engine
    |
    v
Temporary Dataset
    |
    v
Procedure
```

***

# Technology Stack

## Language

```text
Python
```

***

## RPC

```text
grpcio
grpcio-tools
```

***

## PostgreSQL Driver

```text
asyncpg
```

***

## Data Serialization

```text
Apache Arrow
```

***

## Connection Pooling

```text
PgBouncer
```

***

## Database

```text
PostgreSQL
```

***

# V1 Deliverables

### Phase 1

* gRPC server
* PostgreSQL connectivity
* asyncpg integration
* PgBouncer integration

### Phase 2

* SQL execution
* Function execution
* Procedure execution

### Phase 3

* Apache Arrow serialization
* Result streaming
* Input streaming

### Phase 4

* Performance tuning
* Load testing
* Concurrent client validation

***

# Final V1 Goal

Build a **generic, high-performance execution engine** capable of:

* Executing SQL
* Executing Functions
* Executing Procedures
* Streaming input datasets
* Streaming query/function results
* Using Apache Arrow for efficient transport
* Supporting very large datasets
* Remaining scalable and backend-agnostic

without introducing any unnecessary enterprise features until they are actually required.
