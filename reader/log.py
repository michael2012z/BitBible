def log(message):
    log_file = open("debug.log", "at")
    log_file.write(str(message))
    log_file.write('\n')
    log_file.close()

