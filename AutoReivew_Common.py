#################################################

class Export_Report():
    def __init__(self, report_name, report_content):
        self.name = report_name
        self.txt_file = open(self.name, "w")
        self.getcontent(report_content)

    def getcontent(self, content_list):
        self.content = content_list[:]
        self.out()

    def out(self):
        for subcontent in self.content:
            print(subcontent)
            self.txt_file.write(subcontent)
        self.close_file()

    def close_file(self):
        self.txt_file.close()
        del self
        
        
#################################################


