# -*- coding: utf-8 -*-
#
# Copyright (c) 2007-2009 Guillaume Pellerin <yomguy@parisson.com>

# This software is a computer program whose purpose is to backup, analyse,
# transcode and stream any audio content with its metadata over a web frontend.

# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".

# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.

# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.

# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.
#
# Author: Guillaume Pellerin <pellerin@parisson.com>
#
# SpectrogramVisualizer2.m
#
# Depends: octave2.9, octave2.9-forge

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

