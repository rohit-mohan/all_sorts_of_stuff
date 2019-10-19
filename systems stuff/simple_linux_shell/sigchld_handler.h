#ifndef SIGCHLD_HANDLER_H
#define SIGCHLD_H_HANDLER_H

#include <stdio.h>
#include <unistd.h>
#include <signal.h>

void sigchld_handler(int snum, siginfo_t* si, void* parameters);

#endif /*SIGCHLD_HANDLER_H*/
