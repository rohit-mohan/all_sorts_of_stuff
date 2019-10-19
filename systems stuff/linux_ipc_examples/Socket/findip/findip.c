#include "head.h"

int main (int argc, char* argv[])
{
	struct addrinfo hints, *res, *p;
	struct sockaddr_in* ipa;
	char ip4[INET_ADDRSTRLEN]; 
	int status;
//	char hostname[128];
//	char portnum [16];
	
	if (argc < 2) {
		printf ("Usage : findip [hostname] \n");
		return 1;		
	}

	memset (&hints, 0, sizeof (hints)); 
	hints.ai_family = AF_INET;
	hints.ai_socktype = SOCK_STREAM;

	if ((status = getaddrinfo (argv[1], NULL, &hints, &res)) != 0) {
		fprintf (stderr, "getaddrinfo() : %s\n", gai_strerror(status));
		return 2;
	} 
	
	printf ("connecting...\n");

	for (p = res; p != NULL; p = p->ai_next) {
		if (p->ai_family == AF_INET) {
			ipa = (struct sockaddr_in *) p->ai_addr;
			inet_ntop(p->ai_family, &(ipa->sin_addr), ip4, INET_ADDRSTRLEN);
			printf ("IP ADDRESS :	%s\n",ip4);
		}
	}

	freeaddrinfo(res);
		
	return 0;
}
