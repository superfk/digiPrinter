import json

class Config():
    def getValue(self, key:str) -> str:
        with open('config.json', 'r') as f:
            data = json.load(f)
            return data[key]

cfg = Config()

if __name__=='__main__':
    print(cfg.getValue('ip'))
    print(cfg.getValue('time_format'))
    print(cfg.getValue('decimal'))