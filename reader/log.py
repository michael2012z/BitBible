def log(message, new_log=False):
    flag = "at"
    if new_log:
        flag = "wt"
    else:
        flag = "at"
    log_file = open("debug.log", flag)
    log_file.write(str(message))
    log_file.write('\n')
    log_file.close()

