#!/usr/bin/env python3
import os
import re

posts_dir = 'content/posts'
for f in os.listdir(posts_dir):
    if f.endswith('.md'):
        filepath = os.path.join(posts_dir, f)
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Fix plot field - make it single line and escape quotes
        # Match plot: "..." with possible multi-line content
        def fix_plot(match):
            rest = match.group(2)
            # Remove all quotes and newlines, make single line
            rest = rest.replace('\n', ' ').replace('"', "'").strip()
            if rest.endswith('-'):
                rest = rest[:-1]
            return f'plot: "{rest}"'
        
        content = re.sub(r'(plot: )"', fix_plot, content)
        
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(content)

print("Done")
