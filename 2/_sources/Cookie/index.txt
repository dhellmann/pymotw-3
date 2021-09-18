======================
Cookie -- HTTP Cookies
======================

.. module:: Cookie
    :synopsis: Working with HTTP cookies from the server side.

:Purpose: The Cookie module defines classes for parsing and creating HTTP cookie headers.
:Available In: 2.1 and later

Cookies have been a part of the HTTP protocol for a long time. All of the
modern web development frameworks provide easy access to cookies so a
programmer almost never has to worry about how to format them or make sure the
headers are sent properly. It can be instructive to understand how cookies
work, though, and the options they support.

The Cookie module implements a parser for cookies that is mostly :rfc:`2109`
compliant. It is a little less strict than the standard because MSIE 3.0x does
not support the entire standard.

Creating and Setting a Cookie
=============================

Cookies are used as state management, and as such as usually set by the server
to be stored and returned by the client. The most trivial example of creating
a cookie looks something like:

.. include:: Cookie_setheaders.py
    :literal:
    :start-after: #end_pymotw_header

The output is a valid Set-Cookie header ready to be passed to the client as
part of the HTTP response:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'Cookie_setheaders.py'))
.. }}}

::

	$ python Cookie_setheaders.py
	
	Set-Cookie: mycookie=cookie_value

.. {{{end}}}


Morsels
=======

It is also possible to control the other aspects of a cookie, such as the
expiration, path, and domain. In fact, all of the RFC attributes for cookies
can be managed through the Morsel object representing the cookie value.

.. include:: Cookie_Morsel.py
    :literal:
    :start-after: #end_pymotw_header

The above example includes two different methods for setting stored cookies
that expire. You can set max-age to a number of seconds, or expires to a date
and time when the cookie should be discarded.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'Cookie_Morsel.py'))
.. }}}

::

	$ python Cookie_Morsel.py
	
	Set-Cookie: encoded_value_cookie="\"cookie_value\""; Comment=Notice that this cookie value has escaped quotes
	Set-Cookie: expires_at_time=cookie_value; expires=Sat, 14 Feb 2009 19:30:14
	Set-Cookie: restricted_cookie=cookie_value; Domain=PyMOTW; Path=/sub/path; secure
	Set-Cookie: with_max_age="expires in 5 minutes"; Max-Age=300
	
	key = restricted_cookie
	  value = cookie_value
	  coded_value = cookie_value
	  domain = PyMOTW
	  secure = True
	  path = /sub/path
	
	key = with_max_age
	  value = expires in 5 minutes
	  coded_value = "expires in 5 minutes"
	  max-age = 300
	
	key = encoded_value_cookie
	  value = "cookie_value"
	  coded_value = "\"cookie_value\""
	  comment = Notice that this cookie value has escaped quotes
	
	key = expires_at_time
	  value = cookie_value
	  coded_value = cookie_value
	  expires = Sat, 14 Feb 2009 19:30:14

.. {{{end}}}


Both the Cookie and Morsel objects act like dictionaries. The Morsel responds
to a fixed set of keys:

- expires
- path
- comment
- domain
- max-age
- secure
- version

The keys for the Cookie instance are the names of the individual cookies being
stored. That information is also available from the key attribute of the
Morsel.

Encoded Values
==============

The cookie header may require values to be encoded so they can be parsed
properly. 

.. include:: Cookie_coded_value.py
    :literal:
    :start-after: #end_pymotw_header

The Morsel.value is always the decoded value of the cookie, while
Morsel.coded_value is always the representation to be used for transmitting
the value to the client. Both values are always strings. Values saved to a
cookie that are not strings are converted automatically.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'Cookie_coded_value.py'))
.. }}}

::

	$ python Cookie_coded_value.py
	
	integer
	  Set-Cookie: integer=5
	  value=5 <type 'str'>
	  coded_value=5
	
	string_with_quotes
	  Set-Cookie: string_with_quotes="He said\054 \"Hello\054 World!\""
	  value=He said, "Hello, World!" <type 'str'>
	  coded_value="He said\054 \"Hello\054 World!\""
	

.. {{{end}}}

Receiving and Parsing Cookie Headers
====================================

Once the Set-Cookie headers are received by the client, it will return those
cookies to the server on subsequent requests using the Cookie header. The
incoming header will look like::

    Cookie: integer=5; string_with_quotes="He said, \"Hello, World!\""

Depending on your web server and framework, the cookies are either
available directly from the headers or the ``HTTP_COOKIE`` environment
variable. To decode them, pass the string without the header prefix to
the SimpleCookie when instantiating it, or use the load() method.

.. include:: Cookie_parse.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'Cookie_parse.py'))
.. }}}

::

	$ python Cookie_parse.py
	
	From constructor:
	Set-Cookie: integer=5
	Set-Cookie: string_with_quotes="He said, \"Hello, World!\""
	
	From load():
	Set-Cookie: integer=5
	Set-Cookie: string_with_quotes="He said, \"Hello, World!\""

.. {{{end}}}

Alternative Output Formats
==========================

Besides using the Set-Cookie header, it is possible to use JavaScript to add
cookies to a client. SimpleCookie and Morsel provide JavaScript output via the
js_output() method.

.. include:: Cookie_js_output.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'Cookie_js_output.py'))
.. }}}

::

	$ python Cookie_js_output.py
	
	
	        <script type="text/javascript">
	        <!-- begin hiding
	        document.cookie = "another_cookie=\"second value\"";
	        // end hiding -->
	        </script>
	        
	        <script type="text/javascript">
	        <!-- begin hiding
	        document.cookie = "mycookie=cookie_value";
	        // end hiding -->
	        </script>
	        

.. {{{end}}}


Deprecated Classes
==================

All of these examples have used SimpleCookie. The Cookie module also provides
2 other classes, SerialCookie and SmartCookie. SerialCookie can handle any
values that can be pickled. SmartCookie figures out whether a value needs to
be unpickled or if it is a simple value. Since both of these classes use
pickles, they are potential security holes in your application and you should
not use them. It is safer to store state on the server, and give the client a
session key instead.

.. seealso::

    `Cookie <http://docs.python.org/2.7/library/cookie.html>`_
        The standard library documentation for this module.

    :mod:`cookielib`
        The :mod:`cookielib` module, for working with cookies on the client-side.

    :rfc:`2109`
        HTTP State Management Mechanism
