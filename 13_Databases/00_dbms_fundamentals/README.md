# DBMS Fundamentals: university database theory

A **DBMS** (database management system) is the software that stores data safely, lets many people use it at once and answers questions about it quickly (PostgreSQL, MySQL and SQLite are examples); this folder explains *how* a DBMS works inside and *why* good databases are designed the way they are. That knowledge helps an AI developer build training sets, feature tables, RAG stores and prediction logs that stay correct and fast. It is an **optional, university-level track**: you can build AI apps without it, but it is what BS/MS exams, system-design interviews and senior engineers expect you to know.

### Where this track fits in `13_Databases`

The other folders in `13_Databases` are **practical**: they show you how to *use* a kind of database. This folder is the **theory** underneath all of them.

| Folder | What it is | How the theory here helps |
|---|---|---|
| [`01_sql`](../01_sql/01_sql_fundamentals.ipynb) | writing SQL queries, plus an [industry feature-extraction project](../01_sql/02_industry_sql_for_ml_feature_extraction.ipynb) | 03 (relational algebra) explains what a query means; 07 and 08 explain why it is fast or slow |
| [`02_nosql`](../02_nosql/01_nosql_databases.ipynb) | document, key-value and wide-column stores | 09 (replication, CAP, sharding) explains the trade-offs NoSQL makes |
| [`03_vector_db`](../03_vector_db/01_vector_databases.ipynb) | similarity search for embeddings | 07 (indexes) and 08 (pushing filters down) apply directly to vector indexes |
| [`04_orm`](../04_orm/01_orm.ipynb) | using a database through Python objects (SQLAlchemy) | 01 (impedance mismatch) and 05 (transactions) explain what the ORM hides |
| [`05_db_in_ai`](../05_db_in_ai/01_databases_in_ai.ipynb) | which database plays which role in an ML system | the whole track: ACID, design, indexing |
| [`06_data_engineering`](../06_data_engineering/01_data_engineering.ipynb) | pipelines and ETL for ML | 09 (warehouses, star schemas, OLAP) and 04 (denormalization) |
| [`07_graph_databases`](../07_graph_databases/01_graph_databases.ipynb) | Neo4j and relationship-heavy data | 02 (ER model: relationships as first-class things) |
| [`08_time_series_databases`](../08_time_series_databases/01_time_series_databases.ipynb) | time-stamped metrics and events | 06 (storage layout) and 03/07 (column stores, indexes) |

[`22_ML_System_Design/03_relational_db_design.ipynb`](../../22_ML_System_Design/03_relational_db_design.ipynb) is the **applied follow-up**: it uses normalization, indexing and query optimization to design the metadata, experiment and prediction-log tables of a real ML system. It assumes the ideas taught in notebooks 02, 04, 07 and 08 here, so it is easier after this track (notebook 10 here links to it as the next step).

**Course match.** The ten notebooks follow the syllabus of a typical BS/MS **Database Systems / DBMS** course, chapter by chapter, as in the two standard textbooks, *Database System Concepts* (Silberschatz, Korth and Sudarshan) and *Fundamentals of Database Systems* (Elmasri and Navathe), and the free **GeeksforGeeks DBMS tutorial**. Each notebook names the textbook chapters it covers.

### Recommended order with the SQL notebooks

```
 01 DBMS intro  ->  01_sql/01_sql_fundamentals  ->  02 ER  ->  03 relational algebra  ->  04 normalization
                                                                                            |
 22_ML_System_Design/03  <-  01_sql/02 (industry)  <-  10 industry project  <-  05 ... 09  <-+
```

1. Read **notebook 01** first (it needs only Python).
2. Then do [**SQL Fundamentals**](../01_sql/01_sql_fundamentals.ipynb). From notebook 04 on, every notebook lists it as a prerequisite, and notebooks 02 and 03 are easier with it.
3. Work through **02 → 09** in order. Each notebook builds on the one before it.
4. Do the **industry project 10**. Then do the SQL [industry project](../01_sql/02_industry_sql_for_ml_feature_extraction.ipynb) and [`22_ML_System_Design/03`](../../22_ML_System_Design/03_relational_db_design.ipynb).

Short on time? Do `01_sql` first and come back here only for the topics you need (for example, 07 and 08 when queries get slow, 05 when you write concurrent code).

---

## The whole topic explained simply

A database is a big, very well-organized notebook that many people can write in at the same time without making a mess. Before you build one, you **draw a plan** of what you want to store and how the pieces connect (the ER diagram), like an architect drawing a house before anyone lays a brick. Then you split the data into tidy tables so that every fact is written **in exactly one place** (normalization), the same way a school keeps one address card per student instead of copying the address onto every exam paper. When two people change the same data at the same moment, the database makes them take turns in a safe order (transactions and locks), like a single key to a shared bathroom. Before it changes anything, it writes down what it is about to do in a diary (the log), so after a power cut it can finish or undo half-done work. To find one row among millions it uses an index, which works like the index at the back of a textbook. When you ask a question in SQL, the database's planner compares many ways of answering it and picks the cheapest, like a satnav choosing a route. When one computer is not enough, the data is spread over many machines that still have to act as one database.

**Tiny worked example.** A bank account holds 50,000. Clerk 1 withdraws 5,000 and Clerk 2 withdraws 7,000 at the same moment. Both read 50,000. Clerk 1 writes 45,000, then Clerk 2 writes 43,000. The right answer is 50,000 − 5,000 − 7,000 = **38,000**, so 5,000 has silently disappeared (a *lost update*). A DBMS makes Clerk 2 wait until Clerk 1 has finished, so Clerk 2 reads 45,000 and writes **38,000**. Notebook 01 runs exactly this with CSV files (wrong) and with SQLite (right).

---

## Who is this for / prerequisites / time needed

| | |
|---|---|
| **Who** | Beginners who want to understand databases properly; BS/MS AI and CS students revising for DBMS exams; anyone preparing for data-engineering or system-design interviews |
| **Prerequisites** | [Python basics](../../01_Python/01_basic.ipynb) (required). [SQL Fundamentals](../01_sql/01_sql_fundamentals.ipynb) (required from notebook 04). [pandas](../../02_Data_Analysis/03_pandas.ipynb) (helpful). For 07, [hashing](../../00_AI_Fundamentals/dsa/04_hashing.ipynb) and [trees](../../00_AI_Fundamentals/dsa/06_trees_bst_and_heaps.ipynb) from the DSA track help |
| **Time needed** | About **26–28 hours** in total (1.5–4 hours per notebook, plus practice problems) |
| **Runs on** | CPU only, no API key, no internet, no database server. Everything uses SQLite, which ships with Python, plus pandas, numpy, matplotlib and networkx |
| **Optional?** | Yes. It is the university-level fundamentals track. The applied folders work without it |

---

## Study order

| # | Notebook | In one sentence | Time |
|---|---|---|---|
| 01 | [DBMS Introduction and Architecture](01_dbms_introduction_and_architecture.ipynb) | Why plain files break, and what a DBMS is made of | 1.5 h |
| 02 | [The ER Model and EER](02_er_model_and_eer.ipynb) | Draw the plan of a database, then turn it into tables | 2 h |
| 03 | [Relational Model and Relational Algebra](03_relational_model_and_relational_algebra.ipynb) | Keys, constraints, and the math behind every SQL query | 2.5 h |
| 04 | [Functional Dependencies and Normalization](04_functional_dependencies_and_normalization.ipynb) | Split tables so each fact is stored once, and prove the split is safe | 3 h |
| 05 | [Transactions and Concurrency Control](05_transactions_and_concurrency_control.ipynb) | ACID, safe interleaving, locks, deadlocks and MVCC | 3 h |
| 06 | [Recovery and Storage](06_recovery_and_storage.ipynb) | How a database survives crashes and lays data out on disk | 2.5–3 h |
| 07 | [Indexing, B-Trees and Hashing](07_indexing_b_trees_and_hashing.ipynb) | Find one row among millions in a few disk reads | 3 h |
| 08 | [Query Processing and Optimization](08_query_processing_and_optimization.ipynb) | How SQL becomes a plan, and how the cheapest plan is chosen | 3 h |
| 09 | [Distributed Databases, Warehousing and Security](09_distributed_databases_warehousing_and_security.ipynb) | Many machines, history stores for analytics, and keeping data safe | 3–4 h |
| 10 | [Industry Project: Designing a Database End to End](10_industry_designing_a_database_end_to_end.ipynb) | Every step applied to one online-course platform, from blank page to production | 2–3 h |

The conceptual study guide for the whole folder is in [`notes/00_dbms_fundamentals.md`](notes/00_dbms_fundamentals.md).

---

## The notebooks one by one

### 01 · DBMS Introduction and Architecture

*Explained simply.* **Data** are raw facts (`31`, `"Lahore"`); **information** is data that has been processed so it means something ("October in Lahore averaged 31 °C"). Keeping data in plain files works for a while, then copies drift apart, crashes leave half-written changes, and two users overwrite each other. A DBMS fixes this and adds structure: a **schema** (the design of the tables) separate from the **instance** (the rows stored right now). You also meet the parts inside a DBMS: the query processor, the storage manager and the buffer manager. Think of a library: the catalogue rules are the schema, the books on the shelves today are the instance, and the librarians are the DBMS.

*Tiny example.* Data vs. information, from the notebook:

| city | day | temp |
|---|---|---|
| Lahore | 1 | 31 |
| Lahore | 2 | 33 |
| Lahore | 3 | 29 |

Information: Lahore average = (31 + 33 + 29) / 3 = **31.0**.

*You will learn:*
- the eight problems of file-processing systems (redundancy, inconsistency, integrity, atomicity, concurrency, security and more), each reproduced and fixed
- schema vs. instance, data models, the **three-schema (ANSI/SPARC) architecture** and logical vs. physical **data independence**
- the four language groups: **DDL, DML, DCL, TCL**
- the components of a DBMS, including a tiny **LRU buffer manager** you build yourself
- 1-, 2- and 3-tier architectures, types of users, database objects (views, triggers, sequences) and the **impedance mismatch** that ORMs address

*Key takeaway:* a DBMS gives you consistency, safety and data independence that plain files cannot.

### 02 · The ER Model and EER

*Explained simply.* Before creating tables you draw an **Entity–Relationship (ER) diagram**. **Entities** are things (Student, Course), **attributes** are their properties (name, credits), and **relationships** connect them (a Student *takes* a Course). You also record *how many*: one-to-one, one-to-many or many-to-many, and whether taking part is compulsory. **Enhanced ER (EER)** adds "is-a" hierarchies, for example a Person who is a Student or an Employee. Think of a family tree drawn on paper before you fill in the forms for each person.

*Tiny example.* The minimum number of tables for two entities and one relationship between them:

| relationship | minimum tables | why |
|---|---|---|
| M:N | 3 | the relationship needs its own table (e.g. `takes(sid, cid)`) |
| 1:N | 2 | put the foreign key on the N side |
| 1:1, one side total | 1 | merge everything into one table |

Each multivalued attribute (e.g. a student's phone numbers) adds one more table.

*You will learn:*
- every kind of attribute (composite, multivalued, derived, key) and relationship degree (unary, binary, ternary)
- cardinality ratios, total/partial participation and **(min,max)** notation, checked against data by code
- **weak entities**, partial keys and identifying relationships
- EER: specialization/generalization, disjoint/overlapping, categories and aggregation
- the **ER → relational mapping** algorithm rule by rule in SQLite, including options A–D for subclasses
- common design mistakes such as the **connection trap**

*Key takeaway:* a good ER diagram maps almost mechanically to correct tables and constraints.

### 03 · The Relational Model and Relational Algebra

*Explained simply.* In the relational model a table is a **relation**: a *set* of rows (tuples) with no duplicates and no order. **Keys** identify rows, and **foreign keys** link tables. **Relational algebra** is a small set of operations on tables: select rows (σ), pick columns (π), join tables (⋈), union, difference, and **division** for "for all" questions. Every SQL query is translated into these operations. Think of LEGO: a few brick shapes snap together into any model, the same way a few operators combine into any query.

*Tiny example.* Which students passed **all** CS courses? That is division:

```
TAKES (sid, cid)        CS_COURSES (cid)      TAKES ÷ CS_COURSES
S1 C1   S2 C1           C1                    S1
S1 C2   S3 C2           C2
```

S1 took both C1 and C2. S2 and S3 each took only one, so only **S1** is in the answer.

*You will learn:*
- relation, tuple, domain, degree, cardinality; super, candidate, primary, foreign and surrogate keys (with a brute-force key finder)
- integrity constraints in SQLite, including `ON DELETE CASCADE` and the `foreign_keys` pragma, which is OFF by default
- all algebra operators written from scratch in Python, each checked against SQLite with `assert`
- ten classic exam queries in algebra *and* SQL, and why `NOT IN` breaks when the subquery contains `NULL`
- tuple and domain relational calculus, **safe** expressions, Codd's rules, and row vs. column stores

*Key takeaway:* SQL is relational algebra in friendlier clothes, and optimizers rewrite the algebra.

### 04 · Functional Dependencies and Normalization

*Explained simply.* If one table mixes facts about employees *and* departments, renaming a department means changing many rows (an **update anomaly**). A **functional dependency (FD)** `X → Y` says "knowing X fixes Y", for example `ssn → name`. Using FDs you find the keys and check **normal forms** (1NF, 2NF, 3NF, BCNF and beyond), which are rules that remove repeated facts. Then you split the table, and prove the split loses no information and keeps every rule checkable. Think of a school storing the head teacher's name on every report card: when the head changes, some cards get missed.

*Tiny example.* R(A, B, C, G, H, I) with F = {A → B, A → C, CG → H, CG → I, B → H}. Compute the closure of AG:

```
start AG  -> A→B: ABG  -> A→C: ABCG  -> CG→H: ABCGH  -> CG→I: ABCGHI = all of R
```

So AG is a superkey. Neither A⁺ nor G⁺ covers R, so **AG is a candidate key**.

*You will learn:*
- update, insertion and deletion anomalies, shown live
- Armstrong's axioms, attribute closure, finding all candidate keys, prime attributes
- F⁺, equivalence of FD sets, and the **canonical / minimal cover**
- 1NF, 2NF, 3NF, BCNF, 4NF, 5NF and DKNF, each with a violation and a fix
- BCNF decomposition, 3NF synthesis, the **lossless-join test** (chase) and the **dependency-preservation** test, plus five solved exam problems
- when to **denormalize** on purpose (ML feature tables were 5x faster to read in the notebook's demo)

*Key takeaway:* 3NF synthesis is always lossless and dependency-preserving; BCNF is always lossless but may lose an FD.

### 05 · Transactions and Concurrency Control

*Explained simply.* A **transaction** is a group of changes that happen completely or not at all, like a bank transfer. **ACID** names the four promises: Atomicity, Consistency, Isolation, Durability. When transactions run at the same time, the database must make the result look as if they ran one after another (**serializable**). It does this with **locks** (two-phase locking), with **timestamps**, or by keeping several versions of each row (**MVCC**). Think of a shared bathroom key: whoever holds it goes in, and the others wait.

*Tiny example.* A = 100. T1 withdraws 50 and T2 deposits 20. The correct final value is 100 − 50 + 20 = **70**.

```
T1: read A=100            write A=50
T2:          read A=100              write A=120   -> final 120, T1's withdrawal is lost
```

Under strict 2PL, T2 must wait for T1's lock, then reads 50 and writes **70**.

*You will learn:*
- transaction states, ACID, and a real crash halfway through a transaction in SQLite
- conflicts (RW, WR, WW) and anomalies: lost update, dirty read, unrepeatable read, phantom
- **conflict serializability** with the precedence graph, view serializability, and recoverable / cascadeless / strict schedules
- 2PL, strict 2PL and rigorous 2PL; deadlock detection, **wait-die** and **wound-wait**; intention locks (IS, IX, SIX)
- timestamp ordering, Thomas' write rule, optimistic validation, MVCC and snapshot isolation
- SQL isolation levels, and what SQLite actually does ("database is locked", WAL mode)

*Key takeaway:* an acyclic precedence graph means serializable, and 2PL guarantees it at the price of possible deadlocks.

### 06 · Recovery and Storage

*Explained simply.* RAM forgets everything when the power goes, so the database keeps a **log** (a diary) on disk. The **write-ahead logging (WAL)** rule says: write the diary line *before* changing the data. After a crash, the database **redoes** committed work and **undoes** unfinished work. **Checkpoints** are save points, so recovery does not have to read the whole diary. The notebook also covers how disks are made safe (**RAID**) and how rows are packed into pages. Think of a video-game autosave: after a crash you restart from the last save, not from the beginning.

*Tiny example.* The log at the moment of a crash (Silberschatz's classic example):

```
<T0 start> <T0, A, 1000, 950> <T0, B, 2000, 2050> <T0 commit> <T1 start> <T1, C, 700, 600>   CRASH
```

T0 committed, so it is **redone**: A = 950, B = 2050. T1 did not commit, so it is **undone**: C = 700.

*You will learn:*
- failure types; volatile, non-volatile and **stable** storage; the latency of the storage hierarchy
- log records, the WAL rule, deferred vs. immediate modification, undo/redo lists and checkpoints, on a tiny database you crash 3,000 times
- **ARIES** (LSNs, analysis / redo / undo, CLRs) and shadow paging
- buffer replacement (LRU, Clock, MRU), pinning, and **steal / force** policies
- RAID 0, 1, 5, 6, 10 with an XOR parity rebuild; heap, sorted, hashed and clustered files; slotted pages; backups and replication

*Key takeaway:* steal means you need undo, no-force means you need redo, and real systems use both (ARIES).

### 07 · Indexing, B-Trees and Hashing

*Explained simply.* Reading every page to find one row is slow, so the database keeps **indexes**. The most common is the **B+ tree**: a short, very wide, always-balanced tree whose leaves are linked in sorted order, which is good for both exact lookups and ranges. **Hash indexes** jump straight to a bucket and suit exact matches only. **Bitmap indexes** suit columns with few distinct values. **Inverted indexes** suit text search. Every index makes writes slower, because it must be updated too. Think of a dictionary: alphabetical order lets you open the right page instead of reading from page 1.

*Tiny example.* 1,000,000 student rows at 100 rows per page = 10,000 pages. Scanning to find one roll number reads about 5,000 pages on average. A B+ tree with 100 keys per node needs 3 levels (100 × 100 × 100 = 1,000,000), so the lookup costs about **4 reads** (3 index pages + 1 data page).

*You will learn:*
- the cost model in block reads; primary/clustering vs. secondary, dense vs. sparse, multi-level indexes
- a **B+ tree from scratch**: insert with splits, range queries, delete with borrow/merge, tested against a `dict`
- exam formulas for order and height (a 4 KB page with 8-byte keys and pointers gives n = 256)
- static, **extendible** and linear hashing; bitmap indexes; inverted indexes with BM25
- SQLite `EXPLAIN QUERY PLAN`, covering and clustered (`WITHOUT ROWID`) indexes, measured on 200,000 rows
- when indexes hurt: in the demo, 4 indexes made inserts 2.6x slower, and indexes lose to a full scan at low selectivity

*Key takeaway:* a B+ tree finds any key among billions in 3–4 page reads, but every index is paid for on every write.

### 08 · Query Processing and Optimization

*Explained simply.* SQL says *what* you want, not *how* to get it. The DBMS parses the query, turns it into relational algebra, considers many equivalent plans, estimates the cost of each from statistics, and runs the cheapest. Two ideas do most of the work: **filter rows as early as possible**, and **join tables with a clever algorithm** (sort-merge or hash) instead of comparing every pair. The same query can take 5 ms or 5 minutes depending on the plan. Think of a satnav: you give the destination, and it picks the fastest route using traffic data.

*Tiny example.* Join r and s with 200 blocks each, 2,000 rows in r, and M = 50 memory blocks:

| algorithm | formula (block transfers) | cost |
|---|---|---|
| nested-loop | n_r · b_s + b_r = 2000 · 200 + 200 | **400,200** |
| block nested-loop | ⌈b_r/(M−2)⌉ · b_s + b_r = 5 · 200 + 200 | **1,200** |

Same answer, about **333x** fewer disk reads.

*You will learn:*
- the pipeline parse → translate → optimize → plan → execute, with a tiny SQL-to-algebra translator
- selection algorithms and **external merge sort**, with their costs
- five join algorithms implemented, benchmarked and checked against pandas
- materialization vs. **pipelining** (the iterator model)
- heuristic optimization (push σ and π down) and cost-based optimization (selectivity, histograms, **System R dynamic programming** for join order)
- reading real SQLite plans and rewriting a slow correlated subquery (2,332 ms down to 18 ms in the notebook)

*Key takeaway:* push selections down, choose join algorithms by cost, and check `EXPLAIN` instead of guessing.

### 09 · Distributed Databases, Data Warehousing and Security

*Explained simply.* When one machine is not enough, data is split (**fragmentation, sharding**) and copied (**replication**) across many machines that must still act as one database. **Two-phase commit** makes a transaction all-or-nothing across machines. The **CAP theorem** says that during a network split you must choose between always-correct and always-answering. A **data warehouse** is a separate history store organized for big analytical questions (star schemas, OLAP). **Security** covers who may see what (GRANT/REVOKE), and stops attacks such as **SQL injection**. Think of a library with branches in three cities and one shared catalogue.

*Tiny example.* Quorum replication with N = 3 copies. Writes wait for W = 2 copies and reads ask R = 2 copies. Because R + W = 4 > 3, every read set overlaps every write set in at least one copy, so a read always sees the latest write. With R = 1 and W = 1 (sum 2 ≤ 3), a read can miss the latest write.

*You will learn:*
- homogeneous vs. heterogeneous systems; horizontal, vertical and mixed fragmentation; sync/async replication and quorums
- distributed query processing with the **semi-join**; **2PC** (including a coordinator crash), 3PC, Paxos/Raft
- **CAP**, PACELC, BASE vs. ACID; sharding and **consistent hashing** (adding a 5th server moved 19% of keys instead of 80%)
- OLTP vs. OLAP; star, snowflake and galaxy schemas; slowly changing dimensions; roll-up, drill-down, slice, dice, pivot
- KDD, HDFS / HBase / Hive and the lakehouse (Parquet + Delta/Iceberg)
- authentication vs. authorization, RBAC, SQL injection attacked and fixed, auditing, the inference problem, GDPR-style data minimization

*Key takeaway:* distribution trades consistency against latency and availability, so choose consciously and write the choice down.

### 10 · Industry Project: Designing a Database End to End

*Explained simply.* This notebook applies everything to one product, an online-course platform, in the order a real team works: requirements and business rules, ER diagram, mapping to tables, FD check (BCNF), DDL with constraints and triggers, about 50,000 rows of realistic data, ten business queries, indexes chosen from query plans, safe payment transactions, data-quality tests, an ML feature table, and finally migrations, backups and monitoring. Think of planning a new school's filing system before the first day, then testing it with a busy first week.

*Tiny example.* Sara buys "SQL 101" ($20) with a 50% coupon. Three changes must happen together: a **$10 payment** row, an **enrolment** row, and the coupon's use count going from **4 to 5**. If her card is declined, none of the three may happen.

*You will learn:*
- turning numbered business rules into constraints, composite foreign keys and triggers, then testing each rule by trying to break it
- proving the schema is BCNF, lossless and dependency-preserving
- writing business queries with window functions, and choosing indexes from `EXPLAIN QUERY PLAN`
- atomic, **idempotent** payment transactions with `BEGIN IMMEDIATE` and rollback
- SQL data-quality tests and a **point-in-time** ML feature table
- transactional migrations, a backup-and-restore drill and a health check

*Key takeaway:* let the database enforce every rule it can, and treat tests, features and operations as part of the design.

---

## How this connects to the rest of the repo and to real AI systems

- **SQL in practice:** [SQL Fundamentals](../01_sql/01_sql_fundamentals.ipynb) and the [SQL feature-extraction project](../01_sql/02_industry_sql_for_ml_feature_extraction.ipynb) are where you write the queries whose theory is in 03, 07 and 08.
- **ML system design:** [Relational Database Design for ML Systems](../../22_ML_System_Design/03_relational_db_design.ipynb) applies normalization and indexing to experiment tracking and prediction logging. [NoSQL and data stores](../../22_ML_System_Design/04_nosql_and_data_stores.ipynb) and [vector databases](../../22_ML_System_Design/05_vector_databases.ipynb) build on notebook 09.
- **Feature stores:** the point-in-time feature table of notebook 10 is what a [feature store](../../15_MLOps/12_feature_stores.ipynb) serves online and offline.
- **RAG:** inverted indexes and BM25 (07) are the keyword half of hybrid retrieval in [RAG](../../08_LLM/02_rag/01_rag_fundamentals.ipynb). Vector indexes in [`03_vector_db`](../03_vector_db/01_vector_databases.ipynb) are approximate cousins of the B+ tree.
- **Security:** SQL injection (09) is the older twin of prompt injection, which is covered in [LLM security](../../08_LLM/16_llm_security.ipynb).
- **Data structures:** B+ trees and extendible hashing extend [trees](../../00_AI_Fundamentals/dsa/06_trees_bst_and_heaps.ipynb) and [hashing](../../00_AI_Fundamentals/dsa/04_hashing.ipynb) from the DSA track.
- **The big picture:** the module overview in [`../notes/13_Databases.md`](../notes/13_Databases.md) explains how all the database families fit together.

---

## Common beginner mistakes

- Treating "it works on my sample data" as proof of a key or FD. Data can **disprove** a constraint, never prove it. Constraints come from business rules.
- Forgetting that SQLite has **foreign keys OFF by default**: run `PRAGMA foreign_keys = ON` on every connection.
- Writing `NOT IN (subquery)` when the subquery can return `NULL`. The result is silently empty, so use `NOT EXISTS` instead.
- Thinking BCNF is always "better" than 3NF. BCNF can make an FD impossible to check without a join, and 3NF never does.
- Adding an index for every column. Each index slows every insert and update, and at low selectivity a full scan is faster anyway.
- Wrapping an indexed column in a function (`WHERE lower(email) = ?`, `WHERE date(created) = ?`). This makes the predicate non-sargable, so the index cannot be used.
- Believing "Repeatable Read" or "snapshot isolation" means serializable. Snapshot isolation still allows **write skew**.
- Calling RAID or replication a backup. A mistaken `DELETE` is copied to every mirror instantly.
- Building SQL strings with f-strings or `+`. Always use **parameterized queries**.

---

## Exam / interview quick-revision

| Question | Answer |
|---|---|
| Logical vs. physical data independence? | Logical: change the conceptual schema without breaking views. Physical: change storage without breaking the conceptual schema. Physical is easier |
| Minimum tables for an M:N relationship? | 3 (two entities + one relationship table) |
| Superkey vs. candidate key? | A superkey identifies rows; a candidate key is a *minimal* superkey |
| How many superkeys does R(A,B,C,D,E) have if its only key is {A}? | 2⁴ = 16 |
| When is X a superkey? | When X⁺ contains every attribute of R |
| 3NF condition? | For every non-trivial X → A: X is a superkey **or** A is prime |
| BCNF condition? | For every non-trivial X → Y: X is a superkey |
| Lossless test for R → R1, R2? | R1 ∩ R2 → R1 or R1 ∩ R2 → R2 is in F⁺ |
| Test for conflict serializability? | Build the precedence graph; acyclic means serializable |
| What does 2PL guarantee, and what does it cost? | Conflict serializability; deadlocks are still possible |
| Wait-die vs. wound-wait? | Wait-die: an older requester waits, a younger requester dies (aborts). Wound-wait: an older requester wounds (aborts) the younger holder, a younger requester waits |
| Steal / no-force imply? | Steal means undo is needed; no-force means redo is needed |
| Three phases of ARIES? | Analysis, redo (repeat history), undo (writing CLRs) |
| Order of a B+ tree node with B-byte blocks? | n = ⌊(B + K)/(P + K)⌋ for K-byte keys and P-byte pointers |
| Hash join cost (Grace)? | 3(b_r + b_s) + 4n_h block transfers |
| Why push selections down? | Smaller intermediate results make every later step cheaper |
| Quorum condition for reading the latest write? | R + W > N |
| CAP in one line? | During a network partition, choose consistency or availability |

---

## Further reading

**Classic textbooks** (each notebook names the exact chapters):
- Silberschatz, Korth and Sudarshan, *Database System Concepts*, 7th ed. (the university-database running example used here)
- Elmasri and Navathe, *Fundamentals of Database Systems*, 7th ed. (the COMPANY database, LOTS and SUPPLY exam problems)
- Ramakrishnan and Gehrke, *Database Management Systems*, 3rd ed.
- Kleppmann, *Designing Data-Intensive Applications* (replication, partitioning, consistency, for notebook 09)
- Kimball and Ross, *The Data Warehouse Toolkit* (dimensional modelling)

**Free resources:**
- GeeksforGeeks DBMS tutorial, with many solved GATE-style questions: https://www.geeksforgeeks.org/dbms/
- CMU 15-445/645 *Intro to Database Systems*: free lecture videos and notes (storage, buffer pools, indexes, joins, concurrency, recovery)
- Stanford CS145 lecture notes on database design
- SQLite documentation: "Query Planning", "Write-Ahead Logging", "File Locking And Concurrency"
- PostgreSQL documentation, chapter "Concurrency Control"
- C. Mohan et al., "ARIES", *ACM TODS* 1992; Berenson et al., "A Critique of ANSI SQL Isolation Levels", SIGMOD 1995
