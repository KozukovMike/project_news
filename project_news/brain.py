import pandas as pd
import pymorphy3

from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from apscheduler.schedulers.background import BackgroundScheduler
from normalize import df_where_word_in
from charts import Chart
from sentiment_analysis import SentimentAnalysis
from db import DynamoDBClient


app = FastAPI()
scheduler = BackgroundScheduler()
morph = pymorphy3.MorphAnalyzer()

df = pd.DataFrame()
df_norm = pd.DataFrame()

words = {}
df_where_word = {}
number = {}


def read_from_db():
    global df, df_norm
    df = DynamoDBClient.get_from_db('News')
    df_norm = DynamoDBClient.get_from_db('NormalizedNews')


@app.on_event("startup")
def start_scheduler():
    read_from_db()
    scheduler.add_job(read_from_db, 'interval', days=1)
    scheduler.start()


@app.on_event("shutdown")
def shutdown_scheduler():
    scheduler.shutdown()


@app.get("/")
async def read_root():
    return {"success": True,
            "message": df.to_dict(),
            "message1": df_norm.to_dict(),
            }


@app.post("/start")
def start(data: dict):
    text = f'Здравствуйте, {data["first_name"].capitalize()} {data["last_name"].capitalize()}! ' \
           f'напишите команду *project* для информации о проектах ' \
           f'напишите команду *info* для информации о командах ' \
           f'вы можете воспользоваться кнопками в меню'
    return {'status': 'success', 'message': text}


@app.post("/project")
def project(data: dict):
    pass


@app.post("/info")
def info(data: dict):
    text = 'команда *initialization* позволит вам начать работу бота\n' \
           'все последующие команды без предыдущей не работают!!!\n\n' \
           'команда news высылает файл формата txt со всеми новостями, имеющие искомое слово\n\n' \
           'команда *send_pdf1* высылает pdf file с графиком, который показывает сколько' \
           'новостей с вашим словом и в каких категориях эти новости\n\n' \
           'команда *send_pdf2* высылает pdf file с 3 графиками, в которых ' \
           'показаны самые часто упоминаемые знаменитый лица, географические объекты и большие компании\n\n' \
           'команда *sent_analysis* показывает анализ настроения новостей с ващим словом\n\n' \
           'команад *sent_analysis_time* позволяет сделать анализ настроения новостей во времени, ' \
           'подробнее можно узнать вызвав эту команду\n\n'
    return {'status': 'success', 'message': text}


@app.post("/initialization")
def initialization(data: dict):
    word = data['word']
    id_ = data['id']
    if len(word.split()) > 1:
        mes = 'Вы ввели больше одного слова,  к сожалению мы не можем так обработать, чтобы ввести заново слово ' \
              'вызовите команду *initialization*'
        return JSONResponse(status_code=400, content={"error": mes})
    else:
        word_normal = morph.parse(word)[0].normal_form
        df_where_word[id_] = df_where_word_in(df_norm, word_normal)


@app.get("/news/{id_}")
def news(id_: int):
    news = df.loc[df_where_word[id_].index, 'title']
    number[id_] = len(news.index)
    news.to_csv(f'news{id_}.txt', index=False, sep='\t')

    return FileResponse(f'news{id_}.txt')


@app.post('/number')
def get_number(data: dict):
    return {'status': 'success', 'message': number[data['id']]}


@app.get('/send_pdf1/{id_}')
def send_pdf1(id_: int):
    Chart.box_plot_mentions(df_where_word[id_])
    return FileResponse('example.pdf', media_type='application/pdf',
                        filename=f'{id_}.pdf')


@app.get('/send_pdf2/{id_}')
def send_pdf2(id_: int):
    Chart.big_names(df_where_word[id_],  df)
    return FileResponse('example1.pdf', media_type='application/pdf',
                        filename=f'{id_}.pdf')


@app.post('/sent_analysis')
def sent_analysis(data: dict):
    res = SentimentAnalysis.dostoevsky_analysis(df_where_word[data['id']], df)
    res = res.loc[["neutral", "positive", "negative"], :].to_string(header=False)
    return {'status': 'success', 'message': res}
