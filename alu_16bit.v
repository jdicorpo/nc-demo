module alu_16bit (
    input  [15:0] a,
    input  [15:0] b,
    input  [3:0]  alu_control,
    output [15:0] result,
    output        zero,
    output        overflow
);

    reg [15:0] alu_result;
    reg        alu_overflow;

    always @(*) begin
        alu_overflow = 1'b0;
        case (alu_control)
            4'b0000: begin // ADD
                {alu_overflow, alu_result} = {1'b0, a} + {1'b0, b};
                alu_overflow = (a[15] == b[15]) && (alu_result[15] != a[15]);
            end
            4'b0001: begin // SUB
                {alu_overflow, alu_result} = {1'b0, a} - {1'b0, b};
                alu_overflow = (a[15] != b[15]) && (alu_result[15] != a[15]);
            end
            4'b0010: begin // AND
                alu_result = a & b;
            end
            4'b0011: begin // OR
                alu_result = a | b;
            end
            4'b0100: begin // XOR
                alu_result = a ^ b;
            end
            4'b0101: begin // SLT (Set Less Than)
                alu_result = ($signed(a) < $signed(b)) ? 16'h0001 : 16'h0000;
            end
            default: begin
                alu_result = 16'h0000;
            end
        endcase
    end

    assign result = alu_result;
    assign zero = (alu_result == 16'h0000);
    assign overflow = alu_overflow;

endmodule