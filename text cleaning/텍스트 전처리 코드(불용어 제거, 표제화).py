def Delete_StandardStopwords(username, prname):  # 1차 불용어 처리 (불용어 사전을 새로 수정하고 만들어야 합니다.)
    import re, os
    from tqdm import tqdm
    from flashtext import KeywordProcessor
    from utils import Read_Arg_, Read_Sheet_, import_dataframe, export_dataframe
    from flashtext import KeywordProcessor
    kp = KeywordProcessor()
    tqdm.pandas()

    if (username == None) & (prname == None): #!!수정 - None으로
        input_directory = ""  # Non-창민버전
    else:
        input_directory = "/".join([username, prname])  # Non-창민버전
    ref, input_, output_ = Read_Arg_(username,prname,"Delete_StandardStopwords")  # Read_Arg를 통한 backbone dictionary 내
    # project library 내의 Delete_standardstopwords 행을 참조하여 ref, input파일, output파일을 불러옵니다.
    # 이 때 ref는 "JDic_BizStopwords(경영불용어사전)"시트를,
    # input파일은 메세지 csv파일의 이름,
    # output은 처리 후 내보낼 메세지 csv파일의 이름입니다. (local에서 실행할 경우 딕셔너리에 정보를 미리 입력해야 합니다)
    Sym2Remain = Read_Sheet_(username,prname, "JDic_Symbol(특수기호사전)") #!!수정
    #유의기호사전 시트에 접근하여 유의기호 사전을 불러옵니다
    Clean = Read_Sheet_(username,prname,ref)  # Clean이라는 변수에 Read_Sheet를 통해
    # "JDic_BizStopwords(경영불용어사전)"시트를 불러옵니다.
    Clean['space'] = Clean['space'].replace('',0)
    for k in range(len(Clean['space'])):
        if Clean.loc[k,'word'][-1] ==' ':
            Clean.loc[k,'word'] = Clean.loc[k,'word'][:-1] #test
        Clean.loc[k, 'word'] = Clean.loc[k, 'word'] + int(Clean.loc[k, 'space']) * ' '
    #Space 열에 1이 있으면 같은 행의 word 열 문자 뒤에 띄어쓰기를 추가해줍니다

    Clean["unit_length"] = Clean["word"].apply(lambda x: len(x))  # 이 때 하나의 이슈는 표현의 길이에 따른 나열 순서입니다.
    # (https://greeksharifa.github.io/정규표현식(re)/2018/07/22/regex-usage-03-basic/)
    # 만약 "에게"와 "에게서"를 예시로 들 떄,
    # 정규식 인자로 "에게"가 "에게서"보다 먼저 나열될 경우,
    # 메세지에서 "에게"에 대한 데이터를 먼저 찾으므로
    # 실제로 메세지에서 "에게서" 라고 표현되었던 데이터가
    # "에게"로 인해 "서"만으로 남게됩니다.
    # 따라서 위 방법을 사용하게 될 경우,
    # 불용어 사전의 칼럼으로 unit_length를 두고
    # 내림차순으로 정렬하는 것이 바람직해 보입니다.

    Sym2Remain_np = Sym2Remain.fillna("").to_numpy(dtype=list)
    all_V = list(map(lambda x: [i for i in x if i != ""], Sym2Remain_np))
    #형태 = [['$', 'doollar', ''],       ['¥', 'yen', ''], ['£', 'poound', '']......]
    for case in all_V:
        ReplacedText = ' '+str(case[1])+' '
        Symbol = case[0]
        kp.add_keyword(Symbol, ReplacedText) #lemma 코드의 all_V와는 다르게 심볼 사전은 심볼 1개, 대체단어 1개만 작성해야 합니다.

    Clean = Clean.sort_values(by="unit_length", ascending=False)  # unit_length열 기준으로 내림차순으로 정렬해주고 최신화합니다.
    Clean = Clean[~Clean["word"].duplicated()]  # 혹시모를 중복 word를 제거합니다.


    # print(symbol)

    characters = set(Clean.loc[:,"word"])  #! 수정
    # 문자는 Clean 데이터 프레임에서
    # "class" 컬럼이 c인 것들의 "word"컬럼을 리스트화한 것입니다.
    characters = str(characters).replace("{", "").replace("}", "").replace(", ''", "").replace(", ", "|").replace("'", "")


    # 정규표현식을 사용하기 위한 작업입니다.
    # 본디, JDic_Clean은 ["물론", "무엇", "무슨" …] 처럼 리스트의 형태를 취합니다.
    # 정규표현식을 조작하게끔 하는 라이브러리 re는 인자로 문자열을 받습니다.
    # 따라서 리스트를 문자열로 바꿔줍니다. ( str(JDic_Clean) )
    # 또한, 정규식에는 .sub 메소드가 있는데,
    # 이는 세번째 인자(데이터)에서 첫번째 인자(특정 표현)를 발견하면
    # 두번째 인자로 바꿔주는 메소드입니다.
    # 아래에서 item(메세지 데이터의  각 행에 해당하는 데이터) 데이터에서
    # 불용어사전에 등록된 표현을 찾아 공백으로 바꿔주고자 합니다.
    # 이 때, 불용어 사전에 등록된 단어를 하나하나 바꿔주기 보다,
    # or식( | )을 써서 한번에 lookup하고자 합니다.
    # 그러기 위해서는 정규식의 인자에 들어가야할 형태는 다음과 같습니다.
    # "표현 1"|"표현 2"|"표현3"|…"
    # 더욱이 "ㅜ" 같은경우 "ㅜㅜ"로 메세지에서 발견될 수 있습니다.
    # 이는 정규식 내 +를 넣어주면 해결됩니다.
    # +는 해당표현이 1번이상 반복되는 경우를 뜻합니다.
    # 해당표현 바로 뒤에 +를 써줘 정규식에 넣어줘야 합니다.
    # 따라서 위 Clean_Candidates에는 다음과 같이 형태가 이루어져 있습니다.
    # "표현 1 +"|"표현 2 +"|"표현 3 +"|...

    def save_symbol(item):  # lemmatize라는 함수를 정의합니다.

        input = item
        while True:
            input_revised = kp.replace_keywords(input) #input문장을 replace시켜준 후 item_replaced 변수에 저장
            if input == input_revised: #이전 문장과 수정 후 문장이 같다면 더이상 고칠게 없다는 의미이므로 반복문 탈출
                break
            else: # 이전 문장과 다르다면 바꿔줘야할 것이 있었다는 소리이므로 계속 진행. item_revised를 다시 이전의 값을 뜻하는 input으로 변경
                input = input_revised
                pass
        return input_revised

    def save_symbol2(item):  # lemmatize라는 함수를 정의합니다. (무식 버전) !수정 - decode처리
        item_revised = item
        for i in range(len(Sym2Remain)):
            item_revised = item_revised.replace(Sym2Remain.iloc[i]["Symbol"], " "+Sym2Remain.iloc[i]["ReplacedText"]+" ")
        return item_revised

    # def Clean_symbol(item):  # Clean_stopwords라는 사용자정의함수를 정의합니다.
    #     item_edited = re.sub(symbol, " ", item)  # 이는 정규표현식을 통해 item(input_Message의 각행의 데이터)에 대해
    #     # Clean_candidates에 해당하는 패턴이 나올 시 " "(공백)으로 치환해주는 함수입니다.
    #     item_edited = " ".join(item_edited.split())  # 다중공백도 제거해줍니다.
    #     return item_edited  # 이 함수의 리턴값을 치환된 데이터로 최신화된 데이터로 내보내도록 합니다.

    # def add_space_for_symbol(item):
    #    not_words = list(filter(bool, list(set(re.compile("[^\s*\w*\s*]*").findall(item)))))
    #    for end in not_words:                                     # 메세지의 한 행에서 있는 not_words리스트 요소마다
    #        item = item.replace(end," "+end)                                    # replace메소드를 통해 스페이스를 첨가해줍니다.
    #    return item

    def Clean_char(item):  # Clean_stopwords라는 사용자정의함수를 정의합니다.

        item_edited = re.sub(characters, " ", item)  # 이는 정규표현식을 통해 item(input_Message의 각행의 데이터)에 대해
        # Clean_candidates에 해당하는 패턴이 나올 시 " "(공백)으로 치환해주는 함수입니다.
        item_edited = " ".join(item_edited.split()) # 다중공백도 제거해줍니다.
        return item_edited  # 이 함수의 리턴값을 치환된 데이터로 최신화된 데이터로 내보내도록 합니다.


    def Clean_leftover_symbols(item):
        item_edited = re.sub("[^\w\s]", "", item)
        item_edited = " ".join(item_edited.split())  # 다중공백도 제거해줍니다.
        return item_edited

    input_name = os.path.join(input_directory, input_)
    input_Message = import_dataframe(input_name)
    input_Message = input_Message[input_Message["contents"].notna()]  # input Message에 있을 결측치(빈칸)을 제거합니다.
    tqdm.pandas(desc='유의기호 대체')
    input_Message["contents"] = input_Message["contents"].progress_apply(save_symbol)
    #input_Message["contents"] = input_Message["contents"].progress_apply(Clean_symbol)
    # Clean_stopwords를 .apply메소드를 통해 적용시킵니다.
    # input_Message["contents"] = input_Message["contents"].progress_apply(add_space_for_symbol) #살릴 기호들 앞에 스페이스를 첨가해줍니다.
    tqdm.pandas(desc = '불용어 제거')
    input_Message["contents"] = input_Message["contents"].progress_apply(Clean_char)
    # Clean_stopwords를 .apply메소드를 통해 적용시킵니다.
    tqdm.pandas(desc='나머지 유의기호 제거')
    input_Message["contents"] = input_Message["contents"].progress_apply(Clean_leftover_symbols)

    output_name = os.path.join(input_directory, output_)
    export_dataframe(input_Message, output_name)

    return input_Message  # Delete_Characters의 리턴값으로 최신화된 데이터프레임으로 내보내도록 합니다.
if __name__ == '__main__':

    Delete_StandardStopwords(None,None)

#--------------------------------------------------------------------------------------------------------


def Replace_Texts_in_Messages(username, prname):  # 1차 Lemmatization 함수
    # (지금은 "JDic_Lemmatization(일반lemma사전)"의 양이 적어 이렇게 가지만,
    # 양이 많아진다면 2차 Lemmatization 함수처럼 수정해야 합니다.)
    import os, re
    import pandas as pd
    from tqdm import tqdm
    from utils import Read_Arg_, Read_Sheet_, import_dataframe, export_dataframe
    from flashtext import KeywordProcessor
    tqdm.pandas()

    if (username is None) or (prname is None):
        input_directory = ""
    else:
        input_directory = "/".join([username, prname])  # Non-창민버전

    ref, input_, output_ = Read_Arg_(username,prname,"Replace_Texts_in_Messages")  # Read_Arg를 통해 참조파일, input파일, output파일을 불러옵니다.
    # 이 때 ref는 "JDic_Lemmatization(일반lemma사전)"시트를,
    # input파일은 메세지 csv파일의 이름,
    # output은 처리 후 내보낼 메세지 csv파일의 이름입니다.

    # lemma라는 변수에 reference 시트를 불러오기
    lemma = Read_Sheet_(username,prname,ref)  # lemma라는 변수에 Read_Sheet를 통해
    # "JDic_Lemmatization(일반lemma사전)"시트를 불러옵니다.
    lemma = lemma.fillna("").to_numpy(dtype=list)
    all_V = list(map(lambda x: [i for i in x if i != ""], lemma))  # all_V라는 변수에 lemma에 있는 데이터들을 전부 가져옵니다.

    # 이 때 all_V의 형태는 다음과 같습니다.
    # [[기준단어 a, 변형단어 a-1, 변형단어 a-2,... ],
    #  [기준단어 b, 변형단어 b-1, 변형단어 b-2,... ],
    #  ... ]
    # for case in all_V:
    #     standardised = case[0]
    #     for keyword in case[1:]:
    #         kp.add_keyword(keyword, standardised)
    #
    # def lemmatize(item):  # lemmatize라는 함수를 정의합니다.
    #     return kp.replace_keywords(item)
    #     # item_edited = item
    #     # for case in all_V:  # all_V내에 있는 단어세트(case) (ex. [기준단어 a, 변형단어 a-1, 변형단어 a-2,... ])별로
    #     #     exp4re = str(sorted(case[1:], key=len, reverse=True)).replace("[", "").replace("]",
    #     #                 "").replace(", ''", "").replace(", ", "|").replace("'", "")
    #     #     # [변형단어 a-1, 변형단어 a-2,... ]로 있는 case[1:]라는 리스트를 문자열로 바꿔주고,
    #     #     # "변형단어 a-1 +|변형단어 a-2 +|..." 식으로 바꿔줍니다.
    #     #     # 이는 정규식을 사용하기 위한 전처리 작업입니다.
    #     #     # 정규표현식을 사용하면 원하는 패턴의 문자열을 한번에 찾고 한번에 바꿀 수 있습니다.
    #     #     item_edited = re.sub(exp4re, case[0], item_edited)  # 변형단어들을 기준단어로 치환해주고 이를 item_edited라는 변수에 넣어줍니다.
    #     #     item_edited = re.sub("[\s]+", " ", item_edited)  # item_edited의 다중공백(space 두 개 이상의 공백)을 하나의 space로 치환합니다.
    #     # return item_edited  # item_edited을 리턴값으로 내보냅니다.
    #
    #
    # input_name = os.path.join(input_directory, input_)
    # input_Message = import_dataframe(input_name)
    # input_Message["contents"] = input_Message["contents"].progress_apply(lemmatize)  # lemmatize함수를 .apply메소드를 통해
    # # input_Message의 "contents"열에 적용시키고 표시합니다.
    #
    # input_Message = input_Message[input_Message["contents"].notna()]  # Null 값이 아닌 데이터들만을 표시합니다.


    """
    version 2.0 token decomposition 방식(21-05-30)
    """
    # lemee에는 lemmatize될 token을, lemer에서는 기준 token을 추가해준다.
    # lemee와 lemerfmf 열로 갖는 DataFrame을 lemm이라는 변수에 담아둔다.
    lemee = []
    lemer = []
    for case in all_V:
        standardised = case[0]
        for keyword in case[1:]:
            lemee.append(keyword)
            lemer.append(standardised)
    lemm = pd.DataFrame({"raw": lemee, "lem": lemer})

    # 원문데이터를 불러와 DataFrame형식으로 input_Message리는 변수에 담는다.
    if (username is None) or (prname is None):
        input_name = os.path.join(input_)
    else:
        input_directory = "/".join([username, prname])  # Non-창민버전
        input_name = os.path.join(input_directory,input_)
    input_Message = import_dataframe(input_name)

    # 원문 데이터로부 line넘버, token넘버고, token을 추출해
    # line_no, token_no, token 을 열로 갖는 DataFrame을 text_decomposition이라는 의미의 text_decomp 변수에 저장한다.
    line_no = []
    token_no = []
    token = []
    for lines in enumerate(input_Message["contents"]):
        for tokens in enumerate(str(lines[1]).split()):
            line_no.append(lines[0])
            token_no.append(tokens[0])
            token.append(tokens[1])
    text_decomp = pd.DataFrame({"line_no": line_no, "token_no": token_no, "token": token})

    # text_decomp 테이블 기준테이블로 설정하고  text_decomp의 "token"열과  lemm테이블의 "raw" 열을 "left join" 하고,
    #  중복열인 "raw"열을 제거한 후, "lem"열에 빈 부분을 같은 행의 "token"열의 값들로 채워준다.
    res = pd.merge(text_decomp, lemm, left_on=["token"], right_on=["raw"], how="left").drop(["raw"], axis=1)
    res["lem"] = res["lem"].fillna(res["token"])
    # 중간에 res가 어떻게 나오는지, 바뀐 부분이 어떻게 바뀌었는지 확인하는 코드 두 줄
    # print(res.head(30))
    # print(res[res["token"]!=res["lem"]].head(30))

    # lemmatize된 문장으로 뭉쳐주는 코드
    # new_lines라는 빈 리스트를 생성한다.

    # res의 line_no열에 있는 값들을 unique하게 불러온 후, 이들을 기준으로 순서대로 다음과 같은 실행을 거친다.
    #     res의 "line_no"가  i번째인 부분을 가져온 후, "token_no"를 기준으로 오름차순으로 정렬한 후 그 순서대로 "lem"열에 있는 token들을 정렬한다.
    #     정렬된 token 사이를 띄어쓰기로 채워 넣어 한 문장으로 만들어 new_line이라는 변수에 저장한다.
    #     new_lines리스트에 new_line을 추가한다.
    res = res.sort_values(by=["line_no","token_no"])
    renewed = res.groupby("line_no", as_index=False).agg({'lem': ' '.join})["lem"]
    input_Message["contents"] = renewed


    # sen_no = res["line_no"].unique()
    #
    # for i in tqdm(sen_no):
    #     new_line = " ".join(res[res["line_no"] == i].sort_values(by="token_no", ascending=True)["lem"])
    #     new_lines.append(new_line)qs
    # # 최종적으로 누적된 new_lines를 input_Message의 "contents"열에 넣어 갱신해준다.
    # input_Message["contents"] = new_lines

    output_name = os.path.join(input_directory, output_)
    export_dataframe(input_Message, output_name)

    return input_Message  # 처리한 input_Message를 리턴값으로 내보냅니다.


if __name__ =='__main__':

    Replace_Texts_in_Messages(None, None)

