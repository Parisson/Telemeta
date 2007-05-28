# -*- coding: utf-8 -*-
#
# Copyright (C) 2007 Parisson SARL
# Copyright (c) 2006-2007 Guillaume Pellerin <pellerin@parisson.com>
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution. The terms
# are also available at http://svn.parisson.org/telemeta/TelemetaLicense.
#
# Author: Guillaume Pellerin <pellerin@parisson.com>
#
# SpectrogramVisualizer2.m
#
# Depends: octave2.9, octave2.9-forge, spectrogram.m, xloadimage, imagemagick

clear all;
close all;

dest_image = $IMGFILE;
wav_file = $WAVFILE;
octave_path = $OCTAVEPATH;

cd(octave_path);
ncmap = 128; % number of points for colormap
step = 6;   % spectral slice period (ms)
% step_length = fix(5*Fs/1000);
window = 30;   % filter window (ms)
% window = fix(40*Fs/1000);
time_limit = 30; % length limit of the displayed sample (s)

[x, Fs] = wavread(wav_file);
x = x(:,1);  % mono
lx = length(x);

% LIMITING time
lx_lim = Fs.*time_limit;
if lx > lx_lim;
 x = x(1:lx_lim);
end
    
%fftn = 2^nextpow2(window); % next highest power of 2
[S, f, t] = spectrogram(x, Fs, window, step, 4000, 'hanning', -30);
S = flipud(20*log10(S));
%  
%  cmap = [0:1:ncmap-1];
%  map_cos = cos(cmap*3.141/(2*ncmap));
%  map_lin = cmap./ncmap;
%  map_one = ones(1,ncmap);
%
%  cmap = [ [map_cos]' [map_cos]' [fliplr(map_cos)]' ];
%  colormap(jet(ncmap));
cmap = colormap(jet(ncmap));

img = imagesc(t, f, S);
saveimage(dest_image, img, 'ppm', cmap);

quit;

