# MCP Servers

[![Kubernetes](https://img.shields.io/badge/Kubernetes-1.36.3-326CE5?logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Keel](https://img.shields.io/badge/Keel-Kubernetes%20Operator-326CE5?logo=kubernetes&logoColor=white)](https://keel.sh/)
[![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?logo=prometheus&logoColor=white)](https://prometheus.io/)


A collection of Model Context Protocol (MCP) servers built with Python and FastMCP.

The repository currently contains two servers, both ready to run locally, build as Docker images, and deploy to Kubernetes.

## Quick Start

Install dependencies with uv:

```bash
uv sync
```


Each server includes an `.env.example` with the required configuration. Copy it to `.env`, configure it, and run the server from the repository root:

```bash
uv run python -m servers.example.main
```

### 1. Building

The included `build.sh` script handles Docker image builds and versioning.

Build a single server:

```bash
./build.sh runescape
```

### 2. Build all servers:

```bash
./build.sh --all
```


The script also supports version increments, cache control, and pushing images to the configured registry. See `./build.sh --help` for available options.

### 3. Kubernetes

Both servers include complete Kubernetes manifests under their respective `k8s/` directories:
```text
servers/
├── example/
│   └── k8s/
└── runescape/
    └── k8s/
```


After building and pushing an image, the manifests can be applied with `kubectl`:

```bash
kubectl apply -f servers/runescape/k8s/
```

## Contributing

PRs are very welcome! If you have improvements, new servers, tools, or ideas, feel free to open a pull request.