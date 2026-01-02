#!/usr/bin/env python3
"""
Script to add Next/Previous navigation buttons to HTML files in the course structure.
Each HTML file will link to the next/previous lesson folder's HTML files.
"""

import os
import re
from pathlib import Path
from typing import List, Tuple, Optional

def get_sorted_subfolders(pattern_folder: Path) -> List[Path]:
    """Get all subfolders in a pattern folder, sorted by their numeric prefix."""
    subfolders = [d for d in pattern_folder.iterdir() if d.is_dir()]
    
    # For "3. Pattern Two Pointers", exclude the mistakenly placed "4. Pattern Fast _ Slow pointers" folder
    if "3. Pattern Two Pointers" in str(pattern_folder):
        subfolders = [d for d in subfolders if "Pattern Fast" not in d.name]
    
    def extract_number(folder_name: str) -> int:
        # Extract the number from folder names like "1. Introduction" or "10. Solution Review..."
        match = re.match(r'^(\d+)\.', folder_name)
        return int(match.group(1)) if match else 9999
    
    subfolders.sort(key=lambda x: extract_number(x.name))
    return subfolders

def get_first_html_file(folder: Path) -> Optional[Path]:
    """Get the first HTML file in a folder (sorted alphabetically)."""
    html_files = list(folder.glob("*.html"))
    if html_files:
        html_files.sort()
        return html_files[0]
    return None

def get_relative_path(from_file: Path, to_file: Path) -> str:
    """Get relative path from one file to another."""
    try:
        relative = os.path.relpath(to_file, from_file.parent)
        return relative.replace(os.sep, '/')
    except ValueError:
        # If files are on different drives (Windows), return absolute path
        return str(to_file).replace('\\', '/')

def add_navigation_buttons(html_file: Path, prev_file: Optional[Path], next_file: Optional[Path], 
                          prev_folder_name: Optional[str], next_folder_name: Optional[str],
                          next_pattern_file: Optional[Path] = None, next_pattern_name: Optional[str] = None,
                          prev_pattern_file: Optional[Path] = None, prev_pattern_name: Optional[str] = None) -> bool:
    """Add navigation buttons to an HTML file."""
    try:
        with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Remove existing navigation if present (to avoid duplicates)
        # Match the navigation div pattern
        nav_pattern = r'<div style="position: fixed; bottom: 20px; right: 20px[^>]*>.*?</div></div>\s*'
        content = re.sub(nav_pattern, '', content, flags=re.DOTALL)
        
        # Create navigation HTML
        nav_html = '\n<div style="position: fixed; bottom: 20px; right: 20px; z-index: 10000; background: white; padding: 15px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.3); font-family: Arial, sans-serif; border: 2px solid #ddd;">'
        nav_html += '<div style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">'
        
        if prev_file:
            prev_path = get_relative_path(html_file, prev_file)
            nav_html += f'<a href="{prev_path}" style="padding: 12px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; font-weight: bold; white-space: nowrap; transition: background 0.3s;" onmouseover="this.style.background=\'#0056b3\'" onmouseout="this.style.background=\'#007bff\'">← Previous: {prev_folder_name}</a>'
        elif prev_pattern_file:
            # If no previous inner folder but there's a previous pattern folder, show button to previous pattern
            prev_pattern_path = get_relative_path(html_file, prev_pattern_file)
            nav_html += f'<a href="{prev_pattern_path}" style="padding: 12px 20px; background: #6f42c1; color: white; text-decoration: none; border-radius: 5px; font-weight: bold; white-space: nowrap; transition: background 0.3s;" onmouseover="this.style.background=\'#5a32a3\'" onmouseout="this.style.background=\'#6f42c1\'">← Previous Pattern: {prev_pattern_name}</a>'
        else:
            nav_html += '<span style="padding: 12px 20px; background: #ccc; color: #666; border-radius: 5px; font-weight: bold; cursor: not-allowed; white-space: nowrap;">← Previous</span>'
        
        if next_file:
            next_path = get_relative_path(html_file, next_file)
            nav_html += f'<a href="{next_path}" style="padding: 12px 20px; background: #28a745; color: white; text-decoration: none; border-radius: 5px; font-weight: bold; white-space: nowrap; transition: background 0.3s;" onmouseover="this.style.background=\'#218838\'" onmouseout="this.style.background=\'#28a745\'">Next: {next_folder_name} →</a>'
        elif next_pattern_file:
            # If no next inner folder but there's a next pattern folder, show button to next pattern
            next_pattern_path = get_relative_path(html_file, next_pattern_file)
            nav_html += f'<a href="{next_pattern_path}" style="padding: 12px 20px; background: #6f42c1; color: white; text-decoration: none; border-radius: 5px; font-weight: bold; white-space: nowrap; transition: background 0.3s;" onmouseover="this.style.background=\'#5a32a3\'" onmouseout="this.style.background=\'#6f42c1\'">Next Pattern: {next_pattern_name} →</a>'
        else:
            nav_html += '<span style="padding: 12px 20px; background: #ccc; color: #666; border-radius: 5px; font-weight: bold; cursor: not-allowed; white-space: nowrap;">Next →</span>'
        
        nav_html += '</div></div>\n'
        
        # Try to insert before </html> tag
        if '</html>' in content.lower():
            # Find the last occurrence of </html> (case insensitive)
            pattern = re.compile(r'</html>', re.IGNORECASE)
            matches = list(pattern.finditer(content))
            if matches:
                last_match = matches[-1]
                insert_pos = last_match.start()
                new_content = content[:insert_pos] + nav_html + content[insert_pos:]
            else:
                # If </html> not found, append at the end
                new_content = content + nav_html
        else:
            # If </html> not found, append at the end
            new_content = content + nav_html
        
        # Write back to file
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
    except Exception as e:
        print(f"Error processing {html_file}: {e}")
        return False

def get_last_html_file(folder: Path) -> Optional[Path]:
    """Get the last HTML file in a folder (sorted alphabetically)."""
    html_files = list(folder.glob("*.html"))
    if html_files:
        html_files.sort()
        return html_files[-1]
    return None

def process_pattern_folder(pattern_folder: Path, next_pattern_folder: Optional[Path] = None, prev_pattern_folder: Optional[Path] = None):
    """Process all HTML files in a pattern folder."""
    subfolders = get_sorted_subfolders(pattern_folder)
    
    if len(subfolders) == 0:
        return
    
    print(f"Processing pattern folder: {pattern_folder.name}")
    print(f"Found {len(subfolders)} subfolders")
    
    # Clean pattern folder name for display
    def clean_folder_name(name):
        cleaned = re.sub(r'^\d+\.\s*', '', name)
        return cleaned[:50]
    
    # Get next pattern folder info if available
    next_pattern_html = None
    next_pattern_name = None
    if next_pattern_folder:
        next_pattern_subfolders = get_sorted_subfolders(next_pattern_folder)
        if next_pattern_subfolders:
            first_subfolder = next_pattern_subfolders[0]
            next_pattern_html = get_first_html_file(first_subfolder)
            next_pattern_name = clean_folder_name(next_pattern_folder.name)
    
    # Get previous pattern folder info if available
    prev_pattern_html = None
    prev_pattern_name = None
    if prev_pattern_folder:
        prev_pattern_subfolders = get_sorted_subfolders(prev_pattern_folder)
        if prev_pattern_subfolders:
            last_subfolder = prev_pattern_subfolders[-1]
            prev_pattern_html = get_last_html_file(last_subfolder)
            prev_pattern_name = clean_folder_name(prev_pattern_folder.name)
    
    # Process each subfolder
    for i, subfolder in enumerate(subfolders):
        html_files = list(subfolder.glob("*.html"))
        
        # Determine previous and next folders
        prev_folder = subfolders[i - 1] if i > 0 else None
        next_folder = subfolders[i + 1] if i < len(subfolders) - 1 else None
        
        # Get HTML files from previous and next folders
        prev_html = get_first_html_file(prev_folder) if prev_folder else None
        next_html = get_first_html_file(next_folder) if next_folder else None
        
        prev_folder_name = clean_folder_name(prev_folder.name) if prev_folder else None
        next_folder_name = clean_folder_name(next_folder.name) if next_folder else None
        
        # If this is the last subfolder and no next inner folder, use next pattern folder
        use_next_pattern = (next_html is None and next_pattern_html is not None)
        
        # If this is the first subfolder and no previous inner folder, use previous pattern folder
        use_prev_pattern = (prev_html is None and prev_pattern_html is not None)
        
        # Process each HTML file in current subfolder
        for html_file in html_files:
            success = add_navigation_buttons(
                html_file, 
                prev_html, 
                next_html,
                prev_folder_name,
                next_folder_name,
                next_pattern_html if use_next_pattern else None,
                next_pattern_name if use_next_pattern else None,
                prev_pattern_html if use_prev_pattern else None,
                prev_pattern_name if use_prev_pattern else None
            )
            if success:
                print(f"  ✓ Added navigation to {html_file.name}")

def main():
    """Main function to process all pattern folders."""
    base_dir = Path(__file__).parent
    
    # Find all pattern folders (folders starting with a number and containing "Pattern")
    pattern_folders = []
    for item in base_dir.iterdir():
        if item.is_dir() and re.match(r'^\d+\.\s+Pattern', item.name):
            pattern_folders.append(item)
    
    # Also check for other folders that might be pattern folders
    for item in base_dir.iterdir():
        if item.is_dir() and item.name not in [p.name for p in pattern_folders]:
            # Check if it has numbered subfolders
            subfolders = [d for d in item.iterdir() if d.is_dir() and re.match(r'^\d+\.', d.name)]
            if subfolders:
                pattern_folders.append(item)
    
    # Sort pattern folders
    def extract_number(name: str) -> int:
        match = re.match(r'^(\d+)\.', name)
        return int(match.group(1)) if match else 9999
    
    pattern_folders.sort(key=lambda x: extract_number(x.name))
    
    print(f"Found {len(pattern_folders)} pattern folders")
    print("-" * 60)
    
    for i, pattern_folder in enumerate(pattern_folders):
        try:
            # Get next and previous pattern folders if available
            next_pattern = pattern_folders[i + 1] if i < len(pattern_folders) - 1 else None
            prev_pattern = pattern_folders[i - 1] if i > 0 else None
            process_pattern_folder(pattern_folder, next_pattern, prev_pattern)
            print()
        except Exception as e:
            print(f"Error processing {pattern_folder.name}: {e}")
            print()
    
    print("=" * 60)
    print("Navigation buttons added successfully!")

if __name__ == "__main__":
    main()

