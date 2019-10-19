`include "alu.v"

module alu_tb;

	reg [3:0] in1;
	reg [3:0] in0;
	reg cin;
	reg [2:0] instr;
	reg clk;
	reg rstn;

	wire [3:0] out;
	wire cout;

	alu a0(out, cout, in1, in0, cin, instr, clk, rstn);

	initial begin
		$monitor($time, " instr=%b, in1=%d, in0=%d, cin=%b, rstn=%b, clk=%b, out=%d cout=%b", instr, in1, in0, cin, rstn, clk, out, cout);
		$dumpfile("alu_tb.dmp");
		$dumpvars(0, alu_tb);
		#0 rstn = 1'b0; clk = 1'b0;
		#5 rstn = 1'b1; instr = 3'b001; in1=1; in0=2; cin=1'b0;
		#20 rstn = 1'b1; instr = 3'b010; in1=10; in0=4; cin=1'b1;
		#20 rstn = 1'b1; instr = 3'b101; in1=11; in0=11; cin=1'b0;
		#20 rstn = 1'b1; instr = 3'b111; in1=00; in0=11; cin=1'b0;
		#20 rstn = 1'b1; instr = 3'b000; in1=11; in0=11; cin=1'b0;
		#40 $finish; 
	end

	always
		#5 clk = ~clk;

endmodule
