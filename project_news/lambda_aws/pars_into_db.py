from db_for_lambda import DynamoDBClient
from lambda_aws.parsing import ParsNews, GoogleNews, By024, MinskNews, Onliner, Regexparser
from normalization import normalize


def handler(event, context):
    # news = MinskNews().pars_news()
    news = GoogleNews().pars_news()
    # news += Onliner().pars_news()
    # news += By024().pars_news()
    # news += Regexparser().pars_news()
    norm_news = normalize(news)
    print(len(norm_news))
    DynamoDBClient().to_bd(news)
    DynamoDBClient().to_bd(norm_news)
    # print('hello world')


handler(1, 1)
