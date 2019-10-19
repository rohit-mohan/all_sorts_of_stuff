`include "instr_decoder.v"

module instr_decoder_tb;

	wire [3:0] reg_addr;
	wire [3:0] reg_operand;
	wire [2:0] reg_opsel;
	wire carryin;
	wire rwn; 
	wire csn;

	reg [2:0] opcode;
	reg [3:0] mem_addr;
	reg [3:0] imm_val;
	reg clk;
	reg rstn;

	instr_decoder id0(reg_addr, reg_operand, reg_opsel, carryin, rwn, csn, opcode, mem_addr, imm_val, clk, rstn);

	initial begin
		$monitor($time, " rstn=%b, clk=%b, opcode=%b, mem_addr=%d, imm_val=%d, reg_addr=%d, reg_operand=%d, reg_opsel=%d, carryin=%d, rwn=%b, csn=%b", rstn, clk, opcode, mem_addr, imm_val, reg_addr, reg_operand, reg_opsel, carryin, rwn, csn);
		$dumpfile("instr_decoder_tb.dmp");
		$dumpvars(0, instr_decoder_tb);

		#0 rstn=0; clk=0;
		#3 rstn=1; opcode=1; mem_addr=3; imm_val=2; 
		#10 rstn=1; opcode=3; mem_addr=3; imm_val=2; 
		#10 rstn=1; opcode=2; mem_addr=3; imm_val=2;   
		#20 $finish;
	end

	always
		#5 clk = ~clk;

endmodule
