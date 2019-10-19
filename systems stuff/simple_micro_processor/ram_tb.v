`include "ram.v"
module ram_tb;

	wire [3:0] dout;
	
	reg [3:0] addr;
	reg [3:0] din;
	reg rwn;
	reg csn;

	ram r0(dout, addr, din, rwn, csn);

	initial begin
		$monitor($time, " addr=%d, rwn=%b, csn=%b, din=%d, dout=%d", addr, rwn, csn, din, dout);
		$dumpfile("ram_tb.dmp");
		$dumpvars(0, ram_tb);

		#0 addr=0; rwn=1; csn=1; din=0;
		#5 addr=0; rwn=0; csn=0; din=1;
		#5 addr=1; rwn=0; csn=0; din=2;
		#5 addr=2; rwn=0; csn=0; din=3;
		#5 addr=3; rwn=0; csn=0; din=4;		

		#5 addr=3; rwn=1; csn=0; din=0;
		#5 addr=2; rwn=1; csn=0; din=0;
		#5 addr=1; rwn=1; csn=0; din=0;
		#5 addr=0; rwn=1; csn=0; din=0; 
	
		#5 $finish;
	end


endmodule	
