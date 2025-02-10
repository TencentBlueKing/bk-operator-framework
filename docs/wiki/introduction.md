**Note:** Impatient readers may head straight to [Quick Start](quick-start.md).

## Who is this for

#### Kubernetes API extension developers

API extension developers will learn the principles and concepts behind implementing canonical
Kubernetes APIs, as well as simple tools and libraries for rapid execution.

Including:

- How to batch multiple events into a single reconciliation call
- How to configure periodic reconciliation
- When to use the lister cache vs live lookups
- How to use Declarative vs Webhook Validation
- How to implement API versioning

## Why Kubernetes APIs

Kubernetes APIs provide consistent and well defined endpoints for
objects adhering to a consistent and rich structure.

This approach has fostered a rich ecosystem of tools and libraries for working
with Kubernetes APIs.

Users work with the APIs through declaring objects as *yaml* or *json* config, and using
common tooling to manage the objects.

Building services as Kubernetes APIs provides many advantages to plain old REST, including:

* Hosted API endpoints, storage, and validation.
* Rich tooling and CLIs such as `kubectl` and `kustomize`.
* Support for AuthN and granular AuthZ.
* Support for API evolution through API versioning and conversion.
* Facilitation of adaptive / self-healing APIs that continuously respond to changes
  in the system state without user intervention.
* Kubernetes as a hosting environment

Developers may build and publish their own Kubernetes APIs for installation into
running Kubernetes clusters.