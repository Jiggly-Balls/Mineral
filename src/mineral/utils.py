class FileLogger:
    def __init__(self, path: str) -> None:
        self.path = path
        with open(path, "w"): ...
    
    def file_log(self, text: str) -> None:
        with open(self.path, "a") as file:
            file.writelines([text+"\n"])