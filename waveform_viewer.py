#!/usr/bin/env python3
"""
Create an HTML waveform viewer for the ALU testbench VCD file
"""

def parse_vcd_detailed(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    # Parse variable definitions
    variables = {}
    
    for line in lines:
        line = line.strip()
        if line == '$enddefinitions $end':
            break
        elif line.startswith('$var'):
            parts = line.split()
            if len(parts) >= 5:
                symbol = parts[3]
                name = parts[4]
                width = int(parts[2])
                variables[symbol] = {'name': name, 'width': width}
    
    # Parse value changes and organize by signal
    signals = {}
    current_time = 0
    
    # Initialize signals
    for symbol, info in variables.items():
        signals[info['name']] = [(0, 'x')]
    
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
                name = variables[symbol]['name']
                if name in ['a', 'b', 'result', 'alu_control']:  # Focus on key signals
                    try:
                        hex_val = hex(int(value, 2))[2:].upper()
                        signals[name].append((current_time, hex_val))
                    except:
                        signals[name].append((current_time, value))
        elif len(line) == 2 and line[0] in '01xz':
            # Single bit value change
            value = line[0]
            symbol = line[1]
            if symbol in variables:
                name = variables[symbol]['name']
                if name in ['zero', 'overflow']:  # Focus on key signals
                    signals[name].append((current_time, value))
    
    return signals

def create_html_waveform(signals, output_file):
    html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>ALU 16-bit Testbench Waveforms</title>
    <style>
        body { font-family: monospace; margin: 20px; }
        .waveform { margin: 10px 0; }
        .signal-name { display: inline-block; width: 150px; font-weight: bold; }
        .timeline { display: inline-block; }
        .time-marker { display: inline-block; width: 60px; text-align: center; border-left: 1px solid #ccc; }
        .value { display: inline-block; width: 60px; text-align: center; background: #f0f0f0; }
        .value.changed { background: #ffff99; }
        h1 { color: #333; }
        h2 { color: #666; margin-top: 30px; }
        .test-case { margin: 20px 0; padding: 10px; border: 1px solid #ddd; }
    </style>
</head>
<body>
    <h1>ALU 16-bit Testbench Waveforms</h1>
    
    <h2>Signal Values Over Time</h2>
    <div style="font-size: 12px; margin-bottom: 20px;">
        Time units: simulation time steps (each test case runs for 10 time units)
    </div>
"""
    
    # Create time markers
    max_time = 150  # Based on our testbench
    time_markers = list(range(0, max_time + 1, 10))
    
    html_content += '<div class="timeline">'
    html_content += '<span class="signal-name">Time:</span>'
    for t in time_markers:
        html_content += f'<span class="time-marker">{t}</span>'
    html_content += '</div><br/>\n'
    
    # Key signals to display
    key_signals = ['a', 'b', 'alu_control', 'result', 'zero', 'overflow']
    
    for signal_name in key_signals:
        if signal_name in signals:
            html_content += f'<div class="waveform">'
            html_content += f'<span class="signal-name">{signal_name}:</span>'
            
            signal_data = signals[signal_name]
            current_value = 'x'
            
            for t in time_markers:
                # Find the value at time t
                for time_val, value in signal_data:
                    if time_val <= t:
                        current_value = value
                    else:
                        break
                
                # Check if value changed at this time
                changed = any(time_val == t for time_val, _ in signal_data)
                css_class = "value changed" if changed else "value"
                
                html_content += f'<span class="{css_class}">{current_value}</span>'
            
            html_content += '</div>\n'
    
    # Add test case descriptions
    html_content += """
    <h2>Test Case Descriptions</h2>
    <div class="test-case">
        <strong>Time 10-20:</strong> ADD positive numbers (0x1234 + 0x5678 = 0x68AC)
    </div>
    <div class="test-case">
        <strong>Time 20-30:</strong> ADD zero result (0x0000 + 0x0000 = 0x0000, Zero=1)
    </div>
    <div class="test-case">
        <strong>Time 30-40:</strong> ADD overflow (0x7FFF + 0x0001 = 0x8000, Overflow=1)
    </div>
    <div class="test-case">
        <strong>Time 40-50:</strong> SUB positive result (0x5678 - 0x1234 = 0x4444)
    </div>
    <div class="test-case">
        <strong>Time 50-60:</strong> SUB zero result (0xABCD - 0xABCD = 0x0000, Zero=1)
    </div>
    <div class="test-case">
        <strong>Time 60-70:</strong> SUB overflow (0x8000 - 0x0001 = 0x7FFF, Overflow=1)
    </div>
    <div class="test-case">
        <strong>Time 70-80:</strong> AND operation (0xFFFF & 0x5555 = 0x5555)
    </div>
    <div class="test-case">
        <strong>Time 80-90:</strong> OR operation (0x5555 | 0xAAAA = 0xFFFF)
    </div>
    <div class="test-case">
        <strong>Time 90-100:</strong> XOR zero result (0x1234 ^ 0x1234 = 0x0000, Zero=1)
    </div>
    <div class="test-case">
        <strong>Time 100-110:</strong> XOR different values (0xFFFF ^ 0x5555 = 0xAAAA)
    </div>
    <div class="test-case">
        <strong>Time 110-120:</strong> SLT A < B signed (-1 < 1, Result=0x0001)
    </div>
    <div class="test-case">
        <strong>Time 120-130:</strong> SLT A >= B signed (2 >= 1, Result=0x0000, Zero=1)
    </div>
    <div class="test-case">
        <strong>Time 130-140:</strong> ADD max positive + zero (0x7FFF + 0x0000 = 0x7FFF)
    </div>
    <div class="test-case">
        <strong>Time 140-150:</strong> ADD max negative + zero (0x8000 + 0x0000 = 0x8000)
    </div>
    
    <h2>Control Signal Encoding</h2>
    <ul>
        <li><strong>0x0:</strong> ADD (Addition)</li>
        <li><strong>0x1:</strong> SUB (Subtraction)</li>
        <li><strong>0x2:</strong> AND (Bitwise AND)</li>
        <li><strong>0x3:</strong> OR (Bitwise OR)</li>
        <li><strong>0x4:</strong> XOR (Bitwise XOR)</li>
        <li><strong>0x5:</strong> SLT (Set Less Than, signed)</li>
    </ul>
    
</body>
</html>
"""
    
    with open(output_file, 'w') as f:
        f.write(html_content)

if __name__ == "__main__":
    signals = parse_vcd_detailed("alu_16bit_tb.vcd")
    create_html_waveform(signals, "alu_waveforms.html")
    print("HTML waveform viewer created: alu_waveforms.html")