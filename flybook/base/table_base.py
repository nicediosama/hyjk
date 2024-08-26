import re
class Table:
    def __init__(self, url):
        self.parent_type = None
        match = re.search(r"base\/(.*?)\?table=(.*?)&view=(.*)", url)
        if match:
            self.parent_node = match.group(1)
            self.table = match.group(2)
            self.view = match.group(3)
    
    def update_url(self, url):
        match = re.search(r"base\/(.*?)\?table=(.*?)&view=(.*)", url)
        if match:
            self.parent_node = match.group(1)
            self.table = match.group(2)
            self.view = match.group(3)
        else:
            print("FROM: table_base.py | update url error")

        


if __name__=='__main__':
    parent_type = 'bitable_image'
    url = "https://pvca9kku524.feishu.cn/base/DIixbNfRGapT6nsG7p5czpB4nUe?table=tblLxmV6mRr8yz30&view=vewJI9vdRo"
    table = Table(url)
    print(table.parent_type)