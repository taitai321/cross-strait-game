"""
台海战略博弈模拟器 (Streamlit Web版)
直接在手机/电脑浏览器上运行
"""

import streamlit as st
import random

# ========== 势力定义 (不变) ==========
FACTIONS = {
    "中国大陆": {
        "attributes": {"军事威慑力": 80, "经济影响力": 85, "国际话语权": 70,
                       "国内凝聚力": 95, "战略耐心": 60, "灰色地带控制力": 65, "法律战能力": 75},
        "description": "全方位工具箱，反'独'促统日益完备"
    },
    "台湾绿营(民进党)": {
        "attributes": {"执政合法性": 55, "民意支持": 40, "军事自保力": 15,
                       "经济韧性": 30, "外部支持度": 50, "认知作战力": 60, "岛内控制力": 55},
        "description": "顽固固守'台独'立场，用'抗中保台'蒙蔽民众"
    },
    "台湾蓝营(国民党)": {
        "attributes": {"政党凝聚力": 60, "民意支持": 35, "两岸沟通力": 75,
                       "地方执政优势": 55, "媒体话语权": 25, "和平牌效力": 50, "立法机构制衡力": 45},
        "description": "坚守'九二共识'、坚定反'独'"
    },
    "美国": {
        "attributes": {"军事介入决心": 40, "国会亲台势力": 60, "全球信誉": 45,
                       "中美关系温度": 25, "经济成本承受力": 55, "盟友跟随度": 40, "战略模糊性": 50},
        "description": "打'台湾牌'遏制中国，军售掏空台湾"
    },
    "日本": {
        "attributes": {"介入意愿": 30, "国内法理约束": 65, "对华经济依赖": 55,
                       "西南诸岛战备": 45, "右翼政治势力": 55, "日台勾连度": 35},
        "description": "高市早苗上台后，加速西南诸岛军事部署"
    },
    "欧盟/第三方": {
        "attributes": {"战略自主性": 40, "对华经贸依赖": 65, "涉台表态强度": 25,
                       "内部一致性": 30, "美国影响力": 55},
        "description": "安全靠美国，经济靠中国，涉台表态摇摆"
    }
}

# ========== 手牌库 (省略详细注释，保持原样) ==========
CARDS_MAINLAND = [
    {"id":"M01","name":"环台岛联合军演","type":"军事","cost":{"军事威慑力":-8,"战略耐心":-5,"国际话语权":-10},"probability":0.95,"effects":{"台湾绿营(民进党)":{"民意支持":-8,"经济韧性":-6,"执政合法性":-5},"台湾蓝营(国民党)":{"民意支持":+3,"两岸沟通力":+5},"美国":{"军事介入决心":+5,"中美关系温度":-10},"日本":{"介入意愿":+3,"西南诸岛战备":+5},"欧盟/第三方":{"涉台表态强度":+3}},"description":"大规模围岛军演，展示全域封控能力"},
    {"id":"M02","name":"海警环台岛执法巡查","type":"灰色地带","cost":{"灰色地带控制力":-5,"战略耐心":-3},"probability":0.90,"effects":{"台湾绿营(民进党)":{"军事自保力":-5,"岛内控制力":-8,"经济韧性":-4},"台湾蓝营(国民党)":{"和平牌效力":+5},"美国":{"战略模糊性":-8,"军事介入决心":-2},"日本":{"介入意愿":-3},"欧盟/第三方":{"涉台表态强度":-5}},"description":"海警在台岛周边常态化执法，实质推进管辖"},
    {"id":"M03","name":"制裁参与对台军售美企","type":"经济","cost":{"经济影响力":-3,"国际话语权":-5},"probability":0.88,"effects":{"美国":{"经济成本承受力":-10,"国会亲台势力":-5},"台湾绿营(民进党)":{"外部支持度":-5,"军事自保力":-3}},"description":"依据反外国制裁法，精准打击军工企业"},
    {"id":"M04","name":"依法惩治'台独'顽固分子","type":"法律","cost":{"法律战能力":-3,"战略耐心":-2},"probability":0.92,"effects":{"台湾绿营(民进党)":{"执政合法性":-8,"岛内控制力":-6,"民意支持":-3},"台湾蓝营(国民党)":{"民意支持":+3,"和平牌效力":+5},"美国":{"战略模糊性":-5}},"description":"依据惩独22条，终身追责"},
    {"id":"M05","name":"发布惠台新政","type":"融合发展","cost":{"经济影响力":-5,"战略耐心":-3},"probability":0.90,"effects":{"台湾蓝营(国民党)":{"民意支持":+10,"两岸沟通力":+8,"政党凝聚力":+5},"台湾绿营(民进党)":{"民意支持":-5,"经济韧性":+3},"中国大陆":{"国际话语权":+5}},"description":"十项惠台措施，以融促统"},
    {"id":"M06","name":"关键战略资源出口管制","type":"经济","cost":{"经济影响力":-5,"国际话语权":-8},"probability":0.85,"effects":{"美国":{"经济成本承受力":-12,"军事介入决心":-5},"日本":{"对华经济依赖":-8,"介入意愿":-5},"欧盟/第三方":{"对华经贸依赖":-6}},"description":"稀土、镓、锗出口管制，直击军工供应链"},
    {"id":"M07","name":"取消台农产品零关税优惠","type":"经济","cost":{"经济影响力":-2,"国际话语权":-3},"probability":0.93,"effects":{"台湾绿营(民进党)":{"民意支持":-8,"执政合法性":-5,"经济韧性":-6},"台湾蓝营(国民党)":{"和平牌效力":+3,"民意支持":+2}},"description":"精准打击绿营票仓产业"},
    {"id":"M08","name":"中美元首会晤划红线","type":"外交","cost":{"战略耐心":-10,"国际话语权":-3},"probability":0.75,"effects":{"中国大陆":{"国际话语权":+8},"美国":{"中美关系温度":+15,"军事介入决心":-8,"战略模糊性":+5},"台湾绿营(民进党)":{"外部支持度":-10,"民意支持":-5},"台湾蓝营(国民党)":{"和平牌效力":+8},"欧盟/第三方":{"涉台表态强度":-5}},"description":"习近平会见特朗普，明确红线"},
    {"id":"M09","name":"国际'一中原则'巩固行动","type":"外交","cost":{"国际话语权":-3,"战略耐心":-2},"probability":0.88,"effects":{"台湾绿营(民进党)":{"外部支持度":-8,"执政合法性":-4},"美国":{"战略模糊性":-5},"欧盟/第三方":{"涉台表态强度":-5,"战略自主性":+3}},"description":"巩固183国建交共识"},
    {"id":"M10","name":"邀请岛内媒体/政党赴大陆交流","type":"认知/融合","cost":{"经济影响力":-2,"战略耐心":-2},"probability":0.90,"effects":{"台湾蓝营(国民党)":{"民意支持":+8,"媒体话语权":+10,"两岸沟通力":+5},"台湾绿营(民进党)":{"认知作战力":-10,"民意支持":-3},"中国大陆":{"国际话语权":+5}},"description":"打破'台独'叙事垄断"},
    {"id":"M11","name":"强化海峡中线灰色地带存在","type":"灰色地带","cost":{"灰色地带控制力":-3,"战略耐心":-5,"国际话语权":-5},"probability":0.92,"effects":{"台湾绿营(民进党)":{"军事自保力":-8,"岛内控制力":-5},"美国":{"军事介入决心":+3,"战略模糊性":-5}},"description":"军机舰常态化突破所谓中线"},
    {"id":"M12","name":"发表对台政策白皮书/重磅讲话","type":"政治","cost":{"战略耐心":-3},"probability":0.95,"effects":{"中国大陆":{"国际话语权":+5,"国内凝聚力":+3},"台湾蓝营(国民党)":{"两岸沟通力":+5,"和平牌效力":+3},"台湾绿营(民进党)":{"执政合法性":-5,"认知作战力":-5},"美国":{"战略模糊性":-3}},"description":"阐明政策方向，设定统一框架"},
]

CARDS_GREEN = [
    {"id":"G01","name":"推动渐进式'法理台独'","type":"政治挑衅","cost":{"执政合法性":-5,"民意支持":-3,"外部支持度":-3},"probability":0.55,"effects":{"中国大陆":{"军事威慑力":+10,"战略耐心":-15},"台湾蓝营(国民党)":{"和平牌效力":+10,"民意支持":+3},"美国":{"军事介入决心":-3,"战略模糊性":-8},"欧盟/第三方":{"涉台表态强度":+5,"内部一致性":-5}},"description":"修改两岸条例，试探红线"},
    {"id":"G02","name":"渲染'抗中保台'认知作战","type":"认知作战","cost":{"认知作战力":-3,"民意支持":-2},"probability":0.70,"effects":{"台湾绿营(民进党)":{"民意支持":+8,"执政合法性":+5},"台湾蓝营(国民党)":{"民意支持":-5,"媒体话语权":-3},"中国大陆":{"国际话语权":-3}},"description":"通过三民自及网军制造'抗中'声浪"},
    {"id":"G03","name":"向美国游说加大军售","type":"外部倚靠","cost":{"经济韧性":-8,"民意支持":-3,"执政合法性":-3},"probability":0.65,"effects":{"美国":{"国会亲台势力":+8,"经济成本承受力":+5},"中国大陆":{"军事威慑力":+8},"台湾绿营(民进党)":{"军事自保力":+5,"外部支持度":+5}},"description":"提出特别防务预算案，交保护费"},
    {"id":"G04","name":"污名化大陆惠台政策","type":"认知作战","cost":{"认知作战力":-5,"民意支持":-3},"probability":0.55,"effects":{"台湾蓝营(国民党)":{"民意支持":+5,"两岸沟通力":+3},"台湾绿营(民进党)":{"民意支持":-5},"中国大陆":{"国际话语权":-3}},"description":"定性为'统战胁迫'"},
    {"id":"G05","name":"限制大陆APP/产品","type":"社会控制","cost":{"民意支持":-5,"岛内控制力":-3},"probability":0.60,"effects":{"台湾绿营(民进党)":{"认知作战力":+5},"中国大陆":{"经济影响力":-3},"台湾蓝营(国民党)":{"民意支持":+3}},"description":"以安全为由限制小红书等"},
    {"id":"G06","name":"炒作'滨海作战指挥部'成立","type":"军事","cost":{"军事自保力":-3,"经济韧性":-5},"probability":0.75,"effects":{"台湾绿营(民进党)":{"执政合法性":+3},"中国大陆":{"军事威慑力":+5},"美国":{"军事介入决心":+2}},"description":"备战谋'独'动向"},
    {"id":"G07","name":"打击岛内异见/制造'绿色恐怖'","type":"内部镇压","cost":{"民意支持":-8,"执政合法性":-3,"岛内控制力":-3},"probability":0.80,"effects":{"台湾蓝营(国民党)":{"民意支持":+5,"政党凝聚力":+3},"中国大陆":{"国际话语权":+3}},"description":"以法律查办威胁两岸交流人士"},
    {"id":"G08","name":"推动'脱中入美'经济路线","type":"经济","cost":{"经济韧性":-10,"民意支持":-8,"执政合法性":-3},"probability":0.60,"effects":{"台湾蓝营(国民党)":{"民意支持":+8,"政党凝聚力":+5},"美国":{"经济成本承受力":+5},"中国大陆":{"经济影响力":+3}},"description":"配合美国高额关税，掏空制造业"},
]

CARDS_BLUE = [
    {"id":"B01","name":"国共两党高层对话与大陆参访","type":"两岸交流","cost":{"政党凝聚力":-3,"媒体话语权":-3},"probability":0.88,"effects":{"台湾蓝营(国民党)":{"两岸沟通力":+12,"和平牌效力":+15,"民意支持":+8},"台湾绿营(民进党)":{"执政合法性":-5,"认知作战力":-8,"民意支持":-3},"中国大陆":{"战略耐心":+8,"国际话语权":+5},"美国":{"战略模糊性":-5}},"description":"郑丽文和平之旅，国共领导人会面"},
    {"id":"B02","name":"杯葛不合理防务预算","type":"立法制衡","cost":{"立法机构制衡力":-5,"政党凝聚力":-3},"probability":0.80,"effects":{"台湾绿营(民进党)":{"军事自保力":-8,"经济韧性":-5,"执政合法性":-5},"台湾蓝营(国民党)":{"民意支持":+8,"和平牌效力":+10,"政党凝聚力":+5},"中国大陆":{"战略耐心":+5},"美国":{"国会亲台势力":-5}},"description":"军购条例预算上限大幅削减"},
    {"id":"B03","name":"赴美抢占国际话语权","type":"国际发声","cost":{"政党凝聚力":-5,"媒体话语权":-3},"probability":0.75,"effects":{"台湾蓝营(国民党)":{"和平牌效力":+10,"两岸沟通力":+5,"媒体话语权":+8},"台湾绿营(民进党)":{"外部支持度":-8,"认知作战力":-5},"美国":{"战略模糊性":+5,"军事介入决心":-5},"日本":{"介入意愿":-3}},"description":"郑丽文接受外媒专访，阐述避战路线"},
    {"id":"B04","name":"推动地方县市两岸经济合作","type":"经济惠台","cost":{"地方执政优势":-5,"政党凝聚力":-3},"probability":0.85,"effects":{"台湾蓝营(国民党)":{"民意支持":+10,"地方执政优势":+5,"和平牌效力":+8},"台湾绿营(民进党)":{"民意支持":-5,"执政合法性":-3},"中国大陆":{"经济影响力":+5,"国际话语权":+3}},"description":"蓝营县市积极推动两岸经贸交流"},
    {"id":"B05","name":"利用蓝营媒体曝光'台独'危害","type":"认知/媒体","cost":{"媒体话语权":-3},"probability":0.78,"effects":{"台湾蓝营(国民党)":{"民意支持":+5,"和平牌效力":+8,"媒体话语权":+5},"台湾绿营(民进党)":{"认知作战力":-10,"民意支持":-5,"执政合法性":-3}},"description":"中国时报、联合报等揭露战争风险"},
    {"id":"B06","name":"推动蓝白在野整合","type":"政治联盟","cost":{"政党凝聚力":-8,"地方执政优势":-3},"probability":0.65,"effects":{"台湾蓝营(国民党)":{"立法机构制衡力":+10,"政党凝聚力":+5,"和平牌效力":+8},"台湾绿营(民进党)":{"执政合法性":-10,"岛内控制力":-8,"民意支持":-3}},"description":"2026年九合一蓝白合力度增强"},
]

CARDS_US = [
    {"id":"U01","name":"批准大规模对台军售","type":"军事","cost":{"中美关系温度":-18,"全球信誉":-8,"战略模糊性":-5},"probability":0.90,"effects":{"中国大陆":{"军事威慑力":+12,"战略耐心":-20},"台湾绿营(民进党)":{"外部支持度":+10,"军事自保力":+3},"美国":{"国会亲台势力":+5,"经济成本承受力":+5},"日本":{"介入意愿":+3}},"description":"111亿美元军售创纪录"},
    {"id":"U02","name":"签署涉台国防授权法案","type":"法律","cost":{"中美关系温度":-15,"全球信誉":-5},"probability":0.85,"effects":{"中国大陆":{"军事威慑力":+8,"法律战能力":+5},"台湾绿营(民进党)":{"外部支持度":+8,"军事自保力":+3},"美国":{"国会亲台势力":+8},"日本":{"介入意愿":+3}},"description":"2026财年授权法案，推动台湾参加环太军演"},
    {"id":"U03","name":"AIT约见各党候选人划红线","type":"政治干预","cost":{"全球信誉":-3},"probability":0.85,"effects":{"台湾绿营(民进党)":{"外部支持度":+5,"执政合法性":-3},"台湾蓝营(国民党)":{"两岸沟通力":-3},"中国大陆":{"国际话语权":+3}},"description":"选举期间施压在野党"},
    {"id":"U04","name":"中美元首会晤管控危机","type":"外交","cost":{"中美关系温度":-5,"国会亲台势力":-3},"probability":0.70,"effects":{"美国":{"中美关系温度":+15,"军事介入决心":-8,"战略模糊性":+8},"中国大陆":{"战略耐心":+10,"国际话语权":+5},"台湾绿营(民进党)":{"外部支持度":-8,"执政合法性":-5},"台湾蓝营(国民党)":{"和平牌效力":+8},"欧盟/第三方":{"涉台表态强度":-5}},"description":"特朗普表态不认同台独"},
    {"id":"U05","name":"鼓动盟友联合涉台表态/军演","type":"外交军事","cost":{"盟友跟随度":-8,"全球信誉":-5},"probability":0.55,"effects":{"日本":{"介入意愿":+5,"西南诸岛战备":+8},"欧盟/第三方":{"涉台表态强度":+8,"内部一致性":-5},"中国大陆":{"军事威慑力":+5,"国际话语权":-5}},"description":"推动盟友配合，但明哲保身者多"},
    {"id":"U06","name":"施压台积电赴美设厂","type":"经济科技","cost":{"全球信誉":-5,"经济成本承受力":-3},"probability":0.80,"effects":{"台湾绿营(民进党)":{"经济韧性":-8,"外部支持度":-3},"美国":{"经济成本承受力":+5},"中国大陆":{"经济影响力":+5}},"description":"掏空台湾硅盾"},
    {"id":"U07","name":"金融制裁威胁","type":"金融","cost":{"全球信誉":-10,"经济成本承受力":-10},"probability":0.40,"effects":{"中国大陆":{"经济影响力":-5,"军事威慑力":-3},"美国":{"经济成本承受力":-15,"中美关系温度":-25},"欧盟/第三方":{"对华经贸依赖":-10,"战略自主性":+5}},"description":"威胁排除SWIFT，可信度低"},
    {"id":"U08","name":"军舰穿越台湾海峡","type":"军事","cost":{"中美关系温度":-10,"战略模糊性":-5},"probability":0.82,"effects":{"中国大陆":{"军事威慑力":+5,"灰色地带控制力":+3},"台湾绿营(民进党)":{"外部支持度":+5},"日本":{"介入意愿":+3}},"description":"展示航行自由"},
]

CARDS_JAPAN = [
    {"id":"J01","name":"抛出'台湾有事即日本有事'论调","type":"政治挑衅","cost":{"对华经济依赖":-8,"国内法理约束":-5,"介入意愿":-3},"probability":0.72,"effects":{"中国大陆":{"军事威慑力":+8,"国际话语权":-3},"台湾绿营(民进党)":{"外部支持度":+5},"美国":{"盟友跟随度":+5},"欧盟/第三方":{"涉台表态强度":+3}},"description":"高市早苗在国会发言"},
    {"id":"J02","name":"西南诸岛加速军事部署","type":"军事","cost":{"介入意愿":-5,"对华经济依赖":-5},"probability":0.80,"effects":{"日本":{"西南诸岛战备":+10,"介入意愿":+3},"中国大陆":{"军事威慑力":+5},"台湾绿营(民进党)":{"外部支持度":+3}},"description":"导弹、雷达、快速反应部队进驻"},
    {"id":"J03","name":"以'撤侨'为幌子联合军演","type":"军事","cost":{"介入意愿":-5,"对华经济依赖":-5},"probability":0.65,"effects":{"日本":{"西南诸岛战备":+5,"介入意愿":+3},"中国大陆":{"军事威慑力":+8},"美国":{"军事介入决心":+3}},"description":"邀美入局，离间中美"},
    {"id":"J04","name":"日台产业链勾连","type":"经济","cost":{"对华经济依赖":-5},"probability":0.70,"effects":{"台湾绿营(民进党)":{"外部支持度":+5,"经济韧性":+3},"中国大陆":{"经济影响力":-3}},"description":"半导体等领域合作政治化"},
]

CARDS_EU = [
    {"id":"E01","name":"发表涉台声明施压","type":"外交","cost":{"对华经贸依赖":-5,"内部一致性":-3},"probability":0.55,"effects":{"台湾绿营(民进党)":{"外部支持度":+5},"中国大陆":{"国际话语权":-5},"美国":{"盟友跟随度":+3}},"description":"少数国家指责破坏台海稳定"},
    {"id":"E02","name":"派舰象征性'航行自由'行动","type":"军事","cost":{"对华经贸依赖":-5,"战略自主性":-3},"probability":0.45,"effects":{"中国大陆":{"军事威慑力":+3},"台湾绿营(民进党)":{"外部支持度":+3},"美国":{"盟友跟随度":+5}},"description":"规模极小，效果有限"},
    {"id":"E03","name":"重申一个中国政策","type":"外交","cost":{"美国影响力":-3},"probability":0.80,"effects":{"中国大陆":{"国际话语权":+8},"台湾绿营(民进党)":{"外部支持度":-5},"欧盟/第三方":{"战略自主性":+5,"内部一致性":+3}},"description":"多数成员国坚持一中原则"},
    {"id":"E04","name":"对华经贸合作深化","type":"经济","cost":{"美国影响力":-5},"probability":0.72,"effects":{"欧盟/第三方":{"对华经贸依赖":+8,"战略自主性":+8},"中国大陆":{"经济影响力":+8,"国际话语权":+5},"美国":{"盟友跟随度":-8},"台湾绿营(民进党)":{"外部支持度":-5}},"description":"经济利益压过意识形态"},
]

ALL_CARDS = {
    "中国大陆": CARDS_MAINLAND,
    "台湾绿营(民进党)": CARDS_GREEN,
    "台湾蓝营(国民党)": CARDS_BLUE,
    "美国": CARDS_US,
    "日本": CARDS_JAPAN,
    "欧盟/第三方": CARDS_EU
}

# ========== 大事件 (不变) ==========
EVENTS = [
    {"id":"EV01","name":"佩洛西式众议长访台","trigger_round":(3,8),"effects":{"中国大陆":{"军事威慑力":+12,"战略耐心":-20},"台湾绿营(民进党)":{"外部支持度":+15,"民意支持":+5},"台湾蓝营(国民党)":{"和平牌效力":+10},"美国":{"中美关系温度":-20,"国会亲台势力":+10,"战略模糊性":-15},"日本":{"介入意愿":+5},"欧盟/第三方":{"涉台表态强度":+8}},"description":"美高层政治人物窜台"},
    {"id":"EV02","name":"台湾地区领导人选举","trigger_round":(5,10),"effects":{"台湾绿营(民进党)":{"民意支持":+10,"执政合法性":+15},"台湾蓝营(国民党)":{"政党凝聚力":-5},"中国大陆":{"军事威慑力":+5,"战略耐心":-8},"美国":{"国会亲台势力":+5}},"description":"选举结果影响两岸走向"},
    {"id":"EV03","name":"美国大规模对台军售","trigger_round":(2,6),"effects":{"中国大陆":{"军事威慑力":+10,"战略耐心":-15},"台湾绿营(民进党)":{"军事自保力":+5,"外部支持度":+10},"美国":{"中美关系温度":-15,"国会亲台势力":+8},"日本":{"介入意愿":+3}},"description":"百亿军售，大陆反制"},
    {"id":"EV04","name":"中美元首会晤(机遇窗口)","trigger_round":(7,15),"effects":{"中国大陆":{"国际话语权":+5,"战略耐心":+10},"美国":{"中美关系温度":+10,"军事介入决心":-5,"战略模糊性":+5},"台湾蓝营(国民党)":{"和平牌效力":+8},"台湾绿营(民进党)":{"外部支持度":-5},"欧盟/第三方":{"涉台表态强度":-5}},"description":"习近平划红线，特朗普表态不认同台独"},
    {"id":"EV05","name":"国民党主席率团访陆","trigger_round":(4,12),"effects":{"台湾蓝营(国民党)":{"两岸沟通力":+10,"和平牌效力":+15,"民意支持":+8},"台湾绿营(民进党)":{"执政合法性":-5,"认知作战力":-5},"中国大陆":{"战略耐心":+8,"国际话语权":+5}},"description":"郑丽文和平之旅"},
    {"id":"EV06","name":"台湾内部政治危机","trigger_round":(8,18),"effects":{"台湾绿营(民进党)":{"执政合法性":-15,"民意支持":-10,"岛内控制力":-10},"台湾蓝营(国民党)":{"民意支持":+8,"政党凝聚力":+5},"中国大陆":{"国际话语权":+5}},"description":"赖清德遭弹劾，岛内动荡"},
    {"id":"EV07","name":"日本右翼突破红线","trigger_round":(6,14),"effects":{"日本":{"右翼政治势力":+10,"介入意愿":+8},"中国大陆":{"军事威慑力":+8,"国际话语权":-3},"美国":{"盟友跟随度":+5},"欧盟/第三方":{"涉台表态强度":+5}},"description":"允许台高级官员窜访东京"},
    {"id":"EV08","name":"欧盟内部涉台分歧爆发","trigger_round":(9,20),"effects":{"欧盟/第三方":{"内部一致性":-15,"涉台表态强度":-8,"战略自主性":+5},"美国":{"盟友跟随度":-8},"中国大陆":{"国际话语权":+8}},"description":"多数国家回归一中框架"},
]

# ========== 游戏逻辑类 (适配Streamlit) ==========
class CrossStraitGame:
    def __init__(self):
        self.factions = {}
        for name, data in FACTIONS.items():
            self.factions[name] = {
                "attributes": data["attributes"].copy(),
                "description": data["description"]
            }
        self.round = 0
        self.log = []
        self.triggered_events = set()
        self.game_over = False
        self.game_result = ""

    def clamp(self, v):
        return max(0, min(100, v))

    def apply_effects(self, effects, probability=1.0):
        if random.random() > probability:
            return False
        for faction, attr_changes in effects.items():
            if faction in self.factions:
                for attr, change in attr_changes.items():
                    if attr in self.factions[faction]["attributes"]:
                        old = self.factions[faction]["attributes"][attr]
                        self.factions[faction]["attributes"][attr] = self.clamp(old + change)
        return True

    def check_events(self):
        for event in EVENTS:
            if event["id"] in self.triggered_events:
                continue
            mn, mx = event["trigger_round"]
            if mn <= self.round <= mx and random.random() < 0.30:
                self.apply_effects(event["effects"])
                self.log.append(f"【大事件】{event['name']}：{event['description']}")
                self.triggered_events.add(event["id"])
                return True
        return False

    def check_game_over(self):
        f = self.factions
        attrs = lambda faction, attr: f[faction]["attributes"].get(attr, 0)

        # 结局1
        if attrs("中国大陆","军事威慑力") >= 95 and attrs("台湾绿营(民进党)","民意支持") <= 15 and attrs("美国","军事介入决心") <= 15:
            self.game_over = True; self.game_result = "和平统一窗口开启"; return True
        # 结局2
        if attrs("中国大陆","战略耐心") <= 5 and attrs("台湾绿营(民进党)","执政合法性") >= 70 and attrs("美国","军事介入决心") >= 70:
            self.game_over = True; self.game_result = "台海冲突风险急剧升高"; return True
        # 结局3
        if attrs("台湾绿营(民进党)","执政合法性") <= 10 and attrs("台湾绿营(民进党)","民意支持") <= 10:
            self.game_over = True; self.game_result = "民进党政权崩溃"; return True
        # 结局4
        if attrs("美国","军事介入决心") <= 5 and attrs("美国","中美关系温度") >= 70 and attrs("中国大陆","灰色地带控制力") >= 90:
            self.game_over = True; self.game_result = "美国实质退出干预"; return True
        # 结局5
        if attrs("台湾蓝营(国民党)","民意支持") >= 60 and attrs("台湾蓝营(国民党)","和平牌效力") >= 80 and attrs("台湾绿营(民进党)","执政合法性") <= 25:
            self.game_over = True; self.game_result = "国民党主导和平对话"; return True
        # 持久战
        if self.round >= 24:
            self.game_over = True
            self.game_result = "持久消耗战，大陆优势持续扩大" if attrs("中国大陆","灰色地带控制力") >= 70 else "僵局持续"
            return True
        return False

    def ai_choose_card(self, faction_name):
        cards = ALL_CARDS.get(faction_name, [])
        if not cards:
            return None
        f_attrs = self.factions[faction_name]["attributes"]
        affordable = []
        for card in cards:
            can = True
            for attr, cost in card["cost"].items():
                if f_attrs.get(attr, 100) + cost < 5:
                    can = False
                    break
            if can:
                affordable.append(card)
        if not affordable:
            return None
        # 蓝营AI偏向增益牌
        if faction_name == "台湾蓝营(国民党)":
            for card in affordable:
                if card["type"] in ["两岸交流","立法制衡","经济惠台"]:
                    if f_attrs.get("政党凝聚力",0) >= 30:
                        return card
            affordable_sorted = sorted(affordable, key=lambda c: -sum(abs(v) for v in c["cost"].values()))
            return affordable_sorted[-1]
        return random.choice(affordable)

    def run_round(self, player_choice):
        self.round += 1
        self.check_events()
        # 玩家出牌
        if player_choice:
            card = player_choice
            f_attrs = self.factions["中国大陆"]["attributes"]
            can_afford = all(f_attrs.get(attr, 100) + cost >= 0 for attr, cost in card["cost"].items())
            if can_afford:
                self.apply_effects(card["cost"])
                success = self.apply_effects(card["effects"], card["probability"])
                self.log.append(f"[大陆] 打出【{card['name']}】{'✓ 成功' if success else '✗ 失败'}")
            else:
                self.log.append(f"[大陆] 试图打出【{card['name']}】但代价不足")
        # AI出牌
        for faction in ["台湾绿营(民进党)","台湾蓝营(国民党)","美国","日本","欧盟/第三方"]:
            card = self.ai_choose_card(faction)
            if card:
                self.apply_effects(card["cost"])
                success = self.apply_effects(card["effects"], card["probability"])
                if success:
                    self.log.append(f"[{faction}] 打出【{card['name']}】")

        if self.check_game_over():
            return False
        return True


# ========== Streamlit 界面 ==========
def main():
    st.set_page_config(page_title="台海战略博弈模拟器", layout="wide")
    st.title("🎯 台海战略博弈模拟器")
    st.markdown("**基于2025-2026年现实事件设计 | 你扮演中国大陆**")

    # 初始化游戏状态
    if 'game' not in st.session_state:
        st.session_state.game = CrossStraitGame()
        st.session_state.log = []
        st.session_state.round_info = ""

    game = st.session_state.game

    # 如果游戏结束，显示结局
    if game.game_over:
        st.error(f"## 游戏结束：{game.game_result}")
        # 显示最终属性
        for name, data in game.factions.items():
            st.subheader(name)
            for attr, val in data["attributes"].items():
                st.progress(val/100, text=f"{attr}：{val}")
        st.subheader("📜 完整事件日志")
        for entry in game.log:
            st.text(entry)
        if st.button("🔄 重新开始"):
            del st.session_state.game
            st.rerun()
        return

    # 显示当前回合
    st.header(f"第 {game.round} 回合")

    # 显示各方属性
    cols = st.columns(3)
    for i, (name, data) in enumerate(game.factions.items()):
        with cols[i % 3]:
            st.subheader(name)
            for attr, val in data["attributes"].items():
                st.progress(val/100, text=f"{attr}：{val}")
            st.caption(data["description"])

    # 玩家选择手牌
    st.header("🎴 中国大陆可用手牌（你选择一张）")
    cards = CARDS_MAINLAND
    card_names = [f"{c['id']} {c['name']} ({c['type']}) 代价:{c['cost']}" for c in cards]
    selected_idx = st.selectbox("选择手牌", range(len(cards)), format_func=lambda x: card_names[x])
    selected_card = cards[selected_idx]

    # 显示选中手牌的详细信息
    st.info(f"**{selected_card['name']}** | 成功率：{selected_card['probability']*100:.0f}%\n\n{selected_card['description']}")

    # 推进回合按钮
    if st.button("⏭️ 打出此牌，推进一回合"):
       game.run_round(selected_card)
       st.rerun()  # 原来是 st.experimental_rerun()

    # 显示最近日志
    st.subheader("📋 最近事件日志")
    for entry in game.log[-5:]:
        st.text(entry)

if __name__ == "__main__":
    main()
