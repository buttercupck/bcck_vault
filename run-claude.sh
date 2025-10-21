#!/bin/bash

# run-claude.sh - Launch Claude Code in an isolated Docker container
# This script provides filesystem isolation for Claude Code

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running${NC}"
    echo -e "${YELLOW}Please start Docker and try again${NC}"
    exit 1
fi

echo -e "${GREEN}🚀 Starting Claude Code in isolated Docker container...${NC}"
echo -e "${GREEN}📁 Working directory: $(pwd)${NC}"
echo -e "${GREEN}🔒 Filesystem access limited to current directory only${NC}"
echo -e "${GREEN}🔑 Using browser login for authentication${NC}"
echo ""

# Build the image if it doesn't exist
if ! docker images | grep -q "bcck_vault-claude-code"; then
    echo -e "${YELLOW}📦 Building Docker image (this may take a few minutes)...${NC}"
    docker-compose build
fi

# Run Claude Code in the container
docker-compose run --rm claude-code

echo -e "${GREEN}✅ Claude Code session ended${NC}"
