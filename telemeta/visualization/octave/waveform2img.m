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
lim_x_length = 10; % (s)

[x, Fs] = wavread(wav_file);
x = x(:,1);  % mono
lx = length(x);
lim_x_samples = Fs.*lim_x_length;

if lx > lim_x_samples;
 x = x(1:lim_x_samples)
end

t = [1:1:lx]./Fs;

img = plot(t,x);
print(dest_image, '-dpng')

quit
