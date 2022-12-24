#include <arpa/inet.h>
#include <fcntl.h>
#include <string.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <unistd.h>
#include <getopt.h>
#include <netdb.h>
#include <netinet/in.h>
#include <stdio.h>
#include <errno.h>
#include <signal.h>
#include <pthread.h>
#define TIMEOUT_MS 400

typedef struct packet {
  char packet[256];
}
Packet;

typedef struct data             
{
  int frame_kind;                  
  int sq_no;               
  int packetSize;
  int ack;
  Packet packet;
} Data;

void gbn_server(char* iface, long port, FILE* fp) {
    int socket_fd;
    int connect_interface;
    int opt = 1;
    int sequenceNumber = 0;
    int byteReceived = 0;
    char str_port[256]; 
    struct addrinfo *resultAddr = NULL; 
    struct addrinfo hints;               
    memset(&hints, 0, sizeof(struct addrinfo));
    
    hints.ai_family = AF_UNSPEC;                    
    hints.ai_protocol = 0;                          
    hints.ai_flags = AI_PASSIVE;                   
    hints.ai_socktype = SOCK_DGRAM;  

    sprintf(str_port, "%ld", port);   

    connect_interface = getaddrinfo(iface, str_port, &hints, &resultAddr);
    if (connect_interface != 0) {
      exit(1);
    }

    socket_fd = socket(resultAddr->ai_family, resultAddr->ai_socktype, resultAddr->ai_protocol);   
        
    if(socket_fd < 0) {                                     
      perror("Socket Error");
      exit(1);
    }

    if(setsockopt(socket_fd, SOL_SOCKET ,SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt))<0){   
      perror("Setsockopt Error");
      exit(1);
    }

    int bind_value = bind(socket_fd, resultAddr->ai_addr, resultAddr->ai_addrlen);
    if (bind_value < 0) {
      perror("Binding Error");
      exit(1);
    }

    socklen_t lenAddr = sizeof(resultAddr);
    Data ackPacket, dataPacket;
	  ackPacket.frame_kind = 1;

    while((byteReceived = recvfrom(socket_fd, &dataPacket, sizeof(dataPacket), 0, resultAddr->ai_addr, &lenAddr)) > 0){                       
      if(dataPacket.sq_no == sequenceNumber && dataPacket.frame_kind != 0) {                                                                                                                                                              
          fwrite(dataPacket.packet.packet, 1, dataPacket.packetSize, fp);
          ackPacket.sq_no = sequenceNumber;
          sendto(socket_fd, &ackPacket, sizeof(ackPacket), 0, resultAddr->ai_addr, resultAddr->ai_addrlen);                                 
          sequenceNumber += 1;
          bzero(dataPacket.packet.packet, 256);
          close(socket_fd);
          break;
        } 
      else if(dataPacket.sq_no == sequenceNumber && dataPacket.frame_kind >= 0) { 
        fwrite(dataPacket.packet.packet, 1, dataPacket.packetSize, fp);                                                
        ackPacket.sq_no = sequenceNumber;
        sequenceNumber += 1;                                                     
        sendto(socket_fd, &ackPacket, sizeof(ackPacket), 0, resultAddr->ai_addr, resultAddr->ai_addrlen);
        bzero(dataPacket.packet.packet, 256);
      }
    }  
    close(socket_fd);
}

void gbn_client(char* host, long port, FILE* fp) {
    int socket_fd;
    int connect_interface;
    char str_port[256]; 
    int byteReceived;
    int sequenceNumber = 0;
    int l = 0, m = 0, pack = 0;
    int temp = 256, congestionFlag = 0;
    
    struct addrinfo *resultAddr = NULL; 
    struct addrinfo hints;               
    memset(&hints, 0, sizeof(struct addrinfo));

    hints.ai_family = AF_UNSPEC;                    
    hints.ai_protocol = 0;                          
    hints.ai_flags = AI_PASSIVE;                   
    hints.ai_socktype = SOCK_DGRAM;                
    
    sprintf(str_port, "%ld", port); 

    connect_interface = getaddrinfo(host, str_port, &hints, &resultAddr);
    if (connect_interface != 0) {
        perror("Connection Error");
        exit(1);
    }

    socket_fd = socket(resultAddr->ai_family, resultAddr->ai_socktype, resultAddr->ai_protocol);   
        
    if(socket_fd < 0){                                                        
        perror("Socket error");
        exit(1);
    }

    struct timeval timer;                                                
    timer.tv_sec = 0;
    timer.tv_usec = TIMEOUT_MS;
    socklen_t lenAddr = sizeof(resultAddr);                                  

    Data ackPacket[256], dataPacket[256];                                         
	  Data buffer;
    
    int WINDOWSIZE = 2;                                                                                                               

    if(setsockopt(socket_fd, SOL_SOCKET, SO_RCVTIMEO, (char *)&timer, sizeof(struct timeval))<0){      
        perror("Setsockopt Error");
        exit(1);
    }

    while(pack < WINDOWSIZE){                                                   
	    bzero(dataPacket[pack].packet.packet, 256);
      temp = fread(dataPacket[pack].packet.packet, 1, 256, fp);                   \
	    dataPacket[pack].frame_kind=0;

	    if(temp < 256)                                                         
	      dataPacket[pack].frame_kind = 1;    
        dataPacket[pack].packetSize = temp;                                       
        dataPacket[pack].sq_no = sequenceNumber;

	    ackPacket[pack].frame_kind = 1;                                                     
	    ackPacket[pack].sq_no = sequenceNumber;
	    ackPacket[pack].ack = 0;
      sequenceNumber += 1;
	    pack += 1;

	    if(temp < 256) {
          break;
      }
    }

    while(temp == 256){                                                       
      pack = 0;
      while(pack < WINDOWSIZE){                                               
          sendto(socket_fd, &dataPacket[pack], sizeof(dataPacket[pack]), 0, resultAddr->ai_addr, resultAddr->ai_addrlen);
          pack += 1;
      }

      pack = 0;
      while(pack < WINDOWSIZE){                                               
        byteReceived = recvfrom(socket_fd, &buffer, sizeof(buffer), 0, resultAddr->ai_addr, &lenAddr);
        if(byteReceived > 0) {

          for(l=0; l < WINDOWSIZE; l++) {
            if(ackPacket[l].sq_no == buffer.sq_no)
              ackPacket[l].ack=1;
            }
          }
        pack += 1;
      }
      
      for(l = 0; l < WINDOWSIZE; l++) {                                         
        if(ackPacket[l].ack == 0)
        congestionFlag = 1;
      }

      if(congestionFlag == 0){                                                  
        WINDOWSIZE += 1;
        temp = fread(dataPacket[WINDOWSIZE-1].packet.packet, 1, 256, fp);     
        dataPacket[WINDOWSIZE-1].frame_kind = 0;
        dataPacket[WINDOWSIZE-1].packetSize = temp;
        dataPacket[WINDOWSIZE-1].sq_no = sequenceNumber;
        ackPacket[WINDOWSIZE-1].frame_kind = 1;                                    
        ackPacket[WINDOWSIZE-1].sq_no = sequenceNumber;
        ackPacket[WINDOWSIZE-1].ack = 0;
        sequenceNumber += 1;
      }
      congestionFlag = 0;
      pack = 0;

      for(;;){                                                           
        if(ackPacket[0].ack==1){
          for(l=0, m = 1; l < WINDOWSIZE && m < WINDOWSIZE; l++, m++){
            dataPacket[l] = dataPacket[m];
            ackPacket[l] = ackPacket[m];
          }

          if(temp < 256){                                               
            dataPacket[WINDOWSIZE-1].frame_kind = 1;
            break;
          }

          bzero(dataPacket[WINDOWSIZE-1].packet.packet, 256);
          temp = fread(dataPacket[WINDOWSIZE-1].packet.packet, 1, 256, fp); 
          dataPacket[WINDOWSIZE - 1].frame_kind = 0;
          dataPacket[WINDOWSIZE - 1].packetSize = temp;
          dataPacket[WINDOWSIZE - 1].sq_no = sequenceNumber;

          ackPacket[WINDOWSIZE - 1].frame_kind = 1;                                
          ackPacket[WINDOWSIZE - 1].sq_no = sequenceNumber;
          ackPacket[WINDOWSIZE - 1].ack = 0;
          sequenceNumber += 1;

          if(temp < 256){                                             
            dataPacket[WINDOWSIZE-1].frame_kind = 1;
            break;
          }
        }
        else {
          break;
        }
          
      }
	}

    while(ackPacket[WINDOWSIZE-1].ack != 1){                               
		
        pack = 0;
        while(pack < WINDOWSIZE){                                               
            sendto(socket_fd, &dataPacket[pack], sizeof(dataPacket[pack]), 0, resultAddr->ai_addr, resultAddr->ai_addrlen);
            pack += 1;
        }

        pack = 0;
        while(pack < WINDOWSIZE){                                               
		    byteReceived = recvfrom(socket_fd, &buffer, sizeof(buffer), 0, resultAddr->ai_addr, &lenAddr);
            if(byteReceived > 0){
              for(l = 0; l < WINDOWSIZE; l++) {
                if(ackPacket[l].sq_no == buffer.sq_no)
                ackPacket[l].ack = 1;
              }
            }
            pack += 1;
        }                
	}
	close(socket_fd);
}
