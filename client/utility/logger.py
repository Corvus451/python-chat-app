class Logger:
    def __init__(self, log_path: str):
        self.__log_path = log_path

    def log(self, log: str):
        with open(self.__log_path, "a") as file:
            file.write(f"{log}\n")

    

