"""
Apply all 8 feature enhancements to index.html
Adds:
1. Link to enhancements.css in <head>
2. Scroll progress bar div after <body>
3. Particle canvas in hero-visual
4. Back-to-top button before </body>
5. Script tag for enhancements.js before </body>
"""

filepath = r'c:\Users\SOUMYADIP\Desktop\THE VISIONARIES\index.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"Loaded: {len(content):,} characters")

changes_made = 0

# ---- 1. Add enhancements.css link in <head> ----
css_link = '  <link rel="stylesheet" href="enhancements.css">'
if 'enhancements.css' not in content:
    # Insert before </head>
    content = content.replace('</head>', css_link + '\n</head>', 1)
    changes_made += 1
    print("[OK] Added enhancements.css link")
else:
    print("[SKIP] enhancements.css already linked")

# ---- 2. Add scroll progress bar after <body> ----
scroll_div = '  <div class="scroll-progress" id="scrollProgress"></div>'
if 'scrollProgress' not in content:
    content = content.replace('<body>', '<body>\n\n' + scroll_div, 1)
    changes_made += 1
    print("[OK] Added scroll progress bar")
else:
    print("[SKIP] Scroll progress bar already exists")

# ---- 3. Add particle canvas inside hero-visual ----
particle_canvas = '        <canvas id="particleCanvas"></canvas>'
if 'particleCanvas' not in content:
    content = content.replace(
        '<div class="hero-visual">',
        '<div class="hero-visual">\n' + particle_canvas,
        1
    )
    changes_made += 1
    print("[OK] Added particle canvas")
else:
    print("[SKIP] Particle canvas already exists")

# ---- 4. Add back-to-top button before </body> ----
back_to_top = '''  <button class="back-to-top" id="backToTop" aria-label="Back to top">
    <svg viewBox="0 0 24 24"><path d="M12 4l-8 8h5v8h6v-8h5z"/></svg>
  </button>'''
if 'backToTop' not in content:
    content = content.replace('</body>', back_to_top + '\n\n</body>', 1)
    changes_made += 1
    print("[OK] Added back-to-top button")
else:
    print("[SKIP] Back-to-top button already exists")

# ---- 5. Add enhancements.js script before </body> ----
js_script = '  <script src="enhancements.js"></script>'
if 'enhancements.js' not in content:
    content = content.replace('</body>', js_script + '\n\n</body>', 1)
    changes_made += 1
    print("[OK] Added enhancements.js script")
else:
    print("[SKIP] enhancements.js already linked")

# ---- Write back ----
if changes_made > 0:
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"\n[DONE] Applied {changes_made} changes to index.html")
else:
    print("\n[DONE] No changes needed - all enhancements already applied")
