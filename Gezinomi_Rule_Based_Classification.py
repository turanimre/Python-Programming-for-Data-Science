import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
pd.set_option('display.float_format', lambda x: '%.3f' % x)



#### İş Problemi
'''

Gezinomi yaptığı satışların bazı özelliklerini kullanarak seviye tabanlı
(level based) yeni satış tanımları oluşturmak ve bu yeni satış
tanımlarına göre segmentler oluşturup bu segmentlere göre yeni
gelebilecek müşterilerin şirkete ortalama ne kadar kazandırabileceğini
tahmin etmek istemektedir.

'''

#### Veri seti & Değişkenler

'''
miuul_gezinomi.xlsx

Columns  
SaleId:  Satış id
SaleDate:  Satış Tarihi
CheckInDate:  Müşterin otele giriş yaptığı tarih
Price:  Satış için ödenen fiyat
ConceptName:  Otel konsept bilgisi
SaleCityName:  Otelin bulunduğu şehir bilgisi
CInDay:  Müşterinin otele giriş günü
SaleCheckInDayDiff:  Check in ile giriş tarihi gün farkı
Season:  Otele giriş tarihindeki sezon bilgisi

'''



##############################
# Verinin Okunması - Veriye ilk bakış
##############################


df = pd.read_excel("Miuul_Course_1/Python Programming for Data Science/Datasets/miuul_gezinomi.xlsx")
df

## Soru 1: miuul_gezinomi.xlsx dosyasını okutunuz ve veri seti ile ilgili genel bilgileri gösteriniz..


def check_df(dataframe, head=5):
    print("##################### Shape #####################")
    print(dataframe.shape)
    print("##################### Types #####################")
    print(dataframe.dtypes)
    print("##################### Head #####################")
    print(dataframe.head(head))
    print("##################### Tail #####################")
    print(dataframe.tail(head))
    print("##################### NA #####################")
    print(dataframe.isnull().sum())
    print("##################### Quantiles #####################")
    print(dataframe.quantile([0, 0.05, 0.50, 0.95, 0.99, 1]).T)
    print("################### Unique Values ###################")
    print(dataframe.nunique())

check_df(df)


## Soru 2:Kaçunique şehirvardır? Frekanslarınedir?

df["SaleCityName"].nunique()
df["SaleCityName"].value_counts()

## Soru 3:Kaç unique Concept vardır?

df["ConceptName"].nunique()

## Soru4: Hangi Concept’den kaçar tane satış gerçekleşmiş?

df["ConceptName"].value_counts()

## Soru5: Şehirlere göre satışlardan toplam ne kadar kazanılmış?

df.groupby("SaleCityName").agg({"Price": "sum"}).sort_values("Price", ascending=False)

## Soru6: Concept türlerine göre göre ne kadar kazanılmış?

df.groupby("ConceptName").agg({"Price": "sum"}).sort_values("Price", ascending=False)

## Soru7: Şehirlere göre PRICE ortalamaları nedir?

df.groupby("SaleCityName").agg({"Price": "mean"}).sort_values("Price", ascending=False)

## Soru 8: Conceptlere göre PRICE ortalamaları nedir?

df.groupby("ConceptName").agg({"Price": "mean"}).sort_values("Price", ascending=False)

## Soru 9: Şehir-Concept kırılımındaPRICE ortalamaları nedir?

df.groupby(["SaleCityName", "ConceptName"]).agg({"Price": "mean"}).sort_values(["SaleCityName", "Price"], ascending=False)


##############################
# Görev 2: SaleCheckInDayDiff değişkenini kategorik bir değişkene çeviriniz.
##############################

df["CheckInCat"] = df["SaleCheckInDayDiff"]
df.loc[(df["SaleCheckInDayDiff"] >=0) & (df["SaleCheckInDayDiff"] <= 7), "CheckInCat"] = "Last Minuters"
df.loc[(df["SaleCheckInDayDiff"] >7) & (df["SaleCheckInDayDiff"] <= 30), "CheckInCat"] = "Potantial Planners"
df.loc[(df["SaleCheckInDayDiff"] >30) & (df["SaleCheckInDayDiff"] <= 90), "CheckInCat"] = "Planners"
df.loc[(df["SaleCheckInDayDiff"] >90), "CheckInCat"] = "Early Bookers"

df["CheckInCat"].value_counts()


##############################
# Görev 3: COUNTRY, SOURCE, SEX, AGE kırılımında ortalama kazançlar nedir?
##############################

df.groupby(["SaleCityName", "ConceptName", "CheckInCat"]).agg({"Price": ["mean", "count"]})


##############################
# Görev 4: City-Concept-Season kırılımının çıktısını PRICE'a göre sıralayınız.
##############################


agg_df = df.groupby(["SaleCityName", "ConceptName", "Seasons"])["Price"].mean().sort_values(ascending=False)

##############################
# Görev 5: Indekste yer alan isimleri değişken ismine çeviriniz.
##############################

agg_df = agg_df.reset_index()


##############################
# Görev 6: Yeni seviye tabanlı müşterileri (persona) tanımlayınız.
##############################

agg_df["sales_level_based"] = agg_df["SaleCityName"] + "_" + agg_df["ConceptName"] + "_" + agg_df["Seasons"]
agg_df["sales_level_based"] = [agg_df["sales_level_based"][i].upper() for i in agg_df.index]

##############################
# Görev 7: Yeni müşterileri (personaları) segmentlere ayırınız.
##############################

agg_df["Segment"] = pd.qcut(agg_df["Price"], 4, labels=["A", "B", "C", "D"])
agg_df.groupby("Segment").agg({"Price": ["mean", "max", "sum"]})


##############################
# Görev 8: Yeni gelen müşterileri sınıflandırıp, ne kadar gelir getirebileceklerini tahmin ediniz.
##############################

### • Antalya’da herşey dahil ve yüksek sezonda tatil yapmak isteyen bir kişinin ortalama ne kadar gelir kazandırması beklenir?

agg_df[agg_df["sales_level_based"] == "ANTALYA_HERŞEY DAHIL_HIGH"]
"""
     SaleCityName      ConceptName      Seasons       Price          sales_level_based          Segment
       Antalya        Herşey Dahil       High         64.920      ANTALYA_HERŞEY DAHIL_HIGH         C
"""

### • Girne’de yarım pansiyon bir otele düşük sezonda giden bir tatilci hangi segmentte yer alacaktır?

agg_df[agg_df["sales_level_based"] == "GIRNE_YARIM PANSIYON_LOW"]
"""
      SaleCityName      ConceptName   Seasons    Price           sales_level_based         Segment
         Girne       Yarım Pansiyon       Low   48.579       GIRNE_YARIM PANSIYON_LOW       B
"""

