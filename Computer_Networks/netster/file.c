#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <sys/socket.h>
#include <signal.h>
#include <errno.h>
#include <getopt.h>
#include "file.h"

void file_server(char* iface, long port, int use_udp, FILE* fp) {

    int socket_fd, i, bytes;
    struct sockaddr_in server_address;
    struct addrinfo hints;
    struct addrinfo * result;
    
    char str_port[1024];
    int connect_interface;
    char buffer1[1024];
    char buffer2[1024];
    bzero(buffer1, 256);

    hints.ai_family = 0; 

        if (use_udp == 1) {
        hints.ai_socktype = SOCK_DGRAM;
        } else {
        hints.ai_socktype = SOCK_STREAM;
        }

        hints.ai_flags = AI_PASSIVE; 
        hints.ai_protocol = IPPROTO_TCP; 
        sprintf(str_port, "%ld", port);
        connect_interface = getaddrinfo(iface, str_port, & hints, & result);

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
            int n1, n2;

            bzero(buffer2, 256);
            bzero(buffer1, 256);
            recvfrom(socket_fd, &n2, sizeof(n2), 0, (struct sockaddr * ) &server_address, & n);
            printf("%d\n", n2);

            while(n2 > 0) {
                n = sizeof(server_address);
                n1 = recvfrom(socket_fd, buffer1, sizeof(buffer1), 0, (struct sockaddr * ) &server_address, & n);

                if (n1 == 0) {
                    perror("Socket Closed\n");
                    close(socket_fd);
                    break;
                }

                fwrite(buffer1, sizeof(unsigned char), n1, fp);
                n2 = n2 - n1;
            }

            close(socket_fd);
            exit(0);

        } else {
            socklen_t n1 = sizeof(server_address);
            int data_acc = 0;
            listen(socket_fd, 10);

            while (!feof(fp)) {
                data_acc = accept(socket_fd, (struct sockaddr * ) & server_address, & n1);

                if (data_acc == -1) {
                    continue;
                }
                bytes = 0;
                if (fp != NULL) {
                    while ((i = recv(data_acc, buffer2, sizeof(buffer2), 0)) > 0)
                    {
                        bytes += 1;
                        fwrite(buffer2, 1, i, fp);

                        printf("Bytes received: %d\n", bytes);
                        if (i < 0) {
                            fclose(fp);
                        }
                    } 
                } else {
                    perror("File Error");
                }
                close(data_acc);
                exit(0);
            }
        }
}

void file_client(char* host, long port, int use_udp, FILE* fp) {

    struct addrinfo hints;
    struct addrinfo * result;
    int sock, i;
    struct sockaddr_in addr;
    char buffer[1024];
    char buffer1[1024];
    char str_port[1024];
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
        perror("Socket error");
        exit(1);
    }

    if (use_udp == 1) {
        memset(buffer1, 0, 1024);    
        memset( & addr, 0, sizeof(addr));
        addr.sin_family = result -> ai_addr -> sa_family;
        addr.sin_port = htons(port);
        addr.sin_addr.s_addr = INADDR_ANY;
        length_of_server_address = sizeof(addr);
        long result = ftell(fp);
        int x;
        fseek(fp, 0L, SEEK_END);
        sendto(sock, &result , sizeof(result), 0, (struct sockaddr *) &addr, length_of_server_address);
        fseek(fp, 0, SEEK_SET);

        while((i = fread(buffer, 1, sizeof(buffer), fp)) > 0) {
            x = sendto(sock, buffer, i, 0, (struct sockaddr *) & addr, length_of_server_address);
            if (x == -1) {
                perror("Error sending data to server");
                exit(1);
            }
            bzero(buffer, 1024);
        }
        close(sock);

    }else {
        if (connect(sock, result -> ai_addr, result -> ai_addrlen) < 0) {
            perror("Connect Error\n");
        }
        if (fp == NULL) {
            exit(1);
        }

        while((i = fread(buffer, 1, sizeof(buffer), fp)) > 0) {
            send(sock, buffer, i, 0);
        }
        printf("Data Transfer Complete\n");
        close(sock);

    }

  
}
