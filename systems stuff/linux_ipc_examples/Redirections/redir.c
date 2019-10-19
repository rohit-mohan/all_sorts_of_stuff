#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>

int main()
{
	int fdi;
	int fdo;
	int num1, num2;
	
	if ((fdi = open ("infile.txt", O_RDONLY)) < 0) {
		printf ("open failed [1] \n");
		_exit(1);
	}

	if ((fdo = open ("outfile.txt", O_CREAT | O_WRONLY | O_TRUNC, 0666)) < 0) {
		printf ("open failed [2] \n");
		_exit(2);
	}

	close (0);
	dup (fdi);
	close (1);
	dup (fdo);

	scanf ("%d%d", &num1, &num2);
	printf ("%d\n", num1+num2);

	return 0;
}
