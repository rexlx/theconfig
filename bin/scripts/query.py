import argparse
import time
from pymongo import MongoClient
import sysplotter as sp


def make_plot(i):
    """
    an example of how to call make_oned_plot(). takes one parameter, i
    where i is the interval you want to step by. this assumes data was
    collected in one second intervals. 1 is plot every one second, 10
    is plot every 10 seconds

    your_function(5)
    """
    data = {'xlabel': 'string', 'ylabel': 'string', 'title': 'string',
            'line_lbl': 'string', 'line_clr': '#4286F4',
            'outfile': 'string.png'}
    # make some numbers
    cpu_speed = [e ** 2 for e in range(0, 200) if e % 22 == 0]
    # just did this to illustrate how to slice string / array
    x = cpu_speed[0::i]
    sp.make_oned_plot(data, x, dark=True)


def parse_results(args, _type_, cursor):
    data = {'xlabel': 'string', 'ylabel': 'string', 'title': 'string',
            'line_lbl': 'string', 'line_clr': '#4286F4',
            'outfile': 'string.png'}
    if _type_ == "cpu_stats":
        x = []
        for i in cursor:
            x.append(i["stats"][0])
        sp.make_oned_plot(data, x, dark=True)
    elif _type_ == "disk_stats":
        for i in cursor:
            # print(str(i["time"]) + ":")
            for key in i["stats"].keys():
                stats = ",".join([str(e) for e in i["stats"][key].values()])
                line = str(i["time"]) + "," + stats
                print(line)
    elif _type_ == "mem_stats":
        x = []
        # header = "utime,total,used,free,buff,cache,slab,swap\n"
        for i in cursor:
            x.append(i["stats"]["cache"] / (1024 ** 2))
            # x.append(i["stats"]["free"] / (1024 ** 2))
            """KEEP-->line = str(i["time"]) + ","
            line += ",".join([str(i["stats"][e.strip()])
                             for e in header.split(",")[1:]])
            print(line)<--KEEP"""
        sp.make_oned_plot(data, x, dark=True)
        
    else:
        print("received unsupported db type")
        exit()


def main():
    msg = "query mongodb for stats"
    parser = argparse.ArgumentParser(description=msg)
    parser.add_argument('-u', dest='url', required=False)
    parser.add_argument('-q', dest='query', required=False) # TODO DELETE(?)
    parser.add_argument(
                        '--time-minus',
                        dest='timeM',
                        type=int,
                        required=False,
                        metavar="unixtime",
                        nargs="+"
                        )
    parser.add_argument(
                        '--time-plus',
                        dest='timeP',
                        type=int,
                        required=False,
                        metavar="unixtime",
                        nargs="+"
                        )
    parser.add_argument(
                        '--time-range',
                        dest='timeR',
                        type=int,
                        required=False,
                        metavar="unixtime_start unixtime_end",
                        nargs="+"
                        )
    parser.add_argument(
                        '--threshold',
                        dest='threshold',
                        required=False,
                        metavar="unixtime",
                        nargs="+"
                        )
    parser.add_argument(
                        '--dump-all',
                        dest='dump',
                        required=False,
                        action='store_true'
                        )
    parser.add_argument(
                        '--showid',
                        dest='id',
                        required=False,
                        action='store_true'
                        )
    parser.add_argument(
                        '--get-size',
                        dest='get_size',
                        required=False,
                        action='store_true'
                        )
    parser.add_argument(
                        '--csv',
                        dest='csv',
                        required=False,
                        action='store_true'
                        )
    parser.add_argument(
                        '--json',
                        dest='json',
                        required=False,
                        action='store_true'
                        )
    parser.add_argument(
                        '--plot',
                        dest='plot',
                        required=False,
                        action='store_true'
                        )
    args = parser.parse_args()
    if args.url:
        url = args.url.split("/")
        base_url = "/".join(url[0:3])
        if len(url) > 4:
            dbase = url[3]
            coll = url[4]
        else:
            example = "mongodb://ADDR/DB_NAME/COLLECTION_NAME"
            print("exptected a url in the format: {}, got: {}".format(example,
                                                                      args.url
                                                                      ))
            exit()
    else:
        print("no url was supplied...")
        exit()
    if args.query:
        query = args.query
        # print(query)
    else:
        print("received no query, exiting...")
        exit()
    if args.timeM:
        # start the first [0] arg (unixtime) minus the second [1] arg
        # which is the time to subtract by
        start = args.timeM[0] - args.timeM[1]
        # end is the supplied unixtime
        end = args.timeM[0]
        # build the query dict
        query = {"time":{"$gt": start, "$lt": end}}
    elif args.timeP:
        # start the first [0] arg (unixtime) minus the second [1] arg
        # which is the time to subtract by
        start = args.timeP[0]
        # end is the supplied unixtime
        end = args.timeP[0]  + args.timeP[1]
        # build the query dict
        query = {"time":{"$gt": start, "$lt": end}}
    elif args.timeR:
        query = {"time":{"$gt": args.timeR[0], "$lt": args.timeR[1]}}
    elif args.threshold:
        ok = "TODO"
    # print(base_url, dbase, coll)
    client = MongoClient(base_url)
    db = client[dbase]
    col = db[coll]

    """
likely safe to remove
    # print(client, db, col)
    # cursor = col.find()
    # for i in col.find():
    #     print(i)
    # cond = time.time() - 28800
    # print(cond)
    # cursor = col.find({"stats":{"$gt": 15.0}})
    """

    cursor = col.find(query,{ "_id": 0})
    parse_results(args, dbase, cursor)
    # cursor = col.find({"time":{"$gt": cond}})
    with open("results.txt", "a") as f:
        for i in cursor:
            for k, v in i.items():
                line = "{}: {}\n".format(k, v)
            #stats = ",".join([str(e) for e in i["stats"]])
            #line = "{},{}\n".format(str(i["time"]), stats)
                f.write(line)

if __name__ == "__main__":
    main()
