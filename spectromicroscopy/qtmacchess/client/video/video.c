#include <stdio.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <xvid.h>

#define YUV_FRAME_SIZE 1024*768*2
#define XDIM 1024
#define YDIM 768

int socket_fd = -1;
FILE *buffered_socket_stream;
int use_assembler = 1;
unsigned char mp4_buffer[YUV_FRAME_SIZE];
static void *dec_handle = NULL;
int used_bytes = 0;

/*****************************************************************************
 * Routines for decoding: init decoder, use, and stop decoder
 ****************************************************************************/

/* init decoder before first run */
static int
dec_init(int use_assembler)
{
        int xerr;

        XVID_INIT_PARAM xinit;
        XVID_DEC_PARAM xparam;

		if(use_assembler)
#ifdef ARCH_IA64
			xinit.cpu_flags = XVID_CPU_FORCE | XVID_CPU_IA64;
#else
			xinit.cpu_flags = 0;
#endif
		else
			xinit.cpu_flags = XVID_CPU_FORCE;

        xvid_init(NULL, 0, &xinit, NULL);
        xparam.width = XDIM;
        xparam.height = YDIM;

        xerr = xvid_decore(NULL, XVID_DEC_CREATE, &xparam, NULL);
        dec_handle = xparam.handle;

        return xerr;
}

/* decode one frame  */
static int
dec_main(unsigned char *istream,
	 unsigned char *ostream,
	 int istream_size,
	 int *ostream_size)
{

        int xerr;
        XVID_DEC_FRAME xframe;

        xframe.bitstream = istream;
        xframe.length = istream_size;
	xframe.image = ostream;
        xframe.stride = XDIM;
	xframe.colorspace = XVID_CSP_UYVY;             

	xerr = xvid_decore(dec_handle, XVID_DEC_DECODE, &xframe, NULL);

	*ostream_size = xframe.length;

        return xerr;
}

/* close decoder to release resources */
static int
dec_stop()
{
        int xerr;

        xerr = xvid_decore(dec_handle, XVID_DEC_DESTROY, NULL, NULL);

        return xerr;
}


/* Return time elapsed time in miliseconds since the program started */
double msecond()
{	
	clock_t clk;
	clk = clock();
	return clk * 1000 / CLOCKS_PER_SEC;
}



int  macchess_initialize_client(char *ipAddr, int port)
{
 
  int status;
  unsigned char header[4];
  struct sockaddr_in serv;
  //ipAddr[strlen(ipAddr)-1] = '\0';
  
  fprintf(stderr, "Connecting to video at %s on port %d\n", ipAddr, port);
  
  // Initialize the Decoder
  status = dec_init(use_assembler);
  
  // Socket Stuff
  socket_fd = socket(AF_INET,SOCK_STREAM,0);
  // printf("socket returned: %d\n",socket_fd);
  serv.sin_family=AF_INET;
  
  // REG!! hard coded address 
  
// f1-vid  (currently on F2)
  inet_aton(ipAddr, &(serv.sin_addr));
 // inet_aton("128.84.182.123", &(serv.sin_addr));
  
// alanine  
//  inet_aton("128.84.182.123",&(serv.sin_addr));
  
  serv.sin_port=htons(port);
  status = connect(socket_fd,(struct sockaddr *)&serv,sizeof(serv));
  // printf("Connect returned: %d\n",status);
  buffered_socket_stream = fdopen(socket_fd, "r+b");
  //  MP4U format  : read header 
  fread(header, 4, 1, buffered_socket_stream);
  if(header[0] != 'M' || header[1] != 'P' || header[2] != '4' || header[3] != 'U') 
    {
      fprintf(stderr, "Error, this not a readable stream header\n");
      return -1;
      // exit(0);
    }
  else 
  {
      fprintf(stderr, "The mp4u header was successfully read in\n");
      return 0;
  }

}



void macchess_get_decompressed_frame(unsigned char *buf)
{
  int status;	
  long mp4_size;
  status = fread(&mp4_size, sizeof(long), 1, buffered_socket_stream);
  
  status = fread(mp4_buffer, mp4_size, 1, buffered_socket_stream);
  status = dec_main(mp4_buffer, buf, mp4_size, &used_bytes);
}

void macchess_send_kill()
{
    char quit = 'q';    
    int i = fwrite(&quit, sizeof(char), 1, buffered_socket_stream);
    fprintf(stderr, "Sent graceful video quit command, i = %d\n", i);
    sleep(2);
    //fclose(buffered_socket_stream);
    //close(socket_fd);
}

void macchess_close_connection()
{
  dec_stop();
  // fwrite("stop",  4 * sizeof(char), buffered_socket_stream);
  // sleep(1); // 1 second should be enough
 fclose(buffered_socket_stream);
 close(socket_fd);
}

void macchess_send_crosshairs(int crossX, int crossY)
{
    char ch = 'c'; 
 
    int i = fwrite(&ch, sizeof(char), 1, buffered_socket_stream);
    i = fwrite((char*)&crossX, sizeof(int), 1, buffered_socket_stream);
    i = fwrite((char*)&crossY, sizeof(int), 1, buffered_socket_stream);
//    fprintf(stderr, "Just wrote the following crosshairs: %d,%d\n", crossX, crossY);
    
}

/*
int main()
{
  FILE *rgbFile = fopen("/home/degani/testing/rgb", "w+");
  unsigned char buf[1024*768*3];
  int i;
  macchess_initialize_client();
  //for(i = 0; i < 150; i++)
  //  {
      macchess_get_rgb_frame(buf);
      fwrite(buf, 1024*768*3, 1, rgbFile);
      //  }
  macchess_close_connection();
  fclose(rgbFile);
  return 0;
}
*/
