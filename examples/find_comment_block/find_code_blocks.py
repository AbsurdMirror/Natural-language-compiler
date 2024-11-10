import sys

def find_and_print_code_blocks(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    code_blocks = []
    current_block = []
    in_block = False

    for i, line in enumerate(lines):
        stripped_line = line.lstrip()
        if stripped_line.startswith('//='):
            if in_block:
                # Close the current block if we're already in one
                code_blocks.append((current_block[0][0], current_block))
            # Start a new block
            current_block = [(i, stripped_line)]
            in_block = True
        elif in_block and stripped_line.startswith('//'):
            # Add to the current block if it's still open and the line is a comment
            current_block.append((i, stripped_line))
        elif in_block and not stripped_line.startswith('//='):
            # End the current block if we encounter a non-comment line
            code_blocks.append((current_block[0][0], current_block))
            current_block = []
            in_block = False

    # Add the last block if it exists
    if in_block:
        code_blocks.append((current_block[0][0], current_block))

    # Print the found code blocks with their line numbers
    for start_line, block in code_blocks:
        print(f'Code block starting at line {start_line + 1}:')
        for line_num, line in block:
            print(f'{line_num + 1}: {line}')
        print()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python find_code_blocks.py <filename>')
        sys.exit(1)
    
    filename = sys.argv[1]
    find_and_print_code_blocks(filename)
