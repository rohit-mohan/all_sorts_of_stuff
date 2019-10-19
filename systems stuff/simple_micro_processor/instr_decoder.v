module instr_decoder(
	output reg [3:0] reg_addr,
	output reg [3:0] reg_operand,
	output reg [2:0] reg_opsel,
	output reg carryin,
	output reg rwn, 
	output reg csn,

	input [2:0] opcode,
	input [3:0] mem_addr,
	input [3:0] imm_val,
	input clk,
	input rstn	
);

	// state encoding	
	parameter init = 2'b00;
	parameter fetch = 2'b01;
	parameter exec = 2'b10;
	parameter load = 2'b11;	 

	// operations
	parameter op_sto = 3'b000;
	parameter op_add = 3'b001;
	parameter op_sub = 3'b010;
	parameter op_and = 3'b110;
	parameter op_xor = 3'b101;
	parameter op_or = 3'b100;
	parameter op_not = 3'b111;

	// opcode
	parameter sto = 3'b000;
	parameter add = 3'b001; 
	parameter sub = 3'b010; 
	parameter oc_and = 3'b011;
	parameter oc_or = 3'b100; 
	parameter oc_xor = 3'b101; 
	parameter oc_not = 3'b110; 
	parameter sto1 = 3'b111;	


	reg [1:0] state;
	reg [2:0] opsel;
	reg cin;

	// state transition
	always@(posedge clk or negedge rstn) begin
		if (!rstn)
			state <= init;
					
		else begin
			case(state) 
				init : state <= fetch;
				fetch : state <= exec;
				exec : state <= load;
				load : state <= fetch;
			endcase
		end
	end	

	// control line assignment 
	always@(state) begin
		case(state) 
			init : begin reg_addr <= 4'b0; reg_operand <= 4'b0; reg_opsel <= 3'b0; carryin <= 3'b0; rwn <= 1'b1; csn <= 1'b1; end
			fetch : begin reg_addr <= mem_addr; reg_operand <= imm_val; reg_opsel <= opsel; carryin <= cin; rwn <= 1'b1; csn <= 1'b0; end
			exec : begin reg_addr <= mem_addr; reg_operand <= imm_val; reg_opsel <= opsel; carryin <= cin; rwn <= 1'b1; csn <= 1'b0; end
			load : begin reg_addr <= mem_addr; reg_operand <= imm_val; reg_opsel <= opsel; carryin <= cin; rwn <= 1'b0; csn <= 1'b0; end
		endcase
	end

	always@(opcode) begin
		case(opcode)
			sto : begin opsel <= op_sto; cin <= 1'b0; end
			add : begin opsel <= op_add; cin <= 1'b0; end
			sub : begin opsel <= op_sub; cin <= 1'b1; end
			oc_and : begin opsel <= op_and; cin <= 1'b0; end
			oc_or : begin opsel <= op_or; cin <= 1'b0; end
			oc_xor : begin opsel <= op_xor; cin <= 1'b0; end
			oc_not : begin opsel <= op_not; cin <= 1'b0; end
			sto1 : begin opsel <= op_sto; cin <= 1'b0; end
		endcase 
	end

endmodule


