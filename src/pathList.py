import datetime

# https://www.mlit.go.jp/kankocho/siryou/toukei/shukuhakutoukei.html
# 県別外国人宿泊者数
# -> 外国からの流入人数を調べられる
# -> 外国からの渡航者数全体のうち，どの県に散らばるか，%として用いることが可能．
jp_tourism = "jp_tourism_agency_dec_2020.xlsx"

# http://www.mlit.go.jp/sogoseisaku/soukou/sogoseisaku_soukou_fr_000023.html
# RESAS上の観光マップの「外国人入出国空港分析」及び「外国人移動相関分析」で、FF-Dataが掲載されました。
# 外国人入国空港と外国人旅行目的地の人数 47*47 があり．　
# -> 外国人がどれだけ感染を広げるか調べられる．
foreginNum = "001263852.xlsx"


anaTravel = "../dt_main/ana_travel.xlsx"
anaEdit = "../dt_main/ana_edit.xlsx"
pref_pop = "../dt_main/pref_population.xlsx"
dataProp = "../dt_main/prop.npy"
caseRecord = "../dt_main/case_summary.xlsx"
casePrefecture = "../dt_main/case_20200227.xlsx"
recSim = "../dt_sim/simResults_"

baseDate = datetime.date(2020,2,27)
notIn = {'栃木県': 9,
 '群馬県': 10,
 '埼玉県': 11,
 '千葉県': 12,
 '神奈川県': 14,
 '福井県': 18,
 '山梨県': 19,
 '長野県': 20,
 '岐阜県': 21,
 '三重県': 24,
 '滋賀県': 25,
 '京都府': 26,
 '奈良県': 29,
 '和歌山県': 30}
