#include <fcntl.h>
#include <stdio.h>
#include <string.h>
#include <time.h>

//the file i/o and serial device i/o file descriptors
int fd_db, fd_nl, fd_final;

int database_match();
void get_time_string(char *time_str);

int main()
{
	int ret;
	ret = database_match();
	return ret;
}

int database_match()
{
	int i, eof_nl = 1, eof_db = 1; 	
	char c, name[50], address[50], database[50], time[30], wbuffer[110];

	fd_db = open("database.db", O_RDONLY);
	if (fd_db <= 0)
		return 100;
	fd_nl = open("name_list.db", O_RDONLY);
	if (fd_nl <= 0)
		return 101;
	fd_final = open("final.db", O_CREAT | O_WRONLY | O_TRUNC, 0666);	
	if (fd_final <= 0)
		return 102;


	get_time_string(time);	

	do {

		//get address from name_list
		i = 0;		
		do {
			if ((eof_nl = read(fd_nl, &c, 1)) < 0) {
				fprintf(stderr, "Read error in name_list read(1)\n");
				return 103;
			}
			
			else if(eof_nl == 0)
				break;

			address[i] = c;
			i++;	
		}while(c != '\t');
		address[i - 1] = '\0';	
		
		if (eof_nl == 0)
			break;				

		//get name from name_list
		i = 0;
		do {
			if ((eof_nl = read(fd_nl, &c, 1)) <= 0) {
				fprintf(stderr, "Read error in name_list read(2) %d\n", eof_nl);
				return 104;
			}
			
			name[i] = c;					
			i++;
		}while (c != '\n');
		name[i - 1] = '\0'; 

		do {
			//get database entry from database file
			i = 0;
			do {
				if ((eof_db = read(fd_db, &c, 1)) < 0) {
					fprintf(stderr, "Read error in databaase read\n");
					return 105;
				}
				else if (eof_db == 0){
					lseek(fd_db, 0, SEEK_SET);				
					break;
				}
				database[i] = c;
				i++;
			}while (c != '\n');
			database[i -1] = '\0';
			
			if (eof_db == 0)
				break;
		
			if (!strcmp(address, database)) {
				printf("%s PRESENT\n", name);
				sprintf(wbuffer, "%s\t%s", name, time);
				write(fd_final, wbuffer, strlen(wbuffer));
				lseek(fd_db, 0, SEEK_SET);
				break; 
			}
				

		}while(1);

	}while (1);			
	
	return 106;
}





//get system time and convert it into string (time_str is an output parameter)
void get_time_string(char *time_str)
{
	time_t t;
	char *str;
	
	//get system time
	t = time(NULL);
	//convert to string
	str = ctime(&t);
	//copy to output parameter
	strcpy(time_str, str);

	return;
}





