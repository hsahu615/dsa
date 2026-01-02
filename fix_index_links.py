#!/usr/bin/env python3
"""
Script to fix index.html links to point directly to HTML files instead of folders.
"""

import re
from pathlib import Path

def get_first_html_file(folder: Path) -> str:
    """Get the first HTML file in a folder (sorted alphabetically)."""
    html_files = list(folder.glob("*.html"))
    if html_files:
        html_files.sort()
        return html_files[0].name
    return None

def fix_index_html():
    """Fix index.html to link to specific HTML files."""
    base_dir = Path(__file__).parent
    index_file = base_dir / "index.html"
    
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match href attributes pointing to folders
    # Match: href="1. Introduction/" or href="2. Pattern Sliding Window/1. Introduction/"
    pattern = r'href="([^"]+/)"'
    
    def replace_link(match):
        folder_path = match.group(1)
        # Remove trailing slash
        folder_path = folder_path.rstrip('/')
        folder = base_dir / folder_path
        
        if folder.exists() and folder.is_dir():
            first_html = get_first_html_file(folder)
            if first_html:
                # Return the new href with the HTML file
                return f'href="{folder_path}/{first_html}"'
        
        # If folder doesn't exist or no HTML file found, return original
        return match.group(0)
    
    # Replace all folder links with file links
    new_content = re.sub(pattern, replace_link, content)
    
    # Write back
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✓ Fixed index.html links to point to specific HTML files")

if __name__ == "__main__":
    fix_index_html()

