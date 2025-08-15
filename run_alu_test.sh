#!/bin/bash

# 16-bit ALU Test Runner Script
# This script compiles and runs the ALU testbench

echo "========================================="
echo "16-bit ALU Test Runner"
echo "========================================="

# Check if required files exist
if [ ! -f "alu_16bit.v" ]; then
    echo "ERROR: alu_16bit.v not found!"
    exit 1
fi

if [ ! -f "alu_16bit_tb.v" ]; then
    echo "ERROR: alu_16bit_tb.v not found!"
    exit 1
fi

echo "Compiling ALU design and testbench..."

# Compile the design
if iverilog -o alu_16bit_tb alu_16bit.v alu_16bit_tb.v; then
    echo "Compilation successful!"
    echo ""
    echo "Running testbench..."
    echo "========================================="
    
    # Run the simulation
    vvp alu_16bit_tb
    
    echo "========================================="
    echo "Test completed!"
    
    # Clean up
    rm -f alu_16bit_tb
    echo "Cleaned up temporary files."
else
    echo "ERROR: Compilation failed!"
    exit 1
fi