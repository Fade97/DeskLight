// Animations.h

#ifndef _ANIMATIONS_h
#define _ANIMATIONS_h

#if defined(ARDUINO) && ARDUINO >= 100
#include "arduino.h"
#else
#include "WProgram.h"
#endif

class CRGB;
class Animations
{
public:
	Animations( int iLedCount, CRGB* leds )
		: m_iLedCount( iLedCount ), m_leds( leds )
	{}
	void setLeds( int iCount, CRGB* leds );
	void fade(int r=255, int g=64, int b=0);
	void wave( int iStart, int r=255, int g=64, int b=0 );

private:
	int m_iLedCount;
	CRGB *m_leds;
	unsigned long m_ulLast = 0;

	int m_iRound = 0;
};

#endif

