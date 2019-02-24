#if !defined(IO_MMAP)
#define IO_MMAP
#endif

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <getopt.h>
#include <fcntl.h>
#include <unistd.h>
#include <errno.h>
#include <malloc.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/time.h>
#include <time.h>
#include <sys/mman.h>
#include <sys/ioctl.h>
#include <asm/types.h>
#include <linux/videodev2.h>
#include <jpeglib.h>
#include <libv4l2.h>
#include <signal.h>
#include <stdint.h>
#include <inttypes.h>
#include <arpa/inet.h>
#include <netinet/in.h>

#include "config.h"
#include "yuv.h"

#define CLEAR(x) memset (&(x), 0, sizeof (x))
#define VIDIOC_REQBUFS_COUNT 2	

typedef enum {
        IO_METHOD_MMAP,
} io_method;

/**
Initialisation
**/

struct buffer {
        void *                  start;
        size_t                  length;
};

static io_method        io              = IO_METHOD_MMAP;
static int              fd              = -1;
struct buffer *         buffers         = NULL;
static unsigned int     n_buffers       = 0;

// global settings
static unsigned int width = 640;
static unsigned int height = 480;
static unsigned int fps = 30;
static int continuous = 1;
static unsigned char jpegQuality = 70;
static char* jpegFilename = NULL;
static char* jpegFilenamePart = NULL;
static char* deviceName = "/dev/video0";

static const char* const continuousFilenameFmt = "%s_%010"PRIu32"_%"PRId64".jpg";

static unsigned int IMAGE_SIZE = 921600;
static unsigned int PORT_SEND = 15556;
static unsigned int PORT_RECV = 15555;
static struct sockaddr_in IPOFSERVER1;
static struct sockaddr_in IPOFSERVER2;

static int xioctl(int fd, int request, void* argp)
{
	int r;

	do r = v4l2_ioctl(fd, request, argp);
	while (-1 == r && EINTR == errno);

	return r;
}

static void errno_exit(const char* s)
{
	fprintf(stderr, "%s error %d, %s\n", s, errno, strerror(errno));
	exit(EXIT_FAILURE);
}


static void mmapInit(void)
{
	struct v4l2_requestbuffers req;

	CLEAR(req);

	req.count = VIDIOC_REQBUFS_COUNT;
	req.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
	req.memory = V4L2_MEMORY_MMAP;

	if (-1 == xioctl(fd, VIDIOC_REQBUFS, &req)) {
		if (EINVAL == errno) {
			fprintf(stderr, "%s does not support memory mapping\n", deviceName);
			exit(EXIT_FAILURE);
		} else {
			errno_exit("VIDIOC_REQBUFS");
		}
	}

	if (req.count < 2) {
		fprintf(stderr, "Insufficient buffer memory on %s\n", deviceName);
		exit(EXIT_FAILURE);
	}

	buffers = calloc(req.count, sizeof(*buffers));

	if (!buffers) {
		fprintf(stderr, "Out of memory\n");
		exit(EXIT_FAILURE);
	}

	for (n_buffers = 0; n_buffers < req.count; ++n_buffers) {
		struct v4l2_buffer buf;

		CLEAR(buf);

		buf.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
		buf.memory = V4L2_MEMORY_MMAP;
		buf.index = n_buffers;

		if (-1 == xioctl(fd, VIDIOC_QUERYBUF, &buf))
			errno_exit("VIDIOC_QUERYBUF");

		buffers[n_buffers].length = buf.length;
		buffers[n_buffers].start = v4l2_mmap(NULL /* start anywhere */, buf.length, PROT_READ | PROT_WRITE /* required */, MAP_SHARED /* recommended */, fd, buf.m.offset);

		if (MAP_FAILED == buffers[n_buffers].start)
			errno_exit("mmap");
	}
}

/**
Initialisation servers
**/

int init_server(int PORT, struct sockaddr_in ipOfServer)
{
  int clientListn = 0, clientConnt = 0;
  clientListn = socket(AF_INET, SOCK_STREAM, 0); // connection oriented TCP protocol
  if (clientListn == -1)
    {
        printf("Could not create socket");
    }
  // memset(&ipOfServer, '0', sizeof(ipOfServer)); // fills the struct with zeros
  // memset(dataSending, '0', sizeof(dataSending)); // fills the variable with zeros
  ipOfServer.sin_family = AF_INET; // designation of the adress type for communication ipV4
  ipOfServer.sin_addr.s_addr = INADDR_ANY; //htonl(ADDR); // convertion to address byte order
  ipOfServer.sin_port = htons( PORT ); // convertion to address byte order

  if ( bind(clientListn, (struct sockaddr*)&ipOfServer, sizeof(ipOfServer)) < 0 )
    {
       perror("bind failed. Error");
       return 1;
    }

  listen(clientListn, 20);



  printf("Waiting for connection on port %d...\n", PORT);
  clientConnt = accept(clientListn, (struct sockaddr*)NULL, NULL); // accept connexion with client
  if (clientConnt < 0)
  {
     perror("accept failed.");
     return 1;
  }
  printf("Connection established on port %d...\n", PORT);



  return clientConnt;
}

/**
	initialize device
*/
static void deviceInit(void)
{
	struct v4l2_capability cap;
	struct v4l2_cropcap cropcap;
	struct v4l2_crop crop;
	struct v4l2_format fmt;
	struct v4l2_streamparm frameint;
	unsigned int min;

	if (-1 == xioctl(fd, VIDIOC_QUERYCAP, &cap)) {
		if (EINVAL == errno) {
			fprintf(stderr, "%s is no V4L2 device\n",deviceName);
			exit(EXIT_FAILURE);
		} else {
			errno_exit("VIDIOC_QUERYCAP");
		}
	}

	if (!(cap.capabilities & V4L2_CAP_VIDEO_CAPTURE)) {
		fprintf(stderr, "%s is no video capture device\n",deviceName);
		exit(EXIT_FAILURE);
	}

	if (!(cap.capabilities & V4L2_CAP_STREAMING)) {
		fprintf(stderr, "%s does not support streaming i/o\n",deviceName);
		exit(EXIT_FAILURE);
	}

	/* Select video input, video standard and tune here. */
	CLEAR(cropcap);

	cropcap.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;

	if (0 == xioctl(fd, VIDIOC_CROPCAP, &cropcap)) {
		crop.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
		crop.c = cropcap.defrect; /* reset to default */

		if (-1 == xioctl(fd, VIDIOC_S_CROP, &crop)) {
			switch (errno) {
				case EINVAL:
					/* Cropping not supported. */
					break;
				default:
					/* Errors ignored. */
					break;
			}
		}
	} else {
		/* Errors ignored. */
	}

	CLEAR(fmt);

	// v4l2_format
	fmt.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
	fmt.fmt.pix.width = width;
	fmt.fmt.pix.height = height;
	fmt.fmt.pix.field = V4L2_FIELD_INTERLACED;
	fmt.fmt.pix.pixelformat = V4L2_PIX_FMT_YUV420;

	if (-1 == xioctl(fd, VIDIOC_S_FMT, &fmt))
		errno_exit("VIDIOC_S_FMT");

	if (fmt.fmt.pix.pixelformat != V4L2_PIX_FMT_YUV420) {
		fprintf(stderr,"Libv4l didn't accept YUV420 format. Can't proceed.\n");
		exit(EXIT_FAILURE);
	}

	/* Note VIDIOC_S_FMT may change width and height. */
	width = fmt.fmt.pix.width;
	fprintf(stderr,"Image width set to %i by device %s.\n", width, deviceName);
	height = fmt.fmt.pix.height;
	fprintf(stderr,"Image height set to %i by device %s.\n", height, deviceName);

  	/* If the user has set the fps to -1, don't try to set the frame interval */
    CLEAR(frameint);

    /* Attempt to set the frame interval. */
    frameint.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
    frameint.parm.capture.timeperframe.numerator = 1;
    frameint.parm.capture.timeperframe.denominator = fps;
    if (-1 == xioctl(fd, VIDIOC_S_PARM, &frameint))
      fprintf(stderr,"Unable to set frame interval.\n");

	/* Buggy driver paranoia. */
	min = fmt.fmt.pix.width * 2;
	if (fmt.fmt.pix.bytesperline < min)
		fmt.fmt.pix.bytesperline = min;
	min = fmt.fmt.pix.bytesperline * fmt.fmt.pix.height;
	if (fmt.fmt.pix.sizeimage < min)
		fmt.fmt.pix.sizeimage = min;

	mmapInit();

}

static void deviceUninit(void)
{
	unsigned int i;
	for (i = 0; i < n_buffers; ++i)
		if (-1 == v4l2_munmap(buffers[i].start, buffers[i].length))
			errno_exit("munmap");
	free(buffers);
}

/**
	close device
*/
static void deviceClose(void)
{
	if (-1 == v4l2_close(fd))
		errno_exit("close");

	fd = -1;
}

/**
	open device
**/
static void deviceOpen(void)
{
	struct stat st;

	// stat file
	if (-1 == stat(deviceName, &st)) {
		fprintf(stderr, "Cannot identify '%s': %d, %s\n", deviceName, errno, strerror(errno));
		exit(EXIT_FAILURE);
	}

	// check if its device
	if (!S_ISCHR(st.st_mode)) {
		fprintf(stderr, "%s is no device\n", deviceName);
		exit(EXIT_FAILURE);
	}

	// open device
	fd = v4l2_open(deviceName, O_RDWR /* required */ | O_NONBLOCK, 0);

	// check if opening was successfull
	if (-1 == fd) {
		fprintf(stderr, "Cannot open '%s': %d, %s\n", deviceName, errno, strerror(errno));
		exit(EXIT_FAILURE);
	}
}

/**
	stop capturing
*/
static void captureStop(void)
{
	enum v4l2_buf_type type;
	type = V4L2_BUF_TYPE_VIDEO_CAPTURE;

	if (-1 == xioctl(fd, VIDIOC_STREAMOFF, &type))
		errno_exit("VIDIOC_STREAMOFF");
}

/**
  start capturing
*/
static void captureStart(void)
{
	unsigned int i;
	enum v4l2_buf_type type;
	for (i = 0; i < n_buffers; ++i) {
		struct v4l2_buffer buf;

		CLEAR(buf);

		buf.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
		buf.memory = V4L2_MEMORY_MMAP;
		buf.index = i;

		if (-1 == xioctl(fd, VIDIOC_QBUF, &buf))
			errno_exit("VIDIOC_QBUF");
		}

	type = V4L2_BUF_TYPE_VIDEO_CAPTURE;

	if (-1 == xioctl(fd, VIDIOC_STREAMON, &type))
		errno_exit("VIDIOC_STREAMON");

}

/**
	process image read
*/
static void imageProcess(const void* p, struct timeval timestamp, int cli)
{
	//timestamp.tv_sec
	//timestamp.tv_usec
	unsigned char* src = (unsigned char*)p;
	unsigned char* dst = malloc(width*height*3*sizeof(char));

	YUV420toYUV444(width, height, src, dst);

	if(continuous==1)
  {
		static uint32_t img_ind = 0;
		int64_t timestamp_long;
		timestamp_long = timestamp.tv_sec*1e6 + timestamp.tv_usec;
		sprintf(jpegFilename,continuousFilenameFmt,jpegFilenamePart,img_ind++,timestamp_long);

	}

	// write jpeg
	//jpegWrite(dst,jpegFilename);

  // send image via server
  static int sent = 0;
  while (sent < IMAGE_SIZE)
  {
    sent = sent + send(cli, dst, IMAGE_SIZE, 0);
  }

	// free temporary image
	free(dst);
}

/**
	read single frame
*/
static int frameRead(int cli)
{
	struct v4l2_buffer buf;
	CLEAR(buf);

	buf.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
	buf.memory = V4L2_MEMORY_MMAP;

	if (-1 == xioctl(fd, VIDIOC_DQBUF, &buf)) {
		switch (errno) {
			case EAGAIN:
				return 0;

			case EIO:
				// Could ignore EIO, see spec
				// fall through

			default:
				errno_exit("VIDIOC_DQBUF");
		}
	}

	assert(buf.index < n_buffers);

	imageProcess(buffers[buf.index].start,buf.timestamp, cli);

	if (-1 == xioctl(fd, VIDIOC_QBUF, &buf))
		errno_exit("VIDIOC_QBUF");

	return 1;
}


/**
	mainloop: read frames and process them
*/
static void mainLoop(int cli)
{
	int count;
	unsigned int numberOfTimeouts;

	numberOfTimeouts = 0;
	count = 3;

	while (count-- > 0) {
		for (;;) {
			fd_set fds;
			struct timeval tv;
			int r;

			FD_ZERO(&fds);
			FD_SET(fd, &fds);

			/* Timeout. */
			tv.tv_sec = 1;
			tv.tv_usec = 0;

			r = select(fd + 1, &fds, NULL, NULL, &tv);

			if (-1 == r) {
				if (EINTR == errno)
					continue;

				errno_exit("select");
			}

			if (0 == r) {
				if (numberOfTimeouts <= 0) {
					count++;
				} else {
					fprintf(stderr, "select timeout\n");
					exit(EXIT_FAILURE);
				}
			}
			if(continuous == 1) {
				count = 3;
			}

			if (frameRead(cli))
				break;

			/* EAGAIN - continue select loop. */
		}
	}
}

/**
SIGINT interput handler
*/
void StopProcess(int sig_id) {
	printf("stoping continuous capture\n");
	continuous = 0;

}

void InstallSIGINTHandler() {
	struct sigaction sa;
	CLEAR(sa);

	sa.sa_handler = StopProcess;
	if(sigaction(SIGINT, &sa, 0) != 0)
	{
		fprintf(stderr,"could not install SIGINT handler, continuous capture disabled");
		exit(EXIT_FAILURE);
	}
}

/**
Option
**/

static void usage(FILE* fp, int argc, char** argv)
{
	fprintf(fp,
		"Usage: %s [options]\n\n"
		"Options:\n"
		"-h | --help          Print this message\n"
		"-o | --output        JPEG output image is 'image'\n"
		"",
		argv[0]);
	}

static const char short_options [] = "ho:";

static const struct option
long_options [] = {
	{ "help",       no_argument,            NULL,           'h' },
	{ "output",     required_argument,      NULL,           'o' },
	{ 0, 0, 0, 0 }
};

/**
Main
**/


int main(int argc, char **argv)
{

	int max_name_len = snprintf(NULL,0,continuousFilenameFmt,jpegFilename,UINT32_MAX,INT64_MAX);
	jpegFilenamePart = jpegFilename;
	jpegFilename = calloc(max_name_len+1,sizeof(char));
	strcpy(jpegFilename,jpegFilenamePart);


	// open and initialize device
	deviceOpen();
	deviceInit();
	// init server to receive signal
	int clientConnt_rcv = init_server(PORT_RECV, IPOFSERVER1);

	// init server to send images
	int clientConnt_send = init_server(PORT_SEND, IPOFSERVER2);

	InstallSIGINTHandler();


	while(continuous){
		// get flagPhoto from client
		char dataRcv[sizeof(int)];
		int n = recv(clientConnt_rcv, dataRcv, sizeof(dataRcv), 0);
		
		while (n < sizeof(int)) {
		  n += recv(clientConnt_rcv, dataRcv, sizeof(dataRcv), 0);
		}
		
		int flagPhoto = atoi(dataRcv);

		if (flagPhoto == 1) {
		  // start capturing
		  captureStart();

		  // process frames and send to server
		  mainLoop(clientConnt_send);

		  // stop capturing
		  captureStop();
		}
	}

	// close sockets
	close(clientConnt_send);
	close(clientConnt_rcv);

	// close device
	deviceUninit();
	deviceClose();
	exit(EXIT_SUCCESS);

	return 0;
}
