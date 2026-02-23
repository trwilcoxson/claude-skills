# Architecture Anti-Patterns: Detection and Remediation Guide

## What are Anti-Patterns?

Anti-patterns are commonly recurring solutions that appear beneficial but create more problems than they solve. They are distinct from simple "bad practices" in an important way: anti-patterns have a seductive appeal that makes them tempting. They often start as reasonable decisions that degrade over time, or they solve an immediate problem while creating larger systemic issues. A bad practice is something everyone knows is wrong. An anti-pattern is something that looks right until it is too late.

The study of anti-patterns is valuable for three reasons. First, detection: naming a pattern makes it visible. Teams that can identify "distributed monolith" or "lava flow" can discuss and address the problem. Second, prevention: knowing the common traps helps architects avoid them proactively. Third, remediation: each anti-pattern has known remediation strategies that provide a path forward.

Anti-patterns exist at every level: code, design, architecture, process, and organization. This guide focuses on architecture-level anti-patterns -- structural problems that affect the system as a whole, not individual methods or classes. These are the most expensive to fix because they require coordinated, cross-cutting changes.

---

## Anti-Pattern Catalog

### Category 1: Structural Anti-Patterns

---

#### 1. Big Ball of Mud

**Also known as:** Spaghetti architecture, shantytown

**Description:** The system has no discernible architecture. Every component can potentially communicate with every other component. There are no clear boundaries, layers, or modules. The dependency graph is a dense, tangled mesh. Changes anywhere can break anything anywhere else.

**Detection signals:**
- High coupling metrics: dependency graph density approaches a complete graph
- Any module can import any other module with no restriction
- No clear layering or boundary enforcement
- New developers say "I don't know where to put this"
- Changes require "shotgun surgery" across many files

**Impact:** Change is extremely expensive and risky. Onboarding new developers takes months. Testing is nearly impossible because nothing can be tested in isolation. The system is fragile -- small changes cause unexpected failures in unrelated areas.

**Remediation:** Identify natural seams in the system. Define module boundaries and enforce them (linting rules, build constraints). Introduce a dependency rule: inner modules must not know about outer modules. Apply the Strangler Fig pattern to gradually extract well-defined modules from the mud. This is a long-term effort measured in quarters, not sprints.

**Grep pattern:**
```bash
# Measure dependency graph density (JS/TS)
madge --image dependency-graph.svg src/
madge --summary src/

# Count cross-directory imports (Python)
grep -r "^from " src/ | awk -F'from ' '{print $2}' | sort | uniq -c | sort -rn
```

---

#### 2. God Class / God Module

**Also known as:** Blob, monster class, kitchen sink module

**Description:** A single class or module has accumulated far too many responsibilities. It knows too much, does too much, and everything depends on it. It violates the Single Responsibility Principle at a massive scale. It is often the oldest file in the codebase and the one everyone dreads modifying.

**Detection signals:**
- File exceeds 1,000 lines of code
- Class has more than 20 public methods
- Module has more than 50 exports
- File has the highest churn rate in the repo (most commits)
- Multiple unrelated features are implemented in the same file

**Impact:** Merge conflicts are frequent. Testing is difficult because setup is complex. Understanding the class requires understanding the entire domain. Parallel development is blocked because everyone needs to modify the same file.

**Remediation:** Identify clusters of related methods and extract them into focused classes/modules. Use the Extract Class refactoring repeatedly. Apply the Interface Segregation Principle: if different consumers use different subsets of the interface, split accordingly. Introduce a facade if needed for backward compatibility during migration.

**Grep pattern:**
```bash
# Find large files
find . -name "*.py" -exec wc -l {} \; | sort -rn | head -20
find . -name "*.ts" -exec wc -l {} \; | sort -rn | head -20

# Count methods per class (Python)
grep -c "def " src/models/user.py

# Count exports per module (JS/TS)
grep -c "^export" src/utils/index.ts
```

---

#### 3. Distributed Monolith

**Also known as:** Microliths, worst of both worlds

**Description:** The system is deployed as microservices but retains all the coupling characteristics of a monolith. Services must be deployed together, they share a database, they make synchronous calls in chains, and a change in one service requires coordinated changes in multiple others. The team has the operational complexity of microservices with none of the benefits.

**Detection signals:**
- Services must be deployed together or in a specific order
- Multiple services read/write the same database tables
- Long synchronous call chains (A calls B calls C calls D)
- Shared libraries containing domain logic (not just utilities)
- A feature change requires modifying 3+ services simultaneously

**Impact:** Deployment is complex and risky (all-or-nothing). Latency is high due to synchronous chains. Failure cascading is rampant because services are tightly coupled. Development is slow because cross-service coordination is required for every feature. Operational costs are high with no corresponding benefit.

**Remediation:** Decide: go back to a monolith (seriously -- a well-structured monolith is better than a distributed monolith) or fix the coupling. Break shared databases by giving each service its own data store. Replace synchronous chains with asynchronous messaging. Eliminate shared domain libraries. Align service boundaries with business capabilities, not technical layers.

**Grep pattern:**
```bash
# Find shared database connections across services
grep -r "DATABASE_URL\|connection_string\|DB_HOST" services/ --include="*.env" --include="*.yaml"

# Find synchronous inter-service HTTP calls
grep -rn "requests.get\|requests.post\|fetch(\|axios\." services/ --include="*.py" --include="*.ts"

# Find shared libraries in multiple service dependency files
diff <(cat services/svc-a/requirements.txt | sort) <(cat services/svc-b/requirements.txt | sort)
```

---

#### 4. Lasagna Architecture

**Also known as:** Layer cake, abstraction overload, too many layers

**Description:** The system has too many layers of abstraction. A simple operation like "save a user" passes through a controller, a service, a domain model, a repository interface, a repository implementation, a data mapper, a DTO, and a database adapter. Each layer adds ceremony but no value. Most layers are pure pass-through: they receive data and forward it unchanged.

**Detection signals:**
- More than 5 layers in a typical call stack
- Pass-through methods that add no logic, validation, or transformation
- A single feature change requires touching 6+ files across layers
- Developers copy-paste across layers (same field names, same shapes)
- New developers ask "why do we need all these layers?"

**Impact:** Development is slow because every feature requires boilerplate across all layers. Cognitive load is high because developers must navigate many files to understand a single flow. The codebase is larger than necessary, increasing maintenance burden. The layers create a false sense of separation: they are structurally separate but semantically identical.

**Remediation:** Collapse pass-through layers. If a service layer does nothing but call the repository, remove it. Apply the YAGNI principle to abstraction: add layers only when they provide value (validation, transformation, caching, different data shapes). Consider vertical slices (feature-based organization) instead of horizontal layers.

**Grep pattern:**
```bash
# Find pass-through methods (methods that just delegate)
# Look for single-line method bodies that call another method with same args
grep -A 2 "def " src/services/ | grep "return self\.\|return await self\."

# Count files touched per feature (via git)
git log --oneline --name-only --since="30 days" | grep -v "^[a-f0-9]" | sort | uniq -c | sort -rn
```

---

#### 5. Golden Hammer

**Also known as:** Silver bullet, when all you have is a hammer

**Description:** The team uses one technology, pattern, or tool for everything, regardless of fitness. PostgreSQL for OLTP, analytics, caching, and message queuing. REST for every integration, including real-time streaming. Kubernetes for every deployment, including a simple cron job. The familiar tool is applied everywhere, even where a specialized tool would be dramatically better.

**Detection signals:**
- Same database technology used for transactional, analytical, and caching workloads
- Same communication pattern (REST, gRPC, events) used universally regardless of requirements
- Same framework for all services regardless of their nature
- Technology decisions made without evaluating alternatives
- "We already know X, so let's use X" as the primary decision criteria

**Impact:** Suboptimal performance (wrong tool for the job). Increased complexity (forcing a tool to do something it was not designed for). Missed opportunities for better solutions. Vendor lock-in to a single ecosystem.

**Remediation:** Evaluate each technical decision independently based on requirements. Use Architecture Decision Records (ADRs) to document why a technology was chosen for a specific use case. Introduce polyglot persistence where workloads have genuinely different needs. Balance standardization benefits against fitness-for-purpose.

**Grep pattern:**
```bash
# Check for single DB type across all services
grep -r "postgres\|mysql\|mongodb" services/ --include="*.yaml" --include="*.env" | awk -F: '{print $1}' | sort -u
```

---

#### 6. Circular Dependencies

**Also known as:** Import cycles, dependency loops

**Description:** Module A depends on Module B, which depends on Module C, which depends on Module A. Circular dependencies create implicit coupling: you cannot understand, test, deploy, or modify any module in the cycle independently. The cycle behaves as a single coupled unit regardless of how many files are involved.

**Detection signals:**
- Build errors related to import ordering
- Import cycle analysis tools report cycles
- Runtime errors from uninitialized imports
- Modules that "need each other" to function
- Cannot extract a module into its own package without pulling in half the codebase

**Impact:** Modules in a cycle cannot be independently versioned, deployed, or tested. Understanding any module requires understanding all modules in the cycle. Refactoring is difficult because changes propagate through the cycle. Build tools may produce unpredictable results.

**Remediation:** Apply the Dependency Inversion Principle: introduce an interface in the lower-level module that the higher-level module implements. Extract shared types into a separate module that both depend on. Use event-based communication to break direct dependencies. Restructure module boundaries so dependencies flow in one direction.

**Grep pattern:**
```bash
# JavaScript/TypeScript
npx madge --circular src/

# Python
pip install import-linter && lint-imports

# General: visualize dependency graph
npx madge --image deps.svg src/
```

---

#### 7. Inappropriate Intimacy

**Also known as:** Tight coupling, reaching into internals, broken encapsulation

**Description:** Modules access each other's internal implementation details rather than communicating through public interfaces. Service A reads Service B's database directly. Module X imports internal helper functions from Module Y. The frontend hardcodes knowledge of the backend's database schema. When implementation details change, dependent modules break.

**Detection signals:**
- Imports from paths containing `internal`, `private`, `impl`, or `_` prefixed modules
- Direct database access from services that do not own the data
- Hardcoded knowledge of another module's data structures or algorithms
- Tests that break when implementation (not behavior) changes

**Impact:** Changes to internal details ripple across module boundaries. Encapsulation provides no protection because it is routinely violated. Module ownership is meaningless because anyone can reach into any module's internals. Refactoring is dangerous and expensive.

**Remediation:** Define and enforce public APIs for each module. Use linting rules to block imports from internal paths. Introduce API contracts between services. Replace direct database access with API calls. Apply the principle of least knowledge (Law of Demeter).

**Grep pattern:**
```bash
# Find imports from internal paths (Python)
grep -rn "from.*internal\|from.*_private\|from.*\.impl" src/ --include="*.py"

# Find imports from internal paths (JS/TS)
grep -rn "from.*internal\|from.*/private/" src/ --include="*.ts" --include="*.js"

# Find cross-service database access
grep -rn "SELECT\|INSERT\|UPDATE\|DELETE" services/ --include="*.py" --include="*.ts" | grep -v "own-service-name"
```

---

#### 8. Dead Code

**Also known as:** Code graveyard, zombie code

**Description:** The codebase contains unreachable code, unused exports, deprecated modules, and commented-out code blocks that nobody dares remove. This dead code adds confusion (is this still used?), increases maintenance burden, and makes the codebase appear larger and more complex than it actually is.

**Detection signals:**
- Unused function/class exports
- Commented-out code blocks (especially large ones)
- Feature flags that are permanently off
- Modules with zero inbound references
- Code coverage reports showing consistently uncovered code paths

**Impact:** Developers waste time reading and understanding dead code. Refactoring tools report false positives. Build times increase. New developers cannot distinguish active from dead code. Security vulnerabilities may lurk in unmaintained dead code.

**Remediation:** Run dead code detection tools regularly. Remove commented-out code (version control is your backup, not comments). Audit feature flags and remove permanently disabled ones. Set up CI checks that fail on unused exports. Apply the Boy Scout Rule: remove dead code when you encounter it.

**Grep pattern:**
```bash
# Python dead code detection
vulture src/ --min-confidence 80

# JavaScript/TypeScript unused exports
npx ts-prune

# Go dead code
deadcode ./...

# Find commented-out code blocks (heuristic)
grep -rn "^#.*def \|^#.*class \|^//.*function \|^//.*const " src/
```

---

### Category 2: Communication Anti-Patterns

---

#### 9. Chatty Services

**Also known as:** Fine-grained API, death by a thousand calls

**Description:** Services communicate through too many fine-grained calls. Rendering a single page requires 15 API calls to 8 different services. Each call adds network latency, serialization overhead, and failure risk. The aggregate latency and failure probability make the system slow and fragile.

**Detection signals:**
- More than 5 inter-service API calls per user request
- High inter-service network traffic relative to external traffic
- Distributed traces showing wide fan-out patterns
- API endpoints returning single fields or tiny payloads

**Impact:** Latency compounds across calls. Failure probability increases (if each call has 99.9% reliability, 15 calls yield 98.5% reliability). Network saturation between services. Debugging is difficult because a single user action involves many service interactions.

**Remediation:** Introduce aggregate APIs (Backend for Frontend pattern). Use GraphQL to let clients specify exactly what data they need in one call. Batch related operations. Consider denormalizing data to reduce cross-service queries. Use the API Gateway pattern to compose responses.

**Grep pattern:**
```bash
# Count inter-service calls in a request trace (application-specific)
# Look for multiple HTTP client calls in a single handler
grep -A 20 "def handle_request\|async def handle" src/handlers/ | grep -c "await.*client\.\|requests\."
```

---

#### 10. Synchronous Chain

**Also known as:** Call chain of doom, cascade coupling, temporal coupling chain

**Description:** Service A synchronously calls Service B, which synchronously calls Service C, which synchronously calls Service D. The overall latency is the sum of all service latencies. If any service in the chain fails or slows down, the entire chain fails or slows down. The calling service is blocked waiting for the entire chain to complete.

**Detection signals:**
- Request latency is the sum of all service latencies in the chain
- Distributed traces show deep sequential call chains (not fan-out)
- Timeout of one downstream service causes timeout of the entire request
- Cascading failures: one slow service makes the entire system slow

**Impact:** Latency is additive across the chain. Availability is multiplicative (each link reduces it). A single slow service degrades the entire user experience. Timeout tuning becomes a nightmare: each service must account for the full downstream chain.

**Remediation:** Break synchronous chains with asynchronous messaging (events, queues). Use the CQRS pattern to separate reads from writes. Cache data locally to eliminate some downstream calls. Apply the circuit breaker pattern to fail fast rather than wait. Consider event-driven architecture for workflows that span multiple services.

**Grep pattern:**
```bash
# Look for nested service calls (within a handler, one call's result feeds the next)
grep -B 5 -A 10 "def handle\|async def handle" src/ --include="*.py" -r | grep -c "await.*service\."
```

---

#### 11. Shared Database

**Also known as:** Integration database, common datastore

**Description:** Multiple services or applications read from and write to the same database. The database schema becomes a shared contract that no service can change without coordinating with all others. The database becomes a coupling point that defeats the purpose of service decomposition.

**Detection signals:**
- Multiple services have connection strings to the same database
- Schema migrations require coordination across teams
- Database table ownership is unclear or shared
- One service's query patterns degrade another service's performance

**Impact:** No service can evolve its schema independently. Performance isolation is impossible (one service's heavy query affects all others). Data ownership is ambiguous. The database becomes a single point of failure for all services.

**Remediation:** Give each service its own database (database per service pattern). Use events to synchronize data between services when needed. Apply the Strangler Fig pattern to gradually migrate away from the shared database. If full separation is not feasible, at minimum enforce table ownership: each table is owned by exactly one service.

**Grep pattern:**
```bash
# Find identical database hostnames across service configs
grep -rh "DB_HOST\|DATABASE_URL\|POSTGRES_HOST" services/ --include="*.env" --include="*.yaml" | sort | uniq -d
```

---

#### 12. API Versioning Neglect

**Also known as:** Breaking change roulette, YOLO API

**Description:** Public or internal APIs are changed without versioning, backward compatibility, or deprecation notices. Clients break unexpectedly when the API changes. There is no mechanism for clients to pin to a stable version while the API evolves.

**Detection signals:**
- No version indicator in API URLs, headers, or contracts
- Client applications frequently break after backend deployments
- No deprecation process or timeline for old endpoints
- API documentation is absent or perpetually outdated

**Impact:** Client trust erodes. Integration fragility. Fear of changing APIs leads to API stagnation or workaround accumulation. Coordinated deployments become necessary (defeating independent deployability).

**Remediation:** Adopt a versioning strategy (URL path versioning `/v2/`, header versioning, or content negotiation). Establish a deprecation policy (announce deprecation, provide migration window, then remove). Use consumer-driven contract testing to detect breaking changes before deployment. Treat APIs as products with explicit lifecycle management.

**Grep pattern:**
```bash
# Check for version indicators in API routes
grep -rn "v[0-9]\|/api/v" src/routes/ --include="*.py" --include="*.ts"

# Find routes without versioning
grep -rn "@app.route\|@router\." src/ --include="*.py" | grep -v "/v[0-9]"
```

---

#### 13. Event Soup

**Also known as:** Event spaghetti, publish-and-pray

**Description:** Events are overused for everything, including operations that should be commands or queries. Events trigger events that trigger events, creating long, untraceable chains. There is no clear distinction between commands (do this), queries (tell me this), and events (this happened). The system becomes impossible to reason about because cause and effect are separated across many decoupled handlers.

**Detection signals:**
- Events triggering other events in chains of 3+ hops
- Difficulty tracing the full effect of a single action
- Events used as remote procedure calls (expecting a response)
- Event handlers with side effects that trigger more events
- "I published an event but nothing happened" or "something happened twice"

**Impact:** Debugging is extremely difficult. Ordering issues and race conditions proliferate. System behavior is emergent and surprising. Idempotency failures cause duplicate processing.

**Remediation:** Distinguish commands, queries, and events explicitly. Use commands for "do this" (synchronous or via command queue). Use events only for "this happened" (notification, no response expected). Limit event chain depth. Document event flows. Ensure all handlers are idempotent.

**Grep pattern:**
```bash
# Find event handlers that publish events (event chains)
grep -B 2 -A 10 "@event_handler\|on_event\|subscribe" src/ --include="*.py" -r | grep "publish\|emit\|dispatch"
```

---

#### 14. Temporal Coupling

**Also known as:** Order dependency, hidden sequencing, initialization coupling

**Description:** Operations must happen in a specific undocumented order to work correctly. Service A must start before Service B. Method `init()` must be called before `process()`. Config must be loaded before dependencies are injected. These ordering requirements are implicit -- they exist in developers' heads, not in the code or documentation.

**Detection signals:**
- "It works if you restart service X first"
- Race conditions during startup
- `init()` or `setup()` methods that must be called in a specific sequence
- Bugs that appear intermittently based on timing
- Deployment scripts with specific ordering requirements

**Impact:** Deployment is fragile (wrong order causes failures). New developers introduce bugs by not knowing the required sequence. Automated deployments and scaling are unreliable. Testing is difficult because tests must replicate exact ordering.

**Remediation:** Make dependencies explicit. Use constructor injection so objects are fully initialized at creation. Design services to be startup-order independent (retry connections, health checks). Replace implicit ordering with explicit orchestration (workflow engines, init containers). Document any unavoidable ordering requirements.

**Grep pattern:**
```bash
# Find init/setup methods that suggest ordering requirements
grep -rn "def init\|def setup\|def configure\|must_be_called" src/ --include="*.py"

# Find startup ordering in Docker Compose
grep -A 3 "depends_on" docker-compose*.yml
```

---

### Category 3: Data Anti-Patterns

---

#### 15. Anemic Domain Model

**Also known as:** Transaction script with DTOs, logic-free entities

**Description:** Domain objects are mere data containers with getters and setters but no business logic. All behavior lives in "service" classes that manipulate the anemic objects. This violates the fundamental object-oriented principle that data and behavior should live together. The "model" is just a database row wrapper.

**Detection signals:**
- Entity/model classes with only field definitions, getters, and setters
- Fat service classes with all business rules
- Domain objects have no methods beyond property access
- Business logic duplicated across multiple services operating on the same entities

**Impact:** Business logic is scattered across service classes, making it harder to find and maintain. Logic duplication is common because different services re-implement the same rules. The domain model provides no encapsulation or invariant protection. Rich domain concepts are lost in procedural service code.

**Remediation:** Move behavior to the domain objects. If `OrderService.calculateTotal(order)` exists, move it to `Order.calculateTotal()`. Apply domain-driven design principles: aggregates enforce invariants, entities encapsulate behavior, value objects express domain concepts. The service layer should orchestrate, not implement, business logic.

**Grep pattern:**
```bash
# Find model classes with no methods (Python dataclass/Pydantic with no def)
grep -l "@dataclass\|class.*BaseModel" src/models/ | xargs -I{} sh -c 'echo "--- {} ---"; grep -c "def " {}'

# Find fat service files
find src/services/ -name "*.py" -exec wc -l {} \; | sort -rn | head -10
```

---

#### 16. N+1 Query Problem

**Also known as:** Select N+1, lazy loading trap

**Description:** When loading a collection of N records plus their related data, the system executes 1 query to get the N records and then N additional queries to get the related data for each record individually. For 100 users with their orders: 1 query for users + 100 queries for orders = 101 queries instead of 2.

**Detection signals:**
- SQL logs show repetitive queries differing only in ID parameter
- Page load times scale linearly with record count
- ORM lazy loading used within loops
- Database CPU high despite low logical query complexity

**Impact:** Database load scales linearly with collection size. Response times degrade as data grows. Database connection pool exhaustion under load. Unnecessary network round trips between application and database.

**Remediation:** Use eager loading / prefetching (`select_related` and `prefetch_related` in Django, `include` in ActiveRecord, `joinedload` in SQLAlchemy). Use batch queries (`WHERE id IN (...)`). Use DataLoader pattern for GraphQL. Add query count assertions in tests to prevent regression.

**Grep pattern:**
```bash
# Find loops containing DB queries (Python/SQLAlchemy)
grep -B 5 "for.*in.*:" src/ --include="*.py" -r | grep -A 5 "session.query\|.filter("

# Find lazy loading without prefetch (Django)
grep -rn "\.objects\.\(all\|filter\)" src/ --include="*.py" | grep -v "select_related\|prefetch_related"
```

---

#### 17. Database-as-Integration

**Also known as:** Integration database, polling pattern, database-as-message-broker

**Description:** The database is used as a communication mechanism between services or components. One service writes a row; another service polls for new rows. Triggers fire stored procedures that update tables monitored by other systems. The database becomes an implicit message broker without any of the guarantees of a real one.

**Detection signals:**
- Polling queries on "status" or "processed" columns
- Database triggers that implement business workflows
- Multiple services writing to a "queue" table
- Batch jobs that scan tables for unprocessed records

**Impact:** Tight coupling through shared schema. No delivery guarantees (messages can be lost, duplicated, or processed out of order). Polling wastes database resources. Scaling is limited by database capacity. Monitoring and debugging are difficult because the communication is implicit.

**Remediation:** Replace database polling with a proper message broker (RabbitMQ, Kafka, SQS). Use the Outbox pattern for reliable event publishing alongside database transactions. If polling is unavoidable, use change data capture (CDC) tools like Debezium to stream database changes as events.

**Grep pattern:**
```bash
# Find polling patterns
grep -rn "WHERE.*status.*=.*pending\|WHERE.*processed.*=.*false\|WHERE.*is_processed" src/ --include="*.py" --include="*.ts"

# Find database triggers
grep -rn "CREATE TRIGGER\|AFTER INSERT\|BEFORE UPDATE" migrations/ --include="*.sql"
```

---

#### 18. Schemaless Chaos

**Also known as:** Pray-and-parse, unvalidated JSON, YOLO deserialization

**Description:** Data crosses boundaries (API inputs, message payloads, configuration files, database reads) without schema validation. JSON is parsed and accessed by key without verifying structure. Missing fields cause runtime errors deep in the call stack instead of being caught at the boundary. Type safety is absent.

**Detection signals:**
- `JSON.parse` or `json.loads` without subsequent validation
- Direct dictionary/object key access without schema checking
- Runtime `KeyError`, `TypeError`, or `undefined is not a function` errors from malformed data
- No Pydantic, Zod, JSON Schema, or equivalent validation at API boundaries

**Impact:** Runtime errors from malformed data. Security vulnerabilities from unvalidated input. Debugging is difficult because errors surface far from the actual problem. API contracts are implicit and undocumented.

**Remediation:** Validate all data at trust boundaries using schema validation libraries (Pydantic for Python, Zod for TypeScript, JSON Schema for language-agnostic). Define explicit types/models for all API inputs and outputs. Fail fast with clear error messages at the boundary. Generate API documentation from schemas.

**Grep pattern:**
```bash
# Find unvalidated JSON parsing (Python)
grep -rn "json.loads\|json.load(" src/ --include="*.py" | grep -v "pydantic\|validate\|schema"

# Find unvalidated JSON parsing (JS/TS)
grep -rn "JSON.parse" src/ --include="*.ts" --include="*.js" | grep -v "zod\|validate\|schema"

# Find raw dict access without validation
grep -rn '\["[a-z_]*"\]' src/ --include="*.py" | head -20
```

---

#### 19. Data Clump

**Also known as:** Parameter group, field cluster

**Description:** The same group of data fields always travels together -- passed as individual parameters to functions, stored as separate columns, transmitted as loose fields. Street, city, state, zip code appear as four separate parameters in dozens of functions instead of being encapsulated in an Address object.

**Detection signals:**
- Three or more parameters that consistently appear together across function signatures
- Same field group repeated across multiple database tables without normalization
- Copy-paste of field lists across API endpoints

**Impact:** Duplication of validation logic (validate zip code in every function that receives it). Inconsistency (different functions may have different field orderings or names). Missed abstractions (the concept of "Address" exists in the domain but not in the code).

**Remediation:** Extract the recurring field group into a value object, data class, or named type. Replace all occurrences with the new type. Centralize validation in the type's constructor. This is usually a straightforward, low-risk refactoring.

**Grep pattern:**
```bash
# Find functions with many parameters (Python)
grep -rn "def.*,.*,.*,.*,.*," src/ --include="*.py" | head -20

# Find repeated field groups (heuristic: same fields appearing together)
grep -rn "street.*city\|city.*state\|latitude.*longitude" src/ --include="*.py"
```

---

#### 20. Shared Mutable State

**Also known as:** Global variable hell, unprotected concurrency, race condition factory

**Description:** Multiple components, threads, or services modify the same state without proper coordination (locks, transactions, compare-and-swap). This leads to race conditions, inconsistent reads, lost updates, and non-deterministic behavior that is nearly impossible to reproduce and debug.

**Detection signals:**
- Global variables modified by multiple functions or modules
- Race conditions and intermittent bugs ("it works most of the time")
- Thread-unsafe singletons
- Multiple processes writing to the same file or shared memory without locking
- `inconsistent read` or `lost update` bug reports

**Impact:** Data corruption. Non-deterministic behavior. Bugs that appear only under load and disappear when debugging. Security vulnerabilities from time-of-check to time-of-use (TOCTOU) races.

**Remediation:** Eliminate shared mutable state where possible (use immutable data, pass copies, use message passing). Where shared state is necessary, use proper synchronization (mutexes, transactions, CAS operations). Use single-writer patterns. Prefer event sourcing or CQRS to eliminate concurrent writes to the same state.

**Grep pattern:**
```bash
# Find global mutable state (Python)
grep -rn "^[a-z_].*= \[\]\|^[a-z_].*= {}\|^[a-z_].*= set()" src/ --include="*.py"

# Find unsynchronized shared state (Java)
grep -rn "static.*=" src/ --include="*.java" | grep -v "final\|static final"
```

---

### Category 4: Deployment Anti-Patterns

---

#### 21. Snowflake Servers

**Also known as:** Artisanal servers, hand-crafted infrastructure, pet servers

**Description:** Each server is manually configured with unique settings, packages, and tweaks accumulated over months or years. No two servers are identical. Nobody knows the full configuration of any server. Rebuilding a server from scratch is impossible without the person who set it up.

**Detection signals:**
- Cannot rebuild a server from scratch using automation
- "Works on production but not staging" (or vice versa)
- SSH into servers to make manual changes
- Undocumented hotfixes applied directly to production servers
- Fear of rebooting servers because they might not come back correctly

**Impact:** Disaster recovery is impossible or extremely slow. Scaling requires manual setup of each new server. Configuration drift between servers causes inconsistent behavior. Bus factor of 1 for server configuration knowledge.

**Remediation:** Adopt Infrastructure as Code (Terraform, Pulumi, CloudFormation). Use configuration management (Ansible, Chef, Puppet). Build immutable machine images (AMI, Docker). Treat servers as cattle, not pets: replace them, do not repair them. Automate everything; if you SSH into a server, you have failed.

**Grep pattern:**
```bash
# Check for infrastructure-as-code presence
ls terraform/ pulumi/ cloudformation/ ansible/ 2>/dev/null
find . -name "*.tf" -o -name "Pulumi.*" -o -name "*.ansible.yml" 2>/dev/null

# Check for Dockerfiles (containerization)
find . -name "Dockerfile" -o -name "docker-compose*.yml" 2>/dev/null
```

---

#### 22. Configuration Drift

**Also known as:** Environment divergence, snowflake environments

**Description:** Development, staging, and production environments gradually diverge over time. Hotfixes applied to production are not backported to staging. Staging has different library versions, different configuration flags, different data schemas. The environments that are supposed to be identical are not.

**Detection signals:**
- "Works in staging but not production" (or vice versa)
- Environment-specific bugs that cannot be reproduced elsewhere
- Manual configuration changes applied to one environment but not others
- Different dependency versions across environments

**Impact:** Testing in staging does not predict production behavior. Deployments that pass staging fail in production. Debugging requires access to the specific environment where the bug occurs. Confidence in the release process erodes.

**Remediation:** Use the same Infrastructure as Code definitions for all environments, parameterized only by environment-specific values (credentials, URLs, scale). Deploy the same artifact (Docker image, AMI) to all environments. Automate environment provisioning so rebuilding is trivial. Use configuration management tools with drift detection.

**Grep pattern:**
```bash
# Compare environment configs for drift
diff <(sort env/staging.env) <(sort env/production.env)

# Check for environment-specific Dockerfiles (anti-pattern)
find . -name "Dockerfile.*" -o -name "Dockerfile-*" | grep -i "prod\|staging\|dev"
```

---

#### 23. Insufficient Monitoring

**Also known as:** Black box production, flying blind, hope-driven operations

**Description:** The system in production is a black box. There are no dashboards, no alerts, no structured logs, and no distributed traces. The team discovers outages when users report them. Performance degradation goes unnoticed until it becomes catastrophic. There is no data to inform architectural or operational decisions.

**Detection signals:**
- Outages discovered by end users rather than automated alerts
- No operational dashboards for any service
- Logs are unstructured text sent to stdout and never aggregated
- No alert rules defined
- Mean Time to Detect (MTTD) is measured in hours or days

**Impact:** Slow incident response. Root cause analysis is guesswork. Performance degradation is invisible. Capacity planning is impossible. SLA compliance cannot be measured or proven.

**Remediation:** Implement the three pillars of observability: metrics (Prometheus, CloudWatch), logs (structured JSON, aggregated in ELK/Loki), traces (OpenTelemetry, Jaeger). Define RED metrics (Rate, Errors, Duration) for every service. Create dashboards for each service. Set up alerts with escalation policies. Start simple and iterate.

**Grep pattern:**
```bash
# Check for observability tooling presence
grep -r "prometheus\|opentelemetry\|datadog\|newrelic\|jaeger" . --include="*.yaml" --include="*.toml" --include="*.json" -l
grep -r "structlog\|winston\|pino\|serilog" . --include="*.py" --include="*.ts" --include="*.js" -l

# Check for health endpoints
grep -rn "health\|readiness\|liveness" src/ --include="*.py" --include="*.ts" -l
```

---

#### 24. Feature Branch Hell

**Also known as:** Long-lived branches, merge nightmare, integration avoidance

**Description:** Feature branches live for weeks or months, diverging significantly from the main branch. When it is finally time to merge, conflicts are massive and painful. Integration bugs are discovered late. Multiple long-lived branches conflict with each other in unpredictable ways.

**Detection signals:**
- Branches older than 1 week
- Merge conflicts requiring hours to resolve
- "Integration sprints" dedicated to merging branches
- CI runs on feature branches that do not include other in-progress work
- Fear of merging

**Impact:** Integration risk compounds over time. Merge conflicts cause bugs. Developer productivity drops during merge periods. Features cannot be tested together until merged. Deployment frequency drops because merging is painful.

**Remediation:** Adopt trunk-based development: short-lived branches (1-2 days max), merged frequently to main. Use feature flags to decouple deployment from release. Practice continuous integration: merge to main at least daily. Keep branches small and focused. Automate conflict detection.

**Grep pattern:**
```bash
# Find long-lived branches
git for-each-ref --sort=-committerdate refs/heads/ --format='%(committerdate:relative) %(refname:short)' | head -20

# Find branches older than 7 days
git for-each-ref --sort=committerdate refs/heads/ --format='%(committerdate:unix) %(refname:short)' | awk -v cutoff=$(date -v-7d +%s 2>/dev/null || date -d '7 days ago' +%s) '$1 < cutoff {print $2}'
```

---

#### 25. Manual Deployment

**Also known as:** Deployment runbook, artisanal deployment, deploy-and-pray

**Description:** Deployment requires human steps: SSH into servers, run scripts in a specific order, update configuration files manually, restart services one by one, verify each step visually. The deployment process exists as tribal knowledge or a multi-page runbook. Mistakes are common because humans are not reliable executors of repetitive procedures.

**Detection signals:**
- Deployment runbook with more than 10 manual steps
- Deployment failures caused by missed or misordered steps
- Only specific people can deploy ("deploy specialist")
- Deployments take more than 30 minutes
- Deployments only happen during low-traffic windows

**Impact:** Low deployment frequency (deploying is painful, so teams batch changes). High change failure rate (manual steps are error-prone). Long recovery time (manual rollback is slow). Knowledge concentration in a few people. Deployment bottleneck.

**Remediation:** Automate everything. Build CI/CD pipelines (GitHub Actions, GitLab CI, Jenkins, Argo CD). Start with automating the most error-prone steps. Use infrastructure as code. Implement automated smoke tests post-deployment. Target: deployment is a button press (or automatic on merge to main).

**Grep pattern:**
```bash
# Check for CI/CD configuration
ls .github/workflows/ .gitlab-ci.yml Jenkinsfile .circleci/ buildkite/ 2>/dev/null

# Check for deployment automation
find . -name "deploy*" -o -name "release*" | grep -i "\.sh\|\.py\|\.yaml\|\.yml"
```

---

### Category 5: Organizational Anti-Patterns

---

#### 26. Conway's Law Violation

**Also known as:** Inverse Conway maneuver failure, org-architecture mismatch

**Description:** The software architecture does not align with the team structure, or vice versa. A single team owns a microservice that requires coordination with three other teams for every change. Two teams share ownership of one module and constantly conflict. The organization chart and the system architecture are fighting each other.

**Detection signals:**
- Cross-team dependencies for every feature
- Multi-team coordination required for simple changes
- Team boundaries do not match service/module boundaries
- High meeting overhead for technical decisions
- "We need to talk to team X before we can do anything"

**Impact:** Development velocity drops due to coordination overhead. Ownership ambiguity leads to neglected components. Conflicting priorities between teams sharing a component. Release coordination becomes a full-time job.

**Remediation:** Apply the Inverse Conway Maneuver: restructure teams to match the desired architecture (or vice versa). Give each team full ownership of their services (you build it, you run it). Minimize cross-team dependencies to well-defined API contracts. Use Team Topologies concepts: stream-aligned teams, platform teams, enabling teams.

---

#### 27. Architecture Astronaut

**Also known as:** Over-engineering, YAGNI violation, gold plating, speculative generality

**Description:** The architect designs for hypothetical future requirements that may never materialize. The system has plugin architectures with one plugin, abstraction layers with one implementation, configuration systems for settings that never change, and extension points that are never extended. The architecture is impressive on paper but imposes real complexity cost for imaginary benefit.

**Detection signals:**
- Abstract interfaces with only one concrete implementation
- "We might need this someday" as justification
- Configuration for things that never change
- Plugin systems with exactly one plugin
- Architecture documents describe capabilities the system does not need today

**Impact:** Increased complexity without corresponding benefit. Longer development time for features. Harder onboarding because developers must understand abstractions that serve no current purpose. Maintenance burden on unused flexibility.

**Remediation:** Apply YAGNI (You Aren't Gonna Need It) rigorously. Build for today's requirements, not tomorrow's speculation. Refactoring is cheaper than premature abstraction. When in doubt, choose the simpler approach. Add abstraction when the second or third use case demands it, not before.

**Grep pattern:**
```bash
# Find interfaces with single implementation
grep -rn "class.*ABC\|class.*Interface\|class.*Protocol" src/ --include="*.py" -l | while read f; do
  class_name=$(grep -oP "class \K\w+" "$f" | head -1)
  echo "$class_name: $(grep -r "($class_name)\|: $class_name" src/ --include='*.py' -c) implementations"
done

# Find abstractions with single implementation (Java/TS)
grep -rn "implements\|extends" src/ --include="*.ts" | awk -F'implements |extends ' '{print $2}' | sort | uniq -c | sort -n | head -10
```

---

#### 28. Resume-Driven Development

**Also known as:** Technology zoo, shiny object syndrome, hype-driven development

**Description:** Technology choices are made based on what looks good on a resume or what is trending on Hacker News, rather than fitness for the problem. The system uses Kubernetes for a single-server application, Kafka for 10 messages per day, GraphQL for a single consumer, and a service mesh for three services. Each technology adds operational complexity without proportional benefit.

**Detection signals:**
- New frameworks or tools adopted without comparative evaluation
- Technology diversity far exceeding what the problem demands
- Technology choices cannot be justified in terms of specific requirements
- Operations team struggles to maintain the technology zoo
- "We chose it because it's modern / everyone is using it / it's cool"

**Impact:** Operational complexity skyrockets. The team becomes expert in nothing because they use everything. Hiring becomes harder (need polyglot specialists). Incidents increase because operational knowledge is spread thin. Total cost of ownership is high relative to system complexity.

**Remediation:** Require Architecture Decision Records (ADRs) for every technology choice. Evaluate at least two alternatives for each decision. Prioritize operational simplicity. Use a technology radar to manage adoption deliberately. Prefer boring technology that the team knows well.

---

#### 29. Ivory Tower Architecture

**Also known as:** Paper architecture, architecture by committee, disconnected design

**Description:** Architects create designs in isolation without writing code or getting feedback from the implementation teams. The architecture document is a beautiful artifact that does not match the built system. Developers work around the architecture because it does not address real constraints. The architecture and the codebase diverge increasingly over time.

**Detection signals:**
- Architecture documentation that does not match the code
- Developers routinely work around architectural guidelines
- Architects have not committed code in months
- Architecture reviews happen only at the beginning of projects
- "The architecture says X, but we actually do Y"

**Impact:** Architecture decisions are uninformed by implementation reality. Developers lose trust in architecture guidance. The actual architecture drifts from the intended one. Architectural decisions are not tested until it is too late to change them.

**Remediation:** Architects must write code (at least part-time). Architecture decisions should be validated with prototypes. Use evolutionary architecture: make decisions as late as responsibly possible, with real data. Hold regular architecture review sessions with implementers. Treat architecture as a living practice, not a document.

---

#### 30. Tribal Knowledge

**Also known as:** Bus factor 1, head knowledge, oral tradition

**Description:** Critical system knowledge exists only in specific people's heads. There is no documentation, no runbooks, no architectural decision records. When that person goes on vacation, leaves the company, or is unavailable, the team is paralyzed. "Ask Bob, he knows how that works" is the answer to every question.

**Detection signals:**
- "Ask Bob, he knows how that works" (single point of knowledge)
- Bus factor of 1 for critical systems
- No documentation of operational procedures
- Onboarding takes months because knowledge transfer is oral
- Incidents escalated to specific individuals regardless of on-call rotation

**Impact:** Key-person risk: the organization is fragile to personnel changes. Slow onboarding. Inconsistent decisions because different people have different (incomplete) understanding. Incident resolution depends on specific individuals being available.

**Remediation:** Write Architecture Decision Records (ADRs) for every significant decision. Create runbooks for operational procedures. Document system boundaries, data flows, and deployment processes. Rotate on-call and incident command to spread knowledge. Pair programming and code review as knowledge transfer mechanisms. Record video walkthroughs of complex systems.

---

#### 31. Lava Flow

**Also known as:** Dead system walking, deprecated-but-running, zombie infrastructure

**Description:** Dead code, deprecated systems, and abandoned experiments remain in the codebase or infrastructure because nobody is confident they can be safely removed. "We're not sure if anything still uses that service." Over time, these fossilized components accumulate, consuming resources, confusing developers, and increasing the attack surface.

**Detection signals:**
- "Don't touch that -- we're not sure if anything uses it"
- Services running in production with no clear owner
- Configuration files for systems that were replaced years ago
- Dependencies on deprecated libraries with no migration plan
- Code paths guarded by feature flags that are permanently off

**Impact:** Infrastructure costs for unused systems. Security risk from unmaintained components. Developer confusion about what is active vs. abandoned. Dependency updates blocked by abandoned code that nobody wants to touch.

**Remediation:** Inventory all systems and assign clear ownership. Use traffic monitoring to identify truly unused services (zero traffic = safe to remove). Schedule regular cleanup sprints. Apply the "dark launch" technique: turn it off and see if anything breaks. Use feature flag hygiene: remove flags that have been in one position for more than 30 days.

**Grep pattern:**
```bash
# Find old feature flags
grep -rn "feature_flag\|feature_toggle\|FEATURE_" src/ --include="*.py" --include="*.ts" -l

# Find TODO/FIXME/HACK/DEPRECATED markers
grep -rn "TODO\|FIXME\|HACK\|DEPRECATED\|XXX" src/ --include="*.py" --include="*.ts" | wc -l
```

---

#### 32. Analysis Paralysis

**Also known as:** Over-analysis, design-without-building, architecture constipation

**Description:** The team spends excessive time analyzing, comparing, and debating architecture options without building anything. Every decision is agonized over. Proof-of-concept prototypes are never built because the team is still evaluating options on paper. Weeks or months pass with elaborate documents but no working software.

**Detection signals:**
- Architecture documents outnumber working prototypes
- No working software after weeks of design discussions
- Every decision requires committee approval
- Comparison matrices with dozens of criteria and no clear winner
- Recurring meetings to re-discuss the same decision

**Impact:** Delayed delivery. Analysis does not reduce risk because real risk is discovered by building, not by analyzing. Team morale drops. Market window may close. The analysis itself becomes outdated as requirements evolve during the analysis period.

**Remediation:** Timebox decisions: small decisions (< 1 day), medium decisions (< 1 week with a spike/prototype), large decisions (< 2 weeks with a walking skeleton). Use the "two-way door" test: if the decision is reversible, decide quickly and move on. Build prototypes and spikes to answer questions empirically. Accept that some uncertainty is irreducible and must be managed, not eliminated.

---

## Anti-Pattern Detection Automation

A consolidated table of tools and commands for automated detection of anti-patterns.

| Anti-Pattern | Tool / Method | Command / Pattern |
|-------------|--------------|------------------|
| Circular dependencies | madge (JS/TS) | `npx madge --circular src/` |
| Circular dependencies | import-linter (Python) | `lint-imports` |
| God class (file size) | wc | `find . -name "*.py" -exec wc -l {} \; \| sort -rn \| head -20` |
| God class (method count) | grep | `grep -c "def \|function " <file>` |
| Dead code | vulture (Python) | `vulture src/ --min-confidence 80` |
| Dead code | ts-prune (TS) | `npx ts-prune` |
| Dead code | deadcode (Go) | `deadcode ./...` |
| N+1 queries | Django Debug Toolbar | Assert query count in tests: `self.assertNumQueries(2)` |
| Shared database | grep | `grep -rh "DB_HOST\|DATABASE_URL" services/ --include="*.env" \| sort \| uniq -d` |
| Schemaless input | grep | `grep -rn "json.loads\|JSON.parse" src/ \| grep -v "validate\|schema\|pydantic\|zod"` |
| Large functions | radon (Python) | `radon cc src/ -a -nc` (cyclomatic complexity) |
| Complex functions | lizard (multi-lang) | `lizard src/ -l python -T nloc=50` |
| Commented-out code | grep | `grep -rn "^#.*def \|^//.*function " src/` |
| Feature branch age | git | `git for-each-ref --sort=committerdate refs/heads/ --format='%(committerdate:relative) %(refname:short)'` |
| Missing CI/CD | ls | `ls .github/workflows/ .gitlab-ci.yml Jenkinsfile 2>/dev/null` |
| Missing health checks | grep | `grep -rn "health\|readiness\|liveness" src/ -l` |
| Missing observability | grep | `grep -r "prometheus\|opentelemetry\|datadog" . --include="*.yaml" -l` |
| Synchronous chains | distributed tracing | Check Jaeger/Zipkin for sequential spans > 3 hops |
| Data clumps | grep | `grep -rn "def.*,.*,.*,.*,.*," src/ --include="*.py" \| head -20` |
| Deprecated markers | grep | `grep -rn "TODO\|FIXME\|DEPRECATED\|HACK" src/ \| wc -l` |
| Coupling metrics | pydeps (Python) | `pydeps src/ --max-bacon=2 --cluster` |
| Coupling metrics | dependency-cruiser (JS) | `npx depcruise --output-type err-long src/` |
| Test coverage gaps | coverage (Python) | `coverage run -m pytest && coverage report --fail-under=80` |
| Unused dependencies | deptry (Python) | `deptry .` |
| Unused dependencies | depcheck (JS) | `npx depcheck` |

---

## Remediation Priority Matrix

| Severity | Impact | Examples | Action |
|----------|--------|---------|--------|
| **CRITICAL** | System failure risk, data loss, security breach | Shared mutable state, insufficient monitoring, schemaless chaos, security gaps | Fix immediately. Stop feature work if necessary. These are active threats to system integrity. |
| **HIGH** | Scaling or maintenance blocker; will prevent growth | Distributed monolith, god classes, circular dependencies, shared database, synchronous chains | Fix this quarter. Dedicate a portion of each sprint. Create a roadmap for incremental migration. |
| **MEDIUM** | Developer productivity drag; slows the team | Lasagna architecture, anemic domain model, feature branch hell, chatty services, temporal coupling | Plan incremental improvements. Address when working in affected areas. Track with tech debt backlog. |
| **LOW** | Code quality concern; causes friction but not failure | Data clumps, dead code, inconsistent naming, lava flow, golden hammer (mild cases) | Apply the Boy Scout Rule: leave code better than you found it. Address opportunistically during related work. |

### Prioritization Guidelines

1. **Start with CRITICAL items.** These are risks, not inconveniences. Shared mutable state can cause data corruption. Insufficient monitoring means you do not know your system is failing.
2. **Budget for HIGH items quarterly.** Allocate 20% of engineering capacity to architectural improvement. Create measurable goals (reduce coupling metric by 30%, eliminate shared database for 2 services).
3. **Address MEDIUM items opportunistically.** When you are already modifying a module, improve it. Do not create separate "refactoring projects" for medium-severity items.
4. **Track LOW items but do not prioritize them.** Boy Scout Rule: if you touch code with a data clump, extract the value object. Do not schedule dedicated work for low-severity items.
5. **Re-assess quarterly.** A MEDIUM item can become HIGH as the system grows. A LOW item might become irrelevant if the module is deprecated.
