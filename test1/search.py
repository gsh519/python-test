import os

SOURCE=["ねずこ","たんじろう","きょうじゅろう","ぎゆう","げんや","かなお","ぜんいつ"]
CSV_PATH = 'search.csv'

# csv読み込み処理関数
def read_source(csv):
    if not os.path.exists(csv):
        write_source(csv, SOURCE)
    with open(csv, 'r') as f:
        return f.read().split('\n')

# csv書き込み処理関数
def write_source(csv:str, source:list):
    with open(csv, 'w') as f:
        f.write('\n'.join(source))


def search():
    
    source = read_source(CSV_PATH)
    
    while True:
        word =input("鬼滅の登場人物の名前を入力してください >>> ")
        
        if word in source:
            print("{}が見つかりした".format(word))
        else:
            print('{}が見つかりませんでした'.format(word))
            source.append(word)

        # csv書き込み
        write_source(CSV_PATH, source)

if __name__ == "__main__":
    search()