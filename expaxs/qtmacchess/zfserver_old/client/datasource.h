/*  A Master DataSource Class
 *  Saves all client settings to settings.conf 
 *  Reads File Upon Startup
 *  If no file exists, it uses default values
 */
#ifndef DATASOURCE_H
#define DATASOURCE_H

class DataSource
{
    
public:
    static void initialize();
    static void save();
    static void saveDefaults();
    
    /* Connection Related Variables */
    static bool connectToMotor;
    static bool connectToZoomFocus;
    static bool connectedToMotor;
    static bool connectedToZoomFocus;
    static bool connectedToVideo;
    static bool directCompumotor;
    static int videoPort;    
    static int cmotorPort;
    static int zfmotorPort;
    static QString videoIP;
    static QString cmotorIP;
    static QString zfmotorIP;
    
    
    /* Compumotor Related */
    static bool motor_busy;
  
    /* size of pin movement step (mm) */
    
    static float pinStep;
    
    // scale corrections to pin motor movement
    // 45 is the motor that moves up/down when
    // phi = 45 deg etc.
    // corZ = in direction of phi axis
    
    static float cor45;
    static float cor135;
    static float corZ;
	    
    /* Zoom / Focus */
    static bool enableFocus;
    static int zoomLimit;
    static int focusLimit;
    static int zoomCurrent;
    static float pixPerMicron;
    static int focusCurrent;
    static bool zoomBoxDisplayed;
    
    
    /* Video Streaming */
    static int quality;
    static int bitrate;
    static int resolution;

    /* Midpoint Tool Related */
    static bool midpointToolEnabled;
    static int upperLineY;
    static int lowerLineY;
    static int vertLineX;
    static int centerY;
    static int centerX;
    static int midLineY;
    static bool newMidpoint;
    static bool midpointTool;
        
    /* Crosshair / Beam Diameter Display Related */
    static float crossX;   // in microns from zoom center
    static float crossY;
    static int zcenX;    // zoom center in pixels
    static int zcenY;    // zoom center in pixels
     
    static bool crossHairEnabled;
    static bool crossHairDisplayed;
    static bool newCrossHair;
    static int beam_dia;
    
    /* Scale Display Related */
    static bool barDisplayed;
    static float zoomFactor; 
    
    static bool clickAndMove;
};

#endif
