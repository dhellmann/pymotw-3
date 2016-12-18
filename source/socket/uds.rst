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

The ``socket`` needs to be created with address family
``AF_UNIX``. Binding the socket and managing the incoming
connections works the same as with TCP/IP sockets.

.. literalinclude:: socket_echo_server_uds.py
   :caption:
   :start-after: #end_pymotw_header

The client setup also needs to be modified to work with UDS.  It
should assume the file system node for the socket exists, since the
server creates it by binding to the address.  Sending and receiving
data works the same way in the UDS client as the TCP/IP client from
before.

.. literalinclude:: socket_echo_client_uds.py
   :caption:
   :start-after: #end_pymotw_header

The program output is mostly the same, with appropriate updates for
the address information.  The server shows the messages received and
sent back to the client.

.. NOT RUNNING

.. code-block:: none

   $ python3 socket_echo_server_uds.py
   starting up on ./uds_socket
   waiting for a connection
   connection from
   received b'This is the mess'
   sending data back to the client
   received b'age.  It will be'
   sending data back to the client
   received b' repeated.'
   sending data back to the client
   received b''
   no data from
   waiting for a connection

The client sends the message all at once, and receives parts of it
back incrementally.

.. NOT RUNNING

.. code-block:: none

   $ python3 socket_echo_client_uds.py
   connecting to ./uds_socket
   sending b'This is the message.  It will be repeated.'
   received b'This is the mess'
   received b'age.  It will be'
   received b' repeated.'
   closing socket

Permissions
===========

Since the UDS socket is represented by a node on the file system,
standard file system permissions can be used to control access to the
server.

.. NOT RUNNING

.. code-block:: none

    $ ls -l ./uds_socket

    srwxr-xr-x  1 dhellmann  dhellmann  0 Aug 21 11:19 uds_socket
    
    $ sudo chown root ./uds_socket
    
    $ ls -l ./uds_socket

    srwxr-xr-x  1 root  dhellmann  0 Aug 21 11:19 uds_socket

Running the client as a user other than ``root`` now results in an
error because the process does not have permission to open the socket.

.. NOT RUNNING

.. code-block:: none

    $ python3 socket_echo_client_uds.py 
    
    connecting to ./uds_socket
    [Errno 13] Permission denied

Communication Between Parent and Child Processes
================================================

The ``socketpair()`` function is useful for setting up UDS sockets
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
.. cog.out(run_script(cog.inFile, '-u socket_socketpair.py'))
.. }}}

.. code-block:: none

	$ python3 -u socket_socketpair.py
	
	in parent, sending message
	in child, waiting for message
	message from parent: b'ping'
	response from child: b'pong'

.. {{{end}}}
