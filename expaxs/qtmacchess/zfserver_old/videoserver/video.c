/*****************************************************************************
 *  Application notes :
 *		                    
 *  A sequence of YUV pics in PGM file format is encoded and decoded
 *  The speed is measured and PSNR of decoded picture is calculated. 
 *		                   
 *  The program is plain C and needs no libraries except for libxvidcore, 
 *  and maths-lib.
 *	
 ************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "driver.h"
#include <xvid.h>
#ifndef _MSC_VER
#include <sys/time.h>
#else
#include <time.h>
#endif



/*****************************************************************************
 *                            Quality presets
 ****************************************************************************/

static int const motion_presets[7] = {
	0,                                                        /* Q 0 */
	PMV_EARLYSTOP16,                                          /* Q 1 */
	PMV_EARLYSTOP16,                                          /* Q 2 */
	PMV_EARLYSTOP16 | PMV_HALFPELREFINE16,                    /* Q 3 */
	PMV_EARLYSTOP16 | PMV_HALFPELREFINE16,                    /* Q 4 */
	PMV_EARLYSTOP16 | PMV_HALFPELREFINE16 | PMV_EARLYSTOP8 |  /* Q 5 */
	PMV_HALFPELREFINE8,
	PMV_EARLYSTOP16 | PMV_HALFPELREFINE16 | PMV_EXTSEARCH16 | /* Q 6 */
	PMV_USESQUARES16 | PMV_EARLYSTOP8 | PMV_HALFPELREFINE8
};

static int const general_presets[7] = {
	XVID_H263QUANT,	                              /* Q 0 */
	XVID_MPEGQUANT,                               /* Q 1 */
	XVID_H263QUANT,                               /* Q 2 */
	XVID_H263QUANT | XVID_HALFPEL,                /* Q 3 */
	XVID_H263QUANT | XVID_HALFPEL | XVID_INTER4V, /* Q 4 */
	XVID_H263QUANT | XVID_HALFPEL | XVID_INTER4V, /* Q 5 */
	XVID_H263QUANT | XVID_HALFPEL | XVID_INTER4V  /* Q 6 */
};
		

/*****************************************************************************
 *                     Command line global variables
 ****************************************************************************/

/* Maximum number of frames to encode */
#define ABS_MAXFRAMENR 9999

/* HINTMODEs */
#define HINT_MODE_NONE 0
#define HINT_MODE_GET  1
#define HINT_MODE_SET  2
#define HINT_FILE "hints.mv"
#define FORMAT_YUV 0
#define FORMAT_MP4U 1
#define FORMAT_M4V 0

static int   ARG_BITRATE = 900;
static int   ARG_QUANTI = 0;
static int   ARG_QUALITY = 6;
static int   ARG_MINQUANT = 1;
static int   ARG_MAXQUANT = 31;
static float ARG_FRAMERATE = 15.00f;
static int   ARG_HINTMODE = HINT_MODE_NONE;
static int   XDIM = 1024;
static int   YDIM = 768;
unsigned char *in_buffer;
unsigned char *hints_buffer;
long hints_size, totalsize;
#define IMAGE_SIZE(x,y) ((x)*(y)*3/2)

#define MAX(A,B) ( ((A)>(B)) ? (A) : (B) )
#define SMALL_EPS 1e-10

#define LONG_PACK(a,b,c,d) ((long) (((long)(a))<<24) | (((long)(b))<<16) | \
                                   (((long)(c))<<8)  |((long)(d)))

#define SWAP(a) ( (((a)&0x000000ff)<<24) | (((a)&0x0000ff00)<<8) | \
                  (((a)&0x00ff0000)>>8)  | (((a)&0xff000000)>>24) )
/****************************************************************************
 *                     Nasty global vars ;-)
 ***************************************************************************/

int i,filenr = 0, bigendian;

/* the path where to save output */
char filepath[256] = "./";

/* Internal structures (handles) for encoding and decoding */
void *enc_handle = NULL;

/*****************************************************************************
 *               Local prototypes
 ****************************************************************************/

/* Prints program usage message */
void usage();

/* Statistical functions */
double msecond();

/* PGM related functions */
int read_pgmheader(FILE* handle);
int read_pgmdata(FILE* handle, unsigned char *image);

/* MACCHESS Related Functions */
int macchess_initialize_compressor();
unsigned char *macchess_get_frame(unsigned char *mp4_buffer, long *size, int keyframe, double *time);
void macchess_stop_compressor();

;
/* Encoder related functions */
int enc_init(int use_assembler);
int enc_stop();
int enc_main(unsigned char* image, unsigned char* bitstream,
					unsigned char *hints_buffer,
					long *streamlength, long* frametype, long *hints_size, int keyframe);



/*****************************************************************************
 *               MACCHESS Compressor Initialization Function
 ****************************************************************************/
int macchess_initialize_compressor()
{
	int status;
	int use_assembler=1;
	macchess_initialize_camera();
	/* now we know the sizes, so allocate memory */
	// in_buffer = (unsigned char *) malloc(IMAGE_SIZE(XDIM,YDIM));


		/* this should really be enough memory ! 
	mp4_buffer = (unsigned char *) malloc(IMAGE_SIZE(XDIM,YDIM)*2);
	if (!mp4_buffer)
	goto free_all_memory;	*/

	totalsize = LONG_PACK('M','P','4','U');
	if(*((char *)(&totalsize)) == 'M')
		bigendian = 1;
	else
		bigendian = 0;

/*****************************************************************************
 *                            XviD Encoder Initialization
 ****************************************************************************/
	status = enc_init(use_assembler);
	if (status)    
	{ 
		fprintf(stderr, "Encore INIT problem, return value %d\n", status);
	
	}
	return bigendian;
}




/*****************************************************************************
 *                       Get a compressed frame from the XVID CODEC
 ****************************************************************************/
unsigned char *macchess_get_frame(unsigned char *mp4_buffer, long *size, int keyframe, double *time)
{
  int status;
  double enctime;
  long frame_type; 
  long m4v_size;
  unsigned char *raw_frame = macchess_get_raw_frame();
  //  malloc(1024*768*2);
  //FILE *debug = fopen("raw_frame", "r");
  //fread(raw_frame, 1024*768*2, 1, debug);
  // fclose(debug);


	  // =  //in_buffer);
  // printf("get_compressed_frame recieved: %d\n", (int)in_buffer);
  // read_yuvdata(in_buffer);	/* read raw data (YUV-format) */
  
 
  /*****************************************************************************
   *                       Encode and decode this frame
   ****************************************************************************/
  
  
  enctime = msecond();
  status = enc_main(raw_frame, mp4_buffer, hints_buffer,
		    &m4v_size, &frame_type, &hints_size, keyframe);
  enctime = msecond() - enctime;
  *size =  m4v_size;
  if(raw_frame == NULL) printf("NULL inside XVID");
  //printf("Enctime=%6.1f ms, size=%6dbytes\n",
	// (float)enctime, (int)(*size));
  *time = enctime;
  return raw_frame;
  
}

 /*****************************************************************************
  *                  Cleanup function, frees compressor related stuff
   ****************************************************************************/
void macchess_stop_compressor()
{
  int status;
  macchess_stop_transmission();
  if (enc_handle)
    {	
      status = enc_stop();
      if (status)    
	fprintf(stderr, "Encore RELEASE problem return value %d\n", status);
    }
 // free(in_buffer);
}


/*****************************************************************************
 *                        "statistical" functions
 *
 *  these are not needed for encoding or decoding, but for measuring
 *  time and quality, there in nothing specific to XviD in these
 *
 *****************************************************************************/

/* Return time elapsed time in miliseconds since the program started */
double msecond()
{	
#ifndef WIN32
	struct timeval  tv;
	gettimeofday(&tv, 0);
	return tv.tv_sec*1.0e3 + tv.tv_usec * 1.0e-3;
#else
	clock_t clk;
	clk = clock();
	return clk * 1000 / CLOCKS_PER_SEC;
#endif
}

/*****************************************************************************
 *                             Usage message
 *****************************************************************************/
void usage()
{

	fprintf(stderr, "This usage is only for reference. The encoder is not to be called from cmd line\n");
	fprintf(stderr, "--Ismail Degani\n");
	fprintf(stderr, "Options :\n");
	fprintf(stderr, " -asm           : use assembly code\n");
	fprintf(stderr, " -w integer     : frame width ([1.2048])\n");
	fprintf(stderr, " -h integer     : frame height ([1.2048])\n");
	fprintf(stderr, " -b integer     : target bitrate (>0 | default=900kbit)\n");
	fprintf(stderr, " -f float       : target framerate (>0)\n");
	fprintf(stderr, " -i string      : input filename (default=stdin)\n");
	fprintf(stderr, " -t integer     : input data type (yuv=0, pgm=1)\n");
	fprintf(stderr, " -n integer     : number of frames to encode\n");
	fprintf(stderr, " -q integer     : quality ([0..5])\n");
	fprintf(stderr, " -m boolean     : save mpeg4 raw stream (0 False*, !=0 True)\n");
	fprintf(stderr, " -o string      : output container filename (only usefull when -m 1 is used) :\n");
	fprintf(stderr, "                  When this option is not used : one file per encoded frame\n");
	fprintf(stderr, "                  When this option is used :\n");
	fprintf(stderr, "                    + stream.m4v with -mt 0\n");
	fprintf(stderr, "                    + stream.mp4u with -mt 1\n");
	fprintf(stderr, " -mt integer    : output type (m4v=0, mp4u=1)\n");
	fprintf(stderr, " -mv integer    : Use motion vector hints (no hints=0, get hints=1, set hints=2)\n");
	fprintf(stderr, " -help          : prints this help message\n");
	fprintf(stderr, " -quant integer : fixed quantizer (disables -b setting)\n");
	fprintf(stderr, " (* means default)\n");

}

/*****************************************************************************
 *                       Input and output functions
 *
 *      the are small and simple routines to read and write PGM and YUV
 *      image. It's just for convenience, again nothing specific to XviD
 *
 *****************************************************************************/

int read_pgmheader(FILE* handle)
{	
	int bytes,xsize,ysize,depth;
	char dummy[2];
	
	bytes = fread(dummy,1,2,handle);

	if ( (bytes < 2) || (dummy[0] != 'P') || (dummy[1] != '5' ))
   		return 1;

	fscanf(handle,"%d %d %d",&xsize,&ysize,&depth); 
	if ( (xsize > 1440) || (ysize > 2880 ) || (depth != 255) )
	{
		fprintf(stderr,"%d %d %d\n",xsize,ysize,depth);
	   	return 2;
	}
	if ( (XDIM==0) || (YDIM==0) )
	{
		XDIM=xsize;
		YDIM=ysize*2/3;
	}

	return 0;
}

int read_pgmdata(FILE* handle, unsigned char *image)
{	
	int i;
	char dummy;
	
	unsigned char *y = image;
	unsigned char *u = image + XDIM*YDIM;
	unsigned char *v = image + XDIM*YDIM + XDIM/2*YDIM/2; 

	/* read Y component of picture */
	fread(y, 1, XDIM*YDIM, handle);
 
	for (i=0;i<YDIM/2;i++)
	{
		/* read U */
		fread(u, 1, XDIM/2, handle);

		/* read V */
		fread(v, 1, XDIM/2, handle);

		/* Update pointers */
		u += XDIM/2;
		v += XDIM/2;
	}

    /*  I don't know why, but this seems needed */
	fread(&dummy, 1, 1, handle);

	return 0;
}


/*****************************************************************************
 *     Routines for encoding: init encoder, frame step, release encoder
 ****************************************************************************/

#define FRAMERATE_INCR 1001

/* Initialize encoder for first use, pass all needed parameters to the codec */
int enc_init(int use_assembler)
{
	int xerr;
	
	XVID_INIT_PARAM xinit;
	XVID_ENC_PARAM xparam;

	if(use_assembler) {

#ifdef ARCH_IA64
		xinit.cpu_flags = XVID_CPU_FORCE | XVID_CPU_IA64;
#else
		xinit.cpu_flags = 0;
#endif
	}
	else {
		xinit.cpu_flags = XVID_CPU_FORCE;
	}

	xvid_init(NULL, 0, &xinit, NULL);

	xparam.width = XDIM;
	xparam.height = YDIM;
	if ((ARG_FRAMERATE - (int)ARG_FRAMERATE) < SMALL_EPS)
	{
		xparam.fincr = 1;
		xparam.fbase = (int)ARG_FRAMERATE;
	}
	else
	{
		xparam.fincr = FRAMERATE_INCR;
		xparam.fbase = (int)(FRAMERATE_INCR * ARG_FRAMERATE);
	}
	xparam.rc_reaction_delay_factor = 16;
	xparam.rc_averaging_period = 100;
	xparam.rc_buffer = 10;
	xparam.rc_bitrate = ARG_BITRATE*1000; 
	xparam.min_quantizer = ARG_MINQUANT;
	xparam.max_quantizer = ARG_MAXQUANT;
	xparam.max_key_interval = (int)ARG_FRAMERATE*10;

	/* I use a small value here, since will not encode whole movies, but short clips */

	xerr = xvid_encore(NULL, XVID_ENC_CREATE, &xparam, NULL);
	enc_handle=xparam.handle;

	return xerr;
}

int enc_stop()
{
	int xerr;

	xerr = xvid_encore(enc_handle, XVID_ENC_DESTROY, NULL, NULL);
	return xerr;

}

int enc_main(unsigned char* image, unsigned char* bitstream,
					unsigned char* hints_buffer,
					long *streamlength, long *frametype, long *hints_size,
					int keyframe)
{
	int xerr;

	XVID_ENC_FRAME xframe;
	XVID_ENC_STATS xstats;

	xframe.bitstream = bitstream;
	xframe.length = -1; 	/* this is written by the routine */

	xframe.image = image;
	xframe.colorspace = XVID_CSP_UYVY;	/* defined in <xvid.h> */

	/* let the codec decide between I-frame (1) and P-frame (0)  if keyframe == 0*/
	/* if the keyframe is 1, then we force a keyframe */
	xframe.intra = keyframe; 

	xframe.quant = ARG_QUANTI;	/* is quant != 0, use a fixed quant (and ignore bitrate) */

	xframe.motion = motion_presets[ARG_QUALITY];
	xframe.general = general_presets[ARG_QUALITY];
	xframe.quant_intra_matrix = xframe.quant_inter_matrix = NULL;

	xframe.hint.hintstream = hints_buffer;

	if(ARG_HINTMODE == HINT_MODE_SET) {
		xframe.hint.hintlength = *hints_size;
		xframe.hint.rawhints = 0;
		xframe.general |= XVID_HINTEDME_SET;
	}

	if(ARG_HINTMODE == HINT_MODE_GET) {
		xframe.hint.rawhints = 0;
		xframe.general |= XVID_HINTEDME_GET;
	}

	xerr = xvid_encore(enc_handle, XVID_ENC_ENCODE, &xframe, &xstats);

	if(ARG_HINTMODE == HINT_MODE_GET)
		*hints_size = xframe.hint.hintlength;

	/*
	 * This is statictical data, e.g. for 2-pass. If you are not
	 * interested in any of this, you can use NULL instead of &xstats
	 */
	*frametype = xframe.intra;
	*streamlength = xframe.length;

	return xerr;
}
