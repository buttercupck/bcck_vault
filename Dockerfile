FROM node:20-slim

# Install necessary tools
RUN apt-get update && apt-get install -y git curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Claude Code globally
RUN npm install -g @anthropic-ai/claude-code

# Create workspace directory
RUN mkdir -p /workspace

# Create a non-root user with a unique UID (using 1337 instead of 1000)
RUN useradd -m -u 1337 -s /bin/bash claude && \
    chown -R claude:claude /workspace

# Switch to non-root user
USER claude

WORKDIR /workspace

CMD ["claude"]
