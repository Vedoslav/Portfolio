import pandas as pd
import matplotlib.pyplot as plt

"""This script counts mentions of different countries in some media`s Telegram-channel (e.g. Bloomberg, NY Times, Reuters), exported in json-file. Then it rates countries by number of mentions in the media (first plot) and counts special indexes: mentions, divided by total population (in millions), and mentions, divided by GDP of the country (in billions $). The second plot shows, how countries with small population and low GDP can be on the top of news."""

pd.options.display.float_format = '{:.2f}'.format
pd.set_option('display.max_rows', 250)

#collect data about population and GDP from the official World Bank website

GDP = pd.read_csv('GDP.csv')
Population = pd.read_csv('Population.csv')

#create general DataFrame and check it for missing values

data = pd.DataFrame({'Country' : GDP['Country Name'], 'GDP' : GDP['2022 [YR2022]'], 'Population' : Population['2022 [YR2022]']})
data['GDP'].mask(data['GDP'] == '..', None, inplace=True)
data['GDP'] = data['GDP'].astype('float32')

#create list of keywords, useful for search of country`s mentions in the media

keywords = [["Afghan","Talib"], ["albania"], ["alger"], ["andorr"], ["angol", "luanda"], ["antigua", "barbuda"], ["argentin", "buenos"], ["armeni"], ["aruba"], ["australi", "canber"], ["austria", "vienn"], ["azerbaijan"], ["bahamas"], ["bahrain"], ["bangladesh"], ["barbados"], ["belarus"], ["belgium","brussel"], ["beliz"], ["benin"], ["bermud"], ["bhutan","thimphu"], ["bolivia"], ["bosnia"], ["botswana"], ["brazil"], ["brunei"], ["bulgaria"], ["burkina"], ["burundi"], ["verde"], ["cambodia"], ["cameroon"], ["canad"], ["cayman"], ["Central African Rep", "bangui"], ["chad"], ["chile"], ["china", "chine", "beijing"], ["colombia"], ["comoros"], ["Democratic Republic of Congo"], ["The Republic of Congo"], ["Costa Rica"], ["d'Ivoire"], ["croatia"], ["cuba", "havana"], ["cyprus"], ["czech", "prague"], ["denmark", "danish"], ["djibouti"], ["dominican"], ["ecuador"], ["egypt"], ["El Salvador"], ["Equatorial Guinea"], ["eritrea"], ["estonia"], ["eswatini"], ["ethiopia"], ["faroe"], ["fiji"], ["finland", "finnish"], ["france", "french", "paris"], ["gabon"], ["gambia"], ["georgia"], ["german", "berlin", "hamburg", "frankfurt"], ["ghana"], ["gibraltar"], ["greece", "greek"], ["greenland"], ["grenada"], ["guam"], ["guatemala"], ["guinea", "konakry"], ["bissau"], ["guyan"], ["haiti"], ["honduras"], ["hungar"], ["iceland"], ["india", "mumbai"], ["indonesia"], ["iran"], ["iraq", "baghdad"], ["ireland", "irish"], ["israel", "West Bank", "gaza"], ["italy", "itali"], ["jamaica"], ["japan", "tokyo"], ["jordan"], ["kazakh"], ["kenya"], ["kiribati"], [u'North Korea'], ["South Korea"], ["kosovo"], ["kuwait"], ["kyrgyz"], ["laos"], ["latvia"], ["leban"], ["lesotho"], ["liberia"], ["libya"], ["liechtenstein"], ["lithuania", "vilnius"], ["luxembourg"], ["madagascar"], ["malavi"], ["malaysia"], ["maldives"], ["malian", "bamako", "tuareg"], ["malta"], ["Marshall Island"], ["mauritania"], ["mauritius"], ["mexic"], ["micronesia"], ["moldova"], ["monac"], ["mongolia"], ["montenegr"], ["morocc"], ["mozambi"], ["myanmar", "burmese"], ["namibia"], ["nauru"], ["nepal"], ["netherlands", "dutch"], ["caledonia"], ["zealand"], ["nicaragua"], ["nigerien", "niamey"], ["nigeria"], ["macedonia"], ["norw"], ["oman"], ["pakistan"], ["palau"], ["panama"], ["papua"], ["paraguay"], ["peru"], ["philippin"], ["poland", "polish"], ["portug"], ["puerto"], ["qatar"], ["romania"], ["russia", "kreml"], ["rwanda"], ["samoa"], ["marino"], ["principe"], ["saudi"], ["senegal"], ["serbia"], ["seychell"], ["leone"], ["singapor"], ["slovak"], ["slovenia"], ["solomons"], ["somalia"], ["South Africa"], ["South Sudan"], ["spain", "spanish"], ["lanka"], ["kitts", "kittian"], ["Saint Lucia", "St. Lucia"], ["grenadin"], ["sudan"], ["surinam"], ["sweden", "swedish"], ["switzerland", "swiss"], ["syria"], ["tajik"], ["tanzania"], ["thai"], ["timor"], ["togo"], ["tonga"], ["tobago"], ["tunis"], ["turki", "turke"], ["turkm"], ["tuvalu"], ["uganda"], ["ukrain"], ["UAE", "U.A.E.", "United Arab"], ["U.K.", "United Kingdom", "brita", "briti", "engla", "engli"], ["U.S.", "United States"], ["uruguay"], ["uzbek"], ["vanuatu"], ["venezuela"], ["vietnam"], ["yemen"], ["zambia"], ["zimbabwe"]]
data["Keywords"] = keywords

#read channel`s history of some media and count the mentions of each country, using defined keywords 

with open("result_BLoomberg.json", 'r', encoding="utf-8") as file:
    channel = file.read()  
    for idx, row in data.iterrows():
        words = row["Keywords"]    
        total = 0
        for word in words:
            total+=channel.count(word.capitalize())    
        data.loc[idx, "Total"] = total     #new column that shows number of each country`s mentions is added to the general DataFrame
    
    #names of countries that consists several words or abbreviation should be investigated in different way; this fragment of script would be optimized further 
    
    US = channel.count("U.S.")+channel.count("United States")
    data.loc[193, "Total"] = US
    UK = channel.count("U.K.")+channel.count("United Kingdom")
    data.loc[192, "Total"] += UK
    NK = channel.count("North Korea")
    data.loc[95, "Total"] = NK
    SK = channel.count("South Korea")
    data.loc[96, "Total"] = SK
    ES = channel.count("El Salvador")
    data.loc[54, "Total"] = ES
    EG = channel.count("Equatorial Guinea")
    data.loc[55, "Total"] = EG
    ISR = channel.count("West Bank")
    data.loc[87, "Total"] += ISR
    CAR = channel.count("Central African Rep")
    data.loc[35, "Total"] += CAR
    DRC = channel.count("Democratic Republic of Congo")
    data.loc[41, "Total"] = DRC
    RC = channel.count("The Republic of Congo")
    data.loc[42, "Total"] = RC
    CR = channel.count("Costa Rica")
    data.loc[43, "Total"] = CR
    MI = channel.count("Marshall Island")
    data.loc[115, "Total"] = MI
    SAR = channel.count("South Africa")
    data.loc[166, "Total"] = SAR
    SS = channel.count("South Sudan")
    data.loc[167, "Total"] = SS
    SL = channel.count("Saint Lucia")+channel.count("St. Lucia")
    data.loc[171, "Total"] = SL
    UAE = channel.count("UAE")+channel.count("U.A.E.")+channel.count("United Arab")
    data.loc[191, "Total"] = UAE

#add new columns that shows specific indexes of the media: number of mentions per country, divided by population and by GDP
    
for idx, row in data.iterrows():
    data.loc[idx, "Population_index"] = row["Total"]/(row["Population"]/1000000)
    data.loc[idx, "GDP_index"] = row["Total"]/(row["GDP"]/100000000)

#drop all countries that aren`t mentioned in the media, sort the rest of countries by number of mentions    
    
data_not_null = data.drop(data[(data.Total == 0)].index).reset_index(drop=True)
data_not_null = data_not_null.sort_values(by='Total', ascending=False).reset_index(drop=True)

#create new subset, top-10 countries by mentions in the media

data_head = data_not_null.drop(data_not_null[(data_not_null.index > 10)].index).reset_index(drop=True)

#transform countries` names into indexes of DataFrame

data_not_null = data_not_null.set_index("Country")

#the first plot shows the rate of countries by numbers of their mentions

ax = data_not_null.plot(figsize=(120, 50), kind='bar', use_index=True, y="Total", fontsize=70)
ax.set_title('Rate of countries by mentions', fontsize=100, fontweight='bold')
ax.set_xlabel('Countries', fontsize=70, fontweight='bold')
ax.set_ylabel('Number of mentions', fontsize=60, fontweight='bold')

#the second plot shows distribution of top-10 countries between "population index" and "GDP index", created previously

ax1 = data_head.plot.scatter(figsize=(15, 15), x='Population_index', y='GDP_index', fontsize=7)
ax1.set_title('Indexed top-10 countries', fontsize=20, fontweight='bold')
for idx, row in data_head.iterrows():
    ax1.annotate(row['Country'], (row['Population_index'], row['GDP_index']), xytext=(5,-5),
                textcoords='offset points', family='sans-serif', fontsize=12)

#optionally drop the outliers, changing 'A' (and 'B') on appropriate countries` names
    
#data_head = data_head.drop(data_head[(data_head.Country == 'A') | (data_head.Country == 'B')].index).reset_index(drop=True)
