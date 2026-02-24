#!/usr/bin/env python3
import os
import re

posts_dir = 'content/posts'
for f in os.listdir(posts_dir):
    if f.endswith('.md'):
        filepath = os.path.join(posts_dir, f)
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Find plot field and fix it
        lines = content.split('\n')
        new_lines = []
        i = 0
        while i < len(lines):
            line = lines[i]
            if line.startswith('plot:'):
                # Start collecting plot content
                if ': "' in line:
                    key, val = line.split(': ', 1)
                    plot_content = val.strip()
                    
                    # Continue reading until we hit the next field
                    i += 1
                    while i < len(lines):
                        next_line = lines[i].strip()
                        if next_line.startswith(('imdbId', 'tmdbId', '---', 'rating:')):
                            break
                        plot_content += ' ' + next_line
                        i += 1
                    
                    # Clean up plot content
                    plot_content = plot_content.replace('"', "'").replace('\n', ' ').strip()
                    if plot_content.endswith('-'):
                        plot_content = plot_content[:-1].strip()
                    
                    new_lines.append(f'plot: "{plot_content}"')
                    continue
            new_lines.append(line)
            i += 1
        
        content = '\n'.join(new_lines)
        
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(content)

print("Done")
