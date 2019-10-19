`include "instr_decoder.v"
`include "alu.v"
`include "ram.v"

module dsp (
	output [3:0] dsp_out,
	
	input [2:0] opcode, 
	input [3:0] mem_addr,
	input [3:0] imm_val,
	input clk,
	input rstn
);
	
	// wires from instruction decoder
	wire [3:0] addr2mem;
	wire [3:0] val2alu;
	wire [2:0] opsel2alu;
	wire cin2alu, rwn2mem, csn2both;


	// wires from alu
	wire cout;

	// wires from memory
	wire [3:0] dataout;

	// instruciton decoder
	instr_decoder id0(addr2mem, val2alu, opsel2alu, cin2alu, rwn2mem, csn2mem, opcode, mem_addr, imm_val, clk, rstn);
	// arithmetic logical unit
	alu a0(dsp_out, cout, dataout, val2alu, cin2alu, opsel2alu, clk, rstn);
	// memory
	ram r0(dataout, addr2mem, dsp_out, rwn2mem, csn2mem);

endmodule


