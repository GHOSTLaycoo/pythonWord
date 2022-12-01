import pandas as pd

def excelWork():
    pdf = pd.DataFrame(pd.read_excel("C:/Users/GHOSTLaycoo/Desktop/营销场景二/账户日交易明细查询11.10.xls"))
    pdf.drop(len(pdf)-1,inplace=True)
    pdf_hs = pdf[pdf.使用单位 == '国网湖北省电力有限公司黄石供电公司本部']
    pdf_hs.sort_values(by='交易时间',inplace=True)

    pdf_hs.to_excel("C:/Users/GHOSTLaycoo/Desktop/营销场景二/data/temp1.xlsx",index=False)

    start_time = str(pdf_hs['交易时间'].values[1])[0:10]
    end_time = str(pdf_hs['交易时间'].values[len(pdf_hs)-1])[0:10]
    print([start_time,end_time])

if __name__ == '__main__':
    excelWork()

