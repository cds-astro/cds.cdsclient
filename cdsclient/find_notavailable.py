#!/usr/bin/env python
"""G.Landais (CDS) 24-mar-2018
   Query urat1_neighbourhood

   find_notavailable.py [-h] [-a] [-r radius] [-m max] [constraints] [--format=tsv|votable|ascii] [position]
            
     -a: display all columns
     -r: radius in arcsec
     -m: max number of lines in output
     -h: this help
     --format: output (--format=tsv|votable|ascii)
     --sort  : sort by distance (available with position only)
     --add   : column name in output
     --file  : query with a list

     position : ra dec position or target name
                example: find_notavailable.py M1

     Other constraints:
		--sort : ...
		--add= : ...
		--file= : ...


     Example: 

     Licensed under a BSD license - see LICENSE.txt for details

"""

import os, sys
import getopt
try:
    sys.path.append(os.path.split(os.path.abspath(sys.argv[0]))[0])
    import vizquery
except:
    sys.stderr.write("(error) needs vizquery.py in PYTHONPATH\n")
    sys.exit(1)

if int(sys.version[0])<3:
    from urllib2 import quote
else:
    from urllib.parse import quote

NO_FORMAT = "noformat"

class QueryCat():
    def __init__(self):
        self.position = None
        self.radius = vizquery.DEFAULT_RADIUS
        self.format = None

    def query_cat(self, constraints=None, all = False, limit=vizquery.DEFAULT_LIMIT):
        """init constraints parameters
        :param constraints: list of constraints ((name,value), ...)
        :param all: display all columns(efault False)
        :param limit: max number of records
        """
        pass

    def get(self):
        """get astropy table"""
        pass

    def print_stdout(self):
        """print the result on stdout"""
        pass


class QueryCatVizieR(QueryCat):
    def __init__(self):
        QueryCat.__init__(self)
        self.__client = vizquery.CDSClient(default_format=vizquery.FORMAT_ASCII)
        self.limit = vizquery.DEFAULT_LIMIT

    def query_cat(self, constraints=None, all=False, limit=vizquery.DEFAULT_LIMIT, columns=None, filename=None):
        params = []

        if self.position:
            params.append("-c={0}".format(quote(self.position)))

        if self.radius:
            params.append("-c.rs={0:f}".format(self.radius))

        if all is True:
            params.append("-out.all=1")

        if limit is not None:
            params.append("-out.max={0:d}".format(limit))
        else:
            params.append("-out.max={0:d}".format(self.limit))

        if columns is not None:
            for column in columns: params.append("-out={0}".format(column))

        file_col = None
        if constraints is not None:
            for constraint in constraints:
                if constraint[1] == "" or constraint[1] == "-":
                    file_col = constraint[0]
                params.append("{0}={1}".format(constraint[0], constraint[1].replace("+","%2B")))

        if filename is not None:
            #params.append("-out.form=hori")
            #params.append("-out.add=_1")

            if file_col is not None:
                params.append("-sort={0}".format(file_col))
            else:
                params.append("-out.add=_r")
                params.append("-sort=_r")

        self.__client.query("urat1_neighbourhood", params=params, filename=filename)

        if self.format is not None:
            self.__client.format = self.format

    def get(self):
        return self.__client.get()

    def print_stdout(self):
        return self.__client.print_stdout()



if __name__ == "__main__":

    __radius = vizquery.DEFAULT_RADIUS
    __position = None
    __limit = None
    __mime = vizquery.FORMAT_ASCII
    __noformat = False
    __ipix = None
    __all = False
    __sort = False
    __add = None
    __filename = None
    __constraints = []


    __options = ('help','format=','sort','add=','file=')
    try :
        __opts, __args = getopt.getopt(sys.argv[1:], 'har:m:f:', __options)
    except:
        help("__main__")
        sys.exit(1)

    for __o, __a in __opts:
        if __o in ("-h", "--help"):
            help("__main__")
            sys.exit(1)

        elif __o == "-r":
            try:
                __radius = float(__a)
            except:
                sys.stderr.write("(error) wrong radius format\n")

        elif __o == "-m":
            try:
                __limit = int(__a)
            except:
                sys.stderr.write("(error) wrong limit/max format\n")

        elif __o == "-a":
            __all = True

        elif __o == "--format":
            __mime = __a

        elif __o == "--no-format":
            __noformat = True

        elif __o == "--ipix":
            __ipix = __a

        elif __o == "--count":
            __count = True

        elif __o == "--sort":
            __sort = True
            __constraints.append(("-out.add", "_r"))
            __constraints.append(("-sort", "_r"))

        elif __o == "--add":
            if __add is None: __add = []
            __add.append(__a)

        if __o in ("-f", "--file"):
            __filename = __a

        else:
            for opt in __options[2:]:
                value = opt[:len(opt)-1]
                if __o[2:] == value:
                     __constraints.append((value, __a))
                     break

    for __arg in __args:
        if __position is None:
            __position = __arg
        else:
            __position += " "+ __arg

    if __noformat is True or __ipix is not None:
        if __sort is True :
            raise Exception("--sort function is not compatible with --ipix/--no-format")
        if __filename is not None:
            raise Exception("--file option is not compatible with --ipix/--no-format")

        __querycat = QueryCatClient()
        if __ipix is not None:
            __querycat.set_healpix(__ipix)
        __querycat.noformat=__noformat

    else:
        __querycat = QueryCatVizieR()


    __querycat.position = __position
    __querycat.radius = __radius

    if __mime in (vizquery.FORMAT_TSV, vizquery.FORMAT_VOTABLE, vizquery.FORMAT_ASCII):
        __querycat.format = __mime
    else:
        raise Exception("format not yet available")

    __querycat.query_cat(constraints=__constraints, all=__all, limit=__limit, columns=__add, filename=__filename)
    __querycat.print_stdout()

