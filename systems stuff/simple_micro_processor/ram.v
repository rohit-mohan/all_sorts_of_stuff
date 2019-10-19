module ram (
	output [3:0] dout,
	
	input [3:0] addr,
	input [3:0] din,
	input rwn,
	input csn
);


	reg [3:0] mem [15:0];
	
	assign dout = (~csn && rwn) ? mem[addr] : 4'bz; 
	
	always@(rwn or csn or din)
		if (~rwn && ~csn)
			mem[addr] <= din;
		else
			mem[addr] <= mem[addr];

endmodule
