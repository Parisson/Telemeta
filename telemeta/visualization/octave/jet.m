function J = jet(m)
%JET    Variant of HSV
%   JET(M), a variant of HSV(M), is an M-by-3 matrix containing
%   the default colormap used by CONTOUR, SURF and PCOLOR.
%   The colors begin with dark blue, range through shades of
%   blue, cyan, green, yellow and red, and end with dark red.
%   JET, by itself, is the same length as the current figure's
%   colormap. If no figure exists, MATLAB creates one.
%
%   See also HSV, HOT, PINK, FLAG, COLORMAP, RGBPLOT.

%   Copyright 1984-2004 The MathWorks, Inc.
%   $Revision: 5.7.4.2 $  $Date: 2005/06/21 19:31:40 $

if nargin < 1
   m = size(get(gcf,'colormap'),1);
end
n = ceil(m/4);
u = [(1:1:n)/n ones(1,n-1) (n:-1:1)/n]';
g = ceil(n/2) - (mod(m,4)==1) + (1:length(u))';
r = g + n;
b = g - n;
g(g>m) = [];
r(r>m) = [];
b(b<1) = [];
J = zeros(m,3);
J(r,1) = u(1:length(r));
J(g,2) = u(1:length(g));
J(b,3) = u(end-length(b)+1:end);