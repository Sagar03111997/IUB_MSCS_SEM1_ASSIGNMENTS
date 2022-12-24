#include <stdio.h>
#include <string.h>

void send_http(char* host, char* msg, char* resp, size_t len);


/*
  Implement a program that takes a host, verb, and path and
  prints the contents of the response from the request
  represented by that request.
 */
int main(int argc, char* argv[]) {
  if (argc != 4) {
    printf("Invalid arguments - %s <host> <GET|POST> <path>\n", argv[0]);
    return -1;
  }
  char* host = argv[1];
  char* verb = argv[2];
  char* path = argv[3];
 
 char final_str[4096];
 char space[] = " ";
 char http[] = "HTTP/1.1\r\n";
 char endpoint[] = "\r\n\r\n";
 char hostinitial[] = "Host: ";
 
 strcat(final_str, verb);
 strcat(final_str, space);
 strcat(final_str, path);
 strcat(final_str, space);
 strcat(final_str, http);
 strcat(final_str, hostinitial);
 strcat(final_str, host);
 strcat(final_str, endpoint);
  
 char response[4096];
 send_http(host, final_str, response, 4096);
 printf("%s\n", response);
  
  return 0;
}
