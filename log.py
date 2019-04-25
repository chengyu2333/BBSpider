import io
import time
import os
import sys


if not os.path.exists("logs"):
    os.makedirs("logs")


def log_error(msg):
    f = io.open("logs/" + time.strftime("%Y-%m-%d", time.localtime()) + " errors.log", 'a', encoding="utf-8")
    log = time.ctime() + " | \t" + msg + "\r\n\n"
    # print("\033[1;31m" + str(log) + "\033[0m")
    sys.stdout.write("\033[1;31m" + str(log) + "\033[0m")
    f.write(log)
    f.close()


def log_info(msg):
    f = io.open("logs/" + time.strftime("%Y-%m-%d", time.localtime()) + " info.log", 'a', encoding="utf-8")
    log = time.ctime() + " | \t" + msg + "\r\n\n"
    # print("\033[1;33m" + str(log) + "\033[0m")
    sys.stdout.write("\033[1;32m" + str(log) + "\033[0m")
    f.write(log)
    f.close()


def log_success(msg):
    f = io.open("logs/" + time.strftime("%Y-%m-%d", time.localtime()) + " success.log", 'a', encoding="utf-8")
    log = time.ctime() + " | \t" + msg + "\r\n\n"
    # print("\033[1;33m" + str(log) + "\033[0m")
    sys.stdout.write("\033[1;33m" + str(log) + "\033[0m")
    f.write(log)
    f.close()
