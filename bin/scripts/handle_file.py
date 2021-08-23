import os


def handle_file(noheader, append, outfile):
    header = "utime,load,speed\n"
    if not append:
        try:
            os.remove(outfile)
            if not noheader:
                with open(outfile) as f:
                    f.write(header)
        except Exception as e:
            print(e, " continuing...\n")
            if not noheader:
                with open(outfile) as f:
                    f.write(header)
