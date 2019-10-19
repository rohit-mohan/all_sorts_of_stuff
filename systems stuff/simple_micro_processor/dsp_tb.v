`include "dsp.v"

module dsp_tb;

	wire [3:0] dsp_out;
	
	reg [2:0] opcode; 
	reg [3:0] mem_addr;
	reg [3:0] imm_val;
	reg clk;
	reg rstn;

	parameter sto = 3'b000;
	parameter add = 3'b001; 
	parameter sub = 3'b010; 
	parameter oc_and = 3'b011;
	parameter oc_or = 3'b100; 
	parameter oc_xor = 3'b101; 
	parameter oc_not = 3'b110; 
	parameter sto1 = 3'b111;


	dsp d0(dsp_out, opcode, mem_addr,  imm_val, clk, rstn);

	initial begin
		$monitor($time, " rstn=%b, clk=%b, opcode=%d, mem_addr=%d, imm_val=%d, dsp_out=%d", rstn, clk, opcode, mem_addr, imm_val, dsp_out);
		$dumpfile("dsp_tb.dmp");
		$dumpvars(0, dsp_tb);

		#0 rstn=0; clk=0;
		#5 rstn=1; opcode=sto; mem_addr=0; imm_val=4; 
		#30 opcode=add; mem_addr=0; imm_val=6;
		#30 opcode=sto; mem_addr=1; imm_val=7;
		#30 opcode=sub; mem_addr=1; imm_val=5;
		#40 $finish; 
	end

	always
		#5 clk=~clk;

endmodule



