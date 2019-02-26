#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <signal.h>
#include <time.h>

//static unsigned int IMAGE_SIZE = 921600;
static unsigned int PORT_SEND = 15556;
static unsigned int PORT_RECV = 15555;
static struct sockaddr_in IPOFSERVER1;
static struct sockaddr_in IPOFSERVER2;


int init_server(int PORT, struct sockaddr_in ipOfServer)
{
	int clintListn = 0, clintConnt = 0;
	clintListn = socket(AF_INET, SOCK_STREAM, 0); // connection oriented TCP protocol
	if (clintListn == -1)
	{
		printf("Could not create socket");
	}
	// memset(&ipOfServer, '0', sizeof(ipOfServer)); // fills the struct with zeros
	// memset(dataSending, '0', sizeof(dataSending)); // fills the variable with zeros
	ipOfServer.sin_family = AF_INET; // designation of the adress type for communication ipV4
	ipOfServer.sin_addr.s_addr = INADDR_ANY; //htonl(ADDR); // convertion to address byte order
	ipOfServer.sin_port = htons( PORT ); // convertion to address byte order

	if ( bind(clintListn, (struct sockaddr*)&ipOfServer, sizeof(ipOfServer)) < 0 )
	{
	   perror("bind failed. Error");
	   return 1;
	}
	listen(clintListn, 20);

	printf("Waiting for connection on port %d...\n", PORT);
	clintConnt = accept(clintListn, (struct sockaddr*)NULL, NULL); // accept connexion with client
	if (clintConnt < 0)
	{
	perror("accept failed.");
	return 1;
	}
	printf("Connection established on port %d...\n", PORT);

  return clintConnt;
}

void signals_handler(int signal_number)
{
    printf("\n Signal catched.\n");
    exit(EXIT_FAILURE);
}

int main(int argc , char *argv[]){
	// init server to receive signal
	int clintConnt_rcv = init_server(PORT_RECV, IPOFSERVER1);

	// init server to send images
  	int clintConnt_send = init_server(PORT_SEND, IPOFSERVER2);

  	while(1) {
		usleep(50);
		printf("Loop...\n");
  		// get flagPhoto from client
	        char dataRcv[sizeof(int)];
	        recv(clintConnt_rcv, dataRcv, sizeof(dataRcv), 0);
	        int flagPhoto = atoi(dataRcv);

		if (flagPhoto) {
			printf("Calling the library...");
	        	// use of system to call directly the library
	       		system("./v4l2grab -o image.jpg");

	        	FILE *picture;
			char buffer[1];
			int size;

			picture = fopen("image.jpg", "r");
			fseek(picture, 0, SEEK_END);
        		size = ftell(picture);
			printf("%d\n", size);

			send(clintConnt_send, &size, sizeof(size), 0);
			usleep(2000);
	        	//Return to the beginning of the picture
			fseek(picture, 0, SEEK_SET);
 			while(!feof(picture)) {
           			 //Reading a byte of the picture, and sending it through the socket
            			 fread(buffer, 1, sizeof(buffer), picture);
          			 send(clintConnt_send, buffer, sizeof(char), 0);
            			bzero(buffer, sizeof(char));
			}

		fclose(picture);
		}

	}

}
