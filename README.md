# MCP Servers

A collection of **Model Context Protocol (MCP) servers** built with Python and [FastMCP](https://github.com/modelcontextprotocol/python-sdk).

This repository is structured around a simple workflow:

* **Develop and run MCP servers locally** from the repository root
* **Build versioned Docker images** using the included build system
* **Deploy servers to Kubernetes** using server-specific manifests

Each MCP server is self-contained under `servers/`, while common functionality is provided through `shared/`.

## Repository Structure

```text
.
├── build.sh
├── pyproject.toml
├── shared/
│   ├── middleware/
│   ├── config.py
│   ├── db.py
│   ├── errors.py
│   └── logger.py
│
└── servers/
    ├── example/
    │   ├── k8s/
    │   ├── tools/
    │   ├── .env.example
    │   ├── Dockerfile
    │   ├── config.py
    │   ├── main.py
    │   └── server.py
    │
    └── runescape/
        ├── db/
        ├── k8s/
        ├── tools/
        ├── .env.example
        ├── .version
        ├── Dockerfile
        ├── config.py
        ├── main.py
        └── server.py
```

## Requirements

### Local development

* Python **3.12+**
* [uv](https://docs.astral.sh/uv/)

### Container builds

* Docker
* Docker BuildKit

### Kubernetes deployment

* A Kubernetes cluster
* `kubectl`
* Access to the container registry used by the build system

## Running Locally

MCP servers are run directly from the **repository root**.

First, install the project dependencies:

```bash
uv sync
```

Configure the server you want to run:

```bash
cp servers/example/.env.example servers/example/.env
```

Edit the environment file with the required configuration, then start the server from the repository root:

```bash
uv run python -m servers.example.main
```

For another server:

```bash
uv run python -m servers.runescape.main
```

The important part is that the command is run from the repository root. The project is configured so that the individual servers can import the shared infrastructure and their own modules correctly.

## Creating a New MCP Server

The `example` server is intended to be used as the starting point for creating new MCP servers.

A new server should follow the general structure:

```text
servers/<server_name>/
├── k8s/
├── tools/
├── .env.example
├── Dockerfile
├── config.py
├── main.py
└── server.py
```

The exact contents of `tools/` and `k8s/` will depend on the server.

### Server code

Server-specific functionality belongs under:

```text
servers/<server_name>/
```

MCP tools should be organized under:

```text
servers/<server_name>/tools/
```

### Shared functionality

Functionality that is useful across multiple MCP servers belongs under:

```text
shared/
```

The shared package currently provides infrastructure for areas including:

* Configuration
* Database access
* Logging
* Error handling
* Middleware

This keeps individual MCP servers focused on their own functionality rather than duplicating common infrastructure.

## Example Server

The `example` server is a reference implementation for building a new MCP server.

It demonstrates the common patterns used throughout the repository, including:

* FastMCP server setup
* Modular MCP tools
* Configuration through environment variables
* Logging
* Error handling and sanitization
* Prometheus metrics
* Docker packaging
* Kubernetes deployment

The example server should be considered the template for new servers rather than a production application in its own right.

## Kubernetes

Kubernetes is the intended deployment environment for the MCP servers.

Each server can contain its own Kubernetes configuration under:

```text
servers/<server_name>/k8s/
```

This keeps deployment configuration alongside the application it deploys.

For example:

```text
servers/example/
└── k8s/
    ├── ...
```

and:

```text
servers/runescape/
└── k8s/
    ├── ...
```

The Kubernetes manifests should reference the Docker image produced by the repository's build system.

## Building a Server

Docker images are built using the root-level `build.sh` script.

The script is designed to be run from the repository root:

```bash
./build.sh <server_name>
```

For example:

```bash
./build.sh runescape
```

By default, this performs a patch version increment and builds the Docker image for that server.

### Versioning

Each server maintains its own version in:

```text
servers/<server_name>/.version
```

The build script supports semantic version increments:

```bash
./build.sh runescape --patch
```

```bash
./build.sh runescape --minor
```

```bash
./build.sh runescape --major
```

If a `.version` file does not exist, the build system initializes it at `0.0.0`.

The version is only written after a successful Docker build.

### Build all servers

All servers can be built at once:

```bash
./build.sh --all
```

The same versioning and build options can be combined with `--all`:

```bash
./build.sh --all --minor
```

### Disable Docker cache

To perform a build without the Docker layer cache:

```bash
./build.sh runescape --no-cache
```

### Push an image

The build system can push the resulting image to the configured container registry:

```bash
./build.sh runescape --push
```

Options can be combined:

```bash
./build.sh runescape --minor --no-cache --push
```

## Docker Images

Images follow this naming convention:

```text
<registry>/mcp-<server>:<version>
<registry>/mcp-<server>:latest
```

The current build configuration uses:

```text
storage01:5000
```

For example:

```text
storage01:5000/mcp-runescape:1.2.3
storage01:5000/mcp-runescape:latest
```

The build system also adds metadata to each image describing the MCP server, version, registry, and build timestamp.

## Deploying to Kubernetes

Once an image has been built and pushed to the registry, the corresponding Kubernetes manifests can be used to deploy it.

For example, after building:

```bash
./build.sh runescape --push
```

review the manifests under:

```text
servers/runescape/k8s/
```

Ensure that the deployment references the desired image/version and that any environment-specific configuration is correct.

Then apply the manifests with `kubectl`.

For example:

```bash
kubectl apply -f servers/runescape/k8s/
```

The exact resources and deployment structure are server-specific, so the manifests under each server's `k8s/` directory are the source of truth for that deployment.

## Development Workflow

The intended workflow is:

```text
             ┌─────────────────────┐
             │  Develop MCP server │
             └──────────┬──────────┘
                        │
                        ▼
             ┌─────────────────────┐
             │   Run locally with  │
             │         uv          │
             └──────────┬──────────┘
                        │
                        ▼
             ┌─────────────────────┐
             │     ./build.sh      │
             │  Build versioned    │
             │    Docker image     │
             └──────────┬──────────┘
                        │
                        ▼
             ┌─────────────────────┐
             │ Push image to       │
             │ container registry  │
             └──────────┬──────────┘
                        │
                        ▼
             ┌─────────────────────┐
             │     Kubernetes      │
             │      deployment     │
             └─────────────────────┘
```

This keeps local development simple while making the resulting server ready for containerized Kubernetes deployment.

## Observability

The example server includes Prometheus metrics exposed on a dedicated port.

The shared infrastructure also provides common logging, middleware, error handling, and sanitization functionality.

These components are intended to provide a consistent operational baseline across the MCP servers.

## Configuration

Each server provides an `.env.example` file describing the configuration required for local development.

Create a local environment file with:

```bash
cp servers/<server_name>/.env.example servers/<server_name>/.env
```

Do not commit `.env` files or credentials to the repository.

For Kubernetes deployments, configuration should be provided through the appropriate Kubernetes resources rather than relying on local development environment files.

## Project Dependencies

Python dependencies are defined in `pyproject.toml`.

Install them with:

```bash
uv sync
```

The project currently uses FastMCP along with supporting libraries for HTTP requests, database access, PostgreSQL, Prometheus metrics, and application infrastructure.

## Contributing

Contributions and new MCP servers are welcome.

When creating a new server:

* Use `servers/example` as the starting point.
* Keep server-specific code under `servers/<server_name>/`.
* Put reusable functionality under `shared/`.
* Organize MCP tools under the server's `tools/` directory.
* Include a `Dockerfile`.
* Include Kubernetes manifests under `k8s/`.
* Provide an `.env.example` for local configuration.
* Maintain the server's `.version` file.
* Ensure the server can be run from the repository root.
* Ensure the server can be built using `build.sh`.
* Do not commit credentials or production secrets.

## License

This project is licensed under the **MIT License**. See [`LICENSE`](LICENSE) for details.
