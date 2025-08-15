# 16-bit Arithmetic Logic Unit (ALU)

## Overview
This project implements a 16-bit ALU with comprehensive testing. The ALU supports 6 operations and includes overflow detection for arithmetic operations.

## Module: alu_16bit

### Port Description
- **Inputs:**
  - `a[15:0]`: First operand (16-bit)
  - `b[15:0]`: Second operand (16-bit)
  - `alu_control[3:0]`: Operation control signal
- **Outputs:**
  - `result[15:0]`: ALU operation result (16-bit)
  - `zero`: High when result equals zero
  - `overflow`: High when arithmetic overflow occurs

### Control Encoding
| Control[3:0] | Operation | Description |
|--------------|-----------|-------------|
| 0000         | ADD       | Signed addition (a + b) |
| 0001         | SUB       | Signed subtraction (a - b) |
| 0010         | AND       | Bitwise AND (a & b) |
| 0011         | OR        | Bitwise OR (a \| b) |
| 0100         | XOR       | Bitwise XOR (a ^ b) |
| 0101         | SLT       | Set Less Than (signed comparison) |

### Features
1. **Combinational Logic**: All operations are purely combinational
2. **Overflow Detection**: Detects signed overflow for ADD and SUB operations
3. **Zero Flag**: Indicates when the result is zero
4. **Signed Operations**: ADD, SUB, and SLT handle signed 16-bit values

### Overflow Detection Logic
- **ADD**: Overflow occurs when both operands have the same sign but the result has a different sign
- **SUB**: Overflow occurs when operands have different signs and the result sign differs from the first operand

## Testbench: alu_16bit_tb

### Test Coverage
The testbench includes 14 comprehensive test cases covering:

1. **Positive Cases**: Normal arithmetic operations
2. **Zero Results**: Operations that produce zero output
3. **Boundary Cases**: Maximum positive/negative values
4. **Overflow Cases**: Arithmetic operations that cause overflow
5. **Logic Operations**: AND, OR, XOR with various bit patterns
6. **Signed Comparisons**: SLT with positive and negative values

### Test Cases Summary
| Test # | Operation | Description | Expected Behavior |
|--------|-----------|-------------|-------------------|
| 1      | ADD       | Positive numbers | Normal addition |
| 2      | ADD       | Zero result | Zero flag set |
| 3      | ADD       | Overflow case | Overflow flag set |
| 4      | SUB       | Positive result | Normal subtraction |
| 5      | SUB       | Zero result | Zero flag set |
| 6      | SUB       | Overflow case | Overflow flag set |
| 7      | AND       | Bit masking | Logical AND |
| 8      | OR        | Bit combination | Logical OR |
| 9      | XOR       | Same values | Zero result |
| 10     | XOR       | Different values | Bit inversion |
| 11     | SLT       | A < B (signed) | Result = 1 |
| 12     | SLT       | A >= B (signed) | Result = 0, Zero = 1 |
| 13     | ADD       | Max positive + 0 | Boundary test |
| 14     | ADD       | Max negative + 0 | Boundary test |

## Usage

### Compilation and Simulation
```bash
# Compile the design and testbench
iverilog -o alu_16bit_tb alu_16bit.v alu_16bit_tb.v

# Run the simulation
vvp alu_16bit_tb
```

### Expected Output
The testbench will display:
- Individual test results (PASS/FAIL)
- Test summary with total count
- Final status (ALL TESTS PASSED or SOME TESTS FAILED)

## Design Considerations

### Verilog Coding Standards
- Uses combinational always block with `@(*)`
- Proper signal naming conventions
- Clear port declarations
- Appropriate use of signed arithmetic for SLT operation
- No latches or unintended sequential logic

### Performance
- Single-cycle combinational operation
- No clock dependency
- Minimal propagation delay through case statement

### Extensibility
The design can be easily extended to support additional operations by:
1. Adding new control encodings
2. Implementing new case branches
3. Updating the testbench accordingly

## Files
- `alu_16bit.v`: Main ALU module implementation
- `alu_16bit_tb.v`: Comprehensive self-checking testbench
- `README_ALU.md`: This documentation file