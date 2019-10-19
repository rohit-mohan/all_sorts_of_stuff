#pragma comment(lib, "Ws2_32.lib")


#include <process.h>
#include <windows.h>
#include <stdio.h>


#define SERVER_PORT 5001
#define SERVER_ADDR "127.0.0.1"

#define TIME  10000
#define MAX_MSG_LEN 1024

SOCKET sock;
SOCKADDR_IN addr;
volatile double  count = 0;
volatile int flag = 0;

DWORD WINAPI threadSock(LPVOID args)
{
	int wr_len = 0, err = 0;
	char str[MAX_MSG_LEN] = {48};
	wr_len = strlen(str);

	printf("Inside tx thread\n");

	while (flag == 0) {
		err = send(sock, str, MAX_MSG_LEN, 0);
		count = count + err;
		if (err == SOCKET_ERROR) {
			printf("Connection Terminated by remote host!\n");
			break;
		}
//		printf("bytes sent : %d\n", err);
	}

	shutdown(sock, 0);
	closesocket(sock);
	printf("Exiting socket tx thread\n");
}

int main(void)
{
	int time_factor = 1;
	HANDLE h;
	DWORD exitStatus;
	LPWSADATA lpWSAData = (LPWSADATA)malloc(1 * sizeof(WSADATA));

	printf("Started main function\n");

	/****************************************************************************************/
	// Initialize socket functionalites

	if (WSAStartup(0x0202, lpWSAData)) {
		printf("Error in initializing Winsock\n");
		return 2;
	}

	if ((sock = socket(PF_INET, SOCK_STREAM, 0)) == INVALID_SOCKET) {
		printf("Error in initializing socket\n");
		return 3;
	}

	memset(&addr, 0, sizeof(SOCKADDR_IN));
	addr.sin_family = AF_INET;
	addr.sin_addr.s_addr = inet_addr(SERVER_ADDR);
	addr.sin_port = htons(SERVER_PORT);

	if (connect(sock, (const struct sockaddr *)&addr, sizeof(SOCKADDR_IN)) == SOCKET_ERROR) {
		printf("Error in connecting to server\n");
		return 4;
	}

	count = 0;
	/****************************************************************************************/
	// Starting new thread for socket reception

	if (!(h = (HANDLE)_beginthreadex(NULL, 0, (_beginthreadex_proc_type)threadSock, NULL, 0, NULL))) {
		printf("Error creating thread\n");
		return 5;
	}

	printf("Created socket receiver thread\n");

	/****************************************************************************************/

	// Thread clean-up functions and count display
	time_factor = TIME / 1000;
	WaitForSingleObject(h, TIME);
	flag = 1;
	printf("Time Up\n");
	CloseHandle(h);

	printf("Packet tx rate: %f Mb/s \n", (count* 8) / (time_factor * 1000000));
	printf("Successful exit!\n");
	getchar();
	return 0;
}
