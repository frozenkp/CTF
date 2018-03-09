#include"stdio.h"
#include"stdlib.h"


int main(){
  setvbuf(stdout, 0, 2, 0);
  setvbuf(stdin, 0, 2, 0);
  int token = 1234;
  char key[16];

  printf("Welcome !! Challenger ~\n");
  printf("Here is a simple challenge for you.\n");
  printf("Try to find the key to pass :");

  read(0, key, 40);

  if((int)token == 6666){
    printf("wow, That's impossible to touch this token ?!");
    system("/bin/sh");
  }

  return 0;
}
