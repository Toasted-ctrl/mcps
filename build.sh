#!/usr/bin/env bash
set -euo pipefail

# ─────────────────────────────────────────────
# build.sh — MCP Server Build Script
# ─────────────────────────────────────────────
# Usage:
#   ./build.sh <server_name>              # Build + auto-increment PATCH
#   ./build.sh <server_name> --minor      # Bump MINOR, reset PATCH to 0
#   ./build.sh <server_name> --major      # Bump MAJOR, reset MINOR & PATCH to 0
#   ./build.sh --all                      # Build all servers (patch increment)
#   ./build.sh <server_name> --no-cache   # Build without Docker layer cache
#
# Directory structure:
#   /
#   ├── build.sh
#   ├── pyproject.toml
#   ├── shared/
#   └── servers/
#       ├── runescape/
#       │   ├── .version
#       │   ├── Dockerfile
#       │   └── main.py
#       └── ...
#
# Image naming:
#   storage01:5000/mcp-<server_name>:<version>
#   storage01:5000/mcp-<server_name>:latest
# ─────────────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVERS_DIR="${SCRIPT_DIR}/servers"
SHARED_DIR="${SCRIPT_DIR}/shared"

# ─── Registry & naming config ──────────────
REGISTRY="storage01:5000"
IMAGE_PREFIX="mcp"

# ─── Docker config ─────────────────────────
export DOCKER_BUILDKIT=1

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# ─── Helpers ────────────────────────────────

log()   { echo -e "${CYAN}[build]${NC} $*"; }
ok()    { echo -e "${GREEN}[  ok ]${NC} $*"; }
warn()  { echo -e "${YELLOW}[warn ]${NC} $*"; }
err()   { echo -e "${RED}[error]${NC} $*" >&2; }

usage() {
    echo ""
    echo -e "${BOLD}MCP Server Build System${NC}"
    echo ""
    echo "Usage:"
    echo "  $0 <server_name> [--patch|--minor|--major] [--no-cache] [--push]"
    echo "  $0 --all [--patch|--minor|--major] [--no-cache] [--push]"
    echo ""
    echo "Options:"
    echo "  --patch      Increment patch version (default)"
    echo "  --minor      Bump minor version, reset patch to 0"
    echo "  --major      Bump major version, reset minor & patch to 0"
    echo "  --all        Build all servers in /servers"
    echo "  --no-cache   Pass --no-cache to docker build"
    echo "  --push       Push image to registry after build"
    echo ""
    echo "Images are tagged as:"
    echo "  ${REGISTRY}/${IMAGE_PREFIX}-<server>:<version>"
    echo "  ${REGISTRY}/${IMAGE_PREFIX}-<server>:latest"
    echo ""
    echo "Examples:"
    echo "  $0 runescape                # → ${REGISTRY}/${IMAGE_PREFIX}-runescape:0.0.1"
    echo "  $0 runescape --minor        # 1.2.3 → ${REGISTRY}/${IMAGE_PREFIX}-runescape:1.3.0"
    echo "  $0 --all --major --push     # bump all to next major & push"
    exit 1
}

# ─── Version management ────────────────────

read_version() {
    local version_file="$1"
    if [[ ! -f "$version_file" ]]; then
        echo "0.0.0" > "$version_file"
        warn "No .version file found — initialized to 0.0.0"
    fi
    cat "$version_file" | tr -d '[:space:]'
}

bump_version() {
    local current="$1"
    local bump_type="$2"

    local major minor patch
    IFS='.' read -r major minor patch <<< "$current"

    major="${major:-0}"
    minor="${minor:-0}"
    patch="${patch:-0}"

    case "$bump_type" in
        major) major=$((major + 1)); minor=0; patch=0 ;;
        minor) minor=$((minor + 1)); patch=0 ;;
        patch) patch=$((patch + 1)) ;;
        *)     err "Unknown bump type: $bump_type"; exit 1 ;;
    esac

    echo "${major}.${minor}.${patch}"
}

write_version() {
    echo "$2" > "$1"
}

# ─── Build logic ────────────────────────────

build_server() {
    local server_name="$1"
    local bump_type="$2"
    local docker_flags="$3"
    local push="$4"

    local server_dir="${SERVERS_DIR}/${server_name}"
    local version_file="${server_dir}/.version"
    local dockerfile="${server_dir}/Dockerfile"

    # ── Validate ──────────────────────────
    if [[ ! -d "$server_dir" ]]; then
        err "Server directory not found: ${server_dir}"
        return 1
    fi
    if [[ ! -f "$dockerfile" ]]; then
        err "Dockerfile not found: ${dockerfile}"
        return 1
    fi
    if [[ ! -d "$SHARED_DIR" ]]; then
        err "Shared directory not found: ${SHARED_DIR}"
        return 1
    fi

    # ── Version ───────────────────────────
    local current_version new_version
    current_version="$(read_version "$version_file")"
    new_version="$(bump_version "$current_version" "$bump_type")"

    # ── Image naming ──────────────────────
    #   storage01:5000/mcp-runescape:1.2.4
    #   storage01:5000/mcp-runescape:latest
    local image_base="${REGISTRY}/${IMAGE_PREFIX}-${server_name}"
    local image_tagged="${image_base}:${new_version}"
    local image_latest="${image_base}:latest"

    echo ""
    echo "╭──────────────────────────────────────────────────╮"
    printf "│  %-48s │\n" "${server_name}"
    printf "│  %-48s │\n" "${current_version} → ${new_version}  (${bump_type})"
    printf "│  %-48s │\n" "${image_tagged}"
    echo "╰──────────────────────────────────────────────────╯"

    # ── Docker build ──────────────────────
    log "Building Docker image..."

    if ! docker build \
        ${docker_flags} \
        -f "$dockerfile" \
        -t "$image_tagged" \
        -t "$image_latest" \
        --build-arg VERSION="$new_version" \
        --build-arg SERVER_NAME="$server_name" \
        --label "mcp.server=${server_name}" \
        --label "mcp.version=${new_version}" \
        --label "mcp.registry=${REGISTRY}" \
        --label "mcp.built=$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
        "$SCRIPT_DIR"; then

        err "Docker build FAILED for ${server_name} — version not incremented"
        return 1
    fi

    # ── Success: commit version ───────────
    write_version "$version_file" "$new_version"
    ok "Image built: ${image_tagged}"

    # ── Optional push ─────────────────────
    if [[ "$push" == "true" ]]; then
        log "Pushing to ${REGISTRY}..."
        docker push "$image_tagged"
        docker push "$image_latest"
        ok "Pushed ${image_tagged}"
        ok "Pushed ${image_latest}"
    fi

    ok "${server_name} @ v${new_version} ✓"
}

# ─── Entry point ────────────────────────────

main() {
    [[ $# -lt 1 ]] && usage

    local server_name=""
    local bump_type="patch"
    local build_all=false
    local docker_flags=""
    local push=false

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --major)     bump_type="major";         shift ;;
            --minor)     bump_type="minor";         shift ;;
            --patch)     bump_type="patch";         shift ;;
            --all)       build_all=true;            shift ;;
            --no-cache)  docker_flags="--no-cache"; shift ;;
            --push)      push=true;                 shift ;;
            --help|-h)   usage ;;
            -*)          err "Unknown option: $1"; usage ;;
            *)           server_name="$1";          shift ;;
        esac
    done

    echo ""
    echo "╔══════════════════════════════════════════════════╗"
    echo "║           MCP Server Build System                ║"
    printf "║           Registry: %-28s ║\n" "$REGISTRY"
    echo "╚══════════════════════════════════════════════════╝"

    if $build_all; then
        log "Building all servers (${bump_type})..."
        local failed=0
        local built=0
        for dir in "${SERVERS_DIR}"/*/; do
            [[ ! -d "$dir" ]] && continue
            local name
            name="$(basename "$dir")"

            if [[ ! -f "${dir}/Dockerfile" ]]; then
                warn "Skipping ${name} — no Dockerfile"
                continue
            fi

            if build_server "$name" "$bump_type" "$docker_flags" "$push"; then
                built=$((built + 1))
            else
                failed=$((failed + 1))
            fi
        done

        echo ""
        echo "────────────────────────────────────────"
        ok "Built: ${built}  |  Failed: ${failed}"

        [[ $failed -gt 0 ]] && exit 1
    else
        [[ -z "$server_name" ]] && { err "No server name specified."; usage; }
        build_server "$server_name" "$bump_type" "$docker_flags" "$push" || exit 1
    fi
}

main "$@"