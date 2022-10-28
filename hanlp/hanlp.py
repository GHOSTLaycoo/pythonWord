from hanlp_restful import HanLPClient

if __name__ == '__main__':
    HanLP = HanLPClient('https://www.hanlp.com/api', auth=None, language='zh')
    print(HanLP.parse('十多年后你的儿子开宝马上大学，暑假练习开飞机小三偷偷怀孕闹着要跟你结婚，40多度的夏天，你的别墅宽敞而凉爽，每餐都要小酌一杯2000年以前的飞天茅台，经常约了新的嫩模，累到一个人半夜躲到了阳台抽烟，而造成的这一切原因，仅仅是因为2022年的10月27号找到我然后点开我的头像对我打出了4个字，我做代理！'))