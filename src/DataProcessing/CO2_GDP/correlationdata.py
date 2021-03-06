def updatecountry(update, reference):
    """
    @Author Haoyang Ding
    make sure the update and reference have the same keys(country)
    :param update: a dict {country: {year: data}}
    :param reference: a dict {country: {year: data}}
    :return: None
    """
    assert isinstance(update, dict)
    assert isinstance(reference, dict)

    for i in list(update.keys()):
        if i not in list(reference.keys()):
            update.pop(i)


def updateyear(update, reference):
    """
    @Author Haoyang Ding
    make sure each value in update and reference has the same keys(year)
    :param update: a dict {country: {year: data}}
    :param reference: a dict {country: {year: data}}
    :return: None
    """
    assert isinstance(update, dict)
    assert isinstance(reference, dict)

    for i in list(update.keys()):
        temp1 = update[i]
        temp2 = reference[i]
        for j in list(temp1.keys()):
            if j not in temp2.keys() or temp1[j] == 0:
                temp1.pop(j)
        update[i] = temp1


def tempdata(data):
    """
    @Author Haoyang Ding
    change the data style from {country: {year: data}} to {country: [data]}
    :param data: a dict {country: {year: data}}
    :return: a dict {country: [data]}
    """
    assert isinstance(data, dict)

    temp = {}
    for i in list(data.keys()):
        temp[i] = []
        for j in list(data[i].keys()):
            temp[i].append(data[i][j])
    return temp


def dataframemaker(correlation):
    """
    @Author Haoyang Ding
    change the dict to a dataframe
    :param correlation: A dict which will be changed into dataframe
    :return: a dataframe
    """
    assert isinstance(correlation, dict)

    import pandas as pd
    correlationdf = pd.DataFrame({"country": list(correlation.keys()),
                                  "correlation": list(correlation.values())
                                  })
    return correlationdf


def correlationdata(nameco2emi, namegdp, developed, developing):
    """
    @Author Haoyang Ding
    calculate the correlation between co2 emission and gdp per capita of each country
    And write a file according to the correlation data of each country
    the file will be used for plotting word-cloud, correlation scatter plot.
    :param nameco2emi: annual-co-emissions-by-region.xlsx
    :param namegdp: average-real-gdp-per-capita-across-countries-and-regions.xlsx
    :param developed: a list with developed countries names
    :param developing: a list with developing countries names
    :return: None
    """
    assert isinstance(nameco2emi, str)
    assert isinstance(namegdp, str)
    assert isinstance(developed, list)
    assert isinstance(developing, list)

    import xlrd
    import pandas as pd
    import os
    import dictproducer

    fileaddress = os.path.abspath(os.path.join(os.getcwd(), "../../.."))
    co2address = os.path.abspath(os.path.join(fileaddress, "Data\OriginalData", nameco2emi))
    gdpaddress = os.path.abspath(os.path.join(fileaddress, "Data\OriginalData", namegdp))
    fileco2 = xlrd.open_workbook(filename=co2address)
    filegdp = xlrd.open_workbook(filename=gdpaddress)

    sheetco2 = fileco2.sheet_by_index(0)
    sheetgdp = filegdp.sheet_by_index(0)

    globalco2 = dictproducer.dictproducer_country(sheetco2)
    globalgdp = dictproducer.dictproducer_country(sheetgdp)

    # make sure these two datasets have same countries
    updatecountry(globalco2, globalgdp)
    updatecountry(globalgdp, globalco2)

    txtaddress = os.path.abspath(os.path.join(fileaddress, "Data\VisualizationData\CO2_GDP", "cleanglobalco2.txt"))
    f = open(txtaddress, "w")
    f.write(str(globalco2))
    f.close()

    # make sure every country's data has same years
    updateyear(globalco2, globalgdp)
    updateyear(globalgdp, globalco2)

    # now the country and year are same
    # I want to calculate the correlation rate between the gdppc and co2data per country

    tempco2 = tempdata(globalco2)
    tempgdp = tempdata(globalgdp)

    # now I have two big dict, key: country, value: co2 and gdp per year
    correlation = {}
    correlation = correlation.fromkeys(list(tempco2.keys()))
    correlation.pop("Taiwan")
    correlation.pop("World")
    correlation.pop("Hong Kong")
    for i in list(correlation.keys()):
        temps1 = pd.Series(tempco2[i])
        temps2 = pd.Series(tempgdp[i])
        correlation[i] = temps1.corr(temps2)

    correlationdf = dataframemaker(correlation)
    csvaddress=os.path.abspath(os.path.join(fileaddress, "Data\VisualizationData\CO2_GDP", "correlationdata.csv"))

    # pick 44 main developed and developing countries and clean the data.
    countrypick=developed +developing
    correlationpick={}
    developedtemp={}
    developingtemp={}
    for i in developed:
        developedtemp[i]=correlation[i]

    for i in developing:
        developingtemp[i] = correlation[i]

    for i in countrypick:
        correlationpick[i]=correlation[i]

    correlationpickdf = dataframemaker(correlationpick)
    developeddf = dataframemaker(developedtemp)
    developingdf = dataframemaker(developingtemp)

    csvaddress2 = os.path.abspath(os.path.join(fileaddress, "Data\VisualizationData\CO2_GDP", "correlationpick.csv"))
    csvaddress3 = os.path.abspath(os.path.join(fileaddress, "Data\VisualizationData\CO2_GDP", "developed.csv"))
    csvaddress4 = os.path.abspath(os.path.join(fileaddress, "Data\VisualizationData\CO2_GDP", "developing.csv"))

    correlationpickdf.to_csv(csvaddress2)
    developeddf.to_csv(csvaddress3)
    developingdf.to_csv(csvaddress4)

    tempsort = sorted(correlation.items(), key=lambda item: item[1])
    corindex = {}

    for i in range(len(tempsort)):
        country = tempsort[i][0]
        tempcountry = country.split()
        country = "".join(tempcountry)
        corindex[country] = i + 1

    txtaddress2 = os.path.abspath(os.path.join(fileaddress, "Data\VisualizationData\CO2_GDP", "wordcloud.txt"))
    f = open(txtaddress2, "w")
    for i in list(corindex.keys()):
        num = corindex[i] * 30
        for j in range(num):
            f.write(str(i))
            f.write(" ")
    f.close()