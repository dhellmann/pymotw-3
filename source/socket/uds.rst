=====================
 Unix Domain Sockets
=====================

From the programmer's perspective there are two essential differences
between using a Unix domain socket and an TCP/IP socket.  First, the
address of the socket is a path on the file system, rather than a tuple
containing the server name and port.  Second, the node created in the
file system to represent the socket persists after the socket is
closed, and needs to be removed each time the server starts up.  The
echo server example from earlier can be updated to use UDS by making a
few changes in the setup section.

.. literalinclude:: socket_echo_server_uds.py
   :lines: 10-21

The :class:`socket` needs to be created with address family
:const:`AF_UNIX`.

.. literalinclude:: socket_echo_server_uds.py
   :lines: 23-24

Binding the socket and managing the incoming connections works the
same as with TCP/IP sockets.

.. literalinclude:: socket_echo_server_uds.py
   :lines: 26-

The client setup also needs to be modified to work with UDS.  It
should assume the file system node for the socket exists, since the
server creates it by binding to the address.

.. literalinclude:: socket_echo_client_uds.py
   :lines: 10-23

Sending and receiving data works the same way in the UDS client as the
TCP/IP client from before.

.. literalinclude:: socket_echo_client_uds.py
   :lines: 25-

The program output is mostly the same, with appropriate updates for
the address information.  The server shows the messages received and
sent back to the client.

::

    $ python ./socket_echo_server_uds.py 

    starting up on ./uds_socket
    waiting for a connection
    connection from 
    received "This is the mess"
    sending data back to the client
    received "age.  It will be"
    sending data back to the client
    received " repeated."
    sending data back to the client
    received ""
    no data from 
    waiting for a connection

The client sends the message all at once, and receives parts of it
back incrementally.

::

    $ python socket_echo_client_uds.py 

    connecting to ./uds_socket
    sending "This is the message.  It will be repeated."
    received "This is the mess"
    received "age.  It will be"
    received " repeated."
    closing socket

Permissions
===========

Since the UDS socket is represented by a node on the file system,
standard file system permissions can be used to control access to the
server.

::

    $ ls -l ./uds_socket

    srwxr-xr-x  1 dhellmann  dhellmann  0 Sep 20 08:24 ./uds_socket
    
    $ sudo chown root ./uds_socket
    
    $ ls -l ./uds_socket

    srwxr-xr-x  1 root  dhellmann  0 Sep 20 08:24 ./uds_socket

Running the client as a user other than ``root`` now results in an
error because the process does not have permission to open the socket.

::

    $ python socket_echo_client_uds.py 
    
    connecting to ./uds_socket
    [Errno 13] Permission denied

Communication Between Parent and Child Processes
================================================

The :func:`socketpair` function is useful for setting up UDS sockets
for inter-process communication under Unix.  It creates a pair of
connected sockets that can be used to communicate between a parent
process and a child process after the child is forked.

.. literalinclude:: socket_socketpair.py
   :caption:
   :start-after: #end_pymotw_header

By default, a UDS socket is created, but the caller can also pass
address family, socket type, and even protocol options to control how
the sockets are created.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'socket_socketpair.py'))
.. }}}

::

	$ python socket_socketpair.py

	in child, waiting for message
	message from parent: ping
	in parent, sending message
	response from child: pong

.. {{{end}}}
