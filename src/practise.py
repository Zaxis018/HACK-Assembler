import re

# Utility functions

def decimal_to_binary(decimal):
    decimal = int(decimal)
    return format(decimal, '015b')

def is_numeric(s):
    return s.isnumeric()

def extract_C_instruction(instruction):
    # Define a regex pattern to capture the different parts of the instruction
    pattern = re.compile(r'(?:(?P<before_equal>[^=;]+)=)?(?P<after_equal>[^=;]+)(?:;(?P<after_semicolon>[^=;]+))?')
    
    match = pattern.match(instruction)
    if match:
        before_equal = match.group('before_equal')
        after_equal = match.group('after_equal')
        after_semicolon = match.group('after_semicolon')
        
        return before_equal, after_equal, after_semicolon
    else:
        return None, None, None


# Dictionary for C INSTRUCTION
comp = {
    "0":   "0101010",
    "1":   "0111111",
    "-1":  "0111010",
    "D":   "0001100",
    "A":   "0110000",
    "M":   "1110000",
    "!D":  "0001101",
    "!A":  "0110001",
    "!M":  "1110001",
    "-D":  "0001111",
    "-A":  "0110011",
    "-M":  "1110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "M+1": "1110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "M-1": "1110010",
    "D+A": "0000010",
    "D+M": "1000010",
    "D-A": "0010011",
    "D-M": "1010011",
    "A-D": "0000111",
    "M-D": "1000111",
    "D&A": "0000000",
    "D&M": "1000000",
    "D|A": "0010101",
    "D|M": "1010101"
}

dest = {
    None:  "000",  # No destination
    "M":   "001",
    "D":   "010",
    "MD":  "011",
    "A":   "100",
    "AM":  "101",
    "AD":  "110",
    "AMD": "111"
}

jump = {
    None:  "000",  # No jump
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

#Initialize the symbol table
symbol_table = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "R0": 0,
    "R1": 1,
    "R2": 2,
    "R3": 3,
    "R4": 4,
    "R5": 5,
    "R6": 6,
    "R7": 7,
    "R8": 8,
    "R9": 9,
    "R10": 10,
    "R11": 11,
    "R12": 12,
    "R13": 13,
    "R14": 14,
    "R15": 15,
    "SCREEN": 16384,
    "KBD": 24576
}

next_free_location = 16

###########################################################################################
###########################################################################################



def read_asm_file(filename):
    cleaned = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()  # This removes leading/trailing whitespace (including newlines)
            if line and not line.startswith('//'):  # This checks if line is not empty and does not start with '//'
                line = line.split('//')[0]  # Remove inline comments
                line = line.replace(' ', '')
                cleaned.append(line)
    return cleaned

file_path = "./Hack-Assembler/test_files/Rect.asm"
cleaned_data = read_asm_file(file_path)
print("cleaned_data: ", cleaned_data)


# FIRST PASS
count = 0
for instruction in cleaned_data:
    if instruction.startswith('('):
        label = instruction[1:-1]  # Extract the symbol value inside ( )
        symbol_table[label] = count
    else:
        count += 1

machine_code = []

for instruction in cleaned_data:
    print("instruction: ", instruction)
    if instruction.startswith('@'):
        # A instruction 
        value = instruction[1:]
        if is_numeric(value):
            machine_code.append('0' + decimal_to_binary(value))
        else:  # value is symbolic
            try:
                value = symbol_table[value]
                machine_code.append('0'+decimal_to_binary(value))
            except KeyError:  # value not found
                symbol_table[value] = next_free_location
                machine_code.append('0'+decimal_to_binary(next_free_location))
                next_free_location +=1

    elif instruction.startswith('('):
        # Label (to be handled in the symbol table)
        pass
    else:
        # C instruction
        dest_field, comp_field, jump_field = extract_C_instruction(instruction)
        print("dest_field:", dest_field)
        print("comp_field:", comp_field)
        print("jump_field:", jump_field)
        c_instruction = '111' + comp[comp_field] + dest[dest_field] + jump[jump_field]
        machine_code.append(c_instruction)

print(machine_code)

output_file_path = "outputs/"
output_file_path = file_path.replace('.asm', '.hack')
with open(output_file_path, 'w') as file:
    for code in machine_code:
        file.write(code + '\n')

print(f"Machine code has been written to {output_file_path}")