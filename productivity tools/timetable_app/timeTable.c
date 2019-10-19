#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <gtk/gtk.h>
#include <time.h>

FILE *listFile;

int whichDay(){

	time_t curtime = time(NULL);
	struct tm *loctime = localtime(&curtime);
	int y,m,d,weekday;
	
	y = loctime->tm_year + 1900;
	m = loctime->tm_mon + 1;
	d = loctime->tm_mday;
	
	weekday = (d += m<3 ? y-- : y-2, 23*m/9 + d + 4 + y/4 - y/100 + y/400) % 7;

	return weekday;
}


static void activate(GtkApplication *app, gpointer user_data) {
	GtkWidget *window;
	
	window = gtk_application_window_new(app);
	gtk_window_set_title(GTK_WINDOW(window), "Time Table");
	gtk_window_set_default_size(GTK_WINDOW(window), 500, 600);

	char str[100];
 	char days[][10] = {"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"};
	char dayFileName[50];
	FILE *fday;

	GtkWidget *text_view[7];
	GtkTextBuffer *buffer[7];
	GtkTextIter end;
	GtkWidget *label[7];
	GtkWidget *notebook;
	notebook = gtk_notebook_new();
	int i, weekday;
	
	for (i = 0; i < 7; i++){
		buffer[i] = gtk_text_buffer_new(NULL);
//		gtk_text_buffer_set_text(buffer[i], "Hello World", strlen("Hello World"));
		text_view[i] = gtk_text_view_new_with_buffer(buffer[i]);
		gtk_text_view_set_cursor_visible (GTK_TEXT_VIEW (text_view[i]), FALSE);	
		gtk_text_view_set_editable(GTK_TEXT_VIEW(text_view[i]), FALSE);
		fgets(dayFileName, 100, listFile);
		if (dayFileName[strlen(dayFileName) - 1] == '\n'){	
			dayFileName[strlen(dayFileName) - 1] = '\0';
		}
		


		fday = fopen(dayFileName, "r");		
		if (!fday){
			printf("Day file not found\n");
			continue;
		}		
		
		while(fgets(str, 100, fday)){
			gtk_text_buffer_get_end_iter(buffer[i], &end);
			gtk_text_buffer_insert(buffer[i], &end, str, -1);
		}

		label[i] = gtk_label_new(days[i]);
		gtk_notebook_append_page((GtkNotebook *)notebook, text_view[i], label[i]);
		fclose(fday);
	}

	weekday = whichDay();
//-	printf("%d\n", weekday);

	gtk_container_add(GTK_CONTAINER(window), notebook);
// Show 
	gtk_widget_show_all(window);
	gtk_notebook_set_current_page((GtkNotebook *)notebook, weekday);
}

int main(int argc, char **argv) {

	GtkApplication *app;
	int status;

	listFile = fopen("/home/scribbler/.TimeTable/listFile", "r");
	if (!listFile){
		printf("Error opening listFile\n");
		return 1;
	}

	app = gtk_application_new("org.gtk.timetable", G_APPLICATION_FLAGS_NONE);
	g_signal_connect(app, "activate", G_CALLBACK(activate), NULL);
	status = g_application_run(G_APPLICATION(app), argc, argv);
	g_object_unref (app);

	fclose(listFile);

	return status;
}

























