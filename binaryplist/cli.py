# Copyright (c) 2015, Per Rovegard <per@rovegard.se>
# Licensed under the 3-clause BSD license.
# See the LICENSE file for details.

import click
import os
import sys
from binplist import *

def dump(obj, format):
    if 'plist' == (format or 'plist'):
        from plistlib import writePlist
        writePlist(obj, sys.stdout)
    elif 'json' == format:
        import json
        from plistlib import Data
        class DataEncoder(json.JSONEncoder):
            def default(self,obj):
                if isinstance(obj,Data):
                    return obj.asBase64()
                return json.JSONEncoder.default(self,obj)
        s = json.dumps(obj, indent=2, cls=DataEncoder)
        print(s)


@click.command()
@click.version_option()
@click.option('--format', type=click.Choice(['plist', 'json']))
@click.argument('filename', type=click.Path(exists=True))
def run(filename, format):
    with open(filename, 'rb') as fd:
        try:
            root = read_binary_plist(fd) 
            dump(root, format)
        except PListFormatError as e:
            click.echo("Format error: %s" % (e.message, ), err=True)
        except PListUnhandledError as e:
            click.echo("Unhandled: %s" % (e.message, ), err=True)
