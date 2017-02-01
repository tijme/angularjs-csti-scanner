#!/usr/bin/env python

from classes.Exploit import Exploit

# Input for 'Exploit' class
# input_url: The website to test/check the exploit on
# input_version: The AngularJS version that the website uses
# use_javascript_engine: If an extra check needs to be done by a JavaScript engine to ensure the payload is really executed
input_url = "http://localhost/angular/vulnerable.php?test1=aa&test2=bb&test3=cc"
input_version = "1.5.5"
use_javascript_engine = True

# Run the actual exploit
exploit = Exploit.get_instance()
result = exploit.is_vulnerable(input_url, input_version, use_javascript_engine)

# Print the result of the exploit
print("Website is vulnerable: \n" + str(result))
