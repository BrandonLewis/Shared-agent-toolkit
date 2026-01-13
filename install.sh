#!/bin/bash
#
# Shared Agent Toolkit Installation Script
#
# This script installs the shared agent toolkit by creating symlinks
# to the appropriate locations for your AI coding assistant.
#
# Usage:
#   ./install.sh [--global|--project] [--tool claude|cursor|aider]
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Default settings
INSTALL_SCOPE="global"
TOOL="claude"
DRY_RUN=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --global)
            INSTALL_SCOPE="global"
            shift
            ;;
        --project)
            INSTALL_SCOPE="project"
            shift
            ;;
        --tool)
            TOOL="$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --global        Install globally for your user (default)"
            echo "  --project       Install in current project directory"
            echo "  --tool NAME     Specify tool: claude, cursor, aider (default: claude)"
            echo "  --dry-run       Show what would be installed without making changes"
            echo "  --help          Show this help message"
            exit 0
            ;;
        *)
            echo -e "${RED}Error: Unknown option $1${NC}"
            exit 1
            ;;
    esac
done

# Function to print status messages
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Function to create symlink
create_symlink() {
    local source="$1"
    local target="$2"
    local description="$3"

    if [ "$DRY_RUN" = true ]; then
        echo "[DRY RUN] Would link: $target -> $source"
        return
    fi

    # Create parent directory if it doesn't exist
    mkdir -p "$(dirname "$target")"

    # Remove existing symlink or directory if it exists
    if [ -e "$target" ] || [ -L "$target" ]; then
        print_warning "Removing existing $description: $target"
        rm -rf "$target"
    fi

    # Create symlink
    ln -sf "$source" "$target"
    print_status "Linked $description: $target"
}

# Function to install for Claude Code
install_claude() {
    local base_dir="$1"

    echo ""
    echo "Installing for Claude Code..."
    echo "Target directory: $base_dir"
    echo ""

    # Create base directory
    mkdir -p "$base_dir"

    # Install commands
    create_symlink "$SCRIPT_DIR/commands" "$base_dir/commands/shared" "commands"

    # Install agents
    create_symlink "$SCRIPT_DIR/agents" "$base_dir/agents/shared" "agents"

    # Install skills
    create_symlink "$SCRIPT_DIR/skills" "$base_dir/skills/shared" "skills"

    # Install hooks (if global)
    if [ "$INSTALL_SCOPE" = "global" ]; then
        create_symlink "$SCRIPT_DIR/hooks" "$base_dir/hooks/shared" "hooks"
    fi

    print_status "Claude Code installation complete!"
}

# Function to install for Cursor
install_cursor() {
    local base_dir="$1"

    echo ""
    echo "Installing for Cursor..."
    echo "Target directory: $base_dir"
    echo ""

    mkdir -p "$base_dir"

    # Cursor uses .cursor/rules for prompts
    # We need to adapt our commands to Cursor's format
    if [ -f "$SCRIPT_DIR/adapters/cursor_adapter.py" ]; then
        print_warning "Converting commands to Cursor format..."
        if [ "$DRY_RUN" = false ]; then
            python3 "$SCRIPT_DIR/adapters/cursor_adapter.py" \
                --input "$SCRIPT_DIR/commands" \
                --output "$base_dir/rules/shared"
        fi
        print_status "Cursor rules generated"
    else
        print_warning "Cursor adapter not found, skipping conversion"
        create_symlink "$SCRIPT_DIR/commands" "$base_dir/rules/shared" "rules"
    fi

    print_status "Cursor installation complete!"
}

# Function to install for Aider
install_aider() {
    local base_dir="$1"

    echo ""
    echo "Installing for Aider..."
    echo "Target directory: $base_dir"
    echo ""

    mkdir -p "$base_dir"

    # Aider uses .aider directory
    create_symlink "$SCRIPT_DIR/commands" "$base_dir/aider/commands/shared" "commands"

    print_status "Aider installation complete!"
}

# Main installation logic
echo ""
echo "=========================================="
echo "  Shared Agent Toolkit Installation"
echo "=========================================="
echo ""
echo "Toolkit location: $SCRIPT_DIR"
echo "Install scope: $INSTALL_SCOPE"
echo "Tool: $TOOL"
if [ "$DRY_RUN" = true ]; then
    echo "Mode: DRY RUN (no changes will be made)"
fi
echo ""

# Determine installation directory
if [ "$INSTALL_SCOPE" = "global" ]; then
    case "$TOOL" in
        claude)
            BASE_DIR="$HOME/.claude"
            ;;
        cursor)
            BASE_DIR="$HOME/.cursor"
            ;;
        aider)
            BASE_DIR="$HOME/.aider"
            ;;
        *)
            print_error "Unknown tool: $TOOL"
            exit 1
            ;;
    esac
else
    # Project-local installation
    case "$TOOL" in
        claude)
            BASE_DIR="./.claude"
            ;;
        cursor)
            BASE_DIR="./.cursor"
            ;;
        aider)
            BASE_DIR="./.aider"
            ;;
        *)
            print_error "Unknown tool: $TOOL"
            exit 1
            ;;
    esac
fi

# Perform installation
case "$TOOL" in
    claude)
        install_claude "$BASE_DIR"
        ;;
    cursor)
        install_cursor "$BASE_DIR"
        ;;
    aider)
        install_aider "$BASE_DIR"
        ;;
esac

# Install MCP servers (global only)
if [ "$INSTALL_SCOPE" = "global" ] && [ "$TOOL" = "claude" ]; then
    echo ""
    echo "MCP Server Installation"
    echo "----------------------"
    print_warning "MCP servers require manual configuration"
    echo ""
    echo "To install MCP servers:"
    echo "  1. Navigate to the MCP server directory:"
    echo "     cd $SCRIPT_DIR/mcp-servers/[server-name]"
    echo "  2. Install the server:"
    echo "     pip install -e ."
    echo "  3. Configure in ~/.claude/mcp_settings.json"
    echo ""
    echo "Available MCP servers:"
    echo "  - example-mcp: Basic example server"
    echo "  - construction-toolkit: Construction industry tools"
    echo ""
    echo "See mcp-servers/*/README.md for configuration details"
fi

echo ""
echo "=========================================="
print_status "Installation complete!"
echo "=========================================="
echo ""

if [ "$DRY_RUN" = true ]; then
    echo "This was a dry run. No changes were made."
    echo "Run without --dry-run to actually install."
    echo ""
fi

# Show next steps
echo "Next steps:"
case "$TOOL" in
    claude)
        echo "  1. Restart Claude Code or reload your session"
        echo "  2. Try a command: /git-branch"
        echo "  3. Use an agent: @code-reviewer"
        echo "  4. Invoke a skill: /excel-automation"
        ;;
    cursor)
        echo "  1. Restart Cursor"
        echo "  2. Access rules through Cursor's rules system"
        ;;
    aider)
        echo "  1. Restart Aider"
        echo "  2. Access commands through Aider's command system"
        ;;
esac
echo ""
