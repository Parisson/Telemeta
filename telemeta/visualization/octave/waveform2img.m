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
# Depends: octave2.9, spectrogram.m, xloadimage, imagemagick

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
time_limit = 300; % length limit of the displayed sample (s)
% Downsampling factor
D = 100;

% Read audio data
[x, Fs] = wavread(wav_file);
x = x(:,1);  % mono
lx = length(x);

% LIMITING time
lx_lim = Fs.*time_limit;
if lx > lx_lim;
 x = x(1:lx_lim);
end
N = length(x);

% Downsampling by D
t = 1:1:lx;
t = (t-1)./Fs;
x2(1:ceil(N/D)) = x(1:D:N);
t2(1:ceil(N/D)) = t(1:D:N);
%x(ceil(N/D)+1:N) = zeros(1,N-ceil(N/D));

img = plot(t2,x2);
print(dest_image, '-dpng');

quit;

