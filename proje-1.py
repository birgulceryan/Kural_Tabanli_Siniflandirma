######################################################################
#Kural Tabanlı Sınıflandırma ile Potansiyel Müşteri Getirisi Hesaplama
######################################################################
#############################
#İş Problemi
#############################
#Bir oyun şirketi müşterilerinin bazı özelliklerini kullanarak seviye tabanlı (level based) yeni müşteri tanımları (persona) oluşturmak ve bu yeni müşteri
#tanımlarına göre segmentler oluşturup bu segmentlere göre yeni gelebilecek müşterilerin şirkete ortalama ne kadar kazandırabileceğini tahmin etmek istemektedir.
#############################
#Veri Seti Hikayesi
#############################
#Persona.csv veri seti uluslararası bir oyun şirketinin sattığı ürünlerin fiyatlarını ve bu ürünleri satın alan kullanıcıların bazı demografik bilgilerini barındırmaktadır. Veri
#seti her satış işleminde oluşan kayıtlardan meydana gelmektedir. Bunun anlamı tablo tekilleştirilmemiştir. Diğer bir ifade ile belirli demografik özelliklere sahip bir
#kullanıcı birden fazla alışveriş yapmış olabilir.

#############################
#PRICE: Müşterinin harcama tutarı
#SOURCE : Müşterinin bağlandığı cihaz türü
#SEX : Müşterinin cinsiyeti
#COUNTRY : Müşterinin ülkesi
#AGE : Müşterinin yaşı
###############################

##########################################
#Görev 1: Aşağıdaki Soruları Yanıtlayınız.
##########################################
########
#Soru 1: persona.csv dosyasını okutunuz ve veri seti ile ilgili genel bilgileri gösteriniz.
########
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
pd.set_option('display.max_columns', None)
df = pd.read_csv("Kural_Tabanli_Siniflandirma/persona.csv")
df.head()
#########
#Soru 2: Kaç unique SOURCE vardır? Frekansları nedir?
#########
df["SOURCE"].nunique()

########
#Soru 3 : Kaç unique PRICE vardır?
########
df["PRICE"].nunique()

########
#Soru 4: Hangi PRICE'dan kaçar tane satış gerçekleşmiş?
########
df["PRICE"].value_counts()

#########
#Soru 5 : Hangi ülkeden kaçar tane satış olmuş?
#########
df["COUNTRY"].value_counts()

##########
#Soru 6 : Ülkelere göre satışlardan toplam ne kadar kazanılmış?
##########
df.groupby("COUNTRY").agg({"PRICE" : "sum"})
#df.groupby("COUNTRY")["PRICE"].sum()

##########
#Soru 7 : SOURCE türlerine göre satış sayıları nedir?
##########
df["SOURCE"].value_counts()

###########
#Soru 8 : Ülkelere göre PRICE ortalamaları nedir?
###########
df.groupby("COUNTRY").agg({"PRICE" : "mean"})

########
#Soru 9 :SOURCE'lara göre PRICE ortalamaları nedir?
########
df.groupby("SOURCE").agg({"PRICE" : "mean"})

##########
#Soru 10 :COUNTRY-SOURCE kırılımında PRICE ortalamaları nedir?
##########
df.groupby(["COUNTRY","SOURCE"]).agg({"PRICE": "mean"})

###########################################################################
#Görev-2 : COUNTRY, SOURCE, SEX, AGE kırılımında ortalama kazançlar nedir?
###########################################################################
df.groupby(["COUNTRY","SOURCE","SEX","AGE"]).agg({"PRICE": "mean"})

################################################
#Görev-3 : Çıktıyı PRICE’a göre sıralayınız.
################################################
df.groupby(["COUNTRY", 'SOURCE', "SEX", "AGE"]).agg({"PRICE": "mean"}).head()
agg_df = df.groupby(by=["COUNTRY", 'SOURCE', "SEX", "AGE"]).agg({"PRICE": "mean"}).sort_values("PRICE", ascending=False)
agg_df.head()
#################################################################
#Görev-4 : Indekste yer alan isimleri değişken ismine çeviriniz.
##################################################################
agg_df = df.groupby(["COUNTRY","SOURCE","SEX","AGE"]).agg({"PRICE": "mean"})
agg_df.reset_index(inplace=True)
agg_df.head()

##############################################################################
#Görev-5 : Age değişkenini kategorik değişkene çeviriniz ve agg_df’e ekleyiniz.
##############################################################################
bins = [0, 18, 23, 30, 40, agg_df["AGE"].max()]
mylabels = ['0_18', '19_23', '24_30', '31_40', '41_' + str(agg_df["AGE"].max())]
agg_df["AGE_CAT"] = pd.cut(agg_df["AGE"], bins, labels=mylabels)
agg_df.head()
#####################################################################
#Görev-6 : Yeni seviye tabanlı müşterileri (persona) tanımlayınız.
#####################################################################
agg_df.columns
agg_df["customers_level_based"] = [row[0].upper() + "_" + row[1].upper() + "_" + row[2].upper() + "_" + row[5].upper() for row in agg_df.values]
agg_df.head()
agg_df = agg_df.groupby("customers_level_based").agg({"PRICE": "mean"})
agg_df = agg_df.reset_index()
agg_df.head()

###############################################################
#Görev-7 : Yeni müşterileri (personaları) segmentlere ayırınız.
################################################################
agg_df["SEGMENT"] = pd.qcut(agg_df["PRICE"], 4 , labels = ["D","C","B","A"])
agg_df.groupby("SEGMENT").agg({"PRICE": "mean"})
agg_df

###############################################################################################
#Görev-8 : Yeni gelen müşterileri sınıflandırıp, ne kadar gelir getirebileceklerini tahmin ediniz.
###############################################################################################
new_user = "TUR_ANDROID_FEMALE_31_40"
agg_df[agg_df["customers_level_based"] == new_user]









































