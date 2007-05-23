/*
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
 *
*/

/*  Created by Bram de Jong <bram.dejong@gmail.com> for MTG http://www.mtg.upf.edu/
 *  
 *  You will need anyoption ( http://www.hackorama.com/anyoption/ ) and libsndfile
 *  ( http://www.mega-nerd.com/libsndfile/ ) and GD2 (http://www.boutell.com/gd/)
 *  to build this program.
*/

#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdio.h>
#include <cctype>
#include <string>
#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>

#include "sndfile.h"

#ifdef WIN32
#include "gdwin32/gd.h"
#else
#include "gd.h"
#endif

#include "anyoption.h"

typedef std::vector<long> ColorVector;

long hex2dec(char h)
{
	switch(h)
	{
	case 'a': return 10;
	case 'b': return 11;
	case 'c': return 12;
	case 'd': return 13;
	case 'e': return 14;
	case 'f': return 15;
	default:
		{
			char tmp = h - '0';
			if(tmp >= 0 && tmp <= 9)
				return tmp;
			else
				return 0;
		}
	}
}

// string as a HEX HTML value 000000 (black) FF0000 (red) etc...
long string2color(std::string s, gdImagePtr image)
{
	long r,g,b;
	if(s.length() == 6)
	{
    std::transform(s.begin(), s.end(), s.begin(), (int (*)(int)) tolower);
		r = (hex2dec(s.at(0))<<4) + hex2dec(s.at(1));
		g = (hex2dec(s.at(2))<<4) + hex2dec(s.at(3));
		b = (hex2dec(s.at(4))<<4) + hex2dec(s.at(5));
	}
	else
	{
		r = g = b = 0;
	}

	return gdImageColorAllocate(image, r, g, b);
}

void HSVtoRGB( float &r, float &g, float &b, float h, float s, float v )
{
	int i;
	float f, p, q, t;

	if( s == 0 ) {
		// achromatic (grey)
		r = g = b = v;
		return;
	}

	h /= 60;			// sector 0 to 5
	i = (int)floor( h );
	f = h - i;			// factorial part of h
	p = v * ( 1 - s );
	q = v * ( 1 - s * f );
	t = v * ( 1 - s * ( 1 - f ) );

	switch( i ) {
		case 0:
			r = v;
			g = t;
			b = p;
			break;
		case 1:
			r = q;
			g = v;
			b = p;
			break;
		case 2:
			r = p;
			g = v;
			b = t;
			break;
		case 3:
			r = p;
			g = q;
			b = v;
			break;
		case 4:
			r = t;
			g = p;
			b = v;
			break;
		default:		// case 5:
			r = v;
			g = p;
			b = q;
			break;
	}

}

/* The hue value H runs from 0 to 360º. The saturation S is the degree of strength
or purity and is from 0 to 1. Purity is how much white is added to the color, so S=1
makes the purest color (no white). Brightness V also ranges from 0 to 1, where 0 is the black.*/
// x in [0..1]
long float2color(float value, gdImagePtr image)
{
	if(value > 1.f) value = 1.f;
	else if(value < 0.f) value = 0.f;
	
	float h;
	float s;
	float v;

	h = (1.f-value)*360.0;
	s = 0.8f;
	v = 1.f;

	float r,g,b;

	HSVtoRGB(r,g,b,h,s,v);

	return gdImageColorAllocate(image, (int)(r*255), (int)(g*255), (int)(b*255));
}


void getPeakSamplesInBlock(float *samples, long count, long channels,  float &first, float &second, bool verbose)
{
	if (verbose)
		std::cout << "\tprocessing " << count << " samples, " << channels << " channels" << std::endl;
	
	if(count < 1)
	{
		first = second = 0.f;
		if (verbose)
			std::cout << "\texiting as there's no samples" << std::endl;
		return;
	}
	else if(count < 2)
	{
		first = second = samples[0];
		if (verbose)
			std::cout << "\texiting as there's less than two samples" << std::endl;
		return;
		return;
	}
	
	float tlow  = samples[0];
	float thigh = samples[0];
	long high_i = 0;
	long low_i = 0;
	
	for(long i=channels;i<count;i+=channels)
	{
		float val = samples[i];
		
		if(val > thigh)
		{
			thigh = val;
			high_i = i;
		}
		
		if(val < tlow)
		{
			tlow = val;
			low_i = i;
		}
	}
	
	if (high_i > low_i)
	{
		first  = tlow;
		second = thigh;
	}
	else
	{        
		first  = thigh;
		second = tlow;
	}

	if (verbose)
		std::cout << "\tprocessing: done" << std::endl;
}

bool getPositionAndValue(std::string line, long &position, float &value, long positionIncrement = 0)
{
	long pos;
	float val;
	int good;

	good = sscanf(line.c_str(),"%ld,%f",&pos,&val);
	
	if(good == 2 && pos >= 0)
	{
		position = pos;
		value = val;
		return true;
	}

	good = sscanf(line.c_str(),"%f",&val);

	if(good == 1 && good != EOF)
	{
		position += positionIncrement;
		value = val;
		return true;
	}

	return false;
}

bool getPositionAndColor(std::string line, long &position, long &color, gdImagePtr image, long positionIncrement = 0)
{
	long pos;
	char colorString[6];
	int good;

	good = sscanf(line.c_str(),"%ld,#%6s",&pos,colorString);
	
	if(good == 2 && pos >= 0)
	{
		position = pos;
		color = string2color(colorString,image);
		return true;
	}

	good = sscanf(line.c_str(),"#%6s",colorString);

	if(good == 1)
	{
		position += positionIncrement;
		color = string2color(colorString,image);
		return true;
	}

	return false;
}

ColorVector getColorValues(std::string filename, float samplesPerPixel, long width, gdImagePtr image)
{
	ColorVector colors;

	char buffer[256];
	std::string line;
	std::ifstream infile;
	infile.open(filename.c_str(), std::ifstream::in);
	
	float value = 0.f;
	long color = 0;
	long position = 0;
	bool inputGood = true;
	bool colorFileUsesColors = false;
	long stepsize = 0;
	std::vector<float> values;

	if(infile.good())
	{
		infile.getline(buffer,256);
		line = buffer;
		
		int success = sscanf(line.c_str(),"[%ld]",&stepsize);
		if(success == 1)
		{
			if(infile.good())
			{
				infile.getline(buffer,256);
				line = buffer;
			}
			else
			{
				return colors;
			}
		}
		else
		{
			stepsize = 0;
		}
		
		long hasHasChar = std::string(line).find("#");
		
		if(hasHasChar > 0)
		{
			colorFileUsesColors = true;
		}
	}
	else
	{
		return colors;
	}
		
	if(colorFileUsesColors)
		inputGood = getPositionAndColor(line,position,color,image,stepsize);
	else
		inputGood = getPositionAndValue(line,position,value,stepsize);

	float nextValue = value;
	long nextColor = color;
	
	for(long i=0;i<width;i++)
	{
		long sampleLocation = (long)ceilf((double)i * (double)samplesPerPixel);

		while(sampleLocation >= position && inputGood)
		{
			color = nextColor;
			value = nextValue;

			if(infile.good())
			{
				infile.getline(buffer,256);
				line = buffer;
					
				if(colorFileUsesColors)
				{
					inputGood = getPositionAndColor(line,position,nextColor,image,stepsize);
				}
				else
				{
					inputGood = getPositionAndValue(line,position,nextValue,stepsize);
				}
			}
			else
			{
				inputGood = false;
			}
		}
		
		if(colorFileUsesColors)
			colors.push_back(color);
		else
			values.push_back(value);
		
	}

	infile.close();

	if(colorFileUsesColors)
		return colors;

	if(values.size())
	{
		int type = 1;

		switch(type)
		{
			case 0:
				{
					for(unsigned long k=0;k<values.size();k++)
					{
						if(values[k] < 0.f)
							values[k] = 0.f;

						float scaledValue = sqrt(values[k]) / sqrt((double)11025);
						
						colors.push_back(float2color(scaledValue,image));
					}
					
					break;
				}
			case 1:
				{
					for(unsigned long k=0;k<values.size();k++)
					{
						if(values[k] < 0.f)
							values[k] = 0.f;

						float scaledValue = log(values[k]+1) / log((double)(512+1));
						
						colors.push_back(float2color(scaledValue,image));
					}
					
					break;
				}
			case 2:
			default:
				{
					float maxValue = values[0];
					float minValue = values[0];

					for(unsigned long j=1;j<values.size();j++)
					{
						if(values[j] > maxValue)
							maxValue = values[j];

						if(values[j] < minValue)
							minValue = values[j];
					}

					if(minValue != maxValue)
					{
						for(unsigned long k=0;k<values.size();k++)
						{
							colors.push_back(float2color((values[k] - minValue) / (maxValue - minValue),image));
						}
					}
					else
					{
						for(unsigned long k=0;k<colors.size();k++)
						{
							colors.push_back(float2color(1.0,image));
						}
					}
					
					break;
				}
		}
	}

	return colors;
}

inline long round(float x)
{
	return (long)floorf(x + 0.5f);
}

// this is pretty ugly and should be removed :-)
float oldX, oldY;

void moveTo(float x, float y)
{
	oldX = x;
	oldY = y;
}

void lineTo(gdImagePtr image, float x, float y, long color, long padding, long width, long height, bool verbose)
{
	long x1 = (long)round(oldX)+padding;
	long y1 = (long)round(oldY)+padding;
	long x2 = (long)round(x)+padding;
	long y2 = (long)round(y)+padding;

	// GD seems to segfault when we try to draw anti-aliased lines to the teges :-(
	y1 = std::max((long)0,std::min(height-2, y1));
	y2 = std::max((long)0,std::min(height-2, y2));
	
	if (verbose)
		std::cout << "\tdrawing line: (" << x1 << "," << y1 << ") -> (" << x2 << "," << y2 << "), color = " << std::hex << color << " image : " << image << std::dec << std::endl;
	
	gdImageLine(image,x1,y1,x2,y2,color);
	oldX = x;
	oldY = y;

	if (verbose)
		std::cout << "\tdrawing line: done" << std::endl;
}

int main(int argc, char* argv[])
{
	AnyOption *opt = new AnyOption();

	opt->setOption("input",'i');
	opt->setOption("width",'w');
	opt->setOption("height",'h');
	opt->setOption("output",'o');
	opt->setOption("colorfile",'c');
	opt->setOption("linecolor",'l');
	opt->setOption("backgroundcolor",'b');
	opt->setOption("zerocolor",'z');
	opt->setOption("padding",'p');
	opt->setOption("verbose",'v');
	
	opt->setOption("type",'t');
	opt->setOption("quality",'q');
	
	opt->addUsage( "Usage: wav2png --input wavefile.wav" );
	opt->addUsage( "\t" );
	opt->addUsage( "\tAdditional options: --width 300 --height 151 --output image.jpg --linecolor ff00aa --backgroundcolor 002222 --zerocolor ff0000 --colorfile filename --padding 2 --verbose true --type jpeg --quality 85" );
	opt->addUsage( "\tShort command line switches: -i -w -h -o -l -b -z -c -o");
	opt->addUsage( "\t" );
	opt->addUsage( "\twidth: width of PNG (default: 300)");
	opt->addUsage( "\theight: height of PNG (default: 151)");
	opt->addUsage( "\toutput: output filename (default: input filename with '.png' appended)");
	opt->addUsage( "\tlinecolor: color of waveform lines (default: 323232)");
	opt->addUsage( "\tbackgroundcolor: color of background (default: FFFFFF)");
	opt->addUsage( "\tzerocolor: color of line through zero (default: 960000)");
	opt->addUsage( "\t\tcolors are defined like HTML colors in hex");
	opt->addUsage( "\tcolorfile: file with (samplePosition,value) pairs for coloring");
	opt->addUsage( "\tpadding: padding around the edge");
	opt->addUsage( "\tverbose: true or false");
	opt->addUsage( "\ttype: png or jpeg");
	opt->addUsage( "\tquality: jpeg quality between 0 and 100");
	
	opt->processCommandArgs( argc, argv );

	std::string inputFilename;
	std::string outputFilename;

	bool verbose = false;
	if( opt->getValue("verbose") != NULL && strcmp(opt->getValue("verbose"), "true") == 0)
		verbose = true;
	
	if (verbose)
		std::cout << "verbose true" << std::endl;
	
	if (verbose) std::cout << "parsing options" << std::endl;

	long quality = -1;
	if ( opt->getValue("quality") != NULL )
		quality = atoi(opt->getValue("quality"));

	if (verbose)
		std::cout << "quality " << quality << std::endl;
	
	bool isPng = true;
	if ( opt->getValue("type") != NULL && strcmp(opt->getValue("type"), "jpeg") == 0)
		isPng = false;
	
	if (verbose)
		std::cout << "isPng " << (isPng?"true":"false") << std::endl;
	
	if( opt->getValue("input") != NULL )
	{
		inputFilename = opt->getValue("input");
	}
	else
	{
		opt->printUsage();
		return 1;
	}

	if (verbose)
		std::cout << "input filename " << inputFilename << std::endl;

	if( opt->getValue("output") != NULL )
	{
		outputFilename = opt->getValue("output");
	}
	else
	{
		outputFilename = inputFilename + std::string(".png");
	}

	if (verbose)
		std::cout << "output filename " << outputFilename << std::endl;
	
	long width = 354;
	if( opt->getValue("width") != NULL )
	{
		width = atoi(opt->getValue("width"));

		if(width <= 0)
			return 1;
	}


	if (verbose)
		std::cout << "width " << width << std::endl;

	long height = 165;
	if( opt->getValue("height") != NULL )
	{
		height = atoi(opt->getValue("height"));

		if(height <= 0)
			return 1;
	}

	if (verbose)
		std::cout << "height " << height << std::endl;
	
	long padding = 2;
	if( opt->getValue("padding") != NULL )
	{
		padding = atoi(opt->getValue("padding"));

		if(padding<0)
			return 1;
	}

	if (verbose)
		std::cout << "padding " << padding << std::endl;
	
	std::string colorFilename("");
	if( opt->getValue("colorfile") != NULL )
	{
		colorFilename = std::string(opt->getValue("colorfile"));
	}

	if (verbose)
		std::cout << "color filename " << colorFilename << std::endl;
	
	if (verbose) std::cout << "opening wave file" << std::endl;

	SNDFILE *infile;
	SF_INFO sfinfo ;
	
	// open the soundfile
	if(!(infile = sf_open (inputFilename.c_str(), SFM_READ, &sfinfo)))
	{
		return  1;
	};

	if(sfinfo.frames == 0 || sfinfo.channels == 0)
	{
		sf_close(infile);
		return 1;
	}

	float samplesPerPixel = (float) sfinfo.frames / (float) width;
	long maxReadSize = (long)ceilf(samplesPerPixel);
	
	if (verbose) std::cout << "samps/pixel "<< samplesPerPixel << std::endl;

	if (verbose) std::cout << "allocating image..." << std::endl;
	gdImagePtr image = gdImageCreateTrueColor(width+padding*2, height+padding*2);
	if (verbose) std::cout << "done..." << std::endl;
	
	ColorVector colors;
	if(colorFilename != "")
	{
		if (verbose) std::cout << "getting color values" << std::endl;
		colors = getColorValues(colorFilename,samplesPerPixel,width,image);
	}

	
	long backgroundColor;
	long lineColor;
	long zeroColor;
		
	if (verbose) std::cout << "parsing more options" << std::endl;

	if( opt->getValue("linecolor") != NULL )
		lineColor = string2color(opt->getValue("linecolor"),image);
	else
		lineColor = string2color("FFFFFF",image);

	if (verbose)
		std::cout << "line color " << std::hex << lineColor << std::dec << std::endl;
	
	if( opt->getValue("backgroundcolor") != NULL )
		backgroundColor = string2color(opt->getValue("backgroundcolor"),image);
	else
		backgroundColor = string2color("000000",image);
	
	if (verbose)
		std::cout << "background color " << std::hex << backgroundColor << std::dec << std::endl;
	
	if( opt->getValue("zerocolor") != NULL )
		zeroColor = string2color(opt->getValue("zerocolor"),image);
	else
		zeroColor = string2color("960000",image);

	if (verbose)
		std::cout << "zero color " << std::hex << zeroColor << std::dec << std::endl;
	
	gdImageFilledRectangle(image,0,0,width+padding*2-1,height+padding*2-1, backgroundColor);
	gdImageSetAntiAliased(image,lineColor);
	moveTo(0,height*0.5f);

	
	// sampling data
	long dataSize = sfinfo.channels * maxReadSize;
	if (verbose) std::cout << "allocating " << dataSize << " bytes" << std::endl;
	float *data = new float[dataSize];
	if (verbose) std::cout << "allocated..." << std::endl;
		
	float first = 0, second = 0;
		
	// we need at least width samples to do something usefull...
	for(long i=0;i<width;i++)
	{
		if (verbose && !(i % std::max(width/20,(long)1)))
			std::cout << "looping over sound " << i+1 << " of " << width << std::endl;
			
		if (colors.size() && (unsigned) i < colors.size())
		{
			if (verbose)
				std::cout << "\tsetting antialiased line color..." << std::endl;
			gdImageSetAntiAliased(image,colors[i]);
		}

		float start = i * samplesPerPixel;
		float end = (i + 1) * samplesPerPixel;

		long blockSize = (long) floorf(end + 0.5f) - (long) floorf(start + 0.5f);

		if(blockSize > maxReadSize)
		{
			blockSize = maxReadSize;
		}
		else if(blockSize < 1)
		{
			lineTo(image, (float)i, height * 0.5f * (1.f - first), gdAntiAliased, padding, width, height, verbose);
			lineTo(image, (float)i, height * 0.5f * (1.f - second), gdAntiAliased, padding, width, height, verbose);
			continue;
		}
		
		if (verbose && !(i % std::max(width/20,(long)1)))
			std::cout << "\treading wave file" << std::endl;

		long readcount = sf_readf_float(infile, data, blockSize);

		if(readcount == 0)
		{
			if (verbose)
				std::cout << "\tthis is probably a broken wave file... It reported more samples than it has!" << std::endl;
			break;
		}
		if(readcount < blockSize)
		{
			if (verbose)
				std::cout << "\twe just read a non-complete block..." << std::endl;
		}
		
		if (verbose && !(i % std::max(width/20,(long)1)))
			std::cout << "\tread OK" << std::endl;

		if (verbose && !(i % std::max(width/20,(long)1)))
			std::cout << "\tgetting sample peaks" << std::endl;

		getPeakSamplesInBlock(data, readcount, sfinfo.channels, first, second, verbose);

		if (verbose && !(i % std::max(width/20,(long)1)))
			std::cout << "\tpeak OK" << std::endl;

		if(first != second)
		{
			lineTo(image, (float)i, height * 0.5f * (1.f - first), gdAntiAliased, padding, width, height, verbose);
			lineTo(image, (float)i, height * 0.5f * (1.f - second), gdAntiAliased, padding, width, height, verbose);
		}
		else
		{
			lineTo(image, (float)i, height * 0.5f * (1.f - first), gdAntiAliased, padding, width, height, verbose);
		}
	}
	
	if (verbose)
		std::cout << "closing sound file" << std::endl;

	sf_close (infile) ;

	if (verbose)
		std::cout << "closed" << std::endl;

	
	if (verbose)
		std::cout << "generating GD image" << std::endl;

	if (verbose)
		std::cout << "\topening output file" << std::endl;

	FILE *outputFile = fopen(outputFilename.c_str(),"wb");

	if (verbose)
		std::cout << "\tgdImageCreate" << std::endl;

	if (isPng)
		gdImagePng(image,outputFile);
	else
		gdImageJpeg(image,outputFile,quality);

	if (verbose)
		std::cout << "\tclose output file" << std::endl;

	fclose(outputFile);

	if (verbose)
		std::cout << "\tgdImageDestroy" << std::endl;

	gdImageDestroy(image);

	if (verbose)
		std::cout << "deleting data" << std::endl;

	delete data;
	
	if (verbose)
		std::cout << "all fine and dandy, exiting" << std::endl;

	return 0;
}
