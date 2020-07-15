// RawRGB.h

#ifndef _RawRGB_h
#define _RawRGB_h

#if defined(ARDUINO) && ARDUINO >= 100
	#include "arduino.h"
#else
	#include "WProgram.h"
#endif

class CRGB;
class RawRGB
{
public:
	int r = 0;
	int g = 0;
	int b = 0;
	int a = 255;

	RawRGB( int iR = 0, int iG = 0, int iB = 0, int iA = 255 ) 
		: r( iR ), g( iG ), b( iB ), a(iA)
	{

	}
/*
	RawRGB& operator=( CRGB rhs );
	RawRGB& operator+=( const RawRGB& rhs );
	RawRGB& operator-=( const RawRGB& rhs );*/
};
/*
inline RawRGB operator+( RawRGB lhs, const RawRGB& rhs );
inline RawRGB operator-( RawRGB lhs, const RawRGB& rhs );*/
#endif

