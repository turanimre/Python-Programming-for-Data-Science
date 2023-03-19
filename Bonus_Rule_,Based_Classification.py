import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
pd.set_option('display.float_format', lambda x: '%.3f' % x)


#### İş problemi

'''

Bir oyun şirketi müşterilerinin bazı özelliklerini kullanarak seviye tabanlı 
(level based) yeni müşteri tanımları (persona) oluşturmak ve bu yeni müşteri 
tanımlarına göre segmentler oluşturup bu segmentlere göre yeni gelebilecek müşterilerin
şirkete ortalama ne kadar kazandırabileceğini tahmin etmek istemektedir.

'''


#### Veri Seti & Değişkenler

'''

Persona.csv

PRICE:  Müşterinin harcama tutarı
SOURCE:  Müşterinin bağlandığı cihaz türü
SEX:  Müşterinin cinsiyeti
COUNTRY:  Müşterinin ülkesi
AGE:  Müşterinin yaşı

'''

###############################
# Veri Seti & Veriye İlk Bakış
###############################

##############################
## Görev 1: Aşağıdaki Soruları Yanıtlayınız
##############################


### Soru 1: persona.csv dosyasını okutunuz ve veri seti ile ilgili genel bilgileri gösteriniz.

df = pd.read_csv("Miuul_Course_1/Python Programming for Data Science/Datasets/persona.csv")

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

df.columns = [col[0] + (col[1:].lower()) for col in df.columns]

### Soru 2: Kaç unique SOURCE vardır? Frekansları nedir?

df["Source"].nunique()
df["Source"].value_counts()


### Soru 3: Kaç unique PRICE vardır?

df["Price"].nunique()

### Soru 4: Hangi PRICE'dan kaçar tane satış gerçekleşmiş?

df["Price"].value_counts()

### Soru 5: Hangi ülkeden kaçar tane satış olmuş?

df["Country"].value_counts()

### Soru 6: Ülkelere göre satışlardan toplam ne kadar kazanılmış?

df.groupby("Country")["Price"].sum()

### Soru 7: SOURCE türlerine göre satış sayıları nedir?

df["Source"].value_counts()

### Soru 8: Ülkelere göre PRICE ortalamaları nedir?

df.groupby("Country")["Price"].mean()

### Soru 9: SOURCE'lara göre PRICE ortalamaları nedir?

df.groupby("Source")["Price"].mean()

### Soru 10: COUNTRY-SOURCE kırılımında PRICE ortalamaları nedir?

df.groupby(["Country", "Source"])["Price"].mean()


##############################
## Görev 2: COUNTRY, SOURCE, SEX, AGE kırılımında ortalama kazançlar nedir?
##############################

df.groupby(["Country", "Source", "Sex", "Age"])["Price"].mean()



##############################
## Görev 3: Çıktıyı PRICE’a göre sıralayınız.
##############################

agg_df = df.groupby(["Country", "Source", "Sex", "Age"]).agg({"Price": "mean"}).sort_values("Price", ascending=False)



##############################
## Görev 4: Indekste yer alan isimleri değişken ismine çeviriniz.
##############################

agg_df.reset_index(inplace=True)
agg_df



##############################
## Görev 5: Age değişkenini kategorik değişkene çeviriniz ve agg_df’e ekleyiniz.
##############################

agg_df["Age"].max()

agg_df["Age_cat"] = agg_df["Age"]
agg_df.loc[agg_df["Age"] <= 18, "Age_cat"] = "0_18"
agg_df.loc[(agg_df["Age"] > 18) & (agg_df["Age"] <= 23), "Age_cat"] = "19_23"
agg_df.loc[(agg_df["Age"] > 23) & (agg_df["Age"] <= 30), "Age_cat"] = "24_30"
agg_df.loc[(agg_df["Age"] > 30) & (agg_df["Age"] <= 40), "Age_cat"] = "31_40"
agg_df.loc[(agg_df["Age"] > 40) & (agg_df["Age"] <= 66), "Age_cat"] = "41_66" # agg_df["Age"].max() = 66



##############################
## Görev 6: Yeni seviye tabanlı müşterileri (persona) tanımlayınız.
##############################

agg_df["customers_level_based"] = agg_df["Country"] + "_" + agg_df["Source"] + "_" + agg_df["Sex"] + "_" + agg_df["Age_cat"]

agg_df["customers_level_based"] = [row.upper() for row in agg_df["customers_level_based"]]

agg_df.groupby("customers_level_based").agg({"Price": "mean"}).sort_values("Price", ascending=False)



##############################
## Görev 7: Yeni müşterileri (personaları) segmentlere ayırınız.
##############################

agg_df ["Segment"] = pd.qcut(agg_df["Price"], 4, labels=["D", "C", "B", "A"])



##############################
## Görev 8: Yeni gelen müşterileri sınıflandırıp, ne kadar gelir getirebileceklerini tahmin ediniz.
##############################

### • 33 yaşında ANDROID kullanan bir Türk kadını hangi segmente aittir ve ortalama ne kadar gelir kazandırması beklenir?

new_user = "TUR_ANDROID_FEMALE_31_40"
agg_df[agg_df["customers_level_based"] == new_user]
agg_df[agg_df["customers_level_based"] == new_user]["Price"].mean()



### • 35 yaşında IOS kullanan bir Fransız kadını hangi segmente aittir ve ortalama ne kadar gelir kazandırması beklenir?

new_user_1 = "FRA_IOS_FEMALE_31_40"
agg_df[agg_df["customers_level_based"] == new_user_1]
agg_df[agg_df["customers_level_based"] == new_user_1]["Price"].mean()
