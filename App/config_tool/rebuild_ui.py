import json

KEY_NAMES = [
    # Source 0
    "Enter", "Right Shift", "←", "↓", "→", "↑", "Numpad 0", "Numpad .", "\\", "Backspace", "F11", "F10", "=", "]", "-", "F9",
    # Source 1
    ";", "L", ".", "/", "Right GUI", "'", "Menu", "Right Ctrl", "[", "F8", "0", "P", "F7", "9", "F6", "O",
    # Source 2
    "H", "J", "N", "M", "K", ",", "Right Alt", "8", "I", "F5", "7", "U", "F4", "Y", "6",
    # Source 3
    "X", "D", "F", "C", "Space", "G", "V", "B", "5", "T", "F3", "4", "R", "E", "F2", "3",
    # Source 4
    "Numpad 9", "Numpad -", "Numpad 8", "User Key 1", "Numpad *", "User Key 2", "Numpad 7", "Numpad /", "Numpad 1", "Numpad 4", "Numpad 2", "Numpad Enter", "Numpad 5", "Numpad +", "Numpad 6", "Numpad 3",
    # Source 5
    "Scroll Lock", "Home", "Print Screen", "F12", "Insert", "Delete", "End", "Page Down", "Num Lock", "User Key 3", "Page Up", "User Key 4", "Pause",
    # Source 6
    "Caps Lock", "Left Shift", "Left Ctrl", "A", "S", "Z", "Left GUI", "Left Alt", "F1", "2", "W", "1", "Q", "Tab", "Escape", "`"
]

DEFAULT_CODES = [
    # Source 0
    0x28, 0xE5, 0x50, 0x51, 0x4F, 0x52, 0x62, 0x63, 0x31, 0x2A, 0x44, 0x43, 0x2E, 0x30, 0x2D, 0x42,
    # Source 1
    0x33, 0x0F, 0x37, 0x38, 0xE7, 0x34, 0x65, 0xE4, 0x2F, 0x41, 0x27, 0x13, 0x40, 0x26, 0x3F, 0x12,
    # Source 2
    0x0B, 0x0D, 0x11, 0x10, 0x0E, 0x36, 0xE6, 0x25, 0x0C, 0x3E, 0x24, 0x18, 0x3D, 0x1C, 0x23,
    # Source 3
    0x1B, 0x07, 0x09, 0x06, 0x2C, 0x0A, 0x19, 0x05, 0x22, 0x17, 0x3C, 0x21, 0x15, 0x08, 0x3B, 0x20,
    # Source 4
    0x61, 0x56, 0x60, 0x00, 0x55, 0x00, 0x5F, 0x54, 0x59, 0x5C, 0x5A, 0x58, 0x5D, 0x57, 0x5E, 0x5B,
    # Source 5
    0x47, 0x4A, 0x46, 0x45, 0x49, 0x4C, 0x4D, 0x4E, 0x53, 0x00, 0x4B, 0x00, 0x48,
    # Source 6
    0x39, 0xE1, 0xE0, 0x04, 0x16, 0x1D, 0xE3, 0xE2, 0x3A, 0x1F, 0x1A, 0x1E, 0x14, 0x2B, 0x29, 0x35
]

def get_idx(name): return KEY_NAMES.index(name)

# -1: 0.5u gap, -2: 1u standard, -3: empty spot
visual_layout = [
    # Row 1
    [get_idx("Escape"), -2, get_idx("F1"), get_idx("F2"), get_idx("F3"), get_idx("F4"), -1, get_idx("F5"), get_idx("F6"), get_idx("F7"), get_idx("F8"), -1, get_idx("F9"), get_idx("F10"), get_idx("F11"), get_idx("F12"), -1, get_idx("Print Screen"), get_idx("Scroll Lock"), get_idx("Pause"), -1, get_idx("User Key 1"), get_idx("User Key 2"), get_idx("User Key 3"), get_idx("User Key 4")],
    # Row 2
    [get_idx("`"), get_idx("1"), get_idx("2"), get_idx("3"), get_idx("4"), get_idx("5"), get_idx("6"), get_idx("7"), get_idx("8"), get_idx("9"), get_idx("0"), get_idx("-"), get_idx("="), get_idx("Backspace"), -1, get_idx("Insert"), get_idx("Home"), get_idx("Page Up"), -1, get_idx("Num Lock"), get_idx("Numpad /"), get_idx("Numpad *"), get_idx("Numpad -")],
    # Row 3
    [get_idx("Tab"), get_idx("Q"), get_idx("W"), get_idx("E"), get_idx("R"), get_idx("T"), get_idx("Y"), get_idx("U"), get_idx("I"), get_idx("O"), get_idx("P"), get_idx("["), get_idx("]"), get_idx("\\"), -1, get_idx("Delete"), get_idx("End"), get_idx("Page Down"), -1, get_idx("Numpad 7"), get_idx("Numpad 8"), get_idx("Numpad 9"), get_idx("Numpad +")],
    # Row 4
    [get_idx("Caps Lock"), get_idx("A"), get_idx("S"), get_idx("D"), get_idx("F"), get_idx("G"), get_idx("H"), get_idx("J"), get_idx("K"), get_idx("L"), get_idx(";"), get_idx("'"), get_idx("Enter"), -3, get_idx("Numpad 4"), get_idx("Numpad 5"), get_idx("Numpad 6")],
    # Row 5
    [get_idx("Left Shift"), get_idx("Z"), get_idx("X"), get_idx("C"), get_idx("V"), get_idx("B"), get_idx("N"), get_idx("M"), get_idx(","), get_idx("."), get_idx("/"), get_idx("Right Shift"), -1, -2, get_idx("↑"), -2, -1, get_idx("Numpad 1"), get_idx("Numpad 2"), get_idx("Numpad 3"), get_idx("Numpad Enter")],
    # Row 6
    [get_idx("Left Ctrl"), get_idx("Left GUI"), get_idx("Left Alt"), get_idx("Space"), get_idx("Right Alt"), get_idx("Right GUI"), get_idx("Menu"), get_idx("Right Ctrl"), -1,  get_idx("←"), get_idx("↓"), get_idx("→"), -1, get_idx("Numpad 0"), get_idx("Numpad .")]
]

key_classes = {
    "Backspace": "key-200", "Tab": "key-150", "\\": "key-150", 
    "Caps Lock": "key-175", "Enter": "key-225", 
    "Left Shift": "key-225", "Right Shift": "key-275", 
    "Left Ctrl": "key-125", "Left GUI": "key-125", "Left Alt": "key-125",
    "Right Alt": "key-125", "Right GUI": "key-125", "Menu": "key-125", "Right Ctrl": "key-125",
    "Space": "key-space", "Numpad 0": "key-200",
    "Numpad +": "key-h200", "Numpad Enter": "key-h200"
}

def generate_html_grid():
    html = '<div class="keyboard-grid">\n'
    for r_idx, row in enumerate(visual_layout):
        html += f'  <div class="kb-row">\n'
        for key_idx in row:
            if key_idx == -1: html += '    <div class="kb-spacer half"></div>\n'
            elif key_idx == -2: html += '    <div class="kb-spacer std"></div>\n'
            elif key_idx == -3: html += '    <div class="kb-spacer nav"></div>\n'
            else:
                name = KEY_NAMES[key_idx]
                cls = ("kb-key " + key_classes.get(name, "")).strip()
                disp = name
                if disp.startswith("Numpad "): disp = disp[7:]
                if disp in ["Left Shift", "Right Shift"]: disp = "Shift"
                if disp in ["Left Ctrl", "Right Ctrl"]: disp = "Ctrl"
                if disp in ["Left Alt", "Right Alt"]: disp = "Alt"
                if disp in ["Left GUI", "Right GUI"]: disp = "Win"
                if disp == "Caps Lock": disp = "Caps"
                if disp == "Scroll Lock": disp = "ScrLk"
                if disp == "Print Screen": disp = "PrtSc"
                if disp == "Num Lock": disp = "Num"
                if disp == "Page Up": disp = "PgUp"
                if disp == "Page Down": disp = "PgDn"
                if disp == "Backspace": disp = "BS"
                if disp == "Escape": disp = "Esc"
                if disp == "Enter": disp = "Enter"
                if disp == "Delete": disp = "Del"
                if disp == "Insert": disp = "Ins"
                if 'User' in disp: disp = disp.replace('User Key ', 'U')

                html += f'    <div class="{cls}" data-key="{key_idx}" id="kb-key-{key_idx}">{disp}</div>\n'
        html += f'  </div>\n'
    html += '</div>\n'
    return html

css = """
        /* ===== Tab 0: Key Config ===== */
        .key-layout { display: flex; gap: 24px; flex-direction: column; }
        .keyboard-grid {
            display: flex; flex-direction: column; gap: 4px;
            background: #111; padding: 20px; border-radius: 12px;
            overflow-x: auto; zoom: 0.8; width: max-content; margin: 0 auto;
        }
        .kb-row { display: flex; gap: 4px; height: 40px; }
        .kb-key {
            background: var(--surface); border: 1px solid var(--border);
            border-radius: 6px; color: var(--text); font-size: 0.75rem;
            font-weight: 500; display: flex; align-items: center; justify-content: center;
            cursor: pointer; user-select: none; transition: all 0.15s;
            width: 40px; height: 40px; box-sizing: border-box;
        }
        .kb-key:hover { background: var(--surface-hover); border-color: var(--accent); }
        .kb-key.selected { background: rgba(108, 92, 231, 0.2); border-color: var(--accent); box-shadow: 0 0 8px var(--accent-glow); }
        .kb-key.modified { border-color: var(--warning); }
        .key-125 { width: 51px; }
        .key-150 { width: 62px; }
        .key-175 { width: 73px; }
        .key-200 { width: 84px; }
        .key-225 { width: 95px; }
        .key-275 { width: 117px; }
        .key-space { width: 271px; }
        .key-h200 { height: 84px; z-index: 10; display:flex; align-items:flex-end; padding-bottom:10px; }
        .kb-spacer.std { width: 40px; }
        .kb-spacer.half { width: 20px; }
        .kb-spacer.nav { width: 168px; }
"""

with open("index.html", "r", encoding="utf-8") as f:
    text = f.read()

# 1. replace SVG with grid HTML
svg_start = text.find('<svg class="numpad-svg"')
svg_end = text.find('</svg>', svg_start) + 6
text = text[:svg_start] + generate_html_grid() + text[svg_end:]

# 2. replace CSS
css_start = text.find('/* ===== Tab 0: Key Config ===== */')
css_end = text.find('.detail-panel {', css_start)
text = text[:css_start] + css + "\n        " + text[css_end:]

# 3. JS logical replacments
text = text.replace('.key-rect', '.kb-key')
old_update_svg = "const txt = document.querySelector(`text.key-label[data-key=\"${idx}\"]`);\\n            if (txt) txt.textContent = keycodeToLabel(kcValues[idx]);"
new_update_svg = "const rect = document.querySelector(`.kb-key[data-key=\"${idx}\"]`);\\n            if (rect) rect.textContent = keycodeToLabel(kcValues[idx]);"
text = text.replace(old_update_svg.replace("\\n", "\n"), new_update_svg.replace("\\n", "\n"))

# 4. JSON replacments
old_keys = text[text.find("const KEY_NAMES"):text.find("];", text.find("const KEY_NAMES"))+2]
new_keys = f"const KEY_NAMES = {json.dumps(KEY_NAMES, ensure_ascii=False)};"
text = text.replace(old_keys, new_keys)

old_defaults = text[text.find("const DEFAULT_KEYCODES"):text.find("];", text.find("const DEFAULT_KEYCODES"))+2]
new_defaults = f"const DEFAULT_KEYCODES = {json.dumps(DEFAULT_CODES)};"
text = text.replace(old_defaults, new_defaults)

text = text.replace(
    "const DISPLAY_ORDER = [16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 0, 1];",
    "const DISPLAY_ORDER = Array.from({length: 108}, (_, i) => i);"
)
text = text.replace("max-width: 900px;", "max-width: 1100px;")

# 5. Modifier codes
mod_codes = """
            // 修飾キー (0xE0-0xE7) とユーザキー (0x00)
            { code: 0xE0, name: 'Left Ctrl' }, { code: 0xE1, name: 'Left Shift' }, { code: 0xE2, name: 'Left Alt' }, { code: 0xE3, name: 'Left GUI (Win)' },
            { code: 0xE4, name: 'Right Ctrl' }, { code: 0xE5, name: 'Right Shift' }, { code: 0xE6, name: 'Right Alt' }, { code: 0xE7, name: 'Right GUI (Win)' },
            { code: 0x00, name: 'User Key' },
"""
if "{ code: 0xE0," not in text:
    text = text.replace("// アルファベット", mod_codes + "            // アルファベット")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(text)

print("index.html fully rebuilt.")
