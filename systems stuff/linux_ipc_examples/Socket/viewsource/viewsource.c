#include "head.h"

int main (int argc, char* argv[])
{
	int status, sockfd, count, mark, len1, len2, match;
	char rss_feed [512];
	struct addrinfo hints;
	struct addrinfo *res, *p;
	char buffer[1024];
	char checktag[30];

	struct sockaddr_in* ipa;
	char ip4[INET_ADDRSTRLEN];
			
	if (argc < 3) {
		printf("error. Usage ./rss [hostname] [pagename] \n");
		return 5;
	}
	strcpy(rss_feed, argv[1]);
		
	//prepare addrinfo object
	memset (&hints, 0, sizeof(hints));	
	hints.ai_family = AF_INET;
	hints.ai_socktype = SOCK_STREAM;
	
	printf("preparing...\n");
	if ((status = getaddrinfo(rss_feed, "http", &hints, &res)) != 0) {
		fprintf(stderr, "getaddrinfo() : %s\n", gai_strerror(status));
		return 1;
	} 

	
	for (p = res; p != NULL; p = p->ai_next) {
		if (p->ai_family == AF_INET) {
			ipa = (struct sockaddr_in *) p->ai_addr;
			inet_ntop(p->ai_family, &(ipa->sin_addr), ip4, INET_ADDRSTRLEN);
			printf ("IP ADDRESS :	%s\n",ip4);
		}
	}

	
	printf ("creating path...\n");
	sockfd = socket(res->ai_family, res->ai_socktype, res->ai_protocol);
	if (sockfd < 0) {
		perror("socket()");
		return 2;
	}

	printf ("connecting...\n");
	if (connect(sockfd, res->ai_addr, res->ai_addrlen) < 0) {
		perror("connect()");
		return 3;
	}

	printf("requesting...\n");
	sprintf(buffer, "GET %s%s HTTP/1.0\r\n",argv[1], argv[2]);
	if ((count = write(sockfd, buffer, strlen(buffer))) < 0) {
		perror("write()");
		return 4;
	}
	
	memset (buffer, 0, sizeof(buffer));
	printf ("downloading...\n");
	
	strcmp(checktag, "</html>");
	len2 = strlen(checktag);

	while((count = read(sockfd, buffer, len2)) > 0 ) 
		printf("%s", buffer);
	
	
	printf("\nclosing connection...\n");
	close (sockfd);
	freeaddrinfo (res);
	return 0;
}
