import os
import json
import re

def parse_txt_file(filename):
    items = []
    with open(filename, encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) < 2:
                continue
            items.append({"id": parts[0], "desc": parts[1]})
    return items

def dict_to_js(obj, var_name):
    # Generate JavaScript variable assignment with proper formatting
    lines = [f'const {var_name} = {{']
    for k, v in obj.items():
        lines.append(f'  "{k}": [')
        for item in v:
            lines.append(f'    {{ id: "{item["id"]}", desc: "{item["desc"]}" }},')
        if v:
            lines[-1] = lines[-1][:-1]  # Remove trailing comma for last item
        lines.append('  ],')
    if obj:
        lines[-1] = lines[-1][:-1]  # Remove trailing comma for last key
    lines.append('};')
    return '\n'.join(lines)

def main():
    # Step 1: Parse all .txt files in current directory
    result = {}
    for fname in os.listdir('.'):
        if fname.lower().endswith('.txt'):
            key = os.path.splitext(fname)[0]
            result[key.upper()] = parse_txt_file(fname)

    # Step 2: Format as JS code
    js_var_name = 'productsPorCirugia'
    js_code = dict_to_js(result, js_var_name)

    # Step 3: Find and replace between markers in ../index.html
    html_file = '../index.html'
    START = "// --- PASTE YOUR PRODUCT JSONS BELOW ---"
    END = "// --- END OF PRODUCT JSONS ---"

    with open(html_file, encoding='utf-8') as f:
        html = f.read()

    pattern = re.compile(f'({re.escape(START)})(.*)({re.escape(END)})', re.DOTALL)
    replacement = f"{START}\n{js_code}\n{END}"
    new_html, count = pattern.subn(replacement, html)
    if count == 0:
        print("Markers not found in index.html. Aborting update.")
    else:
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(new_html)
        print("index.html updated with new product JSONs.")

    # Step 4: Also save products.json for backup/reference
    with open('products.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print("Exported products.json (for backup/reference).")

if __name__ == "__main__":
    main()
