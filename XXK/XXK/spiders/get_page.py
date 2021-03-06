import requests
from lxml import etree
from .get_proxies_ua import get_ua

BJX = ['赵', '钱', '孙', '李', '周', '吴', '郑', '王','冯', '陈', '褚', '卫', '蒋', '沈', '韩', '杨',
       '朱', '秦', '尤', '许', '何', '吕', '施', '张','孔', '曹', '严', '华', '金', '魏', '陶', '姜',
       '戚', '谢', '邹', '喻', '柏', '水', '窦', '章','云', '苏', '潘', '葛', '奚', '范', '彭', '郎',
       '鲁', '韦', '昌', '马', '苗', '凤', '花', '方','俞', '任', '袁', '柳', '酆', '鲍', '史', '唐',
       '费', '廉', '岑', '薛', '雷', '贺', '倪', '汤','滕', '殷', '罗', '毕', '郝', '邬', '安', '常',
       '乐', '于', '时', '傅', '皮', '卞', '齐', '康','伍', '余', '元', '卜', '顾', '孟', '平', '黄',
       '和', '穆', '萧', '尹', '姚', '邵', '湛', '汪','祁', '毛', '禹', '狄', '米', '贝', '明', '臧',
       '计', '伏', '成', '戴', '谈', '宋', '茅', '庞','高', '夏', '蔡', '田', '樊', '胡', '凌', '霍',
       '虞', '万', '支', '柯', '昝', '管', '卢', '莫','经', '房', '裘', '缪', '干', '解', '应', '宗',
       '丁', '宣', '贲', '邓', '郁', '单', '杭', '洪','包', '诸', '左', '石', '崔', '吉', '钮', '龚',
       '程', '嵇', '邢', '滑', '裴', '陆', '荣', '翁','荀', '羊', '於', '惠', '甄', '曲', '家', '封',
       '宁', '仇', '栾', '暴', '甘', '钭', '厉', '戎','祖', '武', '符', '刘', '景', '詹', '束', '龙',
       '叶', '幸', '司', '韶', '郜', '黎', '蓟', '薄','印', '宿', '白', '怀', '蒲', '邰', '从', '鄂',
       '索', '咸', '籍', '赖', '卓', '蔺', '屠', '蒙','池', '乔', '阴', '鬱', '胥', '能', '苍', '双',
       '闻', '莘', '党', '翟', '谭', '贡', '劳', '逄','姬', '申', '扶', '堵', '冉', '宰', '郦', '雍',
       '郤', '璩', '桑', '桂', '濮', '牛', '寿', '通','边', '扈', '燕', '冀', '郏', '浦', '尚', '农',
       '温', '别', '庄', '晏', '柴', '瞿', '阎', '充','慕', '连', '茹', '习', '宦', '艾', '鱼', '容',
       '向', '古', '易', '慎', '戈', '廖', '庾', '终','暨', '居', '衡', '步', '都', '耿', '满', '弘',
       '匡', '国', '文', '寇', '广', '禄', '阙', '东','欧', '殳', '沃', '利', '蔚', '越', '夔', '隆',
       '师', '巩', '厍', '聂', '晁', '勾(句)', '敖', '融','冷', '訾', '辛', '阚', '那', '简', '饶', '空',
       '曾', '毋', '沙', '乜', '养', '鞠', '须', '丰','巢', '关', '蒯', '相', '查', '后', '荆', '红',
       '游', '竺', '权', '逯', '盖', '益', '桓', '公','万俟', '司马', '上官', '欧阳', '夏侯', '诸葛',
       '闻人', '东方', '赫连', '皇甫', '尉迟', '公羊','澹台', '公冶', '宗政', '濮阳', '淳于', '单于',
       '太叔', '申屠', '公孙', '仲孙', '轩辕', '令狐','钟离', '宇文', '长孙', '慕容', '鲜于', '闾丘',
       '司徒', '司空', '丌官', '司寇', '仉', '督', '子车','颛孙', '端木', '巫马', '公西', '漆雕', '乐正',
       '壤驷', '公良', '拓跋', '夹谷', '宰父', '谷梁','晋', '楚', '闫', '法', '汝', '鄢', '涂', '钦',
       '段干', '百里', '东郭', '南门', '呼延', '归','海', '羊舌', '微生', '岳', '帅', '缑', '亢',
       '况', '郈', '有', '琴', '梁丘', '左丘', '东门','西门', '商', '牟', '佘', '佴', '伯', '赏', '南宫',
       '墨', '哈', '谯', '笪', '年', '爱', '阳', '佟', '第五', '言', '福']

def get_page():
    '''
    获取每个类别下每个关键字所对应的页数
    :return: {类型:{字:页数}}
    '''
    results = {}
    for c in ['24','25']:
        result = {}
        for x in BJX:
            url = 'http://hd.chinatax.gov.cn/xxk/action/ListXxk.do'
            datas={
                'categeryid': c,
                'querystring24': 'articlefield02',
                'querystring25': 'articlefield02',
                'queryvalue': x
            }
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Connection': 'keep-alive',
                'Host': 'hd.chinatax.gov.cn',
                'Origin': 'http://hd.chinatax.gov.cn',
                'Referer': 'http://hd.chinatax.gov.cn/xxk/',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': get_ua(),
                # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',}
            }
            proxies = {
                "http" : "http://115.224.68.24:2314"   # 代理ip
            }

            res = requests.post(url,data=datas,headers=headers,proxies=proxies)
            # 动态获取cookies
            cookies = requests.utils.dict_from_cookiejar(res.cookies)
            # 带cookies再发请求
            response = requests.post(url,data=datas,headers=headers,proxies=proxies,cookies=cookies).text
            # print(response)
            html = etree.HTML(response)
            page = html.xpath('//td[@valign="bottom"]/text()')[0][5]    # 页数
            result.update({x:page})
        results.update({c:result})
        return results