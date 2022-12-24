#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <sys/socket.h>
#include <signal.h>
#include <errno.h>

int connection = 0;

void chat_server(char * iface, long port, int use_udp) {

  struct  addrinfo hints;
  struct addrinfo * result;
  
  char str_port[256];
  int connect_interface;
  int socket_fd, in ;
  struct sockaddr_in server_address, client_address;
  char buffer1[256];
  char buffer2[256];
  char host_buffer[256];
  char service_buff[256];
  bzero(buffer1, 256);

  hints.ai_family = AF_INET; 

    if (use_udp == 1) {
      hints.ai_socktype = SOCK_DGRAM;
    } else {
      hints.ai_socktype = SOCK_STREAM;
    }

    hints.ai_flags = AI_PASSIVE; 
    hints.ai_protocol = 0; 
    sprintf(str_port, "%ld", port);
    connect_interface = getaddrinfo(iface, str_port, & hints, & result); // Creating an getaddrinfo
  
    if (connect_interface != 0) {
      exit(EXIT_FAILURE);
    }
    socket_fd = socket(result -> ai_family, result -> ai_socktype, result -> ai_protocol);

    if (socket_fd < 0) {
      perror("Socket error");
      exit(1);
    }

  memset( & server_address, 0, sizeof(server_address));
  server_address.sin_family = AF_INET;
  server_address.sin_port = htons(port);
  server_address.sin_addr.s_addr = htonl(INADDR_ANY);

  int bind_value = bind(socket_fd, result->ai_addr, result-> ai_addrlen);

  if (bind_value < 0) {
    perror("Binding error");
    exit(1);
  }

  socklen_t n = result-> ai_addrlen;

  if (use_udp == 1) {

    for(;;) {

      bzero(buffer2, 256);
      bzero(buffer1, 256);
      recvfrom(socket_fd, buffer1, sizeof(buffer1), 0, (struct sockaddr * ) & client_address, & n);
      getnameinfo((struct sockaddr * ) & client_address, sizeof(client_address), host_buffer, sizeof(host_buffer), service_buff, sizeof(service_buff), NI_NUMERICHOST | NI_NUMERICSERV);
      printf("got message from ('%s', %s)\n", host_buffer, service_buff);

      if (strcmp(buffer1, "hello\n") == 0) {

        strcpy(buffer2, "world\n");
        sendto(socket_fd, buffer2, strlen(buffer2), 0, (struct sockaddr * ) & client_address, n);
        bzero(buffer1, 256);
        bzero(buffer2, 256);

      } else if (strcmp(buffer1, "goodbye\n") == 0) {

        strcpy(buffer2, "farewell\n");
        sendto(socket_fd, buffer2, strlen(buffer2), 0, (struct sockaddr * ) & client_address, n);
        bzero(buffer1, 256);
        bzero(buffer2, 256);

      } else if (strcmp(buffer1, "exit\n") == 0) {

        strcpy(buffer2, "ok\n");
        sendto(socket_fd, buffer2, strlen(buffer2), 0, (struct sockaddr * ) & client_address, n);
        exit(0);

      } else {

        sendto(socket_fd, buffer1, sizeof(buffer1), 0, (struct sockaddr * ) & client_address, n);
        bzero(buffer1, 256);
      }

    }

  } else {

    socklen_t n1 = sizeof(server_address);
    listen(socket_fd, 10);

    while (( in = accept(socket_fd, (struct sockaddr * ) & server_address, & n1)) > 0) {

      getnameinfo((struct sockaddr * ) & server_address, sizeof(server_address), host_buffer, sizeof(host_buffer), service_buff, sizeof(service_buff), NI_NUMERICHOST | NI_NUMERICSERV);
      printf("connection %d from ('%s', %s)\n",connection++ ,host_buffer,service_buff);
      int childpid, n;

      if ((childpid = fork()) == 0) {
        close(socket_fd);

        //Clear Zeroes
        bzero(buffer1, 256);
        bzero(buffer2, 256);

        while ((n = recv( in , buffer1, 256, 0)) > 0) {

          getnameinfo((struct sockaddr * ) & server_address, sizeof(server_address), host_buffer, sizeof(host_buffer), service_buff, sizeof(service_buff), NI_NUMERICHOST | NI_NUMERICSERV);
          printf("got message from ('%s', %s) \n", host_buffer, service_buff);

          if (strcmp(buffer1, "hello\n") == 0) {

            strcpy(buffer2, "world\n");
            send( in , buffer2, strlen(buffer2), 0);
            bzero(buffer1, 256);

          } else if (strcmp(buffer1, "goodbye\n") == 0) {

            strcpy(buffer2, "farewell\n");
            send( in , buffer2, strlen(buffer2), 0);

          } else if (strcmp(buffer1, "exit\n") == 0) {

            strcpy(buffer2, "ok\n");
            send( in , buffer2, strlen(buffer2), 0);
            kill(childpid, SIGINT);

          } else {

            send( in , buffer1, strlen(buffer1), 0);
            bzero(buffer1, 256);
          }

          bzero(buffer1, 256);
          bzero(buffer2, 256);

        }
        close( in );
        exit(0);
      }

    }
  }

}

void chat_client(char * host, long port, int use_udp) {

  struct addrinfo hints;
  struct addrinfo * result;
  int sock, in ;
  struct sockaddr_in addr;
  char buffer[256];
  char buffer1[256];
  char str_port[256];
  int connect_interface;
  socklen_t length_of_server_address;

  memset( & hints, 0, sizeof(struct addrinfo));

  hints.ai_family = AF_INET; /* Allow IPv4 or IPv6 */
  if (use_udp == 1) {
    hints.ai_socktype = SOCK_DGRAM;
  } else {
    hints.ai_socktype = SOCK_STREAM;
  }

  hints.ai_flags = AI_PASSIVE; 
  hints.ai_protocol = 0; 
  sprintf(str_port, "%ld", port);
  connect_interface = getaddrinfo(host, str_port, & hints, & result);

  if (connect_interface != 0) {
    exit(EXIT_FAILURE);
  }
  sock = socket(result -> ai_family, result -> ai_socktype, result -> ai_protocol);

  if (sock < 0) {
    perror("[-]Socket error");
    exit(1);
  }

  if (use_udp == 1) {

    for(;;) {

      memset(buffer1, 0, 256);    
      memset( & addr, 0, sizeof(addr));
      addr.sin_family = result -> ai_addr -> sa_family;
      addr.sin_port = htons(port);
      addr.sin_addr.s_addr = INADDR_ANY;
      length_of_server_address = sizeof(addr);

      if (strlen(fgets(buffer1, 255, stdin)) == 0) {
        perror("Error!");
      }
      
      sendto(sock, buffer1, sizeof(buffer1), 0, (struct sockaddr * ) & addr, length_of_server_address);
      recvfrom(sock, buffer, sizeof(buffer), 0, (struct sockaddr * ) & addr, & length_of_server_address);
      //printf("%s", buffer);

      if (strcmp(buffer, "farewell\n") == 0) {
        exit(0);
      }
      if (strcmp(buffer, "ok\n") == 0) {
        exit(0);
      }
     bzero(buffer1, 256);
    }

  } else {
    if (connect(sock, result -> ai_addr, result -> ai_addrlen) < 0) {
      perror("Connect Error\n");
    }
    for(;;) {

      bzero(buffer, 256);

      if (strlen(fgets(buffer, 255, stdin)) == 0) {
        perror("Error!");
      }
      
      in = send(sock, buffer, strlen(buffer), 0);

      if ( in < 0) {
        perror("\nClient Error: Writing to Server");
      }

      bzero(buffer, 256); in = recv(sock, buffer, 255, 0);

      if ( in < 0) {
        perror("\nClient Error: Reading from Server");
      }
      printf("%s", buffer);

      if (strcmp(buffer, "farewell\n") == 0) {
        exit(0);
      }
      if (strcmp(buffer, "ok\n") == 0) {
        exit(0);
      }
    }
    freeaddrinfo(result);
  }

}