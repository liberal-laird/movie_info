#!/usr/bin/env python3
import os

posts_dir = 'content/posts'
for f in os.listdir(posts_dir):
    if f.endswith('.md'):
        filepath = os.path.join(posts_dir, f)
        with open(filepath, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        new_lines = []
        in_plot = False
        for i, line in enumerate(lines):
            if line.strip().startswith('plot:'):
                # Replace plot line with properly formatted version
                # Remove all double quotes from plot value
                if ': "' in line:
                    key, val = line.split(': ', 1)
                    val = val.strip()
                    if val.startswith('"') and val.endswith('"'):
                        val = val[1:-1]  # Remove surrounding quotes
                    val = val.replace('"', '')  # Remove internal quotes
                    line = f'{key}: "{val}"\n'
                in_plot = True
            elif in_plot and line.strip() == '---':
                in_plot = False
            new_lines.append(line)
        
        with open(filepath, 'w', encoding='utf-8') as file:
            file.writelines(new_lines)

print("Done")
