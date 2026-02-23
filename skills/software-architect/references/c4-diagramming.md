# C4 Diagramming Reference

A comprehensive guide to the C4 model for software architecture visualization, with copy-paste-ready Mermaid templates for all four levels plus supplementary diagrams. This reference covers purpose, audience, templates, examples, quality checklists, and common mistakes for each diagram level.

---

## C4 Model Overview

The C4 model, created by Simon Brown, provides a hierarchical approach to visualizing software architecture at four levels of abstraction. The name "C4" comes from the four levels: **Context**, **Container**, **Component**, and **Code**. Each level zooms in further, revealing more detail about a specific part of the system.

The key principle is that **different audiences need different levels of detail**. A CTO needs to see how systems interact (Level 1). A development lead needs to see what containers compose a system (Level 2). A developer needs to see the internal structure of a container they are working on (Level 3). Level 4 (code-level) is rarely needed and should be auto-generated when used.

### When to Use Each Level

| Level | Name | Audience | Frequency of Use |
|-------|------|----------|-------------------|
| L1 | System Context | Everyone: executives, product, ops, dev | Every system should have one |
| L2 | Container | Dev leads, architects, ops engineers | Every system should have one |
| L3 | Component | Developers working on a specific container | Only for complex or critical containers |
| L4 | Code | Developers diving into implementation | Rarely — only for critical/complex code |

### Core Principles

1. **Each diagram should be self-contained** — understandable without external context
2. **Every element needs a name, type, and description**
3. **Every relationship needs a label describing the interaction**
4. **Keep diagrams focused** — 15-20 elements maximum per diagram
5. **Use consistent notation** — colors, shapes, and labels should follow a convention

---

## Level 1: System Context Diagram

### Purpose

The System Context diagram is the most zoomed-out view. It shows the system under consideration as a single box, surrounded by the users (people/personas) who interact with it and the external systems it depends on or is depended upon by. This diagram answers: "What is the system, who uses it, and what does it interact with?"

### Elements

- **The System** — the software system being described (highlighted, center)
- **People/Personas** — the human users of the system, grouped by role
- **External Systems** — other software systems that interact with this system (upstream or downstream)

### Mermaid Template

```mermaid
C4Context
    title System Context Diagram — [System Name]

    Person(user, "User Role", "Description of what this user does with the system")
    Person(admin, "Admin Role", "Description of admin responsibilities")

    System(system, "System Name", "Brief description of the system's purpose and core value")

    System_Ext(ext1, "External System 1", "What this external system does")
    System_Ext(ext2, "External System 2", "What this external system does")
    System_Ext(ext3, "External System 3", "What this external system does")

    Rel(user, system, "Uses", "HTTPS")
    Rel(admin, system, "Manages", "HTTPS")
    Rel(system, ext1, "Sends data to", "REST/JSON")
    Rel(system, ext2, "Reads data from", "GraphQL")
    Rel(ext3, system, "Pushes events to", "Webhook")
```

### Example: E-Commerce System Context

```mermaid
C4Context
    title System Context Diagram — ShopWave E-Commerce Platform

    Person(shopper, "Shopper", "Browses products, places orders, tracks deliveries")
    Person(merchant, "Merchant", "Manages product catalog, pricing, and inventory")
    Person(cs_agent, "CS Agent", "Handles customer inquiries and order issues")

    System(shopwave, "ShopWave Platform", "Online marketplace enabling merchants to sell products to shoppers with integrated payments and logistics")

    System_Ext(stripe, "Stripe", "Payment processing and subscription management")
    System_Ext(shippo, "Shippo", "Shipping label generation and tracking")
    System_Ext(sendgrid, "SendGrid", "Transactional and marketing email delivery")
    System_Ext(algolia, "Algolia", "Product search and discovery")

    Rel(shopper, shopwave, "Browses and purchases", "HTTPS")
    Rel(merchant, shopwave, "Manages catalog", "HTTPS")
    Rel(cs_agent, shopwave, "Resolves issues", "HTTPS")
    Rel(shopwave, stripe, "Processes payments", "REST/JSON")
    Rel(shopwave, shippo, "Creates shipments", "REST/JSON")
    Rel(shopwave, sendgrid, "Sends emails", "REST/JSON")
    Rel(shopwave, algolia, "Syncs product index", "REST/JSON")
```

### Quality Checklist for L1

- [ ] The system under consideration is clearly highlighted and centered
- [ ] All user roles/personas are identified with meaningful descriptions
- [ ] All external system dependencies are shown (upstream and downstream)
- [ ] Every relationship has a label describing what interaction occurs
- [ ] No technology details are on the diagram (no "PostgreSQL", no "React" — wrong level)
- [ ] The diagram fits on one page with no more than 15 elements
- [ ] The title clearly identifies this as a System Context diagram
- [ ] A non-technical stakeholder can understand the diagram

---

## Level 2: Container Diagram

### Purpose

The Container diagram zooms into the system boundary and shows the high-level technology building blocks (containers) that make up the system. A "container" in C4 is not a Docker container — it is a separately runnable/deployable unit: a web application, a mobile app, a server-side API, a database, a file system, a message broker, etc. This diagram answers: "What are the major technology choices and how do the containers communicate?"

### Elements

- **Containers** — the deployable units within the system (web apps, APIs, databases, queues, etc.)
- **People/Personas** — carried forward from L1 to show who interacts with which container
- **External Systems** — carried forward from L1 to show which containers interact with external systems

### Mermaid Template

```mermaid
C4Container
    title Container Diagram — [System Name]

    Person(user, "User Role", "Description")

    System_Boundary(system, "System Name") {
        Container(web, "Web Application", "React, TypeScript", "Delivers the single-page application to the user's browser")
        Container(api, "API Service", "Node.js, Express", "Handles all business logic and exposes REST API")
        Container(worker, "Background Worker", "Python", "Processes async jobs: emails, reports, data sync")
        ContainerDb(db, "Primary Database", "PostgreSQL 16", "Stores users, orders, products, and transactions")
        ContainerDb(cache, "Cache", "Redis 7", "Caches frequently accessed data and manages sessions")
        Container(queue, "Message Queue", "RabbitMQ", "Buffers async tasks between API and workers")
    }

    System_Ext(ext1, "External System", "Description")

    Rel(user, web, "Visits", "HTTPS")
    Rel(web, api, "Makes API calls", "REST/JSON over HTTPS")
    Rel(api, db, "Reads/writes", "SQL over TCP")
    Rel(api, cache, "Reads/writes", "Redis protocol")
    Rel(api, queue, "Publishes messages", "AMQP")
    Rel(worker, queue, "Consumes messages", "AMQP")
    Rel(worker, db, "Reads/writes", "SQL over TCP")
    Rel(api, ext1, "Sends requests", "REST/JSON")
```

### Example: E-Commerce Container Diagram

```mermaid
C4Container
    title Container Diagram — ShopWave E-Commerce Platform

    Person(shopper, "Shopper", "Browses and purchases products")
    Person(merchant, "Merchant", "Manages catalog and orders")

    System_Boundary(shopwave, "ShopWave Platform") {
        Container(storefront, "Storefront SPA", "Next.js, React", "Server-rendered storefront for shoppers with product browsing, cart, and checkout")
        Container(merchant_portal, "Merchant Portal", "React, TypeScript", "Dashboard for merchants to manage products, orders, and analytics")
        Container(api, "Core API", "Go, Chi", "Central API handling orders, catalog, users, and payment orchestration")
        Container(search_svc, "Search Service", "Python, FastAPI", "Handles product search queries and faceted filtering")
        Container(notification_svc, "Notification Service", "Node.js", "Sends transactional emails, SMS, and push notifications")
        Container(worker, "Async Worker", "Go", "Processes background jobs: inventory sync, report generation, webhook delivery")
        ContainerDb(primary_db, "Primary Database", "PostgreSQL 16", "Orders, users, products, inventory")
        ContainerDb(search_idx, "Search Index", "Elasticsearch 8", "Product search index with facets and autocomplete")
        ContainerDb(cache, "Cache Layer", "Redis 7", "Session store, product cache, rate limiting counters")
        Container(queue, "Event Bus", "Apache Kafka", "Async event streaming between services")
    }

    System_Ext(stripe, "Stripe", "Payment processing")
    System_Ext(shippo, "Shippo", "Shipping and tracking")

    Rel(shopper, storefront, "Browses and buys", "HTTPS")
    Rel(merchant, merchant_portal, "Manages store", "HTTPS")
    Rel(storefront, api, "API calls", "REST/JSON")
    Rel(merchant_portal, api, "API calls", "REST/JSON")
    Rel(api, primary_db, "Reads/writes", "SQL")
    Rel(api, cache, "Reads/writes", "Redis protocol")
    Rel(api, queue, "Publishes events", "Kafka protocol")
    Rel(search_svc, search_idx, "Queries", "HTTP")
    Rel(queue, search_svc, "Product events", "Kafka protocol")
    Rel(queue, notification_svc, "Notification events", "Kafka protocol")
    Rel(queue, worker, "Job events", "Kafka protocol")
    Rel(worker, primary_db, "Reads/writes", "SQL")
    Rel(notification_svc, stripe, "Payment webhooks", "HTTPS")
    Rel(api, stripe, "Processes payments", "REST/JSON")
    Rel(worker, shippo, "Creates labels", "REST/JSON")
```

### Quality Checklist for L2

- [ ] Every container has a name, technology choice, and description
- [ ] The system boundary is clearly drawn and labeled
- [ ] Users and external systems are shown interacting with specific containers (not the boundary)
- [ ] Databases, caches, queues, and file stores use the appropriate container shape (ContainerDb)
- [ ] Every relationship has a label and (optionally) a protocol
- [ ] Container names describe function, not technology (e.g., "Search Service" not "Elasticsearch Wrapper")
- [ ] No internal component details leak into this diagram (wrong level)
- [ ] A new team member can understand the system's technical landscape from this diagram

---

## Level 3: Component Diagram

### Purpose

The Component diagram zooms into a single container from L2 and shows its internal structure: the major components, modules, or classes within it and how they interact. This diagram answers: "How is this container structured internally, and what are the key building blocks?"

Only create L3 diagrams for containers that are complex enough to warrant it. A simple CRUD API may not need one. A core domain service with multiple modules, patterns, and integrations almost certainly does.

### Elements

- **Components** — the major structural building blocks inside the container (controllers, services, repositories, gateways, etc.)
- **Other Containers** — other containers from L2 that this container communicates with (shown as external)
- **External Systems** — external systems accessed by components within this container

### Mermaid Template

```mermaid
C4Component
    title Component Diagram — [Container Name]

    Container_Boundary(api, "API Service") {
        Component(ctrl_orders, "Order Controller", "REST Controller", "Handles HTTP requests for order operations")
        Component(ctrl_products, "Product Controller", "REST Controller", "Handles HTTP requests for product operations")
        Component(svc_orders, "Order Service", "Business Logic", "Orchestrates order creation, validation, and fulfillment")
        Component(svc_products, "Product Service", "Business Logic", "Manages product catalog operations")
        Component(svc_payment, "Payment Gateway", "Integration", "Coordinates payment processing with external provider")
        Component(repo_orders, "Order Repository", "Data Access", "Persists and retrieves order data")
        Component(repo_products, "Product Repository", "Data Access", "Persists and retrieves product data")
        Component(auth, "Auth Middleware", "Security", "Validates JWT tokens and enforces permissions")
    }

    ContainerDb(db, "Primary Database", "PostgreSQL", "Stores orders and products")
    Container(queue, "Event Bus", "Kafka", "Async event streaming")
    System_Ext(stripe, "Stripe", "Payment processing")

    Rel(ctrl_orders, auth, "Validates request")
    Rel(ctrl_orders, svc_orders, "Delegates to")
    Rel(ctrl_products, auth, "Validates request")
    Rel(ctrl_products, svc_products, "Delegates to")
    Rel(svc_orders, repo_orders, "Uses")
    Rel(svc_orders, svc_payment, "Initiates payment")
    Rel(svc_orders, queue, "Publishes OrderPlaced event")
    Rel(svc_products, repo_products, "Uses")
    Rel(svc_payment, stripe, "Processes payment", "REST/JSON")
    Rel(repo_orders, db, "Reads/writes", "SQL")
    Rel(repo_products, db, "Reads/writes", "SQL")
```

### Example: Core API Component Diagram

```mermaid
C4Component
    title Component Diagram — ShopWave Core API

    Container_Boundary(core_api, "Core API (Go, Chi)") {
        Component(router, "HTTP Router", "Chi Router", "Routes incoming HTTP requests to appropriate handlers")
        Component(auth_mw, "Auth Middleware", "JWT Validator", "Extracts and validates JWT, enforces RBAC policies")
        Component(rate_limiter, "Rate Limiter", "Token Bucket", "Enforces per-user and per-IP rate limits using Redis")
        Component(order_handler, "Order Handler", "HTTP Handler", "Handles order CRUD endpoints")
        Component(catalog_handler, "Catalog Handler", "HTTP Handler", "Handles product and category endpoints")
        Component(order_svc, "Order Domain Service", "Domain Logic", "Validates orders, calculates totals, manages order state machine")
        Component(catalog_svc, "Catalog Domain Service", "Domain Logic", "Manages product lifecycle, pricing rules, inventory checks")
        Component(payment_port, "Payment Port", "Interface", "Defines payment processing contract")
        Component(payment_adapter, "Stripe Adapter", "Integration", "Implements payment port using Stripe API")
        Component(order_repo, "Order Repository", "Data Access", "SQL queries for order persistence")
        Component(catalog_repo, "Catalog Repository", "Data Access", "SQL queries for product persistence")
        Component(event_pub, "Event Publisher", "Integration", "Publishes domain events to Kafka")
    }

    ContainerDb(db, "PostgreSQL", "Primary data store")
    ContainerDb(cache, "Redis", "Cache and rate limiting")
    Container(queue, "Kafka", "Event streaming")
    System_Ext(stripe, "Stripe", "Payment processing")

    Rel(router, auth_mw, "Chains")
    Rel(auth_mw, rate_limiter, "Chains")
    Rel(rate_limiter, order_handler, "Routes to")
    Rel(rate_limiter, catalog_handler, "Routes to")
    Rel(order_handler, order_svc, "Delegates to")
    Rel(catalog_handler, catalog_svc, "Delegates to")
    Rel(order_svc, payment_port, "Uses")
    Rel(payment_port, payment_adapter, "Implemented by")
    Rel(payment_adapter, stripe, "Calls", "REST/JSON")
    Rel(order_svc, order_repo, "Uses")
    Rel(catalog_svc, catalog_repo, "Uses")
    Rel(order_repo, db, "Queries", "SQL")
    Rel(catalog_repo, db, "Queries", "SQL")
    Rel(rate_limiter, cache, "Checks counters", "Redis")
    Rel(order_svc, event_pub, "Publishes events")
    Rel(event_pub, queue, "Sends", "Kafka protocol")
```

### Quality Checklist for L3

- [ ] Every component has a name, type/stereotype, and description
- [ ] Components represent meaningful abstractions (not individual classes)
- [ ] The container boundary is clearly labeled with name and technology
- [ ] Relationships to external containers and systems are shown
- [ ] The diagram shows the primary responsibility of each component
- [ ] The diagram does not exceed 20 components (split if needed)
- [ ] Architectural patterns are visible (e.g., ports and adapters, layered structure)
- [ ] A developer unfamiliar with this container can understand its structure

---

## Level 4: Code Diagram

### Purpose

The Code diagram shows the implementation-level details of a specific component from L3: classes, interfaces, their relationships, methods, and fields. This is the most detailed level and should be used sparingly — only for components that are architecturally significant, complex, or frequently misunderstood.

### When to Include L4

- The component implements a critical algorithm or state machine
- The component has complex inheritance or composition relationships that developers need to understand
- Onboarding documentation requires understanding the code structure of a specific component
- **Do not create L4 diagrams for every component** — they become stale quickly

### Mermaid Template (Class Diagram)

```mermaid
classDiagram
    class OrderService {
        -orderRepo: OrderRepository
        -paymentPort: PaymentPort
        -eventPublisher: EventPublisher
        +createOrder(request: CreateOrderRequest): Order
        +cancelOrder(orderId: string): void
        +getOrder(orderId: string): Order
        -validateOrder(request: CreateOrderRequest): ValidationResult
        -calculateTotal(items: LineItem[]): Money
    }

    class OrderRepository {
        <<interface>>
        +save(order: Order): void
        +findById(id: string): Order
        +findByCustomer(customerId: string): Order[]
    }

    class PaymentPort {
        <<interface>>
        +charge(amount: Money, method: PaymentMethod): PaymentResult
        +refund(paymentId: string, amount: Money): RefundResult
    }

    class Order {
        +id: string
        +customerId: string
        +items: LineItem[]
        +status: OrderStatus
        +total: Money
        +createdAt: DateTime
        +addItem(item: LineItem): void
        +removeItem(itemId: string): void
        +transition(newStatus: OrderStatus): void
    }

    class OrderStatus {
        <<enumeration>>
        DRAFT
        PLACED
        PAID
        SHIPPED
        DELIVERED
        CANCELLED
    }

    class LineItem {
        +productId: string
        +quantity: int
        +unitPrice: Money
        +subtotal(): Money
    }

    OrderService --> OrderRepository : uses
    OrderService --> PaymentPort : uses
    OrderService --> Order : creates/manages
    Order --> OrderStatus : has
    Order --> LineItem : contains 1..*
```

### Quality Checklist for L4

- [ ] Only created for architecturally significant or complex components
- [ ] Shows key classes, interfaces, enumerations, and their relationships
- [ ] Includes important methods and fields (not every getter/setter)
- [ ] Uses standard UML notation (interface, enumeration, abstract)
- [ ] Relationship types are correct (inheritance, composition, association, dependency)
- [ ] The diagram can be auto-generated from code where possible
- [ ] The diagram is kept up to date or flagged as "point-in-time snapshot"

---

## Supplementary Diagrams

### Dynamic Diagram (Sequence)

Dynamic diagrams show how elements from any C4 level interact for a specific scenario or use case. They complement the static structure diagrams by showing runtime behavior.

**When to create:** For key scenarios that are architecturally significant, involve multiple containers or components, or are frequently asked about.

```mermaid
sequenceDiagram
    title Order Placement Flow

    actor Shopper
    participant SF as Storefront SPA
    participant API as Core API
    participant DB as PostgreSQL
    participant Pay as Stripe
    participant Bus as Kafka
    participant Notify as Notification Service
    participant Inv as Inventory Service

    Shopper->>SF: Submit order
    SF->>API: POST /api/orders
    API->>API: Validate order
    API->>DB: Begin transaction
    API->>DB: Insert order (status: PENDING)
    API->>Pay: Create payment intent
    Pay-->>API: Payment intent ID
    API->>DB: Update order (payment_intent_id)
    API->>DB: Commit transaction
    API-->>SF: 201 Created (order ID, payment client secret)
    SF->>Pay: Confirm payment (client-side)
    Pay-->>SF: Payment confirmed
    SF->>API: POST /api/orders/{id}/confirm
    API->>DB: Update order (status: PAID)
    API->>Bus: Publish OrderPaid event
    Bus-->>Notify: OrderPaid event
    Notify->>Shopper: Send confirmation email
    Bus-->>Inv: OrderPaid event
    Inv->>DB: Decrement inventory
```

### Deployment Diagram

Deployment diagrams show how containers from L2 are mapped to infrastructure: servers, cloud services, containers, regions, and availability zones.

```mermaid
graph TB
    subgraph "AWS us-east-1"
        subgraph "VPC"
            subgraph "Public Subnet"
                ALB[Application Load Balancer]
                CDN_ORIGIN[CloudFront Origin]
            end
            subgraph "Private Subnet — AZ-1"
                ECS_1[ECS Task: Core API x3]
                ECS_2[ECS Task: Search Service x2]
                ECS_3[ECS Task: Notification Service x1]
            end
            subgraph "Private Subnet — AZ-2"
                ECS_4[ECS Task: Core API x3]
                ECS_5[ECS Task: Async Worker x2]
            end
            subgraph "Data Subnet"
                RDS[(RDS PostgreSQL — Multi-AZ)]
                REDIS[(ElastiCache Redis — Cluster)]
                ES[(OpenSearch Domain)]
            end
        end
        MSK[Amazon MSK — Kafka]
    end

    subgraph "AWS CloudFront"
        CDN[CDN Edge Locations]
    end

    subgraph "Vercel"
        NEXT[Next.js Storefront — Edge]
        MERCHANT[Merchant Portal — Edge]
    end

    CDN --> CDN_ORIGIN
    NEXT --> ALB
    MERCHANT --> ALB
    ALB --> ECS_1
    ALB --> ECS_2
    ALB --> ECS_4
    ECS_1 --> RDS
    ECS_1 --> REDIS
    ECS_1 --> MSK
    ECS_4 --> RDS
    ECS_2 --> ES
    MSK --> ECS_3
    MSK --> ECS_5
    ECS_5 --> RDS
```

---

## Styling Conventions

Consistent visual styling makes C4 diagrams immediately recognizable and scannable across teams and documentation.

### Color Coding

| Element Type | Color | Hex Code | Usage |
|-------------|-------|----------|-------|
| Internal System / Container | Medium Blue | `#438DD5` | Systems and containers owned by the team |
| External System | Dark Blue | `#08427B` | Systems outside the team's control |
| Component | Light Blue | `#85BBF0` | Internal building blocks within a container |
| Person / User | Gray | `#08427B` | Users and personas |
| Database / Data Store | Medium Blue | `#438DD5` | With database shape/icon |
| Security Boundary | Red Border | `#FF6B6B` | Trust boundaries, DMZ, auth zones |
| Deprecated / Legacy | Gray | `#999999` | Systems being sunset or replaced |

### Label Conventions

**Element names:**
- Maximum 4 words (e.g., "Order Processing Service", not "The Service That Handles All Order Processing Logic")
- Use noun phrases for elements (e.g., "Payment Gateway", "User Database")
- Include technology in parentheses at L2+ (e.g., "Core API (Go, Chi)")

**Relationship labels:**
- Use verb + noun format (e.g., "Sends events", "Reads data", "Authenticates via")
- Include protocol when relevant at L2+ (e.g., "REST/JSON over HTTPS", "SQL over TCP")
- Avoid vague labels like "Uses" or "Connects to" — be specific about what the interaction does

### Layout Guidelines

- **Top-down** for hierarchical relationships (users at top, databases at bottom)
- **Left-to-right** for flow-oriented diagrams (request flows, data pipelines)
- **Group related elements** using subgraph boundaries
- **Place the primary system or container at the center** of its diagram
- **External systems at the edges** of the diagram

### Title Format

Every diagram must have a title following this convention:

```
[Level] — [System or Container Name]
```

Examples:
- `System Context Diagram — ShopWave E-Commerce Platform`
- `Container Diagram — ShopWave E-Commerce Platform`
- `Component Diagram — Core API`
- `Code Diagram — Order Domain Service`
- `Dynamic Diagram — Order Placement Flow`
- `Deployment Diagram — ShopWave Production (AWS us-east-1)`

---

## Common Mistakes

### 1. Too Many Elements

**Problem:** Diagrams with 25+ elements become unreadable walls of boxes and arrows. Viewers cannot identify key relationships or follow flows.

**Fix:** Limit each diagram to 15-20 elements maximum. If you need more, split into multiple diagrams. At L1, group related external systems. At L2, consider whether your system boundary is too broad. At L3, only show architecturally significant components.

### 2. Missing Relationship Labels

**Problem:** Arrows between elements without labels force the reader to guess what the interaction is. An unlabeled arrow between "API" and "Database" could mean reads, writes, migrations, or health checks.

**Fix:** Every relationship must have a label. Use verb + noun format: "Reads user profiles", "Publishes order events", "Validates JWT tokens". At L2+, include the protocol or technology: "REST/JSON", "gRPC", "SQL over TCP".

### 3. Inconsistent Abstraction Levels

**Problem:** Mixing abstraction levels within a single diagram. For example, showing "PostgreSQL" (a technology) alongside "Order Management" (a capability) at L1, or showing individual classes at L2.

**Fix:** Strictly adhere to the level definitions:
- L1: Systems and people only. No technology names.
- L2: Containers (deployable units) with technology choices. No internal classes.
- L3: Components (major building blocks) within one container. No low-level classes.
- L4: Classes, interfaces, and their relationships within one component.

### 4. Technology on Context Diagrams

**Problem:** L1 System Context diagrams that include "PostgreSQL", "React", "Kafka" — these are implementation details that do not belong at this level of abstraction.

**Fix:** L1 diagrams should describe what things are and what they do, not how they are built. "ShopWave Platform" with a description of its purpose is correct. "React + Node.js + PostgreSQL E-Commerce Stack" is wrong for L1. Save technology details for L2.

### 5. No System Boundary

**Problem:** Container diagrams where it is unclear which boxes are inside the system and which are external. This makes it impossible to understand scope and ownership.

**Fix:** Always draw explicit system boundaries at L2 using `System_Boundary`. Everything inside the boundary is owned by the team. Everything outside is external. The boundary should be labeled with the system name.

### 6. Using C4 Diagrams as Flowcharts

**Problem:** Treating C4 diagrams as process flowcharts with decision diamonds, loops, and sequential steps. C4 diagrams show static structure, not dynamic behavior.

**Fix:** Use C4 diagrams (L1-L3) for static structure: what exists and how it is connected. Use Dynamic diagrams (sequence diagrams) for runtime behavior: how elements interact for specific scenarios. Keep the two concerns separate.

### 7. Stale Diagrams

**Problem:** Diagrams that were accurate 6 months ago but have not been updated as the system evolved. Stale diagrams are worse than no diagrams because they actively mislead.

**Fix:** Treat L1 and L2 diagrams as living documentation — update them as part of architectural decision processes. Generate L4 diagrams from code rather than maintaining them manually. Include a "last updated" note on each diagram. Review diagrams quarterly or as part of architecture review sessions.

### 8. Diagram Without Narrative

**Problem:** A diagram alone, without any surrounding text explaining the key decisions, trade-offs, or important relationships, forces viewers to interpret everything themselves.

**Fix:** Accompany each diagram with a brief narrative (3-5 sentences) explaining: why the system is structured this way, what the key architectural decisions are, and what the most important relationships are. The narrative should highlight what is not obvious from the diagram alone.

---

## Quick Reference: Mermaid C4 Syntax

For use in tools that support Mermaid C4 directives:

```
C4Context      — Level 1 diagrams
C4Container    — Level 2 diagrams
C4Component    — Level 3 diagrams
classDiagram   — Level 4 diagrams (standard UML)
sequenceDiagram — Dynamic diagrams
graph TB/LR    — Deployment diagrams
```

**Element types:**
```
Person(alias, "Name", "Description")
System(alias, "Name", "Description")
System_Ext(alias, "Name", "Description")
Container(alias, "Name", "Technology", "Description")
ContainerDb(alias, "Name", "Technology", "Description")
Container_Boundary(alias, "Name") { ... }
System_Boundary(alias, "Name") { ... }
Component(alias, "Name", "Type", "Description")
```

**Relationships:**
```
Rel(from, to, "Label")
Rel(from, to, "Label", "Protocol")
BiRel(from, to, "Label")
```

These templates can be copied directly into Mermaid-compatible tools, architecture decision records, or project documentation.
