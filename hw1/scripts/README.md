# Information Security and Privacy - Homework 1

These instructions are meant to briefly explain how to run the scripts for exercise 3, 4 and 5 of homework 1.

## Getting Started

A Docker installation and configuration as described in the homework handout is necessary in order to run the scripts of exercise 3 and 4. For exercise 5, it is necessary to use the virtual machine provided for the task. See homework instructions and repository for more details. 

## Exercise 3 and 4

Once everything is set up, you can run the following command to start the container generator with my personal email address:

```
sh run_dockers_new.sh andrea.piccione@epfl.ch
```

### Exercise 3

The secret and personal token was obtained by creating and running a personal script: 

```
docker exec -it attacker python3 shared/interceptor_ex3.py
```

The script basically analyzes the traffic, modify the shipping address of the target and sends the request to the server with the modified address. The server answers back with my token.

Use CTRL + C to stop the traffic inspection once you received the token. 

### Exercise 4

The secret and personal token was obtained by creating and running a personal script: 

```
docker exec -it attacker python3 shared/interceptor_ex4.py
```

The script basically analyzes the traffic, finds the secrets according to the specifications given and, once got all the 5 unique secrets, it sends a request to the server with the secrets found. The server answers back with my token.

Use CTRL + C to stop the traffic inspection once you received the token. 

## Exercise 5

First, untar the tar file and move all the scripts in a folder (for example, "sploits"). Make sure to:

* run "make" inside the "sploits" folder in order to compile and generate the executables for sploits 1, 2 and 3
* run "make" and "make install" (and eventually "sudo make setuid") in the "target" directory to install the target binaries (see homework instructions for details).

Then, you can just execute the sploits in the "sploits" folder by running one of the sploits, for example:

```
./sploits1
```

and eventually get the shell in all three cases.

