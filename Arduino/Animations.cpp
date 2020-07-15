// 
// 
// 

#include "Animations.h"
#include "FastLED.h"
#define UPDATES_PER_SECOND 50

//void updateLEDs()
//{
//
//	bool bAnim = false;
//	unsigned long uLast;
//
//	int diff = millis() - uLast;
//	if ( millis() - uLast > 500 )
//	{
//		bAnim = false;
//		uLast = millis();
//	}
//	if ( bAnim )
//	{
//		diff = diff / 500 * 255;
//	}
//	if ( !bAnim )
//	{
//		diff = 255 - ( diff / 500 * 255 );
//	}
//
//
//	for ( int i = 0; i < NUM_LEDS; ++i )
//	{
//		leds[i] = CRGB( 128, 16, 0 );
//	}
//
//	for ( int i = 36; i < 78; ++i )
//	{
//		float j = 255 / 100.f;
//		if ( Leben <= 20 )
//		{
//			j = diff;
//		}
//		leds[i] = CRGB( 255 - int( j*Leben ), int( j*Leben ), 0 );
//	}
//
//	leds[36] = CRGB::Green;
//	leds[77] = CRGB::Green;
//
//	
//}

void Animations::setLeds( int iCount, CRGB* leds )
{
	m_iLedCount = iCount;
	m_leds = leds;
}

void Animations::fade(int r/*=255*/, int g/*=64*/, int b/*=0*/)
{

	if (millis() - m_ulLast >= 1000 / UPDATES_PER_SECOND )
	{
		for ( int i = 0; i < m_iLedCount; ++i )
		{
			float ir = inoise8( i*10, 10*m_iRound, i + 10 * m_iRound ) / 255.f;
			float iG = inoise8( i, m_iRound, i + 3 * m_iRound * 10 ) / 255.f;
			float iB = inoise8( i, m_iRound, i + 3 * m_iRound * 100 ) / 255.f;
			//Serial.println( 200 + int( ir * 55 ) );
			m_leds[i] = CRGB( int( ir * r ), int( ir * g ), int( ir * b ) );
		}
		m_ulLast = millis();
		m_iRound++;
	}
}

void Animations::wave( int iStart, int r, int g, int b )
{

	if ( millis() - m_ulLast >= 1000 / UPDATES_PER_SECOND )
	{
	
		float *fLedMult = new float[m_iLedCount];
		float fMult[] = { 0.1, 0.15, 0.2, 0.3, 0.4, 0.6, 0.8, 1., 1., 1., 0.8, 0.6, 0.4, 0.3, 0.2, 0.15, 0.1 };
		int iMultCnt = 17;
		int iR = iStart - m_iRound;
		int iL = iStart + m_iRound;
		for ( int i = 0; i < m_iLedCount; ++i )
		{
			m_leds[i] = CRGB::Black;
			fLedMult[i] = 0.;
		}
	
		for ( int i = 0; i < iMultCnt; ++i )
		{
			if ( iL - int( iMultCnt / 2 ) + i < m_iLedCount && iL - int( iMultCnt / 2) + i >= 0 )
			{
				fLedMult[iL - int( iMultCnt / 2 ) + i] += fMult[i];
			}
			if ( iR - int( iMultCnt / 2 ) + i >= 0 && iR - int( iMultCnt / 2 ) + i >= 0 )
			{
				fLedMult[iR - int( iMultCnt / 2 ) + i] = fMult[i];
			}
		}
	
		for ( int i = 0; i < m_iLedCount; ++i )
		{
			if ( fLedMult[i] > 1. )
				fLedMult[i] = 1.;
			//Serial.println( fLedMult[i] );
			m_leds[i] = CRGB( fLedMult[i] * r, fLedMult[i] * g, fLedMult[i] * b );
		}
		m_ulLast = millis();
		++m_iRound;
		//Serial.println( m_iLedCount );
		if ( m_iRound > m_iLedCount - iStart + iMultCnt )
			m_iRound = 0;

		delete[] fLedMult;
		fLedMult = nullptr;
	}
}
