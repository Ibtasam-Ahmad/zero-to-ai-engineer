# DBMS Fundamentals: University Database Theory

A **database** is an organized collection of related data. A **database management system (DBMS)** is the software that defines that data, stores it, lets many users read and change it at the same time, protects it from crashes and from unauthorized people, and answers questions about it efficiently. This guide walks through the theory behind a DBMS in the same order as the ten notebooks of this folder, which follow a standard BS/MS database course (Silberschatz, Korth and Sudarshan, *Database System Concepts*; Elmasri and Navathe, *Fundamentals of Database Systems*). The practical "how do I write it" side lives in [`../../01_sql`](../../01_sql/01_sql_fundamentals.ipynb); this guide is the "why does it work" side. A folder overview and study order are in [`../README.md`](../README.md).

---

## 1. Why a DBMS exists (notebook 01)

### Data, information, and the file-processing problem

**Data** are raw recorded facts (`72`, `"2026-10-01"`, `"Lahore"`). **Information** is data that has been processed and put in context so that it supports a decision ("the average October temperature in Lahore was 31 °C").

Before DBMSs, organizations kept each department's data in its own files, with programs written for each file. This **file-processing system** has well-known problems, and notebook 01 reproduces each one:

| Problem | What goes wrong | How a DBMS fixes it |
|---|---|---|
| Redundancy and inconsistency | the same address is stored by the registrar and by accounts, and the two copies drift apart | one copy, shared through the schema |
| Difficult access | every new question needs a new program | a declarative query language (SQL) |
| Data isolation | data is scattered across files in different formats | one integrated database |
| Integrity problems | nothing stops `age = -5` | constraints (`CHECK`, `NOT NULL`, keys) |
| Atomicity problems | a crash halfway through a transfer loses money | transactions with rollback |
| Concurrent-access anomalies | two clerks overwrite each other's update (the *lost update*) | concurrency control |
| Security problems | anyone who can read the file can read everything | users, privileges, views |

A DBMS has costs too: licences or operations effort, skilled staff, and overhead that a tiny single-user script does not need.

### Schema, instance, data models

- The **schema** is the description of the database (tables, columns, types, constraints). It is stored in the **catalog** (data dictionary) and changes rarely.
- An **instance** (database state) is the data stored at one moment. It changes with every insert.
- A **data model** is the set of concepts used to describe a schema: hierarchical, network, **relational**, object-relational, document and other NoSQL models. The **ER model** is used for conceptual design.

### The three-schema (ANSI/SPARC) architecture and data independence

```
   external level     view 1   view 2   view 3        (what each user group sees)
                         \       |       /
                  external/conceptual mapping
                              |
   conceptual level      whole logical schema         (tables, keys, constraints)
                              |
                  conceptual/internal mapping
                              |
   internal level        files, pages, indexes         (how it is stored)
```

**Data independence** is the ability to change one level without changing the level above it:

- **Physical data independence**: change the internal schema (move a table to an SSD, add an index) without changing the conceptual schema. This is relatively easy, and every modern DBMS provides it.
- **Logical data independence**: change the conceptual schema (split a table in two) without breaking external views and programs, by redefining the views. This is harder.

### Languages and components

| Group | Purpose | Examples |
|---|---|---|
| DDL (data definition) | define the schema | `CREATE`, `ALTER`, `DROP`, `TRUNCATE` |
| DML (data manipulation) | read and change data | `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `MERGE` |
| DCL (data control) | privileges | `GRANT`, `REVOKE` |
| TCL (transaction control) | transaction boundaries | `COMMIT`, `ROLLBACK`, `SAVEPOINT` |

A DML is **procedural** if you say how to get the data, and **declarative** (like SQL) if you only say what you want.

Inside a DBMS, the **query processor** contains the DDL interpreter, the DML compiler, the query optimizer and the evaluation engine. The **storage manager** contains the authorization and integrity manager, the transaction manager, the file manager and the **buffer manager**, which decides which disk pages are kept in memory (for example with LRU, *least recently used*, replacement).

Architectures: **1-tier** (the application and the DBMS on one machine, like SQLite in a script), **2-tier** (client application talks directly to a database server), **3-tier** (client, then application server, then database). By location, systems are centralized, client-server, parallel, distributed or cloud.

The **impedance mismatch** is the clash between SQL, which works on sets of flat rows, and programming languages, which work on objects and loops one item at a time. Cursors, embedded SQL and **ORMs** (object-relational mappers, see [`../../04_orm`](../../04_orm/01_orm.ipynb)) bridge the two.

*Why it matters for AI:* the training data, labels, feature tables and prediction logs of every ML system need exactly the guarantees in the table above.

---

## 2. Conceptual design with the ER model (notebook 02)

### Building blocks

- An **entity** is a distinguishable real-world thing. An **entity set** is the collection of entities of one type (all students).
- **Attributes** describe entities. They can be **simple** or **composite** (name = first + last), **single-valued** or **multivalued** (several phone numbers), **stored** or **derived** (age derived from birth date), and a **key** attribute identifies each entity uniquely.
- A **relationship set** is a subset of the Cartesian product of entity sets, for example `advisor ⊆ Instructor × Student`. Its **degree** is the number of participating entity sets: unary (recursive, with role names such as *prereq-of*), binary or ternary.

### Constraints on relationships

- The **cardinality ratio** is the *maximum* number of relationships an entity can be in: 1:1, 1:N or M:N.
- **Participation** is the *minimum*. It is **total** (every entity must take part, drawn as a double line) or **partial**.
- **(min, max) notation** gives both numbers, written next to the entity they describe. For "each employee works in exactly one department, and each department has at least one employee": Employee (1,1), Department (1,N).

A **weak entity** has no key of its own. It is identified by its **owner** entity through an **identifying relationship** (total participation) plus a **partial key** (discriminator). Example: `Section(sec_id, semester, year)` belongs to a `Course`.

### Enhanced ER (EER)

- **Specialization** (top-down) and **generalization** (bottom-up) create superclass/subclass hierarchies with **inheritance**.
- Constraints: **disjoint** (an entity is in at most one subclass) or **overlapping**; **total** (every superclass entity is in some subclass) or **partial**.
- A **category** (union type) is a subclass of the *union* of different superclasses (an Owner is a Person *or* a Bank *or* a Company).
- **Aggregation** treats a relationship as an entity, so that it can take part in another relationship.

### Minimum number of tables (a classic exam question)

For two entity sets E1 and E2 joined by one relationship:

| Cardinality | Participation | Minimum tables |
|---|---|---|
| M:N | any | 3 |
| 1:N | any | 2 (foreign key on the N side) |
| 1:1 | both partial | 2 |
| 1:1 | at least one side total | 1 (merge) |

Add one table per multivalued attribute.

### ER → relational mapping algorithm

1. Strong entity → table. Simple attributes become columns, composite attributes are flattened, the key becomes the primary key.
2. Weak entity → table whose primary key = owner key + partial key, with `FOREIGN KEY ... ON DELETE CASCADE`.
3. 1:1 relationship → a foreign key on one side (preferably the side with total participation) plus `UNIQUE`.
4. 1:N relationship → a foreign key on the N side.
5. M:N relationship → a new table whose primary key combines both foreign keys.
6. Multivalued attribute → a new table (owner key, value).
7. n-ary relationship → a new table with n foreign keys.
8. Specialization → option A (a table for the superclass plus one per subclass), B (subclass tables only, which works for total disjoint hierarchies), C (one table with a type column) or D (one table with a Boolean flag per subclass).
9. Category → a surrogate key in the category table, referenced by every superclass.

The **connection trap** is a design mistake: a path of relationships that seems to give a fact but actually generates **spurious** combinations when you join along it. Notebook 02 shows a supplier–part–project example where rebuilding facts from binary relationships produces a tuple that never existed.

---

## 3. The relational model and relational algebra (notebook 03)

### Terms

A **relation** on schema $R(A_1, \dots, A_n)$ is a *set* of **tuples**, where each value comes from the attribute's **domain**. Sets have no duplicates and no order, and values are **atomic**. The **degree** is the number of attributes; the **cardinality** is the number of tuples. `NULL` means "unknown or not applicable".

### Keys

- A **superkey** is any set of attributes whose values identify a tuple uniquely.
- A **candidate key** is a *minimal* superkey: removing any attribute breaks uniqueness.
- The **primary key** is the candidate key you choose. The other candidate keys are **alternate keys**.
- A **foreign key** is a set of attributes that must match a primary key in another relation (or be `NULL`).
- A **surrogate key** is a system-generated identifier with no business meaning.

**Counting superkeys.** If R has n attributes and its only candidate key has k attributes, every superset of that key is a superkey, so there are $2^{\,n-k}$ superkeys. With two keys $K_1, K_2$, use inclusion–exclusion: $|SK| = 2^{n-|K_1|} + 2^{n-|K_2|} - 2^{n-|K_1 \cup K_2|}$. For R(A,B,C,D,E) with keys {A} and {B,C}: $16 + 8 - 4 = 20$.

Data can *refute* a key (two rows with the same value) but can never *prove* one. Keys come from business rules.

### Integrity constraints

Domain constraints (type, `CHECK`), key constraints (`UNIQUE`), **entity integrity** (no primary-key value may be `NULL`), **referential integrity** (foreign keys, with actions `CASCADE`, `SET NULL`, `SET DEFAULT`, `RESTRICT` / `NO ACTION`) and general `CHECK` constraints. In SQLite, foreign-key enforcement is **off** until you run `PRAGMA foreign_keys = ON`, and `STRICT` tables enforce column types.

### The operators

| Operator | Symbol | Meaning | SQL |
|---|---|---|---|
| Selection | $\sigma_{p}(R)$ | rows satisfying p | `WHERE` |
| Projection | $\pi_{A,B}(R)$ | columns A, B, duplicates removed | `SELECT DISTINCT A, B` |
| Rename | $\rho_{S}(R)$ | rename relation or attributes | `AS` |
| Union, difference | $R \cup S$, $R - S$ | union-compatible relations only | `UNION`, `EXCEPT` |
| Cartesian product | $R \times S$ | every pair | `CROSS JOIN` |
| Intersection | $R \cap S = R - (R - S)$ | derived | `INTERSECT` |
| Theta / natural join | $R \bowtie_{\theta} S = \sigma_{\theta}(R \times S)$ | matching pairs | `JOIN ... ON` |
| Outer joins | ⟕ ⟖ ⟗ | keep unmatched rows, padded with NULL | `LEFT/RIGHT/FULL JOIN` |
| Semi-join / anti-join | ⋉ / ▷ | rows of R with / without a match in S | `EXISTS` / `NOT EXISTS` |
| Division | $R \div S$ | values of R paired with **every** tuple of S | double `NOT EXISTS` |
| Grouping | $_{G}\gamma_{f(A)}(R)$ | aggregation per group | `GROUP BY` |

The six **fundamental** operators are σ, π, ρ, ∪, −, ×. All the others can be derived from them. Division, for $R(A,B)$ and $S(B)$:

$$R \div S = \pi_A(R) - \pi_A\big((\pi_A(R) \times S) - R\big)$$

Read it as: take every A value, remove those that are missing at least one S partner.

**Exam patterns:** "not" → difference or anti-join; "all" → division; "the maximum, without aggregates" → difference trick (remove every value that is smaller than some other value); "at least two" → self-join with $\ne$.

**Cardinality facts:** $|R \times S| = |R| \cdot |S|$, and $0 \le |R \bowtie S| \le |R| \cdot |S|$.

**The `NOT IN` trap.** If the subquery returns a `NULL`, `x NOT IN (...)` is never true, so the query returns nothing. `NOT EXISTS` and anti-joins do not have this problem.

### Relational calculus and Codd

**Tuple relational calculus (TRC)** writes queries as $\{ t \mid P(t) \}$; **domain relational calculus (DRC)** as $\{ \langle x_1, \dots, x_n \rangle \mid P \}$. Both are declarative. An expression is **safe** if its answer depends only on values that appear in the database (it is domain-independent); $\{ t \mid \neg (t \in \text{STUDENT}) \}$ is unsafe. **Codd's theorem**: relational algebra, safe TRC and safe DRC have the same expressive power. A language with that power is **relationally complete**, and SQL is more than complete (it adds aggregation and recursion). Codd's 12 rules (numbered 0–12) describe what makes a DBMS truly relational.

**Row vs. column storage:** a row store keeps each tuple together (good for OLTP, fetching whole records); a column store keeps each column together (good for OLAP, scanning one column of many rows). In notebook 03, averaging one column read 3,125 pages in a row store and 391 in a column store.

### Expression trees

Algebra is closed (every result is a relation), so operators nest into **expression trees**. Optimizers rewrite these trees; pushing σ below a join cut the intermediate tuples in notebook 03 from 514 to 47.

---

## 4. Functional dependencies and normalization (notebook 04)

### Anomalies

A table that mixes facts about different things, such as `EMP_DEPT(ssn, ename, dnumber, dname, dmgr_ssn)`, suffers from:

- **update anomaly**: renaming department 5 must change every employee row, and missing one leaves two names;
- **insertion anomaly**: you cannot store a new department until it has an employee;
- **deletion anomaly**: deleting the last employee deletes the department.

### Functional dependencies

$X \to Y$ holds on R if any two tuples that agree on X also agree on Y, in **every legal instance**. An FD is **trivial** if $Y \subseteq X$.

**Armstrong's axioms** (sound and complete):

1. Reflexivity: if $Y \subseteq X$ then $X \to Y$.
2. Augmentation: if $X \to Y$ then $XZ \to YZ$.
3. Transitivity: if $X \to Y$ and $Y \to Z$ then $X \to Z$.

Derived rules: union ($X \to Y, X \to Z \Rightarrow X \to YZ$), decomposition ($X \to YZ \Rightarrow X \to Y$), pseudo-transitivity ($X \to Y, WY \to Z \Rightarrow WX \to Z$).

### Attribute closure

$X^+$ is the set of all attributes determined by X. Algorithm: start with $X^+ = X$; repeat: for each $A \to B$ in F with $A \subseteq X^+$, add B; stop when nothing changes. It runs in polynomial time.

- $X \to Y$ follows from F iff $Y \subseteq X^+$.
- X is a superkey iff $X^+ = R$.

**Worked example (Silberschatz).** $R(A,B,C,G,H,I)$, $F = \{A \to B, A \to C, CG \to H, CG \to I, B \to H\}$.

| Step | FD used | $AG^+$ |
|---|---|---|
| start | | AG |
| 1 | A → B | ABG |
| 2 | A → C | ABCG |
| 3 | CG → H | ABCGH |
| 4 | CG → I | ABCGHI |

$AG^+ = R$, while $A^+ = ABCH$ and $G^+ = G$, so **AG is a candidate key**.

**Finding all keys quickly.** Attributes that never appear on any right-hand side must be in every key (the **core**). Attributes that appear only on right-hand sides are in no key. Try adding the remaining (middle) attributes to the core. For $R(ABCDEH)$, $F = \{A \to B, BC \to D, E \to C, D \to A\}$: E and H never appear on a right side, $EH^+ = EHC$, and adding A, B or D completes it, so the keys are **AEH, BEH, DEH**. A **prime attribute** belongs to some candidate key.

### Covers

$F^+$ is the set of all FDs implied by F; it can be exponentially large (two FDs on three attributes already imply 35). F and G are **equivalent** if each implies every FD of the other. A **canonical cover** (Silberschatz) or **minimal cover** (Elmasri) has single attributes on the right-hand side, no **extraneous** attribute on any left-hand side, and no redundant FD. Example: $\{A \to BC, B \to C, A \to B, AB \to C\}$ reduces to $\{A \to B, B \to C\}$. Covers are not unique.

### Normal forms

| NF | Condition | Removes |
|---|---|---|
| 1NF | atomic values, no repeating groups | lists in a cell |
| 2NF | 1NF, and no non-prime attribute depends on a *proper part* of a candidate key | partial dependencies |
| 3NF | for every non-trivial $X \to A$: X is a superkey **or** A is prime | transitive dependencies |
| BCNF | for every non-trivial $X \to Y$: X is a superkey | all FD-based redundancy |
| 4NF | for every non-trivial MVD $X \twoheadrightarrow Y$: X is a superkey | independent multivalued facts |
| 5NF (PJNF) | every join dependency is implied by the candidate keys | cyclic three-way facts |
| DKNF | every constraint follows from domain and key constraints | every anomaly (theoretical ideal) |

Each form implies the previous: BCNF ⊂ 3NF ⊂ 2NF ⊂ 1NF.

**3NF but not BCNF.** $R(\text{Student}, \text{Course}, \text{Instructor})$ with $\{\text{Student}, \text{Course}\} \to \text{Instructor}$ and $\text{Instructor} \to \text{Course}$. The keys are {Student, Course} and {Student, Instructor}, so every attribute is prime and R is in 3NF. But Instructor is not a superkey, so R violates BCNF. Any BCNF decomposition loses the FD $\{\text{Student}, \text{Course}\} \to \text{Instructor}$.

### Decomposition properties

- **Lossless join**: joining the pieces gives back exactly the original relation, with no spurious tuples. For two pieces: $R_1 \cap R_2 \to R_1$ or $R_1 \cap R_2 \to R_2$ must be in $F^+$. For more pieces, use the **chase** (tableau) test: the decomposition is lossless iff some row becomes all "a" symbols.
- **Dependency preservation**: $(F_1 \cup \dots \cup F_n)^+ = F^+$, where $F_i$ is the projection of $F^+$ onto $R_i$. This lets every FD be checked inside a single table.

Example: $R(A,B,C)$, $F = \{A \to B, B \to C\}$. Splitting into (A,B), (B,C) is lossless (common B → C) and preserving. Splitting into (A,B), (A,C) is lossless (common A → B) but **loses** $B \to C$.

### The two algorithms

| Algorithm | Result | Lossless? | Dependency-preserving? |
|---|---|---|---|
| BCNF decomposition (split on a violating $X \to Y$ into $XY$ and $R - (Y - X)$, repeat) | BCNF | always | not always |
| 3NF synthesis (Bernstein: one table per FD of a canonical cover, add a key table if no table contains a key, drop subsumed tables) | 3NF | always | **always** |

In random trials in notebook 04, BCNF decomposition lost an FD in 67 of 224 cases.

### MVDs, 4NF and 5NF

A **multivalued dependency** $X \twoheadrightarrow Y$ says the set of Y values for an X is independent of the other attributes. Example: an employee's projects and dependents stored in one table must list every combination (16 rows instead of 6 + 5). 4NF splits the table into (Ename, Pname) and (Ename, Dname). A **join dependency** says R equals the join of several projections. The Elmasri SUPPLY example needs three projections; any two of them produce spurious tuples.

### Denormalization

Normalization optimizes for correct writes. Read-heavy derived data (dashboards, ML feature tables) is often **denormalized** on purpose for speed, while a normalized source of truth is kept. In notebook 04, reading a precomputed feature table was 5x faster than recomputing it with joins.

---

## 5. Transactions and concurrency control (notebook 05)

### ACID and states

A **transaction** is a unit of work that must execute completely or not at all.

- **Atomicity**: all or nothing (implemented by undo logging).
- **Consistency**: a correct transaction takes the database from one valid state to another.
- **Isolation**: concurrent transactions do not see each other's intermediate states.
- **Durability**: after commit, changes survive crashes (implemented by redo logging).

States: active → partially committed → committed, or active → failed → aborted.

### Schedules and conflicts

A **schedule** interleaves the operations of several transactions. Two operations **conflict** if they belong to different transactions, access the same item, and at least one is a write (RW, WR or WW conflict). Uncontrolled interleaving causes:

| Anomaly | Example |
|---|---|
| Lost update | T1 and T2 both read A = 100; T1 writes 50, T2 writes 120; T1's update is lost (correct: 70) |
| Dirty read | T2 reads a value T1 wrote but later rolled back |
| Unrepeatable read | T1 reads A twice and gets two values because T2 committed in between |
| Phantom | T1 re-runs a range query and sees new rows inserted by T2 |

### Serializability

- A schedule is **conflict serializable** if it can be turned into a serial schedule by swapping adjacent non-conflicting operations. **Test**: draw the **precedence graph**, with an edge $T_i \to T_j$ when an operation of $T_i$ conflicts with and comes before one of $T_j$. The schedule is conflict serializable iff the graph is **acyclic**, and a topological order gives an equivalent serial order.
- **View serializability** is broader: it also accepts some schedules with **blind writes**, such as $r_1(Q)\, w_2(Q)\, w_1(Q)\, w_3(Q)$. Testing it is NP-complete.

Recoverability: a schedule is **recoverable** if a transaction commits only after every transaction it read from has committed; **cascadeless** if transactions read only committed data; **strict** if no item is read *or overwritten* until its last writer finishes. Strict ⊂ cascadeless ⊂ recoverable.

### Lock-based protocols

Shared (S) locks allow reading, and exclusive (X) locks allow writing. S is compatible with S; X is compatible with nothing.

- **Two-phase locking (2PL)**: a growing phase (acquire only) and then a shrinking phase (release only). 2PL guarantees conflict serializability.
- **Strict 2PL**: hold X locks until commit, which also makes schedules strict (no cascading aborts).
- **Rigorous 2PL**: hold all locks until commit; transactions are serializable in commit order.

**Deadlocks.** Detection: build a **wait-for graph** and abort a victim when there is a cycle. Prevention with timestamps (a smaller timestamp means older):

| Scheme | Requester older than holder | Requester younger than holder |
|---|---|---|
| Wait-die (non-preemptive) | requester waits | requester dies (restarts with its old timestamp) |
| Wound-wait (preemptive) | holder is wounded (rolled back) | requester waits |

Timeouts are a simple alternative.

The **tree protocol** (lock an item only while holding its parent) is deadlock-free and serializable without being two-phase. **Multiple-granularity locking** adds intention locks so a transaction can lock a whole table or a single row efficiently:

| Requested \ held | IS | IX | S | SIX | X |
|---|---|---|---|---|---|
| IS | ✓ | ✓ | ✓ | ✓ | ✗ |
| IX | ✓ | ✓ | ✗ | ✗ | ✗ |
| S | ✓ | ✗ | ✓ | ✗ | ✗ |
| SIX | ✓ | ✗ | ✗ | ✗ | ✗ |
| X | ✗ | ✗ | ✗ | ✗ | ✗ |

### Timestamp, optimistic and multiversion methods

**Timestamp ordering**: every item Q keeps R-TS(Q) and W-TS(Q).

- $T_i$ reads Q: if $TS(T_i) < W\text{-}TS(Q)$, roll $T_i$ back; otherwise read and set $R\text{-}TS(Q) = \max(R\text{-}TS(Q), TS(T_i))$.
- $T_i$ writes Q: if $TS(T_i) < R\text{-}TS(Q)$, roll back; if $TS(T_i) < W\text{-}TS(Q)$, roll back (or, under **Thomas' write rule**, simply ignore the obsolete write); otherwise write and set $W\text{-}TS(Q) = TS(T_i)$.

No transaction ever waits, so there are no deadlocks. **Optimistic (validation-based)** concurrency runs read, validation and write phases, and checks for conflicts only at commit, which suits low contention. **MVCC** keeps several versions so readers see a consistent **snapshot** and never block writers. Plain **snapshot isolation** still allows **write skew**; serializable snapshot isolation (SSI, used by PostgreSQL's `SERIALIZABLE`) fixes it.

### SQL isolation levels

| Level | Dirty read | Unrepeatable read | Phantom |
|---|---|---|---|
| Read uncommitted | possible | possible | possible |
| Read committed | no | possible | possible |
| Repeatable read | no | no | possible |
| Serializable | no | no | no |

Real systems differ from this table. SQLite allows one writer at a time and reports `database is locked`; WAL mode lets readers and the writer proceed in parallel.

---

## 6. Recovery and storage (notebook 06)

### Failures and storage

| Failure | What is lost | Remedy |
|---|---|---|
| Transaction failure | that transaction's work | undo it |
| System crash | main memory (buffer pool) | undo + redo from the log |
| Disk failure | the disk's contents | restore a backup and replay the archived log |

**Volatile** storage (DRAM) loses data on power loss; **non-volatile** storage (SSD, HDD) keeps it; **stable** storage is an abstraction that is never lost, approximated by keeping several copies on independent devices. Disk access is about $10^5$ times slower than DRAM, which is why costs are counted in **block I/Os**.

### Log-based recovery

An update log record $\langle T_i, X, V_{old}, V_{new} \rangle$ stores the old value (for undo) and the new value (for redo), alongside $\langle T_i\ \text{start} \rangle$, $\langle T_i\ \text{commit} \rangle$ and $\langle T_i\ \text{abort} \rangle$ records.

**Write-ahead logging (WAL) rule:** (1) a log record must reach stable storage before the data page it describes is written to disk; (2) a transaction is committed only once its commit record is on stable storage.

- **Deferred modification** writes data only after commit, so recovery needs only **redo**.
- **Immediate modification** may write uncommitted data, so recovery needs **undo and redo**.

After a crash: the **redo list** holds transactions with a commit (or abort) record; the **undo list** holds transactions with a start record but neither. Undo runs backwards through the log, redo runs forwards. Both are **idempotent**, so a crash during recovery is harmless.

**Worked example.** Log at the crash: `<T0 start> <T0,A,1000,950> <T0,B,2000,2050> <T0 commit> <T1 start> <T1,C,700,600>`. T0 is redone (A = 950, B = 2050); T1 is undone (C = 700).

**Checkpoints** flush the log and dirty pages and record the active transactions, so recovery starts near the last checkpoint. In notebook 06, checkpointing every 70 transactions cut the records examined from about 2,000 to a few hundred.

### ARIES

ARIES is the recovery algorithm used by real systems. Every log record has a **log sequence number (LSN)**; every page stores the **PageLSN** of the last update applied to it; a **dirty page table** stores each dirty page's recLSN; a transaction table stores each active transaction's last LSN. After a crash:

1. **Analysis**: scan forward from the last checkpoint to rebuild the tables and find the loser transactions.
2. **Redo**: *repeat history* from the smallest recLSN, applying a record only if the page's PageLSN is smaller than the record's LSN.
3. **Undo**: roll back the losers, writing **compensation log records (CLRs)** so that nothing is undone twice.

**Shadow paging** is the alternative to logging: copy-on-write pages plus an atomic swap of the page-table pointer at commit. It needs no undo or redo, but forces pages at commit, scatters data, and needs garbage collection.

### Buffer management

The buffer manager keeps a **pin count** (pages in use cannot be evicted) and a **dirty bit** per frame. Replacement policies include LRU, Clock (an approximation of LRU) and MRU. MRU wins for repeated sequential scans larger than the buffer, where LRU suffers *sequential flooding*. The write policy determines the recovery algorithm:

| | Force (write pages at commit) | No-force |
|---|---|---|
| **No-steal** (uncommitted pages never written) | no undo, no redo | redo only |
| **Steal** | undo only | undo **and** redo (ARIES, real systems) |

### RAID

| Level | Idea | Usable capacity of n disks | Failures survived |
|---|---|---|---|
| RAID 0 | striping | n | 0 |
| RAID 1 | mirroring | 1 disk's worth (n-way mirror) | n − 1 |
| RAID 5 | striping + one distributed XOR parity block | n − 1 | 1 |
| RAID 6 | two parity blocks | n − 2 | 2 |
| RAID 10 | mirrored pairs, striped | n / 2 | at least 1 (one per pair) |

Parity $P = D_0 \oplus D_1 \oplus D_2$, so a lost block equals the XOR of the survivors. A RAID 5 small write costs 4 I/Os (read old data and old parity, write new data and new parity). RAID protects against disk failure, **not** against a mistaken `DELETE`. That is what backups and **point-in-time recovery (PITR)** are for, sized by RPO (how much data you may lose) and RTO (how long recovery may take).

### File organization

With block size B and record size R, the **blocking factor** is $bfr = \lfloor B / R \rfloor$, and a file of r records needs $b = \lceil r / bfr \rceil$ blocks. Variable-length records live in **slotted pages**: a header holds slot offsets, so records can move inside the page while their record ID (page, slot) stays stable.

| File organization | Equality search on key | Range search | Insert |
|---|---|---|---|
| Heap (unordered) | b/2 on average, b worst | b | 1 read + 1 write at the end |
| Sorted (sequential) | $\log_2 b$ | $\log_2 b$ + matching blocks | expensive (shift records) |
| Hashed | ≈ 1 (+ overflow chains) | b (no order) | ≈ 1 read + 1 write |

---

## 7. Indexing (notebook 07)

### Vocabulary

- A **primary (clustering) index** is built on the attribute the file is sorted by. It can be **sparse**, with one entry per block.
- A **secondary index** is on any other attribute and must be **dense**, with one entry per record. A table has at most one clustering order but can have many secondary indexes.
- A **multi-level index** is an index on the index. Its cost is about $\log_{fo} b$, where *fo* is the fan-out.

### B+ trees

A B+ tree of order n (Silberschatz) is balanced (every leaf is at the same depth); every internal node except the root has between $\lceil n/2 \rceil$ and n children, and every leaf holds between $\lceil (n-1)/2 \rceil$ and n − 1 keys; all data pointers are in the **leaves**, which are linked for range scans. A **B-tree** also stores data pointers in internal nodes, which saves a little space but gives lower fan-out and no easy range scan. That is why databases use B+ trees.

- **Insert**: put the key in its leaf. If the leaf overflows, split it and **copy up** the first key of the new leaf. An internal node that overflows splits and **moves up** its middle key. The tree grows at the root.
- **Delete**: remove the key. If a node underflows, **borrow** from a sibling or **merge** with it. The tree shrinks at the root.

**Exam formulas.** An internal node with n pointers (P bytes each) and n − 1 keys (K bytes each) must fit in a block of B bytes:

$$n \cdot P + (n-1) \cdot K \le B \;\Rightarrow\; n = \left\lfloor \frac{B + K}{P + K} \right\rfloor$$

With B = 4096 and K = P = 8, n = ⌊4104 / 16⌋ = 256. A leaf holds $\lfloor (B - P) / (K + P_r) \rfloor$ entries, where $P_r$ is a record pointer. The height for N keys is at most about $\lceil \log_{\lceil n/2 \rceil} N \rceil$, so 3–4 levels cover billions of keys. **Worked example:** 1,000,000 records at 100 per page = 10,000 pages; a scan reads about 5,000 pages, while a B+ tree with 100 keys per node has 3 levels and needs 3 + 1 = 4 reads.

### Hashing, bitmaps, inverted indexes

| Index | Best for | Cost of an equality lookup | Range queries? |
|---|---|---|---|
| B+ tree | equality and ranges, `ORDER BY` | h + 1 | yes |
| Static hash | equality | ≈ 1, worse as overflow chains grow | no |
| Extendible hash | equality on growing data | ≈ 1 (directory + bucket) | no |
| Linear hash | equality, no directory | ≈ 1 + overflow | no |
| Bitmap | low-cardinality columns, AND/OR/COUNT | bit operations | via bitmaps |
| Inverted | text search (term → posting list) | intersect sorted lists | n/a |

**Extendible hashing** uses a directory of $2^{d}$ pointers, where d is the **global depth**. Each bucket has a **local depth** $d' \le d$. When a full bucket with $d' = d$ overflows, the directory doubles; when $d' < d$, only the bucket splits. **Linear hashing** splits buckets in round-robin order, with no directory. **BM25** ranks documents from an inverted index by term frequency, inverse document frequency and document length.

### Indexes in practice

A **covering index** contains every column a query needs, so the table is never touched. A **clustered** table (SQLite `WITHOUT ROWID`, or InnoDB's primary key) stores rows in key order, and was 5.6x faster than a secondary index for a range query in the notebook. Indexes **hurt** writes (4 indexes made inserts 2.6x slower) and lose to a full scan when a query matches a large fraction of rows (low selectivity). A function applied to an indexed column (`lower(email)`) prevents the index from being used, unless an expression index exists.

---

## 8. Query processing and optimization (notebook 08)

### Pipeline and cost model

```
SQL --parse--> parse tree --translate--> relational algebra --optimize--> evaluation plan --execute--> rows
```

Notation: $n_r$ = number of tuples of r, $b_r$ = blocks of r, M = buffer blocks in memory, $h_i$ = index height. Cost is counted in **block transfers** (and seeks).

### Selection

- Linear scan: $b_r$ (or $b_r/2$ on average for an equality on a key).
- Primary B+ tree, equality on the key: $h_i + 1$.
- Clustering index, equality on a non-key: $h_i + $ the number of matching blocks.
- Secondary index: $h_i + $ one block per matching record, which can be worse than a scan.

### External merge sort

Pass 0 creates $\lceil b_r / M \rceil$ sorted **runs** of M blocks. Each merge pass merges M − 1 runs at a time. Counting the final write:

$$\text{cost} = 2\, b_r \left(1 + \left\lceil \log_{M-1} \lceil b_r / M \rceil \right\rceil \right)$$

Example: $b_r = 108$, M = 5 → 22 runs → 6 → 2 → 1, i.e. 3 merge passes, cost $2 \cdot 108 \cdot 4 = 864$, which matches the notebook's measurement. Two passes suffice when $M \gtrsim \sqrt{b_r}$.

### Join algorithms (r outer, s inner)

| Algorithm | Block transfers | Notes |
|---|---|---|
| Nested-loop | $n_r \cdot b_s + b_r$ | any condition |
| Block nested-loop | $\lceil b_r / (M-2) \rceil \cdot b_s + b_r$ | $b_r + b_s$ if r fits in memory |
| Index nested-loop | $b_r + n_r \cdot c$ | c = cost of one index lookup on s |
| Sort-merge | $b_r + b_s$ + cost of sorting | equi-joins; output is sorted |
| Grace hash | $3(b_r + b_s) + 4 n_h$ | equi-joins; each partition of the build input must fit in memory |

**Worked example.** $n_r = 2000$, $b_r = b_s = 200$, M = 50. Nested-loop: $2000 \cdot 200 + 200 = 400{,}200$. Block nested-loop: $\lceil 200/48 \rceil \cdot 200 + 200 = 1{,}200$. Hash join: $3 \cdot 400 = 1{,}200$ plus a little for partition overflow. Same answer, about 333x fewer transfers than the plain nested loop.

Duplicate elimination and grouping use sorting or hashing with running aggregates. **Pipelining** (the iterator model: `open`, `next`, `close`) passes tuples between operators without temporary tables. **Blocking** operators such as sort and hash-build break the pipeline. With `LIMIT 5`, pipelining read 12 tuples instead of 30,000.

### Heuristic optimization

Equivalence rules include: a conjunctive selection splits into a cascade, $\sigma_{p \wedge q}(E) = \sigma_p(\sigma_q(E))$; a selection over a product becomes a join, $\sigma_\theta(E_1 \times E_2) = E_1 \bowtie_\theta E_2$; joins are commutative and associative; a selection on attributes of one input moves below the join, $\sigma_p(E_1 \bowtie E_2) = \sigma_p(E_1) \bowtie E_2$. Heuristics: split conjunctions, **push σ down**, replace σ(×) with ⋈, push π down, and do the most selective joins first.

### Cost-based optimization

The catalog keeps $n_r$, $b_r$ and $V(A, r)$, the number of distinct values of A in r, plus **histograms**. Estimates:

- $\sigma_{A = v}(r)$: about $n_r / V(A, r)$ tuples (the uniformity assumption).
- Conjunction: multiply the selectivities (the independence assumption).
- Natural join on A: about $\dfrac{n_r \cdot n_s}{\max(V(A,r), V(A,s))}$.

Uniformity and independence often fail on real data, and histograms fix much of that error (notebook 08: mean error 31% of the table with min/max only, 4.9% with an equi-width histogram). **System R** (Selinger et al., 1979) picks the join order by **dynamic programming** over subsets of relations, classically restricted to left-deep trees and keeping "interesting orders". In practice, read plans with `EXPLAIN QUERY PLAN`, decorrelate subqueries, add the right index, and write **sargable** predicates (comparisons on the bare column, so an index can be used).

---

## 9. Distributed databases, warehousing and security (notebook 09)

### Distribution

A **distributed database** appears as one database but is stored at several sites. **Homogeneous** systems run the same DBMS everywhere; **heterogeneous** (federated) systems integrate different ones.

**Fragmentation:** horizontal (by rows, $\sigma$, rebuilt with ∪), vertical (by columns, $\pi$ keeping the key, rebuilt with ⋈), or mixed. It is correct only if it is **complete**, **reconstructable** and **disjoint**.

**Replication:** synchronous replication keeps fresh replicas but slows commits; asynchronous replication gives fast commits but stale reads and possible data loss on fail-over. With N copies, write quorum W and read quorum R, every read overlaps the latest write iff

$$R + W > N$$

**Distributed queries** minimize the data shipped between sites. A **semi-join** ships only the join keys to the other site, reduces the other relation there, and ships back only the matching rows.

**Two-phase commit (2PC):** phase 1, the coordinator sends PREPARE and every participant force-writes its log and votes YES or NO; phase 2, the coordinator decides COMMIT only if all voted YES, logs the decision and tells everyone. 2PC is atomic but **blocking**: if the coordinator fails after the votes, prepared participants must wait. **3PC** adds a pre-commit phase and is non-blocking only if there are no network partitions. Real systems replicate the coordinator with **Paxos** or **Raft**; a majority quorum of $2f + 1$ nodes tolerates f failures.

**CAP theorem** (Brewer 2000; proved by Gilbert and Lynch 2002): during a network **partition**, a system cannot be both **consistent** (linearizable) and **available**. **PACELC** (Abadi) adds: *else*, when there is no partition, trade **latency** against consistency. **BASE** (basically available, soft state, eventually consistent) is the alternative to ACID that many NoSQL systems choose.

**Sharding:** by range (simple, but recent keys pile onto one shard), by hash (even spread), by directory, or by geography. **Consistent hashing** places servers and keys on a ring, so adding a server moves only about $1/N$ of the keys. In the notebook, adding a fifth server moved 19.3% of keys with consistent hashing versus 79.7% with `key mod N`.

### Data warehousing

A **data warehouse** (Inmon) is subject-oriented, integrated, time-variant and non-volatile. Data flows from operational sources through ETL/ELT into the warehouse, then to data marts and BI tools.

| | OLTP | OLAP |
|---|---|---|
| Workload | many short reads and writes | few large read-only scans and aggregations |
| Schema | normalized (3NF/BCNF) | dimensional (star/snowflake) |
| Data | current | historical |
| Storage | row store | column store |

**Dimensional modelling** (Kimball): a **fact table** holds measures at a declared **grain** (for example one row per product per basket), with foreign keys to **dimension tables** (date, store, product, customer). Measures can be **additive** (sales amount), **semi-additive** (stock level, which must not be summed over time; the notebook shows the wrong sum, 10,346, next to the correct month-end value, 595) or non-additive (ratios). A **star schema** has denormalized dimensions and needs one join per dimension; a **snowflake** normalizes the dimensions; a **galaxy** (fact constellation) shares **conformed** dimensions between several fact tables. **Slowly changing dimensions**: type 1 overwrites the old value, type 2 adds a new versioned row with valid-from and valid-to dates.

**OLAP operations:** roll-up (aggregate up a hierarchy: day → month → year), drill-down (the reverse), slice (fix one dimension), dice (restrict several dimensions), pivot (rotate the axes). ROLAP runs them as SQL on relational tables, MOLAP on a multidimensional array (cube), and HOLAP mixes the two. Data marts can be dependent (fed from the warehouse) or independent.

**KDD** (knowledge discovery in databases): selection → preprocessing → transformation → data mining → interpretation. Association rules use **support** (the fraction of baskets containing A and B) and **confidence** (P(B | A)).

**Big-data stores:** HDFS (large blocks replicated three times), HBase (sorted, sparse, versioned wide-column store), Hive (SQL over files), and the **lakehouse** (Parquet files plus a Delta Lake or Iceberg transaction log, which gives ACID commits and time travel on object storage).

### Security

- **Authentication** checks who you are (salted password hashes). **Authorization** checks what you may do: `GRANT ... WITH GRANT OPTION`, `REVOKE` with cascading revocation, and **role-based access control (RBAC)**. Views and masking limit what each role can see.
- **SQL injection**: user input is concatenated into SQL (`' OR '1'='1`). The fix is **parameterized queries**, never string building.
- Encryption in transit (TLS) and at rest; **audit trails** of who changed what.
- **The statistical-database inference problem**: even with only aggregate queries allowed, a **tracker** (the difference of two allowed queries) can reveal one person's value. Minimum query-set sizes do not stop it; **differential privacy** (adding calibrated noise) does.
- GDPR-style **data minimization** and pseudonymization: store only what you need, and replace identifiers with pseudonyms.

---

## 10. Designing a database end to end (notebook 10)

The industry project ties everything together for an online-course platform. The design process:

1. **Requirements and numbered business rules**, each mapped to the place it is enforced (constraint, trigger, application code or test).
2. **ER diagram** (9 entities, a weak entity, an associative entity) → **relational mapping**, with composite foreign keys that make a cross-table rule impossible to break.
3. **FD analysis**: closure, candidate keys, BCNF decomposition, chase test (lossless), dependency-preservation test. The ER route and the FD route should arrive at the same schema; if they disagree, one is wrong.
4. **DDL**: `STRICT` tables, `CHECK`, `UNIQUE` (case-insensitive email), triggers, plus negative tests that try to break each rule.
5. **Realistic data** (about 50,000 rows) loaded through all the constraints in one transaction.
6. **Business queries** with window functions; **indexes** chosen from `EXPLAIN QUERY PLAN` and measured, weighing their write cost.
7. **Transactions** for enrolment + payment: `BEGIN IMMEDIATE`, an atomic conditional `UPDATE` for limited coupons, an **idempotency key** so a retried payment is not charged twice, and rollback on a declined card.
8. **Data-quality tests** in SQL, and a **point-in-time** ML feature table (features computed only from data available at prediction time, to avoid leakage).
9. **Operations**: transactional, idempotent migrations; a backup-and-restore drill; query monitoring and a health check.

This is the same sequence that [`../../../22_ML_System_Design/03_relational_db_design.ipynb`](../../../22_ML_System_Design/03_relational_db_design.ipynb) applies to ML metadata, and the feature table is what a [feature store](../../../15_MLOps/12_feature_stores.ipynb) serves.

---

## Summary of key formulas

| Topic | Formula |
|---|---|
| Superkeys with one key of size k | $2^{\,n-k}$ |
| Superkey test | $X^+ = R$ |
| Lossless binary decomposition | $R_1 \cap R_2 \to R_1$ or $R_1 \cap R_2 \to R_2 \in F^+$ |
| Division | $\pi_A(R) - \pi_A((\pi_A(R) \times S) - R)$ |
| Blocking factor | $bfr = \lfloor B/R \rfloor$, $b = \lceil r / bfr \rceil$ |
| B+ tree order | $n = \lfloor (B+K)/(P+K) \rfloor$ |
| B+ tree height bound | $\lceil \log_{\lceil n/2 \rceil} N \rceil$ |
| External sort | $2 b_r (1 + \lceil \log_{M-1} \lceil b_r/M \rceil \rceil)$ |
| Block nested-loop join | $\lceil b_r/(M-2) \rceil \cdot b_s + b_r$ |
| Hash join | $3(b_r + b_s) + 4 n_h$ |
| Equality selectivity | $n_r / V(A, r)$ |
| Join size estimate | $n_r n_s / \max(V(A,r), V(A,s))$ |
| Quorum overlap | $R + W > N$ |
| Consensus fault tolerance | $2f + 1$ nodes tolerate f failures |

---

## Glossary

- **ACID** — atomicity, consistency, isolation, durability: the four guarantees of a transaction.
- **Aggregation (EER)** — treating a relationship as an entity so it can take part in another relationship.
- **Anomaly (update/insert/delete)** — an inconsistency or loss of information caused by storing one fact in many rows.
- **ANSI/SPARC architecture** — the external, conceptual and internal schema levels.
- **ARIES** — a steal/no-force recovery algorithm with analysis, redo and undo phases and CLRs.
- **Armstrong's axioms** — reflexivity, augmentation, transitivity: sound and complete rules for FDs.
- **Attribute closure ($X^+$)** — all attributes functionally determined by X.
- **B+ tree** — a balanced multi-way search tree with data in linked leaves.
- **BASE** — basically available, soft state, eventually consistent.
- **BCNF** — every non-trivial FD has a superkey on its left side.
- **Bitmap index** — one bit vector per distinct value, for low-cardinality columns.
- **Buffer manager** — the component that caches disk pages in memory and chooses which to evict.
- **CAP theorem** — during a partition, a distributed system must choose consistency or availability.
- **Candidate key** — a minimal superkey.
- **Canonical / minimal cover** — a simplest FD set equivalent to F.
- **Cardinality (relation)** — the number of tuples; **cardinality ratio** — the 1:1, 1:N or M:N limit on a relationship.
- **Cascadeless schedule** — transactions read only committed data.
- **Checkpoint** — a log point that bounds how far back recovery must read.
- **CLR** — compensation log record, written when an update is undone.
- **Conflict serializable** — equivalent to a serial schedule by swapping non-conflicting operations; the precedence graph is acyclic.
- **Consistent hashing** — a hash ring where adding a node moves only about 1/N of the keys.
- **Covering index** — an index containing every column a query needs.
- **Data independence** — changing one schema level without changing the level above.
- **Data warehouse** — a subject-oriented, integrated, time-variant, non-volatile store for analysis.
- **DDL / DML / DCL / TCL** — the language groups for schema, data, privileges and transactions.
- **Deadlock** — a cycle of transactions each waiting for a lock another holds.
- **Degree** — the number of attributes of a relation, or of entity sets in a relationship.
- **Denormalization** — deliberately storing redundant data to speed up reads.
- **Dependency preservation** — every FD can be checked within a single decomposed table.
- **Dimension / fact table** — descriptive context / numeric measures at a declared grain.
- **Division (÷)** — the relational operator for "for all" queries.
- **DKNF** — every constraint follows from domain and key constraints.
- **Extendible hashing** — dynamic hashing with a doubling directory and global/local depths.
- **Foreign key** — attributes that must match a key in another relation.
- **Fragmentation** — splitting a relation by rows (horizontal) or columns (vertical) across sites.
- **Functional dependency (FD)** — $X \to Y$: equal X values imply equal Y values.
- **Impedance mismatch** — the clash between set-based SQL and object-based programming languages.
- **Index (primary/secondary, dense/sparse)** — an auxiliary structure that speeds up lookups.
- **Instance** — the data in the database at one moment.
- **Intention lock (IS, IX, SIX)** — a lock announcing finer-grained locks below it.
- **Inverted index** — maps each term to the list of documents containing it.
- **Isolation level** — how much interference between concurrent transactions is allowed.
- **Lossless join** — joining the decomposed tables gives back exactly the original.
- **LSN** — log sequence number, the unique, increasing ID of a log record.
- **MVCC** — multiversion concurrency control; readers see a snapshot.
- **MVD ($X \twoheadrightarrow Y$)** — multivalued dependency, the basis of 4NF.
- **Normal form (1NF–5NF)** — rules that remove redundancy.
- **OLAP / OLTP** — analytical vs. transactional workloads.
- **Participation (total/partial)** — whether every entity must take part in a relationship.
- **PACELC** — if partitioned, choose A or C; else choose latency or consistency.
- **Precedence graph** — the conflict graph used to test serializability.
- **Prime attribute** — an attribute that is part of some candidate key.
- **Quorum** — the number of replicas that must take part in a read (R) or write (W).
- **RAID** — combining disks for speed (striping) and safety (mirroring, parity).
- **Recoverable schedule** — a transaction commits only after those it read from have committed.
- **Relation** — a set of tuples over a schema.
- **Relational algebra / calculus** — procedural / declarative formal query languages.
- **Sargable** — a predicate written so an index can be used.
- **Schema** — the structure of the database.
- **Semi-join** — the tuples of R that have a match in S; used to reduce data shipped between sites.
- **Serializable** — equivalent to some serial execution.
- **Slotted page** — a page layout with a slot directory for variable-length records.
- **Slowly changing dimension (SCD)** — type 1 overwrites, type 2 keeps history.
- **Snapshot isolation** — each transaction reads a consistent snapshot; allows write skew.
- **Star / snowflake / galaxy schema** — denormalized / normalized dimensions / shared dimensions.
- **Steal / force** — whether uncommitted pages may be written to disk / whether pages must be written at commit.
- **Strict schedule** — no item is read or overwritten until its last writer finishes.
- **Superkey** — a set of attributes that identifies tuples uniquely.
- **System R optimizer** — dynamic programming over join orders using cost estimates.
- **Thomas' write rule** — ignore an obsolete write in timestamp ordering.
- **Timestamp ordering** — concurrency control that orders conflicts by transaction timestamps.
- **Two-phase commit (2PC)** — the prepare/vote then commit/abort protocol for distributed atomicity.
- **Two-phase locking (2PL)** — acquire all locks before releasing any; strict and rigorous variants hold locks to commit.
- **View serializable** — equivalent in reads-from and final writes to a serial schedule.
- **WAL (write-ahead logging)** — log records reach stable storage before the data pages they describe.
- **Wait-die / wound-wait** — timestamp-based deadlock-prevention schemes.
- **Weak entity** — an entity identified through its owner plus a partial key.
