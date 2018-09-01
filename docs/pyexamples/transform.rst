<p>from colorspace.colorlib import HCL</p><br>
<comment>Let's specify a set of HCL colors.</comment><br>
<comment>These three colors are a bright blue (260, 100, 50),</comment><br>
<comment>a neutral light gray (310, 0, 90) and a bright red (360, 100, 50)</comment><br>
<comment>from the "Red-Blue 2" diverging color palette.</comment><br>
<p>c = HCL(H = [260, 310, 360], C = [100, 0, 100], L = [50, 90, 50])</p><br>
<comment>Show current values, as "c" is a HCL object the method</comment><br>
<comment>prints the H, C, L color coordinates.</comment><br>
<p>c.show()</p><br>
<comment>Following the image above we would like to do the following:</comment><br>
<comment>(1) convert HCL to CIEXYZ,</comment><br>
<comment>(2) convert CIEXYZ to sRGB,</comment><br>
<comment>(3) convert sRGB to hex colors,</comment><br>
<comment>(4) convert hex colors to RGB,</comment><br>
<comment>(5) convert RGB to polarLAB,</comment><br>
<comment>(6) and finally back to HCL.</comment><br>
<p>c.to("CIEXYZ");    c.show()  # (1)<br>
c.to("sRGB");      c.show()  # (2)<br>
c.to("hex");       c.show()  # (3)<br>
c.to("RGB");       c.show()  # (4)<br>
c.to("polarLAB");  c.show()  # (5)<br>
c.to("HCL");       c.show()  # (6)</p><br>