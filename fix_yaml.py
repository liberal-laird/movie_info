#!/usr/bin/env python3
import os
import re

posts_dir = 'content/posts'
for f in os.listdir(posts_dir):
    if f.endswith('.md'):
        filepath = os.path.join(posts_dir, f)
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Fix plot field - replace plot: "value with " inside with proper escaping
        # Pattern: plot: "some text "quoted" text"
        pattern = r'(plot: )(".*?)"([^"]*?)(".*?)'
        def replacer(m):
            return m.group(1) + '"' + m.group(2).replace('"', '\\"') + '\\"' + m.group(3).replace('"', '\\"') + '"'
        
        content = re.sub(pattern, replacer, content)
        
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(content)

print("Done")
