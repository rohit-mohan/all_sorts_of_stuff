CC=gcc
CF=-c
SOURCE=shellshock.c redirections.c tokens.c sigchld_handler.c 
OBJ=$(SOURCE:.c=.o)
TARGET=shellshock

all : begin $(TARGET) end

$(TARGET) : $(OBJ)
	@$(CC) -ggdb3 $(OBJ) -o $(TARGET)

$(OBJ):%.o : %.c
	@$(CC) $(CF) $< 

begin :
	@echo begining execution

end :
	@echo execution complete. $(TARGET) created 

clean : 
	@rm -f $(OBJ) $(TARGET)
	@rm -f .*.*.swp
	@rm -f *.*~

.PHONY : clean
