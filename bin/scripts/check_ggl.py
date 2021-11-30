import multiprocessing
import requests as r
import time
  
def ping_svr(host):
    """
    using the request module, do an http get on a url
    """
    data = r.get(url=host)
    print(f"{data.status_code}: {host}\t{data.elapsed.total_seconds()}")

def main():
    # creating processes
    start = time.time()
    p1 = multiprocessing.Process(target=ping_svr, args=("https://mail.google.com", ))
    p2 = multiprocessing.Process(target=ping_svr, args=("https://youtube.com", ))
    p3 = multiprocessing.Process(target=ping_svr, args=("https://drive.google.com", ))
    p4 = multiprocessing.Process(target=ping_svr, args=("https://photos.google.com", ))
    p5 = multiprocessing.Process(target=ping_svr, args=("https://docs.google.com", ))
    # start the threads
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()

    # join here does not mean concat as we would typically assume, instead it means:
    # wait for a thread to complete
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()

    # how long did the test take
    total = (time.time() - start)

    # print results
    print(f"completed, took {total} seconds")


if __name__ == "__main__":
    main()
