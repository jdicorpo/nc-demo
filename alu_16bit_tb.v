module alu_16bit_tb;

    reg  [15:0] a;
    reg  [15:0] b;
    reg  [3:0]  alu_control;
    wire [15:0] result;
    wire        zero;
    wire        overflow;

    integer test_count;
    integer pass_count;
    integer fail_count;

    alu_16bit dut (
        .a(a),
        .b(b),
        .alu_control(alu_control),
        .result(result),
        .zero(zero),
        .overflow(overflow)
    );

    task check_result;
        input [15:0] expected_result;
        input        expected_zero;
        input        expected_overflow;
        input [255:0] test_name;
        begin
            test_count = test_count + 1;
            if (result == expected_result && zero == expected_zero && overflow == expected_overflow) begin
                $display("PASS: %s - A=%h, B=%h, Control=%b, Result=%h, Zero=%b, Overflow=%b", 
                         test_name, a, b, alu_control, result, zero, overflow);
                pass_count = pass_count + 1;
            end else begin
                $display("FAIL: %s - A=%h, B=%h, Control=%b", test_name, a, b, alu_control);
                $display("      Expected: Result=%h, Zero=%b, Overflow=%b", expected_result, expected_zero, expected_overflow);
                $display("      Got:      Result=%h, Zero=%b, Overflow=%b", result, zero, overflow);
                fail_count = fail_count + 1;
            end
        end
    endtask

    initial begin
        $dumpfile("alu_16bit_tb.vcd");
        $dumpvars(0, alu_16bit_tb);
        
        $display("Starting ALU 16-bit Test");
        $display("========================");
        
        test_count = 0;
        pass_count = 0;
        fail_count = 0;

        #10;

        // Test Case 1: ADD - Positive numbers
        a = 16'h1234;
        b = 16'h5678;
        alu_control = 4'b0000;
        #10;
        check_result(16'h68AC, 1'b0, 1'b0, "ADD positive numbers");

        // Test Case 2: ADD - Zero result
        a = 16'h0000;
        b = 16'h0000;
        alu_control = 4'b0000;
        #10;
        check_result(16'h0000, 1'b1, 1'b0, "ADD zero result");

        // Test Case 3: ADD - Overflow (positive + positive = negative)
        a = 16'h7FFF;
        b = 16'h0001;
        alu_control = 4'b0000;
        #10;
        check_result(16'h8000, 1'b0, 1'b1, "ADD overflow positive");

        // Test Case 4: SUB - Positive result
        a = 16'h5678;
        b = 16'h1234;
        alu_control = 4'b0001;
        #10;
        check_result(16'h4444, 1'b0, 1'b0, "SUB positive result");

        // Test Case 5: SUB - Zero result
        a = 16'hABCD;
        b = 16'hABCD;
        alu_control = 4'b0001;
        #10;
        check_result(16'h0000, 1'b1, 1'b0, "SUB zero result");

        // Test Case 6: SUB - Overflow (negative - positive = positive)
        a = 16'h8000;
        b = 16'h0001;
        alu_control = 4'b0001;
        #10;
        check_result(16'h7FFF, 1'b0, 1'b1, "SUB overflow");

        // Test Case 7: AND - All bits set
        a = 16'hFFFF;
        b = 16'h5555;
        alu_control = 4'b0010;
        #10;
        check_result(16'h5555, 1'b0, 1'b0, "AND operation");

        // Test Case 8: OR - Mixed bits
        a = 16'h5555;
        b = 16'hAAAA;
        alu_control = 4'b0011;
        #10;
        check_result(16'hFFFF, 1'b0, 1'b0, "OR operation");

        // Test Case 9: XOR - Same values (zero result)
        a = 16'h1234;
        b = 16'h1234;
        alu_control = 4'b0100;
        #10;
        check_result(16'h0000, 1'b1, 1'b0, "XOR zero result");

        // Test Case 10: XOR - Different values
        a = 16'hFFFF;
        b = 16'h5555;
        alu_control = 4'b0100;
        #10;
        check_result(16'hAAAA, 1'b0, 1'b0, "XOR different values");

        // Test Case 11: SLT - A < B (signed)
        a = 16'hFFFF; // -1 in signed
        b = 16'h0001; // +1 in signed
        alu_control = 4'b0101;
        #10;
        check_result(16'h0001, 1'b0, 1'b0, "SLT A < B (signed)");

        // Test Case 12: SLT - A >= B (signed)
        a = 16'h0002; // +2 in signed
        b = 16'h0001; // +1 in signed
        alu_control = 4'b0101;
        #10;
        check_result(16'h0000, 1'b1, 1'b0, "SLT A >= B (signed)");

        // Test Case 13: Boundary case - Maximum positive
        a = 16'h7FFF;
        b = 16'h0000;
        alu_control = 4'b0000;
        #10;
        check_result(16'h7FFF, 1'b0, 1'b0, "ADD max positive + zero");

        // Test Case 14: Boundary case - Maximum negative
        a = 16'h8000;
        b = 16'h0000;
        alu_control = 4'b0000;
        #10;
        check_result(16'h8000, 1'b0, 1'b0, "ADD max negative + zero");

        #10;

        $display("\n========================");
        $display("Test Summary:");
        $display("Total Tests: %0d", test_count);
        $display("Passed:      %0d", pass_count);
        $display("Failed:      %0d", fail_count);
        
        if (fail_count == 0) begin
            $display("ALL TESTS PASSED!");
        end else begin
            $display("SOME TESTS FAILED!");
        end
        $display("========================");

        $finish;
    end

endmodule