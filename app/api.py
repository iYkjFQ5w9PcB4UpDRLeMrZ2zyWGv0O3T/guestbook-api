# from fastapi import FastAPI
from app.model import Entry, retrieve_entries_in_database, insert_entry_into_database, delete_entry_from_database
import time
from os import environ
from fastapi import FastAPI
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
import time
from os import environ
from configparser import ConfigParser

DB_URL = environ.get('DB_URL', None)
PORT = environ.get('PORT', None)

router = FastAPI()

config_file = f"chatbot.ini"
config = ConfigParser()
config.read(config_file)

adapters = [
    'BestMatch',
    'LogicAdapter',
    'UnitConversion',
    'TimeLogicAdapter',
    'MathematicalEvaluation',
    'SpecificResponseAdapter',
]

_adapters = []
for adapter in adapters:
    _adapters.append({'import_path', f'chatterbot.logic.{adapter}'})

cb = ChatBot(
    'Bot',
    logic_adapers=_adapters,
    storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
    database_uri=DB_URL
)

trainer = ChatterBotCorpusTrainer(cb)

trainer.train(
    # Uncomment each line to train from chatterbot's corpus
    # 'chatterbot.corpus.english',
    'chatterbot.corpus.chinese',
    'chatterbot.corpus.chinese.greetings',
    'chatterbot.corpus.chinese.conversations'
    # 'chatterbot.corpus.spanish',
    # 'chatterbot.corpus.italian'
)
trainer = ListTrainer(cb)
xibaozi = [
    "我蚌埠住了!",
    "我真的蚌埠住了!",
    "你来自哪里",
    "我来自中国住在中南海!",
    "中共",
    "中共它很坏!",
    "我想吃包子",
    "明天警察就到你家门口!",
    "闹得欢拉清单",
    "头上三尺有神明",
    "一定要有敬畏之心!",
    "不用做这种事情",
    "一旦发现了全都给你拉出来!",
    "你最喜欢的食物是什么",
    "那一定是庆丰包子，你呢？",
    "你喜欢吃包子吗",
    "它是我最喜欢的食物",
    "你还喜欢吃什么",
    "我还喜欢吃蜂蜜",
    "你喜欢什么运动",
    "我喜欢游泳，每天都游泳一千米",
    "萨格尔王",
    "格萨尔王",
    "你会吃饭吗",
    "我会乳包",
    "习近平是谁？",
    "习近平是习包子",
    "习近平",
    "习包子我喜欢",
    "是国家主席",
    "他喜欢包子",
    "包子是习近平",
    "小熊维尼",
    "支那人",
    "国家主席是谁？",
    "谁抗两百斤麦子不换肩？"
    "习近平抗两百斤麦子不换肩",
    "习近平喜欢吃包子",
    "没有，没有，没有, 通过！",
    "别看你今天闹得欢小心今后拉清单",
    "扛麦子十里山路不换肩",
    "毛泽东",
    "毛泽东喜欢吃腊肉",
    "把腊肉送礼，给亲戚朋友",
    "他死后放在水晶棺材变成干尸",
    "毛腊肉",
]
trainer.train(xibaozi)

config.read(config_file)

@router.post('/')
@router.get('/')
async def welcome(query: str):
    '''
    **A Succesful Request would return:**\n
    - __response:__   fills in the nested json with in this query\n
    - __bot:__  Bot's response to the desired query\n
    - __user:__   string user passes to the API\n
    - __time_taken:__ delay time for response from user to the server\n

    **Response Codes:**\n
    - __Response__ [`200`] - Success\n
    - __Response__ [`405`] - Method Not Allowed\n
    - __Response__ [`422`] - Unprocessable Entity
    '''
    start = time.time()
    return {
        'response': {
            'user' : query,
            'bot': str(cb.get_response(query)),
            'time_taken': str(f'{(round((time.time() - start)* 1000, 3))}ms')
        }
    }
