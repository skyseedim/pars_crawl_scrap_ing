from pymongo import MongoClient


class JobparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.vacansy


    def process_item(self, item, spider):
        collection = self.mongobase['Job_Seeker']
        collection.insert_one(item)
        return item
