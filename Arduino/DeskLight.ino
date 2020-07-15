// Visual Micro is in vMicro>General>Tutorial Mode
// 
/*
	Name:       DeskLight.ino
	Created:	04.06.2020 16:27:34
	Author:     DESKTOP-A3HO5R0\Fabian
*/

#include "RawRGB.h"
#include "Animations.h"
#include <FastLED.h>
#include <eeprom.h>

#define LED_PIN     5
#define BUT_PIN		4
#define NUM_LEDS    286
#define BRIGHTNESS  64
#define LED_TYPE    WS2811
#define COLOR_ORDER GRB

#pragma region Points

#define MONITOR_MIDDLE 57
#define MONITOR_LEFT 78
#define MONITOR_RIGHT 36

#pragma endregion


const byte numChars = 32;
char receivedChars[numChars];
char tempChars[numChars];

int cmd = 1;
int cmd_ir = 255, cmd_ig = 64, cmd_ib = 0;

boolean newData = false;

CRGB leds[NUM_LEDS];

bool _bButState = false;
int _iMode = 0;

int Leben = 100;

Animations *anim;

void setup()
{
	Serial.begin( 115200 );
	delay( 1000 ); // power-up safety delay

	FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>( leds, NUM_LEDS ).setCorrection( TypicalLEDStrip );
	FastLED.setBrightness( BRIGHTNESS );

	anim = new Animations( NUM_LEDS, leds );
	//engine->addAnimation( ePerlin );
	cmd = EEPROM.read( 0 );
	cmd_ir = EEPROM.read( 1 );
	cmd_ig = EEPROM.read( 2 );
	cmd_ib = EEPROM.read( 3 );

	pinMode( BUT_PIN, INPUT );
}

#define UPDATES 50
unsigned long ulLast = 0;
void loop()
{


	if ( millis() - ulLast >= 1000 / 50 )
	{
		if ( digitalRead( BUT_PIN ) == HIGH && !_bButState )
		{
			++_iMode;
			if ( Leben >= 10 )
			{
				Leben -= 10;
			}
			_bButState = true;
		}
		else if ( digitalRead( BUT_PIN ) == LOW && _bButState )
		{
			_bButState = false;
		}
		//engine->animate();

		updateLEDs();

		FastLED.show();
		ulLast = millis();
	}
	else
	{
		recvWithStartEndMarkers();

		if ( newData == true )
		{
			strcpy( tempChars, receivedChars );
			  // this temporary copy is necessary to protect the original data
			  //   because strtok() used in parseData() replaces the commas with \0
			parseData();
			showParsedData();
			newData = false;
		}
	}

}

void updateLEDs()
{


	if ( cmd == 1 )
		anim->fade( cmd_ir, cmd_ig, cmd_ib );
	if ( cmd == 2 )
		anim->wave( MONITOR_MIDDLE, cmd_ir, cmd_ig, cmd_ib );
}

void recvWithStartEndMarkers()
{
	static boolean recvInProgress = false;
	static byte ndx = 0;
	char startMarker = '<';
	char endMarker = '>';
	char rc;

	Serial.println( "<XON>" );
	//delay( 10 );
	unsigned long ulStart = millis();

	while ( Serial.available() > 0 && newData == false )
	{
		rc = Serial.read();
		if ( millis() - ulStart > 100 )
		{
			break;
		}
		if ( rc == startMarker )
		{
			recvInProgress = true;
		}
		while ( recvInProgress == true )
		{
			if ( millis() - ulStart > 100 )
			{
				break;
				recvInProgress = false;
			}
			if ( Serial.available() > 0 )
			{
				rc = Serial.read();

				if ( rc != endMarker )
				{
					receivedChars[ndx] = rc;
					ndx++;
					if ( ndx >= numChars )
					{
						ndx = numChars - 1;
					}
				}
				else
				{
					receivedChars[ndx] = '\0'; // terminate the string
					recvInProgress = false;
					ndx = 0;
					newData = true;
				}
			}
		}

	}
	Serial.println( "<XOFF>" );
	Serial.flush();
}

void parseData()
{      // split the data into its parts

	char * strtokIndx; // this is used by strtok() as an index

	strtokIndx = strtok( tempChars, "," );      // get the first part - the string
	cmd = atoi( strtokIndx );   // copy it to messageFromPC

	strtokIndx = strtok( NULL, "," ); // this continues where the previous call left off
	cmd_ir = atoi( strtokIndx );     // convert this part to an integer

	strtokIndx = strtok( NULL, "," );
	cmd_ig = atoi( strtokIndx );     // convert this part to a float

	strtokIndx = strtok( NULL, "," );
	cmd_ib = atoi( strtokIndx );     // convert this part to a float

	EEPROM.write( 0, cmd );
	EEPROM.write( 1, cmd_ir );
	EEPROM.write( 2, cmd_ig );
	EEPROM.write( 3, cmd_ib );
}

void showParsedData()
{
	Serial.print( "< " );
	Serial.print( cmd );
	Serial.print( ", " );
	Serial.print( cmd_ir );
	Serial.print( ", " );
	Serial.print( cmd_ig );
	Serial.print( ", " );
	Serial.print( cmd_ib );
	Serial.print( ">" );
}