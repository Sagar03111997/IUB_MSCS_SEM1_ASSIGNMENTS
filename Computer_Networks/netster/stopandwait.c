#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netdb.h>
#include <signal.h>
#include <arpa/inet.h>
#include <errno.h>
#define TIMEOUT_MS 30

/*
 *  Here is the starting point for your netster part.3 definitions. Add the 
 *  appropriate comment header as defined in the code formatting guidelines
 */

/* Add function definitions */

typedef struct packet {
  char data[1024];
}
Packet;

typedef struct frame {
  int frame_kind; 
  int sq_no;
  int ack;
  int packetSize;
  Packet packet;
}
Frame;

void getHostEntry(struct hostent * hostentry) {
  if (hostentry == NULL) {
    perror("Get host by name");
    exit(1);
  }
}

void stopandwait_server(char * iface, long port, FILE * fp) {

  int socket_fd;
  int id = 0;
  struct sockaddr_in server_address;
  struct addrinfo hints;
  struct addrinfo * result;
    
  char str_port[1024];
  int connect_interface;
  char buffer1[1024];
  char buffer2[1024];
  bzero(buffer1, 1024);

  Frame frame_receive;
  Frame frame_send; 
  bzero(buffer1, 1024);
  bzero(buffer2, 1024);

  memset( & hints, 0, sizeof(struct addrinfo));
  memset( & server_address, 0, sizeof(server_address));

  hints.ai_family = AF_UNSPEC; 
  hints.ai_socktype = SOCK_DGRAM; 
  hints.ai_flags = AI_PASSIVE; 
  hints.ai_protocol = 0; 
  hints.ai_canonname = NULL;
  hints.ai_addr = NULL;
  hints.ai_next = NULL;

  sprintf(str_port, "%ld", port);
  connect_interface = getaddrinfo(NULL, str_port, & hints, & result);

  if (connect_interface != 0) {
    exit(EXIT_FAILURE);
  }

  socket_fd = socket(result -> ai_family, result -> ai_socktype,
    result -> ai_protocol);

  if (socket_fd < 0) {
        perror("Socket error");
        exit(1);
  }

  int bind_value = bind(socket_fd, result->ai_addr, result-> ai_addrlen);

  if (bind_value < 0) {
      perror("Binding error");
      exit(1);
  }

  socklen_t addr_size;
  addr_size = sizeof(server_address);

  for(;;) {

    int frame_size_here = sizeof(frame_receive);
    printf("Frame size %d\n", frame_size_here);

    int file_receive_size = recvfrom(socket_fd, &frame_receive, sizeof(Frame), 0, (struct sockaddr*) &server_address, &addr_size);
    if(file_receive_size <= 0){
      break;
    }

    if (file_receive_size > 0 && frame_receive.frame_kind == 1 && frame_receive.sq_no == id) {

      printf("Frame Received: %s\n", frame_receive.packet.data);
      memcpy(buffer1,frame_receive.packet.data,frame_receive.packetSize);

      fwrite(buffer1, sizeof(unsigned char), frame_receive.packetSize, fp);
      fflush(fp);

      frame_send.sq_no = 0;
      frame_send.frame_kind = 0;
      frame_send.ack = frame_receive.sq_no + 1;
      sendto(socket_fd, &frame_send, sizeof(frame_send), 0, (struct sockaddr*)&server_address, addr_size);
      printf("Acknowledgement Sent\n");
      
    }

    if(frame_receive.frame_kind == 2){
      printf("File done here as frame kind received is 2\n");
      close(socket_fd);
      fflush(fp);
    }
    
    bzero(buffer1, 1024);
    id++; 
  }

}

void stopandwait_client(char * host, long port, FILE * fp) {

  struct timeval timeout; 
  timeout.tv_usec = TIMEOUT_MS * 1000;     
  timeout.tv_sec = 0;
  
    
  char * IPbuffer;
  struct hostent * host_entry;

  host_entry = gethostbyname(host);
  getHostEntry(host_entry);

  IPbuffer = inet_ntoa( * ((struct in_addr * ) host_entry -> h_addr_list[0]));

  struct addrinfo hints;
  struct addrinfo * result;
  int socket_fd,b;
  char buffer[1024];
  char str_port[1024];
  int connect_interface;
  struct sockaddr_in addr;
  socklen_t length_of_server_address;

  int id = 0;
  Frame frame_send;
  Frame frame_receive;
  int acknowledgement_received = 1;

  memset( & hints, 0, sizeof(struct addrinfo));

  hints.ai_family = AF_UNSPEC; 
  hints.ai_socktype = SOCK_DGRAM;
  hints.ai_flags = AI_PASSIVE; 
  hints.ai_protocol = 0; 
  hints.ai_flags = 0;

  sprintf(str_port, "%ld", port);
  connect_interface = getaddrinfo(host, str_port, & hints, & result);

  if (connect_interface != 0) {
        exit(EXIT_FAILURE);
  }

  socket_fd = socket(result -> ai_family, result -> ai_socktype,
    result -> ai_protocol);

  if (socket_fd < 0) {
        perror("Socket error");
        exit(1);
  }

  int connected = connect(socket_fd, result -> ai_addr, result -> ai_addrlen);
  if (connected == -1) {
    perror("Socket error");
    exit(1);
  }

  memset( & addr, 0, sizeof(addr));
  addr.sin_family = result -> ai_addr -> sa_family;
  addr.sin_port = htons(port);
  addr.sin_addr.s_addr = inet_addr(IPbuffer);
  length_of_server_address = sizeof(addr);
  
  for(;;){
    if(acknowledgement_received == 0){
      printf("Acknowledgement not received. Sending again\n");
      frame_send.sq_no = id;
      frame_send.frame_kind = 1;
      frame_send.ack = 0;
      frame_send.packetSize=b;   
      memcpy(frame_send.packet.data, buffer,1024);
      sendto(socket_fd, &frame_send, sizeof(Frame), 0, (struct sockaddr*)&addr, sizeof(addr));
    }

    b = fread(buffer, 1, sizeof(buffer), fp);
    if(b <= 0){
      break;
    }
    
    
    if(acknowledgement_received == 1){
      frame_send.sq_no = id;
      frame_send.frame_kind = 1;
      frame_send.ack = 0;   
      frame_send.packetSize = b;
      printf("Data from file\n%s",buffer );
      memcpy(frame_send.packet.data, buffer,1024);
      int frame_size_here = sizeof(frame_send);
      printf("Frame size %d\n", frame_size_here);
      sendto(socket_fd, &frame_send, sizeof(Frame), 0, (struct sockaddr*)&addr, sizeof(addr));
      printf("Frame Sent\n");
    }
    if (setsockopt (socket_fd, SOL_SOCKET, SO_RCVTIMEO, &timeout,sizeof timeout) < 0){
      perror("setsockopt failed\n");
    }
        
    int file_receive_size = recvfrom(socket_fd, &frame_receive, sizeof(frame_receive), 0 ,(struct sockaddr*)&addr, &length_of_server_address);
    
    if(file_receive_size > 0 && frame_receive.sq_no == 0 && frame_receive.ack == id+1){
      printf("\nAcknowledgement Received\n");
      acknowledgement_received = 1;
      id++;   
    } else {
      acknowledgement_received = 0;
    } 
    
  }
  frame_send.sq_no = id;
  frame_send.frame_kind = 2;
  frame_send.ack = 0;  
  bzero(buffer, 1024);
  strcpy(frame_send.packet.data, buffer);
  sendto(socket_fd, &frame_send, sizeof(Frame), 0, (struct sockaddr*)&addr, sizeof(addr));
  printf("\nFile done.\n");
  close(socket_fd);
}