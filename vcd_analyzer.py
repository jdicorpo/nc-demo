#!/usr/bin/env python3
"""
Simple VCD file analyzer to show signal transitions
"""

def parse_vcd(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    # Parse variable definitions
    variables = {}
    in_definitions = False
    
    for line in lines:
        line = line.strip()
        if line == '$enddefinitions $end':
            in_definitions = False
            break
        elif line.startswith('$var'):
            parts = line.split()
            if len(parts) >= 5:
                var_type = parts[1]
                width = parts[2]
                symbol = parts[3]
                name = parts[4]
                variables[symbol] = {'name': name, 'width': width, 'type': var_type}
    
    # Parse value changes
    changes = []
    current_time = 0
    
    for line in lines:
        line = line.strip()
        if line.startswith('#'):
            current_time = int(line[1:])
        elif line.startswith('b') and ' ' in line:
            # Binary value change
            parts = line.split(' ', 1)
            value = parts[0][1:]  # Remove 'b' prefix
            symbol = parts[1]
            if symbol in variables:
                changes.append((current_time, variables[symbol]['name'], value, 'binary'))
        elif len(line) == 2 and line[0] in '01xz':
            # Single bit value change
            value = line[0]
            symbol = line[1]
            if symbol in variables:
                changes.append((current_time, variables[symbol]['name'], value, 'bit'))
    
    return variables, changes

def print_signal_transitions(filename):
    print(f"VCD File Analysis: {filename}")
    print("=" * 60)
    
    variables, changes = parse_vcd(filename)
    
    print("\nSignal Definitions:")
    print("-" * 40)
    for symbol, info in variables.items():
        print(f"  {info['name']:<20} [{info['width']}] -> {symbol}")
    
    print(f"\nSignal Transitions:")
    print("-" * 40)
    print(f"{'Time':<8} {'Signal':<20} {'Value':<20} {'Type'}")
    print("-" * 60)
    
    for time, name, value, val_type in changes[:50]:  # Show first 50 changes
        if val_type == 'binary':
            # Convert binary to hex for readability
            try:
                hex_val = hex(int(value, 2))[2:].upper().zfill(4)
                display_val = f"{value} (0x{hex_val})"
            except:
                display_val = value
        else:
            display_val = value
        
        print(f"{time:<8} {name:<20} {display_val:<20} {val_type}")
    
    if len(changes) > 50:
        print(f"... and {len(changes) - 50} more transitions")

if __name__ == "__main__":
    print_signal_transitions("alu_16bit_tb.vcd")