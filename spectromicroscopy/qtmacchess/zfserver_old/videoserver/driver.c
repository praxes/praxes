/* This is the macchess digital 1394 driver that 
   pipes raw data to ffserver for streaming in 
   a variety of bitrates and formats. It requests the
   data from the camera in an uncompressed 1024x768 pixels at
   15 frames per second, which is the highest the camera can
   support.


    -- Ismail Degani
    -- Saturday, February 8th
*/       


#include <stdio.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <libraw1394/raw1394.h>
#include <libdc1394/dc1394_control.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <fcntl.h>
#include <string.h>
#include "driver.h"
#define PMIN(x,y) ((x) > (y) ? (y) : (x))
#define BLACK_Y 0
#define BLACK_U 128
#define BLACK_V 128
#define FALSE 0
#define TRUE 1

//  These need to be global so that the cleanup function 
//  will work through signals - Ismail

dc1394_cameracapture camera;
raw1394handle_t handle;




void  macchess_initialize_camera()
{

  int numNodes;
  int numCameras;
  nodeid_t * camera_nodes;
  quadlet_t supported_framerates;
  int framerate;
  const char *dma_device_file;
  
  int i;

  /*-----------------------------------------------------------------------
   *  Set kill signal to exit cleanly via my cleanup function
   *-----------------------------------------------------------------------*/
  signal(SIGINT, macchess_stop_transmission);
  signal(SIGQUIT, macchess_stop_transmission);
  signal(SIGKILL, macchess_stop_transmission);
  
  /*-----------------------------------------------------------------------
   *  Open ohci and asign handle to it
   *-----------------------------------------------------------------------*/
  handle = dc1394_create_handle(0);
  if (handle==NULL)
  {
    fprintf( stderr, "Unable to aquire a raw1394 handle\n\n"
             "Please check \n"
	     "  - if the kernel modules `ieee1394',`raw1394' and `ohci1394' are loaded \n"
	     "  - if you have read/write access to /dev/raw1394\n\n");
    exit(1);
  }

  
  /*-----------------------------------------------------------------------
   *  get the camera nodes and describe them as we find them
   *-----------------------------------------------------------------------*/
  numNodes = raw1394_get_nodecount(handle);
  camera_nodes = dc1394_get_camera_nodes(handle,&numCameras,0);
  fflush(stdout);
  if (numCameras<1)
  {
    fprintf( stderr, "no cameras found :(\n");
    dc1394_destroy_handle(handle);
    exit(1);
  }
  fprintf(stderr, "working with the first camera on the bus\n");
  
  /*-----------------------------------------------------------------------
   *  to prevent the iso-transfer bug from raw1394 system, check if
   *  camera is highest node. For details see 
   *  http://linux1394.sourceforge.net/faq.html#DCbusmgmt
   *  and
   *  http://sourceforge.net/tracker/index.php?func=detail&aid=435107&group_id=8157&atid=108157
   *-----------------------------------------------------------------------*/
  for (i=0; i<numCameras; i++) {
    if( camera_nodes[i] == numNodes-1)
      {
	fprintf( stderr, "\n"
             "Sorry, your camera is the highest numbered node\n"
             "of the bus, and has therefore become the root node.\n"
             "The root node is responsible for maintaining \n"
             "the timing of isochronous transactions on the IEEE \n"
             "1394 bus.  However, if the root node is not cycle master \n"
             "capable (it doesn't have to be), then isochronous \n"
             "transactions will not work.  The host controller card is \n"
             "cycle master capable, however, most cameras are not.\n"
             "\n"
             "The quick solution is to add the parameter \n"
             "attempt_root=1 when loading the OHCI driver as a \n"
             "module.  So please do (as root):\n"
             "\n"
             "   rmmod ohci1394\n"
             "   insmod ohci1394 attempt_root=1\n"
             "\n"
             "for more information see the FAQ at \n"
             "http://linux1394.sourceforge.net/faq.html#DCbusmgmt\n"
             "\n");
	exit( 1);
      }
  }

  /*
   * Check fastest available framerate.
   */
    if (dc1394_query_supported_framerates(handle, camera_nodes[0],
					FORMAT_SVGA_NONCOMPRESSED_1,
					MODE_1024x768_YUV422,
					&supported_framerates) != DC1394_SUCCESS) {
    fprintf(stderr, "dc1394_query_supported_framerates() failed.");
    exit(1);
    }

  if (supported_framerates & (1U << (31-5)))
    framerate = FRAMERATE_60;
  else if (supported_framerates & (1U << (31-4)))
    framerate = FRAMERATE_30;
  else if (supported_framerates & (1U << (31-3)))
    framerate = FRAMERATE_15;
  else if (supported_framerates & (1U << (31-2)))
    framerate = FRAMERATE_7_5;
  else if (supported_framerates & (1U << (31-1)))
    framerate = FRAMERATE_3_75;
  else if (supported_framerates & (1U << (31-0)))
    framerate = FRAMERATE_1_875;
  else {
    fprintf(stderr, "No available framerate?\n");
    exit(1);
    } 

  /*-----------------------------------------------------------------------
   *  setup capture
   *-----------------------------------------------------------------------*/
  if (access("/dev/video1394/0", R_OK) == 0)
    dma_device_file = "/dev/video1394/0";
  else if (access("/dev/video1394", R_OK) == 0)
    dma_device_file = "/dev/video1394";
  else {
    fprintf(stderr, "Cannot access the video1394 device file.\n");
    exit(1);
  }


  /* This is where libdc1394 (explicitly not raw1394) specific code starts
     I replaced libdc with libraw, so this libdc specific code is commented out
     -- Ismail August 8th, 2003
  */
  /*
  if (dc1394_dma_setup_capture(handle,camera_nodes[0],
			       0,  channel 
			       FORMAT_SVGA_NONCOMPRESSED_1,
			       MODE_1024x768_YUV422,
			       SPEED_400,
			       framerate, 4, 1, dma_device_file,
			       &camera)!=DC1394_SUCCESS) 
  {
    fprintf( stderr,"unable to setup camera-\n"
             "check line %d of %s to make sure\n"
             "that the video mode,framerate and format are\n"
             "supported by your camera\n",
             __LINE__,__FILE__);
    dc1394_dma_release_camera(handle,&camera);
    dc1394_destroy_handle(handle);
    exit(1);
  }


*/
  /* Here is the libraw1394 replacement
     Switched from libdc to libraw because of a bug in libdc, but 
     there are many changes that I made throughout the file to accomodate
     the switch, so if libdc does eventually get better, you'll have to 
     look at coriander's source code (thread_iso.c) if you want to switch back
     -- Ismail Degani August 8th, 2003
  */
  if(dc1394_setup_capture(handle, camera_nodes[0],
			  0, /* channel */
			  FORMAT_SVGA_NONCOMPRESSED_1,
			  MODE_1024x768_YUV422,
			  SPEED_400,
			  framerate, &camera) != DC1394_SUCCESS)
  {
    fprintf( stderr,"unable to setup camera-\n"
             "check line %d of %s to make sure\n"
             "that the video mode,framerate and format are\n"
             "supported by your camera\n",
             __LINE__,__FILE__);
    dc1394_release_camera(handle,&camera);
    dc1394_destroy_handle(handle);
    exit(1);
  }
  

  if (dc1394_start_iso_transmission(handle,camera.node)
      !=DC1394_SUCCESS) 
    {
      fprintf( stderr, "unable to start camera iso transmission\n");
      dc1394_release_camera(handle, &camera);
      dc1394_destroy_handle(handle);
      exit(1);
    }
}


// For our current camera, buf must be at least 1179648 bytes
// (A single 1024x768 frame in color is exactly that size
unsigned char *macchess_get_raw_frame() // unsigned char *buf)
{
  /*-----------------------------------------------------------------------
   *  have the camera start sending us data
   *-----------------------------------------------------------------------*/
  //unsigned char buf[1179648]; // 1024x768x(3/2)
  //unsigned char buf[2048*2048]; // 1024x768x(3/2)

      
    if (dc1394_single_capture(handle, &camera)!=DC1394_SUCCESS) 
      {
	fprintf( stderr, "unable to capture a frame\n");
	dc1394_release_camera(handle,&camera);
	dc1394_destroy_handle(handle);
	exit(1);
      }
    
    // uyvy422_yuv420p((const char *)camera.capture_buffer, buf);
    // memcpy(buf, camera.capture_buffer, 1572864);
    // printf("Buf is: %d\n", (int)(buf));
    return  (unsigned char*)(camera.capture_buffer);
    // printf("Buf is now: %d\n", (int)(buf));
    // write(1, buf, camera.frame_height*camera.frame_width*3/2);
    // dc1394_dma_done_with_buffer(&camera);
  
}

// Manual Cleanup
void macchess_stop_transmission()
{
  /*-----------------------------------------------------------------------
   *  Stop data transmission
   *-----------------------------------------------------------------------*/
  if (dc1394_stop_iso_transmission(handle,camera.node)!=DC1394_SUCCESS) 
    {
      fprintf(stderr, "couldn't stop the camera?\n");
    }
  
  /*-----------------------------------------------------------------------
   *  Close camera
   *-----------------------------------------------------------------------*/
  // dc1394_dma_unlisten(handle, &camera);
  dc1394_release_camera(handle,&camera);
  dc1394_destroy_handle(handle);
}



/*
int main(int argc, char *argv[])
{
  macchess_initialize_camera();
  // macchess_start_transmission("balh");
  // macchess_get_raw_data();
  macchess_stop_transmission();
  return 0;
}

*/
