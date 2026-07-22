# Generic Execution Engine (GEE)

## Vision

Generic Execution Engine (GEE) is a high-performance gRPC-based execution layer built on top of PostgreSQL.

The goal is to provide a single, generic, scalable execution interface capable of:

- Executing arbitrary SQL statements
- Executing PostgreSQL functions
- Executing PostgreSQL procedures
- Streaming large input datasets
- Streaming large query and function result sets
- Minimizing network traffic using Apache Arrow
- Supporting large engineering datasets
- Supporting tens of thousands of client connections through an asynchronous architecture

The engine is intentionally designed to remain generic so that PostgreSQL is only the first backend implementation. Future backends may include:

- PostgreSQL
- OpeCore
- SQL Server
- Oracle
- MySQL
- Other data platforms

---

# Current Implementation Status

## Completed

### Core Infrastructure

- Python package structure
- Conda development environment
- pyproject.toml packaging
- pip installable package
- Async PostgreSQL connection pooling
- gRPC Server
- gRPC Client
- Execution Engine
- Apache Arrow serialization
- Apache Arrow deserialization

### SQL

- SQL Execution
- SQL Streaming Output
- PostgreSQL cursor streaming
- Apache Arrow batch conversion
- gRPC streaming responses

### Functions

- Function Execution
- Function Streaming Output
- Table-returning Function support
- Apache Arrow streaming

### Procedures

- Procedure Execution

### Streaming

- PostgreSQL cursor streaming
- Apache Arrow batch streaming
- gRPC response streaming

---

## Planned

### Procedure Stream Input

Planned architecture:

```text
Client
    ↓
Arrow Batch Stream
    ↓
Temporary Table
    ↓
CALL procedure(temp_table_name)
````

Status:

```text
Not Implemented Yet
```

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

The execution engine executes PostgreSQL functions and streams returned result sets.

***

### Procedure Execution

Example:

```sql
CALL public.import_data(...);
```

The execution engine executes PostgreSQL procedures.

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
Apache Arrow Stream
```

### Streaming

```text
Input  : No
Output : Yes
```

### Status

```text
Implemented ✅
```

***

## Function

### Input

Function parameters.

Example:

```sql
SELECT *
FROM public.generate_numbers(10000);
```

### Output

Function result set.

### Streaming

```text
Input  : Parameters Only
Output : Yes
```

Functions returning tables are streamed exactly like SQL queries.

### Status

```text
Implemented ✅
```

***

## Procedure

### Input

Parameters

or

Streamed Dataset (Planned)

### Output

Final execution result

### Streaming

```text
Input  : Planned
Output : No
```

Procedures execute to completion and return a final response.

### Status

```text
Procedure Execution      ✅
Procedure Stream Input   ❌ Planned
```

***

# Streaming Architecture

## SQL Streaming

```text
PostgreSQL Cursor
         ↓
Batch (1000 rows)
         ↓
Arrow Batch
         ↓
gRPC Stream
         ↓
Client
```

Validated and working.

***

## Function Streaming

```text
PostgreSQL Function
         ↓
Cursor
         ↓
Batch (1000 rows)
         ↓
Arrow Batch
         ↓
gRPC Stream
         ↓
Client
```

Validated and working.

***

## Procedure Stream Input (Planned)

```text
Client
    ↓
Arrow Batch #1
Arrow Batch #2
Arrow Batch #3
    ↓
Temporary Table
    ↓
CALL procedure(
    temp_table_name
)
```

Example:

```sql
CALL process_data(
    'tmp_dataset_123'
);
```

The procedure reads input data directly from the temporary table.

Benefits:

* No massive payloads
* No millions of procedure parameters
* Memory efficient
* Scalable

***

# Apache Arrow Workflow

## SQL / Function Export

```text
PostgreSQL Cursor
       ↓
Row Batch
       ↓
Arrow Table
       ↓
Arrow Binary
       ↓
gRPC Stream
       ↓
Client
```

Status:

```text
Implemented ✅
```

***

## Procedure Import

```text
Client
      ↓
Arrow Batch Stream
      ↓
Execution Engine
      ↓
Temporary Table
      ↓
Procedure
```

Status:

```text
Planned ❌
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

## Database

```text
PostgreSQL
```

***

# Current Project Structure

```text
src/
└── gee/
    ├── arrow/
    │   ├── serializer.py
    │   ├── deserializer.py
    │   └── stream_serializer.py
    │
    ├── execution/
    │   ├── execution_engine.py
    │   ├── sql_executor.py
    │   ├── function_executor.py
    │   └── procedure_executor.py
    │
    ├── postgres/
    │   ├── database.py
    │   └── pool.py
    │
    ├── grpc/
    │   ├── server.py
    │   ├── service.py
    │   └── generated/
    │
    ├── config/
    └── models/
```

***

# Validated End-to-End Flows

## SQL Streaming

```text
Client
    ↓
gRPC
    ↓
ExecutionEngine
    ↓
SqlExecutor.stream()
    ↓
PostgreSQL Cursor
    ↓
Arrow Batch
    ↓
gRPC Stream
    ↓
Client
```

Status:

```text
Validated ✅
```

***

## Function Streaming

```text
Client
    ↓
gRPC
    ↓
ExecutionEngine
    ↓
FunctionExecutor.stream()
    ↓
PostgreSQL Function
    ↓
Arrow Batch
    ↓
gRPC Stream
    ↓
Client
```

Status:

```text
Validated ✅
```

***

# V1 Deliverables

## Completed

### Infrastructure

* Python Package
* Async PostgreSQL Pool
* gRPC Server
* gRPC Client
* Apache Arrow

### Execution Engine

* SQL Executor
* SQL Stream Executor
* Function Executor
* Function Stream Executor
* Procedure Executor

### Streaming

* PostgreSQL Cursor Streaming
* Apache Arrow Batch Streaming
* gRPC Response Streaming

***

## Remaining

### Procedure Input Streaming

```text
Arrow Upload
    ↓
Temporary Table
    ↓
Procedure Execution
```

### Performance

* Benchmarking
* Load Testing
* Batch Size Tuning

***

# Final V1 Goal

Build a generic high-performance execution engine capable of:

* SQL Execution
* SQL Streaming Output
* Function Execution
* Function Streaming Output
* Procedure Execution
* Procedure Input Streaming
* Apache Arrow Data Transfer
* gRPC Streaming
* Large Dataset Processing
* Backend Agnostic Design

Current Validation Status:

```text
SQL Execution            ✅
SQL Streaming            ✅

Function Execution       ✅
Function Streaming       ✅

Procedure Execution      ✅
Procedure Stream Input   ⏳ Next

Apache Arrow             ✅
gRPC Streaming           ✅
```

The project focuses on a minimal, scalable, high-performance execution engine without introducing unnecessary enterprise features until they are required.

```
