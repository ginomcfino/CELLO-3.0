module Main (input in76, a0, output out81, out84);

	wire \$n10_0;
	wire \$n9_0;
	wire \$n8_0;
	wire \$n7_0;
	wire \$n6_0;
	wire \$n6_1;
	wire \$n5_0;
	wire \$n5_1;

	nor (\$n7_0, in76, a0);
	nor (\$n8_0, \$n6_1, \$n5_0);
	nor (out81, \$n8_0, \$n7_0);
	not (\$n6_0, in76);
	not (\$n6_1, in76);
	not (\$n5_0, a0);
	not (\$n5_1, a0);
	nor (\$n9_0, in76, \$n5_1);
	nor (\$n10_0, \$n6_0, a0);
	nor (out84, \$n10_0, \$n9_0);

endmodule
