# A quick script to convert a spec file written 
# in plain english, into a list of tokens that can
# So that I do not have to do this manually each time

import re
import os

# Specify the input file
input_file = 'specs/en-toks.txt'

if not os.path.exists('generated'):
    os.makedirs('generated')
output_file = 'generated/tokens.txt'

SYMBOL_MAP = {
    '{': 'LBRACE',
    '}': 'RBRACE',
    '(': 'LPAREN',
    ')': 'RPAREN',
    '[': 'LBRACKET',
    ']': 'RBRACKET',
    ';': 'SEMICOLON',
    '->': 'ARROW',
    ',': 'COMMA',
    '...': 'ELLIPSIS',
    ':': 'COLON',
    '+=': 'PLUS_ASSIGN',
    '-=': 'MINUS_ASSIGN',
    '*=': 'STAR_ASSIGN',
    '/=': 'SLASH_ASSIGN',
    '+': 'PLUS',
    '-': 'MINUS',
    '*': 'STAR',
    '/': 'SLASH',
    '%': 'MOD',
    "'": 'TRANSPOSE',
    '.+': 'DOT_PLUS',
    '.-': 'DOT_MINUS',
    '.*': 'DOT_STAR',
    './': 'DOT_SLASH',
    '==': 'EQ_EQ',
    '!=': 'NOT_EQ',
    '<=': 'LESS_EQ',
    '>=': 'GREATER_EQ',
    '<': 'LESS',
    '>': 'GREATER',
    '=': 'ASSIGN',
}

tokens = []
category_stack = []

with open(input_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

    for line in lines:
        raw_line = line.rstrip()
        if not raw_line.strip():
            continue

        indent_level = (len(raw_line) - len(raw_line.lstrip())) // 2
        content = raw_line.strip()

        category_stack = category_stack[:indent_level]

        if content.startswith('-'):
            item_raw = content.lstrip('-').strip()

            # Extract annotations/comments in parenthetical notes if present (e.g. "... (ellipses)")
            token_val = item_raw
            if '(' in item_raw and not item_raw.startswith('('):
                token_val = item_raw.split('(')[0].strip()

            if token_val in SYMBOL_MAP:
                clean_name = SYMBOL_MAP[token_val]
            else:
                word_str = token_val
                # Replace multi-character symbols first to avoid mis-matches
                for sym in sorted(SYMBOL_MAP.keys(), key=len, reverse=True):
                    word_str = word_str.replace(sym, SYMBOL_MAP[sym])

                # Match any remaining non-alphanumeric characters and
                # replace them with underscores: spaces, punctuation, etc.
                # Also, convert to uppercase for consistency.
                # Then do a final cleanup to remove any leading/trailing 
                # underscores and collapse multiple underscores into one.
                clean_name = re.sub(r'[^a-zA-Z0-9_]', '', word_str.replace(' ', '_')).upper()
                clean_name = re.sub(r'_+', '_', clean_name).strip('_')

            if category_stack:
                # Prepend the category stack to the token name, 
                # separated by underscores
                prefix = "_".join([re.sub(r'[^a-zA-Z0-9_]', '', c.replace(' ', '_')).upper() for c in category_stack])
                tokens.append(f"{prefix}_{clean_name}")
            else:
                tokens.append(clean_name)
        else:
            cat_name = content.rstrip(':')
            category_stack.append(cat_name)



with open(output_file, 'w') as f:
    for token in tokens:
        f.write(f"{token}\n")
