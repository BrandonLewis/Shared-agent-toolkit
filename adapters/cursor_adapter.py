#!/usr/bin/env python3
"""
Cursor Adapter
Converts Claude Code commands to Cursor rules format
"""

import argparse
import frontmatter
import sys
from pathlib import Path


def convert_command_to_cursor_rule(command_file: Path) -> str:
    """
    Convert a Claude Code command (markdown with frontmatter) to Cursor rule format

    Args:
        command_file: Path to Claude Code command file

    Returns:
        Cursor rule content as string
    """
    # Parse frontmatter
    with open(command_file, 'r') as f:
        post = frontmatter.load(f)

    # Extract metadata
    description = post.get('description', '')
    args = post.get('args', [])

    # Build Cursor rule
    cursor_rule = f"# {command_file.stem}\n\n"

    if description:
        cursor_rule += f"{description}\n\n"

    # Add instructions from content
    cursor_rule += post.content

    # Add arguments section if present
    if args:
        cursor_rule += "\n\n## Arguments\n\n"
        for arg in args:
            arg_name = arg.get('name', 'unnamed')
            arg_desc = arg.get('description', '')
            required = " (required)" if arg.get('required', False) else " (optional)"
            cursor_rule += f"- `{arg_name}`: {arg_desc}{required}\n"

    return cursor_rule


def convert_directory(input_dir: Path, output_dir: Path):
    """
    Convert all command files in a directory to Cursor rules

    Args:
        input_dir: Directory containing Claude Code commands
        output_dir: Output directory for Cursor rules
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # Process all .md files
    for command_file in input_dir.rglob("*.md"):
        # Preserve directory structure
        relative_path = command_file.relative_to(input_dir)
        output_file = output_dir / relative_path

        # Create output directory
        output_file.parent.mkdir(parents=True, exist_ok=True)

        try:
            # Convert and write
            cursor_rule = convert_command_to_cursor_rule(command_file)
            with open(output_file, 'w') as f:
                f.write(cursor_rule)

            print(f"✓ Converted: {relative_path}")

        except Exception as e:
            print(f"✗ Error converting {relative_path}: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description='Convert Claude Code commands to Cursor rules'
    )
    parser.add_argument(
        '--input',
        required=True,
        help='Input directory containing Claude Code commands'
    )
    parser.add_argument(
        '--output',
        required=True,
        help='Output directory for Cursor rules'
    )

    args = parser.parse_args()

    input_dir = Path(args.input)
    output_dir = Path(args.output)

    if not input_dir.exists():
        print(f"Error: Input directory does not exist: {input_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"Converting commands from {input_dir} to {output_dir}...")
    convert_directory(input_dir, output_dir)
    print("Conversion complete!")


if __name__ == '__main__':
    main()
