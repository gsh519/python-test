import os
# 検索ソース
source=["ねずこ","たんじろう","きょうじゅろう","ぎゆう","げんや","かなお","ぜんいつ"]

### 検索ツール
def search():
    
    if not os.path.exists('search.csv'):
        with open('search.csv', 'w') as f:
            f.write('\n'.join(source))
    with open('search.csv', 'r') as f:
        f.read()
    
    while True:
        word =input("鬼滅の登場人物の名前を入力してください >>> ")
        
        if word in source:
            print("{}が見つかりした".format(word))
        else:
            print('{}が見つかりませんでした'.format(word))
            source.append(word)

        with open('search.csv', 'w') as f:
            f.write('\n'.join(source))

if __name__ == "__main__":
    search()