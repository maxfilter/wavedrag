A = 100.0;F = 10.0;X = 20000.0;H = 400.0;
lc = 20.; // mesh spacing
lcBed = lc/4; // mesh spacing bed
nPointsBed = 20*F; // number of points used to resolve bed

// define glacier extent
Point(1) = {X, 0., 0., lc};
Point(2) = {X, H, 0., lc};
Point(3) = {0., H, 0., lc};
Point(4) = {0., 0., 0., lc};

Line(11) = {1, 2};
Line(12) = {2, 3};
Line(13) = {3, 4};

// build sinusoidal curve for bed
bedPoints[0] = 4;
For i In {1 : nPointsBed}
    xi = i/(nPointsBed + 1)*X;
    yi = -A*Sin(F*2*Pi/X*xi);
    bedPoints[i] = newp;
    Point(bedPoints[i]) = {xi, yi, 0., lcBed};
EndFor
bedPoints[nPointsBed + 1] = 1;
Spline(14) = bedPoints[];

// define meshing surface 
Curve Loop(21) = {11, 12, 13, 14};
Plane Surface(31) = {21};

// define physical boundaries and surfaces
Physical Line(41) = {11};
Physical Line(42) = {12};
Physical Line(43) = {13};
Physical Curve(44) = {14};
Physical Surface(51) = {31};
