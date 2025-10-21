# Claude Code Docker Setup - Filesystem Isolation

This Docker setup provides **complete filesystem isolation** for Claude Code, restricting its access to only the `~/bcck_vault` directory while maintaining full bash capabilities within that sandboxed environment.

## 🔒 Why Filesystem Isolation?

Running Claude Code in a Docker container provides:

1. **Security**: Claude Code can only access files within the mounted directory (`~/bcck_vault`)
2. **Safety**: No accidental modifications to system files or other directories
3. **Controlled Environment**: Predictable, reproducible execution environment
4. **Peace of Mind**: Work with AI assistance without worrying about unintended filesystem access

## 📋 Prerequisites

- Docker installed and running (located at `~/Applications/Docker.app`)
- Web browser for Claude Code authentication

## 🚀 Quick Start

### 1. Make the script executable

```bash
chmod +x run-claude.sh
```

### 2. Run Claude Code

Simply execute:

```bash
./run-claude.sh
```

The script will:
- ✅ Check Docker is running
- ✅ Build the Docker image (first run only)
- ✅ Launch Claude Code in an isolated container

### 3. Authenticate via Browser

On first run, Claude Code will prompt you to authenticate via your web browser:
- Follow the prompts in the terminal
- Complete authentication in your browser
- Your authentication will be saved and persist between container sessions

## 📁 What Claude Code Can Access

**Inside the container:**
- ✅ Full read/write access to `/workspace` (maps to `~/bcck_vault` on your host)
- ✅ All bash commands (git, npm, node, etc.)
- ✅ Network access for API calls

**Outside the container:**
- ❌ No access to your home directory
- ❌ No access to system files
- ❌ No access to other directories on your computer
- ❌ No access to host processes or containers

## 🏗️ Architecture

```
Host Machine (macOS)
└── ~/bcck_vault/                    ← Your current directory
    │
    ├── Dockerfile                   ← Container configuration
    ├── docker-compose.yml           ← Service orchestration
    ├── run-claude.sh                ← Launch script
    └── .dockerignore                ← Files excluded from image
    │
    └── [Your Files]                 ← All your project files
        │
        └─────────────────────────▶ Mounted as /workspace in container
                                     │
                                     ▼
                            Docker Container
                            ├── /workspace/      ← Read/Write access
                            └── /home/claude/.config/claude-code/
                                └── (persisted auth in Docker volume)
```

## 🔧 Manual Usage

If you prefer manual control:

```bash
# Build the image
docker-compose build

# Run Claude Code
docker-compose run --rm claude-code

# Run a specific command
docker-compose run --rm claude-code claude --help
```

## 🛠️ How It Works

### Dockerfile
- **Base Image**: Node.js 20 (slim variant for smaller size)
- **Claude Code**: Installed globally via npm
- **User**: Runs as non-root user `claude` (UID 1337)
- **Working Directory**: `/workspace`

### docker-compose.yml
- **Volume Mounts**:
  - `.:/workspace` (current directory only)
  - `claude-config` (persisted Docker volume for authentication)
- **Authentication**: Browser login (no API key required)
- **Network**: Bridge mode (isolated from host network)
- **Interactive**: TTY and stdin enabled for interactive use

### run-claude.sh
- **Docker Check**: Verifies Docker is running
- **Auto-Build**: Builds image if not present
- **User-Friendly**: Color-coded output and clear error messages
- **Browser Auth**: Supports browser-based authentication

## 🔐 Security Notes

1. **Authentication**: Browser login credentials stored in isolated Docker volume
2. **Limited Scope**: Container can only access the mounted directory
3. **No Privileged Mode**: Container runs without elevated privileges
4. **Non-Root User**: Claude Code runs as user `claude`, not root
5. **Network Isolation**: Bridge network prevents access to host network
6. **Persistent Auth**: Authentication persists in named volume `claude-config`

## 🐛 Troubleshooting

### Docker Not Running
```bash
# Start Docker
open ~/Applications/Docker.app
# Wait for Docker to start, then run ./run-claude.sh again
```

### Authentication Issues
```bash
# If you need to re-authenticate, remove the auth volume
docker volume rm bcck_vault_claude-config

# Then run Claude Code again - it will prompt for browser login
./run-claude.sh
```

### Permission Issues
```bash
# Rebuild the container
docker-compose build --no-cache

# Remove old containers
docker-compose down
```

### Image Build Fails
```bash
# Clean up Docker
docker system prune -a

# Rebuild from scratch
docker-compose build --no-cache
```

## 📝 Additional Notes

- The container shares the same working directory as your host
- Git commits made inside the container will appear on your host
- Files created inside the container are owned by UID 1337 on the host
- The container is automatically removed after each session (`--rm` flag)
- Authentication persists in a Docker volume and survives container restarts

## 🔄 Updating Claude Code

To update Claude Code to the latest version:

```bash
# Rebuild the image
docker-compose build --no-cache
```

## ⚠️ Important Limitations

- Claude Code inside the container cannot access files outside `~/bcck_vault`
- Cannot interact with Docker on the host (no Docker-in-Docker)
- Cannot access host environment variables (except those passed explicitly)

## 📚 Additional Resources

- [Claude Code Documentation](https://docs.claude.com/claude-code)
- [Docker Documentation](https://docs.docker.com/)
- [Anthropic API](https://console.anthropic.com/)

---

**Created**: 2025-10-18
**Purpose**: Secure, isolated execution of Claude Code with filesystem constraints
