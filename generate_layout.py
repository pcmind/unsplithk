import json

def generate_layout():
    # Hardcoded left-hand layout coordinates (20 keys) from xxxxx.info.yaml
    # Thumb cluster is shifted closer horizontally towards the center by 0.4 units
    left = [
        # Row 0 (Top Row)
        {"x": 0.0, "y": 2.75, "r": 0.0, "rx": 0.0, "ry": 2.75},
        {"x": 1.0, "y": 1.75, "r": 0.0, "rx": 1.0, "ry": 1.75},
        {"x": 2.0, "y": 1.0, "r": 0.0, "rx": 2.0, "ry": 1.0},
        {"x": 3.0, "y": 0.5, "r": 0.0, "rx": 3.0, "ry": 0.5},
        {"x": 4.0, "y": 1.0, "r": 0.0, "rx": 4.0, "ry": 1.0},
        {"x": 5.0, "y": 1.75, "r": 0.0, "rx": 5.0, "ry": 1.75},

        # Row 1 (Home Row)
        {"x": 0.25, "y": 3.75, "r": 0.0, "rx": 0.25, "ry": 3.75},
        {"x": 1.15, "y": 2.75, "r": 0.0, "rx": 1.15, "ry": 2.75},
        {"x": 2.1, "y": 2.0, "r": 0.0, "rx": 2.1, "ry": 2.0},
        {"x": 3.0, "y": 1.5, "r": 0.0, "rx": 3.0, "ry": 1.5},
        {"x": 3.9, "y": 2.0, "r": 0.0, "rx": 3.9, "ry": 2.0},
        {"x": 4.85, "y": 2.75, "r": 0.0, "rx": 4.85, "ry": 2.75},

        # Row 2 (Bottom Row)
        {"x": 1.3, "y": 3.75, "r": 0.0, "rx": 1.3, "ry": 3.75},
        {"x": 2.2, "y": 3.0, "r": 0.0, "rx": 2.2, "ry": 3.0},
        {"x": 3.0, "y": 2.5, "r": 0.0, "rx": 3.0, "ry": 2.5},
        {"x": 3.8, "y": 3.0, "r": 0.0, "rx": 3.8, "ry": 3.0},
        {"x": 4.7, "y": 3.75, "r": 0.0, "rx": 4.7, "ry": 3.75},

        # Left Thumb Cluster (Sweeping Outward Right) - Shifted horizontally right (inwards) by 0.4 units
        {"x": 3.65, "y": 4.7, "r": 30.0, "rx": 3.65, "ry": 4.7},
        {"x": 4.5, "y": 5.5, "r": 35.0, "rx": 4.5, "ry": 5.5},
        {"x": 5.25, "y": 6.4, "r": 40.0, "rx": 5.25, "ry": 6.4}
    ]
    
    # We enforce perfect mathematical symmetry across the x = 7.5 axis
    x_center = 7.5
    
    # 1. Left side keys extraction (20 keys defined, but only 19 are used in the 38-key layout)
    # - Row 0: Pinky Top, Ring Top, Middle Top, Index Top, Inner Top (5 keys, skipping index 0)
    left_top = left[1:6]
    
    # - Row 1: Outer Pinky Extension (index 0 from top row), Pinky Home, Ring Home, Middle Home, Index Home, Inner Home (6 keys)
    left_home = [left[0]] + left[7:12]
    
    # - Row 2: Pinky Bottom, Ring Bottom, Middle Bottom, Index Bottom, Inner Bottom (5 keys)
    left_bottom = left[12:17]
    
    # - Thumbs: Key 1, Key 2, Key 3 (3 keys)
    left_thumbs = left[17:20]
    
    # 2. Re-mirror left keys to right keys to ensure absolute mathematical symmetry
    # Mirrored top-left corner coordinate is: 2 * x_center - x - key_width (where key_width = 1.0)
    right_top = []
    for k in reversed(left_top):
        right_top.append({
            'x': 2 * x_center - k['x'] - 1.0,
            'y': k['y'],
            'r': -k['r'],
            'rx': 2 * x_center - k['rx'],
            'ry': k['ry']
        })
        
    right_home = []
    for k in reversed(left_home):
        right_home.append({
            'x': 2 * x_center - k['x'] - 1.0,
            'y': k['y'],
            'r': -k['r'],
            'rx': 2 * x_center - k['rx'],
            'ry': k['ry']
        })
        
    right_bottom = []
    for k in reversed(left_bottom):
        right_bottom.append({
            'x': 2 * x_center - k['x'] - 1.0,
            'y': k['y'],
            'r': -k['r'],
            'rx': 2 * x_center - k['rx'],
            'ry': k['ry']
        })
        
    right_thumbs = []
    # Left thumbs are Outer-to-Inner, so mirrored Right thumbs innermost-to-outermost are:
    # Mirrored Key 3 (innermost), Mirrored Key 2 (middle), Mirrored Key 1 (outermost)
    for k in [left_thumbs[2], left_thumbs[1], left_thumbs[0]]:
        right_thumbs.append({
            'x': 2 * x_center - k['x'] - 1.0,
            'y': k['y'],
            'r': -k['r'],
            'rx': 2 * x_center - k['rx'],
            'ry': k['ry']
        })

    # 3. Assemble all 38 keys row-by-row
    all_keys = []
    # Row 0: 10 keys
    all_keys.extend(left_top)
    all_keys.extend(right_top)
    
    # Row 1: 12 keys
    all_keys.extend(left_home)
    all_keys.extend(right_home)
    
    # Row 2: 10 keys
    all_keys.extend(left_bottom)
    all_keys.extend(right_bottom)
    
    # Row 3: 6 keys
    all_keys.extend(left_thumbs)
    all_keys.extend(right_thumbs)
    
    # 4. Normalize coordinates for centering and scaling in keymap-drawer
    xs = [k['x'] for k in all_keys]
    ys = [k['y'] for k in all_keys]
    
    offset_x = 0.5 - min(xs)
    offset_y = 0.5 - min(ys)
    
    formatted_keys = []
    for k in all_keys:
        formatted_keys.append({
            'x': round(k['x'] + offset_x, 3),
            'y': round(k['y'] + offset_y, 3),
            'r': round(k['r'], 1),
            'rx': round(k['rx'] + offset_x, 3),
            'ry': round(k['ry'] + offset_y, 3)
        })
        
    info_json = {
        "keyboard_name": "unsplithk",
        "layouts": {
            "LAYOUT_unsplithk": {
                "layout": formatted_keys
            }
        }
    }
    
    # Write to unsplithk_info.json
    with open('unsplithk_info.json', 'w') as f:
        json.dump(info_json, f, indent=2)
        
    # Open unsplithk.yaml and replace the layout line
    try:
        with open('unsplithk.yaml', 'r') as f:
            content = f.read()
    except FileNotFoundError:
        content = "layout: {zmk_keyboard: unsplithk}\n"
        
    # Post-process layers to highlight the active/held toggle keys
    held_keys = {
        'nav': {33: '  - {type: held}'},
        'num': {36: '  - {type: held}'},
        'mouse': {34: '  - {type: held}'},
        'sym': {35: '  - {type: held}'},
        'fun': {32: '  - {type: held}'},
        'macro_l': {25: '  - {type: held}'},
    }

    new_lines = []
    current_layer = None
    key_counter = 0
    
    lines = content.split('\n')
    for line in lines:
        stripped = line.strip()
        
        # Detect start of layers section
        if stripped == 'layers:':
            current_layer = None
            new_lines.append(line)
            continue
            
        # Detect end of layers / start of combos
        if stripped == 'combos:':
            current_layer = None
            new_lines.append(line)
            continue
            
        # Detect none_l layer definition
        if stripped.startswith('none_l:'):
            new_lines.append("  none_l:")
            for idx in range(38):
                if idx in (10, 21):
                    new_lines.append("  - {type: held}")
                else:
                    new_lines.append("  - ''")
            current_layer = 'none_l'
            continue
            
        # Detect regular layer names
        if line.startswith('  ') and line.endswith(':') and not line.startswith('    '):
            current_layer = line.replace(':', '').strip()
            key_counter = 0
            new_lines.append(line)
            continue
            
        # If we are parsing keys in none_l, skip them (since we already expanded it)
        if current_layer == 'none_l' and line.startswith('  - '):
            continue
            
        # If we are parsing keys in other layers, perform replacement
        if current_layer and line.startswith('  - '):
            if current_layer in held_keys and key_counter in held_keys[current_layer]:
                new_lines.append(held_keys[current_layer][key_counter])
            else:
                new_lines.append(line)
            key_counter += 1
        else:
            new_lines.append(line)
            
    content = '\n'.join(new_lines)

    # Post-process combos to ensure they are visually positioned beautifully:
    # 1. none_layer / soft_off combo: keep trigger on [10, 21] (origin) but align to top of keyboard restricted to default layer
    content = content.replace(
        "- p: [10, 21]\n  k: {t: none_l, h: toggle}",
        "- p: [10, 21]\n  k: {t: none_l, h: toggle}\n  l: [default]\n  a: top"
    ).replace(
        "- p: [10, 21]\n  k: none_l",
        "- p: [10, 21]\n  k: none_l\n  l: [default]\n  a: top"
    ).replace(
        "- p: [10, 21]\n  k: '&soft_off'",
        "- p: [10, 21]\n  k: '&soft_off'\n  l: [default]\n  a: top"
    ).replace(
        "- p: [10, 21]\n  k: soft_off",
        "- p: [10, 21]\n  k: soft_off\n  l: [default]\n  a: top"
    )

    # 2. bluetooth combo: ensure it has l: [default] and a: bottom
    if "- p: [35, 36, 37]\n  k: bluetooth\n  l: [default]\n  a: bottom" not in content and "- p: [35, 36, 37]\n  k: bluetooth" in content:
        content = content.replace(
            "- p: [35, 36, 37]\n  k: bluetooth\n  a: bottom\n  l: [default]",
            "- p: [35, 36, 37]\n  k: bluetooth\n  l: [default]\n  a: bottom"
        ).replace(
            "- p: [35, 36, 37]\n  k: bluetooth\n  l: [default]\n  a: bottom",
            "- p: [35, 36, 37]\n  k: bluetooth\n  l: [default]\n  a: bottom"
        ).replace(
            "- p: [35, 36, 37]\n  k: bluetooth\n  a: bottom",
            "- p: [35, 36, 37]\n  k: bluetooth\n  l: [default]\n  a: bottom"
        ).replace(
            "- p: [35, 36, 37]\n  k: bluetooth",
            "- p: [35, 36, 37]\n  k: bluetooth\n  l: [default]\n  a: bottom"
        )

    # 3. game combo: ensure it has l: [default, game] and a: bottom
    if "- p: [32, 33, 34]\n  k: {t: game, h: toggle}\n  l: [default, game]\n  a: bottom" not in content and "- p: [32, 33, 34]\n  k: {t: game, h: toggle}" in content:
        content = content.replace(
            "- p: [32, 33, 34]\n  k: {t: game, h: toggle}\n  a: bottom",
            "- p: [32, 33, 34]\n  k: {t: game, h: toggle}\n  l: [default, game]\n  a: bottom"
        ).replace(
            "- p: [32, 33, 34]\n  k: {t: game, h: toggle}",
            "- p: [32, 33, 34]\n  k: {t: game, h: toggle}\n  l: [default, game]\n  a: bottom"
        )
        
    # 4. align underscore and star combos to top of the keyboard (above the entire keyboard layout)
    if "- p: [12, 14]\n  k: {t: _, h: Alt+Ctrl}\n  a: top" not in content:
        content = content.replace(
            "- p: [12, 14]\n  k: {t: _, h: Alt+Ctrl}",
            "- p: [12, 14]\n  k: {t: _, h: Alt+Ctrl}\n  a: top\n  o: 2.5"
        )
    if "- p: [17, 19]\n  k: {t: '*', h: Alt+Ctrl}\n  a: top" not in content:
        content = content.replace(
            "- p: [17, 19]\n  k: {t: '*', h: Alt+Ctrl}",
            "- p: [17, 19]\n  k: {t: '*', h: Alt+Ctrl}\n  a: top\n  o: 2.5"
        )


    lines = content.split('\n')
    layout_index = -1
    for idx, line in enumerate(lines):
        if line.startswith('layout:'):
            layout_index = idx
            break
            
    layout_str = "layout:\n  qmk_keyboard: unsplithk\n  qmk_layout: LAYOUT_unsplithk"
    
    if layout_index != -1:
        lines[layout_index] = layout_str
        new_content = '\n'.join(lines)
    else:
        new_content = layout_str + "\n" + content
        
    with open('unsplithk.yaml', 'w') as f:
        f.write(new_content)
        
    print("Success! Symmetrical physical layout coordinates with rotation centers successfully generated!")

if __name__ == '__main__':
    generate_layout()
