import json

def generate_layout():
    # Exact left-hand key center coordinates (mm) and rotations (deg CCW) from ergogen.yaml (u = 19.0 mm)
    u = 19.0
    left_top_mm = [
        {"x": 24.8722284, "y": 35.8762077, "r": -9.0},   # matrix_pinky_top
        {"x": 53.9125537, "y": 41.7069054, "r": -20.0},  # matrix_ring_top
        {"x": 78.0183072, "y": 42.4122248, "r": -24.0},  # matrix_middle_top
        {"x": 95.8915730, "y": 30.0190226, "r": -27.0},  # matrix_index_top
        {"x": 111.4587065, "y": 18.7201727, "r": -27.0}, # matrix_inner_top
    ]
    left_home_mm = [
        {"x": 2.0045821, "y": 22.9124781, "r": -5.0},    # matrix_outer_home
        {"x": 21.8999639, "y": 17.1101242, "r": -9.0},   # matrix_pinky_home
        {"x": 47.4141695, "y": 23.8527481, "r": -20.0},  # matrix_ring_home
        {"x": 70.2903152, "y": 25.0548650, "r": -24.0},  # matrix_middle_home
        {"x": 87.2657435, "y": 13.0899199, "r": -27.0},  # matrix_index_home
        {"x": 102.8328770, "y": 1.7910700, "r": -27.0},  # matrix_inner_home
    ]
    left_bottom_mm = [
        {"x": 18.9276993, "y": -1.6559591, "r": -9.0},   # matrix_pinky_bottom
        {"x": 40.9157853, "y": 5.9985908, "r": -20.0},   # matrix_ring_bottom
        {"x": 62.5623232, "y": 7.6975051, "r": -24.0},   # matrix_middle_bottom
        {"x": 78.6399140, "y": -3.8391827, "r": -27.0},  # matrix_index_bottom
        {"x": 94.2070475, "y": -15.1380326, "r": -27.0}, # matrix_inner_bottom
    ]
    left_thumbs_mm = [
        {"x": 78.4361693, "y": -30.6713244, "r": -37.0}, # thumbs_layer_cluster
        {"x": 93.5115853, "y": -44.9324773, "r": -47.0}, # thumbs_space_cluster
        {"x": 106.0630753, "y": -61.0990206, "r": -57.0},# thumbs_tab_cluster
    ]

    # Mirror axis from ergogen.yaml: ref matrix_inner_top, distance 2.5kx
    axis_x_mm = left_top_mm[-1]["x"] + 1.25 * u  # 135.2087065 mm
    axis_x_u = axis_x_mm / u

    def to_qmk_key(pt_mm):
        # Convert Ergogen (center in mm, +y up, +r CCW) to QMK/Keymap Editor (top-left x/y in u, center rx/ry in u, +y down, +r CW)
        cx = pt_mm["x"] / u
        cy = -pt_mm["y"] / u
        r = -pt_mm["r"]
        return {"x": cx - 0.5, "y": cy - 0.5, "r": r, "rx": cx, "ry": cy}

    def mirror_qmk_key(k):
        cx_mirrored = 2.0 * axis_x_u - k["rx"]
        cy_mirrored = k["ry"]
        return {
            "x": cx_mirrored - 0.5,
            "y": cy_mirrored - 0.5,
            "r": -k["r"],
            "rx": cx_mirrored,
            "ry": cy_mirrored,
        }

    left_top = [to_qmk_key(p) for p in left_top_mm]
    left_home = [to_qmk_key(p) for p in left_home_mm]
    left_bottom = [to_qmk_key(p) for p in left_bottom_mm]
    left_thumbs = [to_qmk_key(p) for p in left_thumbs_mm]

    right_top = [mirror_qmk_key(k) for k in reversed(left_top)]
    right_home = [mirror_qmk_key(k) for k in reversed(left_home)]
    right_bottom = [mirror_qmk_key(k) for k in reversed(left_bottom)]
    right_thumbs = [mirror_qmk_key(k) for k in reversed(left_thumbs)]

    # Assemble all 38 keys row-by-row
    all_keys = (
        left_top + right_top +
        left_home + right_home +
        left_bottom + right_bottom +
        left_thumbs + right_thumbs
    )

    # Normalize coordinates so mirror axis is at x = 8.0 and top-most key starts at y = 0.5
    ys = [k['y'] for k in all_keys]
    offset_x = 8.0 - axis_x_u
    offset_y = 0.5 - min(ys)

    # Ortholinear row/col matrix positions required by Keymap Editor (with col 6 gap between halves)
    row_cols = (
        [(0, c) for c in [1, 2, 3, 4, 5, 7, 8, 9, 10, 11]] +
        [(1, c) for c in [0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12]] +
        [(2, c) for c in [1, 2, 3, 4, 5, 7, 8, 9, 10, 11]] +
        [(3, c) for c in [3, 4, 5, 7, 8, 9]]
    )
    
    formatted_keys = []
    for idx, k in enumerate(all_keys):
        row, col = row_cols[idx]
        x_val = round(k['x'] + offset_x, 3)
        y_val = round(k['y'] + offset_y, 3)
        r_val = round(k['r'], 1)
        if r_val == 0:
            r_val = 0.0
            rx_val = x_val
            ry_val = y_val
        else:
            rx_val = round(k['rx'] + offset_x, 3)
            ry_val = round(k['ry'] + offset_y, 3)

        formatted_keys.append({
            'row': row,
            'col': col,
            'x': x_val,
            'y': y_val,
            'r': r_val,
            'rx': rx_val,
            'ry': ry_val
        })
        
    info_json = {
        "id": "unsplithk",
        "name": "Unsplithk",
        "keyboard_name": "unsplithk",
        "layouts": {
            "default_transform": {
                "name": "default_transform",
                "layout": formatted_keys
            },
            "LAYOUT_unsplithk": {
                "name": "LAYOUT_unsplithk",
                "layout": formatted_keys
            }
        },
        "sensors": []
    }
    
    # Write to unsplithk_info.json and config/unsplithk.json
    with open('unsplithk_info.json', 'w') as f:
        json.dump(info_json, f, indent=2)
        f.write('\n')

    with open('config/unsplithk.json', 'w') as f:
        json.dump(info_json, f, indent=2)
        f.write('\n')
        
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

    # 3. game combo: ensure it has l: [default, gamefps] and a: bottom
    content = content.replace("l: [default, game]", "l: [default, gamefps]")
    for game_layer in ("gamefps", "game"):
        content = content.replace(
            f"- p: [32, 33, 34]\n  k: {{t: {game_layer}, h: toggle}}\n  a: bottom",
            f"- p: [32, 33, 34]\n  k: {{t: {game_layer}, h: toggle}}\n  l: [default, gamefps]\n  a: bottom"
        )
        if f"- p: [32, 33, 34]\n  k: {{t: {game_layer}, h: toggle}}\n  l: [default, gamefps]\n  a: bottom" not in content:
            content = content.replace(
                f"- p: [32, 33, 34]\n  k: {{t: {game_layer}, h: toggle}}",
                f"- p: [32, 33, 34]\n  k: {{t: {game_layer}, h: toggle}}\n  l: [default, gamefps]\n  a: bottom"
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


    layout_str = "layout:\n  qmk_keyboard: unsplithk\n  qmk_layout: LAYOUT_unsplithk"
    
    if "layout:\n  qmk_keyboard: unsplithk\n  qmk_layout: LAYOUT_unsplithk" in content:
        new_content = content
    else:
        lines = content.split('\n')
        layout_index = -1
        for idx, line in enumerate(lines):
            if line.startswith('layout:'):
                layout_index = idx
                break
        if layout_index != -1:
            end_idx = layout_index + 1
            while end_idx < len(lines) and lines[end_idx].startswith('  '):
                end_idx += 1
            lines[layout_index:end_idx] = [layout_str]
            new_content = '\n'.join(lines)
        else:
            new_content = layout_str + "\n" + content
        
    with open('unsplithk.yaml', 'w') as f:
        f.write(new_content)
        
    print("Success! Symmetrical physical layout coordinates with rotation centers successfully generated!")

if __name__ == '__main__':
    generate_layout()
