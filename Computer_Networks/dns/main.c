#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netdb.h>
#include <errno.h>
#include <arpa/inet.h>

/*
  Use the `getaddrinfo` and `inet_ntop` functions to convert a string host and
  integer port into a string dotted ip address and port.
 */
int main(int argc, char* argv[]) {
  if (argc != 3) {
    printf("Invalid arguments - %s <host> <port>", argv[0]);
    return -1;
  }
  char* host = argv[1];
  char* port = argv[2];

  struct addrinfo hints;
  char output_address[INET6_ADDRSTRLEN];
  struct addrinfo *result, *resultantpointer;
  int output;

  hints.ai_family = AF_UNSPEC;
  hints.ai_socktype = SOCK_STREAM;
  hints.ai_flags = AI_PASSIVE;
  hints.ai_protocol = IPPROTO_TCP;

  output =  getaddrinfo(host, port, &hints, &result);

  if (output != 0) {
  	exit(EXIT_FAILURE);
  }
  else {
  
    for(resultantpointer = result; resultantpointer != NULL; resultantpointer = resultantpointer -> ai_next) {
        if (resultantpointer -> ai_family == AF_INET6) {
                inet_ntop(AF_INET6, &((struct sockaddr_in6 *)resultantpointer -> ai_addr) -> sin6_addr, output_address, sizeof(output_address));
                printf("IPv6 %s\n", output_address);
        }
        else
        {
                inet_ntop(AF_INET, &((struct sockaddr_in *)resultantpointer -> ai_addr) -> sin_addr, output_address, sizeof(output_address));
                printf("IPv4 %s\n", output_address);
        } 
     }
  }
  return 0;
}
