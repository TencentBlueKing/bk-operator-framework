# Quick Start

This Quick Start guide will cover:

- [Creating a project](#create-a-project)
- [Creating an API](#create-an-api)
- [Running locally](#test-it-out)
- [Running in-cluster](#run-it-on-the-cluster)

## Prerequisites

- [python](https://www.python.org/) version v3.9+
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) version v1.11.3+.
- [helm](https://helm.sh/docs/intro/install/) version v3.17.0 +.
- [docker](https://docs.docker.com/install/) version 17.03+.
- Access to a Kubernetes v1.11.3+ cluster.


## Installation

Install [bk_operator_framework](https://pypi.org/project/bk-operator-framework/):

```bash
# download bof and install locally.
pip install bk_operator_framework
```

## Create a Project

Create a directory, and then run the init command inside of it to initialize a new project. Follows an example.

```bash
mkdir -p ~/projects/guestbook
cd ~/projects/guestbook
bof init --domain power.dev
```

## Create an API

Run the following command to create a new API (group/version) as `apps/v1` and the new Kind(CRD) `Guestbook` on it:

```bash
bof create api --group apps --version v1 --kind Guestbook
```

<aside class="note">
<h1>Press Options</h1>

If you press `y` for Create Resource [y/n] and for Create Controller [y/n] then this will create the files `api/apps/v1/guestbook_schemas.py` where the API is defined
and the `internal/controller/guestbook_controller.py` where the reconciliation business logic is implemented for this Kind(CRD).

</aside>


**OPTIONAL:** Edit the API definition and the reconciliation business
logic. For more info see [Designing an API](cronjob-tutorial/api-design.md) and [What's in
a Controller](cronjob-tutorial/controller-overview.md).

<details><summary>Click here to see an example. (api/webapp/v1/guestbook_schemas.py)</summary>
<p>

```python
from pydantic import BaseModel, Field
from bk_operator_framework.generator.schemas import AdditionalPrinterColumn

# guestbooks is the plural form of GuestBook.
# Edit guestbook_schemas.py and project_desc.yaml to update it.
GUESTBOOK_PLURAL = "guestbooks"


class GuestBookSpec(BaseModel):
    """
    GuestBookSpec defines the desired state of GuestBook.
    """
    foo: str = Field(description="Foo is an example field of GuestBook. Edit guestbook_schemas.py to remove/update")


class GuestBookStatus(BaseModel):
    """
    GuestBookStatus defines the observed state of  GuestBook.
    """
    phase: str = Field(description="Phase is an example field of GuestBook. Edit guestbook_schemas.py to remove/update")


class GuestBook(BaseModel):
    """
    GuestBook is the Schema for the guestbooks API.
    """
    spec: GuestBookSpec
    status: GuestBookStatus


# Specifies additional columns returned in Table output.
# See https://kubernetes.io/docs/reference/using-api/api-concepts/#receiving-resources-as-tables for details.
# If no columns are specified, a single column displaying the age of the custom resource is used.
ADDITIONAL_PRINTER_COLUMN_LIST: list[AdditionalPrinterColumn] = []
```

</p>
</details>


## Test It Out

You'll need a Kubernetes cluster to run against.  You can use
[KIND](https://sigs.k8s.io/kind) to get a local cluster for testing, or
run against a remote cluster.

<aside class="note">
<h1>Context Used</h1>

Your controller will automatically use the current context in your
kubeconfig file (i.e. whatever cluster `kubectl cluster-info` shows).

</aside>

Install the CRDs into the cluster:
```bash
# create or update the project chart
bof chart

kubectl apply -f chart/crds/guestbooks.apps.power.dev.yaml
```

For quick feedback and code-level debugging, run your controller (this will run in the foreground, so switch to a new
terminal if you want to leave it running).More information can be found here: https://kopf.readthedocs.io/en/stable/cli/:

```bash
python main.py run controller -A --debug
```

## Run It On the Cluster
When your controller is ready to be packaged and tested in other clusters.

```bash
# build project image
docker build . -t <some-registry>/<project-name>:tag
docker push <some-registry>/<project-name>:tag

# create or update the project chart
bof chart

# modify chart.values.yaml and deploy
helm install {project_name} chart/
```

<aside class="note">

<h1>RBAC errors</h1>

If you encounter RBAC errors, you may need to grant yourself cluster-admin
privileges or be logged in as admin. See [Using RBAC Authorization](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) which may be your case.

</aside>

## Uninstall Project

To delete your Project from the cluster:

```bash
helm uninstall {project_name}
```