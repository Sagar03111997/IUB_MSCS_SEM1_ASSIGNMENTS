#include <stdio.h>
#include <string.h>

int connect_smtp(const char* host, int port);
void send_smtp(int sock, const char* msg, char* resp, size_t len);



/*
  Use the provided 'connect_smtp' and 'send_smtp' functions
  to connect to the "lunar.open.sice.indian.edu" smtp relay
  and send the commands to write emails as described in the
  assignment wiki.
 */
int main(int argc, char* argv[]) {
  if (argc != 3) {
    printf("Invalid arguments - %s <email-to> <email-filepath>", argv[0]);
    return -1;
  }

  char* rcpt = argv[1];
  char* filepath = argv[2];
  char message[4096];
  char response[4096];
  char show_content[4096];
  char temp[100];

  int socket = connect_smtp("lunar.open.sice.indiana.edu", 25);

  send_smtp(socket, "HELO iu.edu\n", response, 4096);
  printf("%s\n", response);
  strcat(message,"MAIL FROM: ");
  strcat(message,rcpt);
  strcat(message,"\r\n");
  send_smtp(socket, message, response, 4096);
  printf("%s\n", response);
  bzero(message, 4096);
  bzero(response, 4096);

  strcat(message,"RCPT TO: ");
  strcat(message,rcpt);
  strcat(message,"\r\n");
  send_smtp(socket, message, response, 4096);
  printf("%s\n", response);
  bzero(message, 4096);
  bzero(response, 4096);

  strcat(message,"DATA\n");
  send_smtp(socket, message, response, 4096);
  printf("%s\n", response);
  bzero(message, 4096);
  bzero(response, 4096);

  bzero(show_content, 4096);
  bzero(temp, 100);

  FILE* fp = fopen(filepath,"r");
  if( NULL != fp)
  {
   
   while(fgets(temp, 100, fp)) {
      strcat(show_content,temp);
   }
 }

  strcat(message,show_content);
  strcat(message,"\r\n");
  strcat(message,".");
  strcat(message,"\r\n");

  send_smtp(socket,message, response, 4096);
  printf("%s\n", response);

  send_smtp(socket,"QUIT\r\n", response, 4096);

  return 0;
}
