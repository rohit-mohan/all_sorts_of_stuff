module alu(
	output reg [3:0] reg_out,
	output cout,	

	input [3:0] in1,
	input [3:0] in0,
	input cin,
	input [2:0] instr,
	input clk,
	input rstn	
);

	reg [3:0] reg_in1, reg_in0;
	reg [2:0] reg_instr;
	reg reg_cin;
	
	//input registering 

	always@(posedge clk or negedge rstn) begin
		if (!rstn) begin
			reg_in1 = 4'b0;
			reg_in0 = 4'b0;
			reg_instr = 4'b0;
			reg_cin = 1'b0;
		end

		else begin
			reg_in1 = in1;
			reg_in0 = in0;
			reg_instr = instr;
			reg_cin = cin;	
		end
	end

	// output registering
	
	wire [3:0] sub_ans = reg_in1 + ~(reg_in0) + reg_cin;
	wire [3:0] add_ans = reg_in1 + reg_in0 + reg_cin;
	wire [3:0] dec_ans = reg_in1 + ~({reg_cin, reg_cin, reg_cin, reg_cin});
	wire [3:0] or_ans  = reg_in1 | reg_in0;
	wire [3:0] xor_ans  = reg_in1 ^ reg_in0;
	wire [3:0] and_ans  = reg_in1 & reg_in0;
	wire [3:0] not_ans  = ~(reg_in1);
	

	always@(posedge clk or negedge rstn) begin
		if (!rstn) 
			reg_out <= 4'b0;
		else
			case(instr)
				3'b000, 3'b111 : reg_out <= reg_in0; 		
				3'b001 : reg_out <= add_ans;
				3'b010 : reg_out <= sub_ans;
				3'b011 : reg_out <= dec_ans;
				3'b100 : reg_out <= or_ans;				
				3'b101 : reg_out <= xor_ans;
				3'b110 : reg_out <= and_ans;
			endcase
	end

endmodule
