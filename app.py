import streamlit as st
from datetime import datetime
from PIL import Image, ImageDraw
import random
import os
from dotenv import load_dotenv

load_dotenv()

THREADS_ID = "@사주포커스"
INSTA_ID = os.getenv("INSTA_ID", "")
BANK_NAME = os.getenv("BANK_NAME", "은행명")
BANK_ACCOUNT = os.getenv("BANK_ACCOUNT", "계좌번호")
BANK_HOLDER = os.getenv("BANK_HOLDER", "예금주명")

띠_맵 = {
    0: "원숭이띠", 1: "닭띠", 2: "개띠", 3: "돼지띠",
    4: "쥐띠", 5: "소띠", 6: "호랑이띠", 7: "토끼띠",
    8: "용띠", 9: "뱀띠", 10: "말띠", 11: "양띠"
}

띠_이모지 = {
    "쥐띠": "🐭", "소띠": "🐮", "호랑이띠": "🐯", "토끼띠": "🐰",
    "용띠": "🐲", "뱀띠": "🐍", "말띠": "🐴", "양띠": "🐑",
    "원숭이띠": "🐵", "닭띠": "🐔", "개띠": "🐶", "돼지띠": "🐷"
}

기본_성향 = {
    "쥐띠": {
        "봄": "총명하고 감각이 뛰어나며 새로운 아이디어가 넘칩니다. 사교성이 좋아 인간관계가 풍부하며 직관력이 강하고 변화에 빠르게 적응합니다. 다만 너무 많은 것을 동시에 하려는 성향이 있으니 집중력을 키우는 것이 중요합니다.",
        "여름": "열정적이고 리더십이 강한 쥐띠입니다. 강한 추진력으로 목표를 향해 끝까지 나아가는 의지가 있습니다. 빠른 실행력이 최대 강점이며, 사람을 끌어당기는 매력이 있습니다.",
        "가을": "신중하고 분석력이 뛰어난 쥐띠입니다. 계획적으로 일을 처리하며 재치 있는 언변과 날카로운 판단력으로 주변의 신뢰를 얻습니다. 논리와 직관을 동시에 갖춘 사람입니다.",
        "겨울": "깊은 사고력과 인내심을 가진 쥐띠입니다. 겉으로 드러나지 않지만 강한 의지와 집중력이 있습니다. 오래 고민해서 내린 결정은 거의 틀리지 않는 탁월한 판단력이 있습니다.",
    },
    "소띠": {
        "봄": "성실하고 믿음직한 소띠로, 꾸준함과 인내심이 최대 강점입니다. 한번 마음먹은 일은 반드시 이루어내며 새로운 시작에 강한 힘을 발휘합니다.",
        "여름": "열정과 끈기를 동시에 가진 소띠입니다. 넘치는 에너지와 소띠 특유의 인내심으로 지치지 않습니다. 강한 책임감으로 맡은 일을 완벽하게 처리합니다.",
        "가을": "지혜롭고 현실적인 소띠입니다. 계획적이고 실용적인 사고로 안정적인 삶을 만들어가며, 착실히 쌓아온 것들이 결실을 맺습니다.",
        "겨울": "묵직하고 깊이 있는 소띠입니다. 말보다 행동으로 보여주는 스타일로 주변의 깊은 신뢰를 받습니다. 강한 신념으로 어떤 상황에도 흔들리지 않습니다.",
    },
    "호랑이띠": {
        "봄": "카리스마 넘치고 도전적인 호랑이띠로, 타고난 리더십과 자신감으로 주변을 이끌어갑니다. 강한 생동감으로 어디서나 존재감을 발휘합니다.",
        "여름": "불같은 열정과 강한 의지를 가진 호랑이띠입니다. 뜨거운 추진력으로 장애물을 돌파하며 용감하고 과감한 결정을 내릴 수 있는 사람입니다.",
        "가을": "전략적이고 냉철한 호랑이띠입니다. 상황을 정확하게 파악하고 최적의 타이밍에 움직입니다. 호랑이의 기세와 지혜가 더해진 강인한 성격입니다.",
        "겨울": "신비롭고 강한 내면을 가진 호랑이띠입니다. 표면은 고요하지만 내면에 강렬한 에너지가 있습니다. 결정적인 순간에 폭발적인 힘을 발휘합니다.",
    },
    "토끼띠": {
        "봄": "온화하고 감수성이 풍부한 토끼띠로, 섬세한 감각과 따뜻한 마음으로 주변 사람들에게 편안함을 줍니다. 예술적 감각이 뛰어납니다.",
        "여름": "활발하고 사교적인 토끼띠입니다. 다양한 사람들과 어울리는 것을 좋아하며 밝고 긍정적인 에너지로 주변을 활기차게 만듭니다.",
        "가을": "지적이고 신중한 토끼띠입니다. 감성과 이성이 균형을 이루며, 예리한 판단력과 섬세한 배려심으로 신뢰받는 사람입니다.",
        "겨울": "깊이 있고 직관력이 뛰어난 토끼띠입니다. 풍부한 내면세계를 가지고 있으며 혼자만의 시간을 통해 에너지를 충전합니다.",
    },
    "용띠": {
        "봄": "강렬하고 카리스마 넘치는 용띠로, 타고난 리더십과 열정으로 큰 꿈을 향해 달려가는 사람입니다. 무한한 가능성을 발산합니다.",
        "여름": "불꽃 같은 열정을 가진 용띠입니다. 압도적인 에너지를 발산하며 어떤 상황에서도 중심을 잃지 않는 강한 정신력이 있습니다.",
        "가을": "지혜로운 용띠입니다. 강한 기세와 냉철한 판단력을 함께 갖추었으며 장기적인 안목으로 큰 그림을 그리는 능력이 탁월합니다.",
        "겨울": "깊고 신비로운 용띠입니다. 때를 기다릴 줄 알며, 결정적인 순간에 누구도 따라올 수 없는 힘을 발휘합니다.",
    },
    "뱀띠": {
        "봄": "지혜롭고 직관력이 뛰어난 뱀띠로, 탁월한 관찰력으로 다른 사람이 보지 못하는 것을 파악합니다. 새로운 아이디어와 통찰력이 빛납니다.",
        "여름": "열정적이고 신비로운 뱀띠입니다. 매력이 강하며 주변 사람들을 자연스럽게 끌어당기는 흡인력이 있습니다.",
        "가을": "냉철하고 전략적인 뱀띠입니다. 완벽한 타이밍에 움직이는 능력이 탁월하며 감정보다 이성으로 판단하는 뛰어난 전략가입니다.",
        "겨울": "깊은 사고력을 가진 뱀띠입니다. 겉으로는 조용해 보이지만 내면에는 강렬한 통찰력이 있습니다.",
    },
    "말띠": {
        "봄": "자유롭고 활기찬 말띠로, 솔직하고 개방적인 성격으로 주변에 긍정적인 영향을 줍니다. 강한 추진력을 발휘합니다.",
        "여름": "열정적이고 도전적인 말띠입니다. 뜨거운 에너지로 목표를 향해 질주하며 경쟁 상황에서 더욱 빛을 발합니다.",
        "가을": "균형 잡힌 말띠입니다. 빠른 추진력과 신중한 판단이 조화를 이루며, 실용적인 방법으로 목표를 달성합니다.",
        "겨울": "의지가 강한 말띠입니다. 역경 속에서 더욱 빛나는 성격으로, 멈추지 않는 끈기가 가장 큰 무기입니다.",
    },
    "양띠": {
        "봄": "온화하고 예술적 감각이 뛰어난 양띠로, 창의적인 아이디어와 배려심 깊은 성격으로 주변의 사랑을 받습니다.",
        "여름": "밝고 사교적인 양띠입니다. 따뜻하고 에너지 넘치는 성격으로 어디서나 분위기를 화사하게 만듭니다.",
        "가을": "지적이고 섬세한 양띠입니다. 내면이 풍부하고 감수성이 깊으며 예술적 감각과 현실적 판단력을 함께 갖추었습니다.",
        "겨울": "깊은 내면을 가진 양띠입니다. 진정성 있는 관계를 중시하고 깊은 신뢰를 나누는 사람입니다.",
    },
    "원숭이띠": {
        "봄": "영리하고 재치 넘치는 원숭이띠로, 빠른 두뇌 회전과 뛰어난 적응력으로 어떤 상황에서도 해결책을 찾습니다.",
        "여름": "호기심 넘치고 활발한 원숭이띠입니다. 새로운 것을 빠르게 흡수하며 사교성이 뛰어나 어디서나 인기를 얻습니다.",
        "가을": "계획적이고 전략적인 원숭이띠입니다. 재치 있는 두뇌와 신중한 판단력이 조화를 이루며 장기적인 목표를 체계적으로 달성합니다.",
        "겨울": "깊이 있는 원숭이띠입니다. 겉으로는 조용하지만 내면에 탁월한 분석력과 전략적 사고가 있습니다.",
    },
    "닭띠": {
        "봄": "꼼꼼하고 성실한 닭띠로, 완벽을 추구하는 성격으로 어떤 일이든 철저하게 처리합니다. 새로운 시작에 강한 에너지를 발휘합니다.",
        "여름": "열정적이고 자신감 넘치는 닭띠입니다. 자신의 주장을 명확히 표현하고 뚜렷한 존재감을 발휘합니다.",
        "가을": "분석력이 뛰어난 닭띠입니다. 세부사항까지 놓치지 않는 꼼꼼함과 논리적 사고로 신뢰를 얻습니다.",
        "겨울": "신중하고 깊은 닭띠입니다. 인내심이 강하고 오랜 시간 준비한 것이 결국 빛을 발합니다.",
    },
    "개띠": {
        "봄": "따뜻하고 의리 있는 개띠로, 진심 어린 관계를 중시하며 신뢰를 쌓아가는 사람입니다. 활발하고 긍정적인 에너지가 넘칩니다.",
        "여름": "열정적이고 충직한 개띠입니다. 소중한 사람들을 위해 헌신하며 정의감이 강하고 용감하게 나섭니다.",
        "가을": "신중하고 책임감 강한 개띠입니다. 감정보다 신중한 결정을 내리며 한번 맺은 관계는 끝까지 지키는 의리 있는 성격입니다.",
        "겨울": "깊고 강인한 개띠입니다. 조용히 지켜보다 필요한 순간에 반드시 곁에 있어주는 사람입니다.",
    },
    "돼지띠": {
        "봄": "풍요롭고 낙천적인 돼지띠로, 넓은 마음과 너그러운 성격으로 주변에 복을 불러옵니다. 밝고 긍정적인 에너지가 넘칩니다.",
        "여름": "활발하고 열정적인 돼지띠입니다. 다양한 경험을 즐기며 대인관계가 넓고 분위기를 화사하게 만드는 능력이 있습니다.",
        "가을": "현실적이고 지혜로운 돼지띠입니다. 직관력이 뛰어나고 좋은 기회를 포착하는 능력이 있습니다.",
        "겨울": "깊은 내면의 풍요로움을 가진 돼지띠입니다. 진정한 풍요가 무엇인지 아는 지혜로운 사람입니다.",
    },
}

올해_운세 = {
    "쥐띠": "2026년 쥐띠는 기회가 오는 해이지만 방심하면 안 됩니다. 상반기엔 좋은 인연이 찾아오고 하반기엔 노력이 결실을 맺을 수 있어요. 단, 5~6월 사이 판단력이 흐려지는 시기가 있어 충동적인 결정을 내리면 크게 후회할 수 있습니다. 이 시기를 어떻게 넘기느냐가 올해 전체를 좌우해요.",
    "소띠": "2026년 소띠는 노력이 빛을 발하는 해입니다. 직장에서 인정받을 기회가 오지만, 주변에 당신의 공을 가로채려는 사람이 있을 수 있어요. 믿었던 사람에게 배신당할 수 있는 기운이 있으니 인간관계를 조심해야 합니다.",
    "호랑이띠": "2026년 호랑이띠는 에너지가 넘치지만 그만큼 부작용도 큽니다. 새로운 도전에서 성과를 낼 수 있지만, 과욕을 부리면 한 번에 무너질 수 있어요. 특히 상반기에 충동적인 투자나 사업 결정은 절대 금물입니다.",
    "토끼띠": "2026년 토끼띠는 겉으로는 안정적으로 보이지만 내면에 불안 요소가 있습니다. 오래된 관계에서 갈등이 생기거나, 믿었던 사람이 돌아서는 상황이 생길 수 있어요. 감정적으로 힘든 시기가 반드시 옵니다.",
    "용띠": "2026년 용띠는 큰 기회가 오는 해지만 함정도 많습니다. 하반기에 중요한 결정을 내려야 할 순간이 오는데, 이때 잘못 선택하면 3년은 고생할 수 있어요. 어떤 선택을 해야 하는지 사주로 미리 파악해두는 것이 중요합니다.",
    "뱀띠": "2026년 뱀띠는 준비해온 것들이 드러나는 해입니다. 좋은 소식도 있지만, 건강 문제나 가족 관계에서 예상치 못한 변수가 생길 수 있어요. 특히 하반기에 심리적으로 많이 지치는 기운이 있습니다.",
    "말띠": "2026년 말띠는 변화가 많은 해입니다. 새로운 환경이 찾아오지만 적응하는 과정에서 스트레스가 극심할 수 있어요. 이직이나 이사를 고려하고 있다면 타이밍을 잘못 잡으면 오히려 독이 됩니다.",
    "양띠": "2026년 양띠는 창의성이 빛나는 해이지만 감정 기복이 심해집니다. 좋은 인연이 오는 동시에 오래된 상처가 다시 올라오는 시기예요. 멘탈 관리를 못 하면 좋은 기회를 스스로 날려버릴 수 있습니다.",
    "원숭이띠": "2026년 원숭이띠는 가능성이 열리는 해지만 집중력이 흐트러지기 쉬운 시기입니다. 여러 가지를 동시에 시도하다가 아무것도 못 이루는 패턴에 빠질 수 있어요. 무엇에 집중해야 하는지가 올해의 핵심입니다.",
    "닭띠": "2026년 닭띠는 준비가 빛을 발하는 해입니다. 하지만 완벽주의적 성향이 발목을 잡을 수 있어요. 좋은 기회가 왔을 때 망설이다가 놓치는 상황이 생길 수 있습니다. 언제 뛰어야 하는지 판단이 중요한 해입니다.",
    "개띠": "2026년 개띠는 신뢰가 복이 되는 해이지만 그 신뢰를 악용하는 사람이 주변에 있을 수 있습니다. 오래된 인연이 기회를 가져오기도 하지만, 의리 때문에 손해를 보는 상황도 생겨요.",
    "돼지띠": "2026년 돼지띠는 기회가 많은 해이지만 그만큼 유혹도 많습니다. 재물운이 상승하는 시기에 오히려 큰 지출이나 손실이 생길 수 있어요. 좋아 보이는 것이 함정일 수 있으니 판단력을 잃지 마세요.",
}

재물운 = {
    "쥐띠": "수입이 생기는 기운은 있지만 지출도 만만치 않은 해입니다. 돈이 들어오는 만큼 나가는 구조라 실제로 남는 게 없을 수 있어요. 특히 충동구매나 인간관계에서의 지출을 조심해야 합니다.",
    "소띠": "재물운은 안정적이지만 느립니다. 노력 대비 결과가 늦게 나오는 구조라 중간에 포기하고 싶어질 수 있어요. 올해 무리한 투자는 절대 금물 — 한 번 실수하면 회복이 오래 걸립니다.",
    "호랑이띠": "수익 기회는 오지만 리스크도 큽니다. 욕심을 부리면 있던 것도 잃을 수 있는 구조예요. 주변에서 투자나 사업을 권유하는 사람을 특히 조심해야 합니다.",
    "토끼띠": "귀인이 경제적 도움을 줄 수 있지만, 그 과정에서 불필요한 지출이 생기기도 합니다. 남을 도와주다가 내 돈이 새는 상황이 생길 수 있어요.",
    "용띠": "재물운이 강하지만 과욕이 문제입니다. 큰 기회가 왔을 때 더 큰 것을 바라다가 놓치는 패턴이 반복될 수 있어요. 적당한 선에서 멈출 줄 아는 것이 올해의 핵심입니다.",
    "뱀띠": "예상치 못한 수익이 생기지만 예상치 못한 지출도 함께 옵니다. 특히 건강이나 가족 관련 비용이 갑자기 생길 수 있어요.",
    "말띠": "활발하게 움직이면 수익이 생기지만 쉬는 순간 바로 막힙니다. 올해는 쉬면 안 되는 해예요 — 하지만 그 페이스를 버티지 못하면 번아웃이 옵니다.",
    "양띠": "창의적 활동에서 수익이 생길 수 있지만 감정 상태에 따라 들쭉날쭉합니다. 멘탈이 흔들리면 재물운도 같이 흔들리는 구조예요.",
    "원숭이띠": "아이디어는 있지만 실행력이 문제입니다. 좋은 기회를 여러 번 잡았다가 놓치는 패턴이 반복될 수 있어요. 올해 결단력이 재물운을 결정합니다.",
    "닭띠": "꼼꼼하게 관리하면 모이지만, 예상치 못한 지출이 갑자기 발생하는 시기가 있습니다. 상반기 특히 조심해야 할 금전 손실의 기운이 있어요.",
    "개띠": "신뢰 관계에서 수익이 생기지만 그 신뢰 때문에 손해를 보는 상황도 생깁니다. 돈 문제로 관계가 틀어지는 상황을 조심해야 해요.",
    "돼지띠": "재물운이 좋아 보이지만 함정이 있습니다. 돈이 들어오는 시기에 오히려 큰 지출이 생기는 구조예요. 좋은 투자처럼 보이는 것에 속지 마세요.",
}

프리미엄_탭 = {
    "✨ 내 사주": [
        {"name": "타고난 기질", "emoji": "✨", "price": 9900,
         "desc": "사주로 보는 진짜 내 성격, 타고난 강점과 약점, 에너지 유형 분석",
         "teaser": "당신의 사주 원국에서 가장 강한 기운은 ○○입니다. 이 기운이 당신의 말투, 결정 방식, 대인관계 패턴까지 전부 설명해요. 왜 나는 이런 사람인지 — 사주가 정확하게 말해줍니다."},
        {"name": "대운 분석", "emoji": "🌊", "price": 9900,
         "desc": "10년 단위 대운의 흐름, 현재 대운이 내 삶에 미치는 영향 상세 분석",
         "teaser": "지금 당신은 어떤 대운 위에 서 있을까요? 현재 대운이 ○○한 기운이라면, 지금 안 되는 것들이 왜 안 되는지 바로 이해됩니다. 언제 터닝포인트가 오는지도 함께 알려드려요."},
        {"name": "세운 (올해 상세)", "emoji": "📆", "price": 9900,
         "desc": "2026년 세운이 내 사주와 어떻게 작용하는지, 월별 흐름 포함 상세 분석",
         "teaser": "2026년이 유독 이상하게 느껴진다면 이유가 있습니다. 세운이 당신의 사주와 충돌하는 시기가 있어요. 어느 달에 조심하고 어느 달에 밀어붙여야 하는지 월별로 알려드립니다."},
        {"name": "인생 흐름", "emoji": "🔮", "price": 9900,
         "desc": "과거·현재·미래의 큰 흐름, 인생 전환점과 중요한 결정 시기 분석",
         "teaser": "당신의 인생에서 가장 큰 변화가 오는 시기는 ○○대입니다. 지금 이 시점이 그 흐름의 어디쯤인지 — 알면 덜 불안하고, 더 잘 준비할 수 있어요."},
    ],
    "💰 재물·커리어": [
        {"name": "재물운 상세", "emoji": "💰", "price": 9900,
         "desc": "타고난 재물 그릇, 돈이 들어오는 방식, 재물운이 좋은 시기 상세 분석",
         "teaser": "당신의 재물 그릇은 ○○형입니다. 이 유형은 특정 방식으로 돈을 벌 때 훨씬 잘 흘러들어와요. 지금 하고 있는 방식이 맞는지, 언제 재물운이 열리는지 알려드립니다."},
        {"name": "적성·직업운", "emoji": "💼", "price": 9900,
         "desc": "타고난 직업 적성, 잘 맞는 직종, 커리어 방향이 맞는지 분석",
         "teaser": "당신의 사주에서 가장 빛나는 직업 기질은 ○○입니다. 지금 하는 일이 사주와 맞는지, 왜 이 일이 유독 힘들게 느껴지는지 — 커리어 방향을 사주로 점검해드려요."},
        {"name": "이직운", "emoji": "🚀", "price": 9900,
         "desc": "이직·창업에 유리한 시기, 지금 움직여도 되는지 사주로 판단",
         "teaser": "지금 이직하면 잘 될까요, 아니면 더 기다려야 할까요? 사주상 가장 유리한 이동 시기는 ○○월 전후입니다. 잘못된 타이밍의 이직이 3년을 망칠 수 있어요."},
    ],
    "💕 연애·관계": [
        {"name": "애정·연애운", "emoji": "💕", "price": 9900,
         "desc": "타고난 연애 패턴, 이상형 유형, 2026년 만남의 시기 분석",
         "teaser": "당신의 연애 기질은 ○○형입니다. 이 유형은 특정 패턴으로 상처받고, 특정 유형에게 끌리는 경향이 있어요. 2026년 인연운이 열리는 시기와 어떤 사람을 만나야 하는지 알려드립니다."},
        {"name": "결혼운", "emoji": "💍", "price": 9900,
         "desc": "결혼 시기, 배우자 인연의 특징, 결혼 후 운의 변화 분석",
         "teaser": "당신의 배우자 인연은 ○○한 기운을 가진 사람일 가능성이 높습니다. 결혼 시기가 사주상 언제인지, 지금 만나는 사람이 그 인연인지 — 사주가 힌트를 줍니다."},
        {"name": "궁합 분석", "emoji": "🤝", "price": 18900,
         "desc": "연인·친구·직장동료 등 원하는 관계의 두 사람 궁합 상세 분석",
         "teaser": "두 사람의 사주를 함께 놓으면, 말로는 설명하기 힘들었던 그 관계가 보입니다. 왜 맞는 것 같은데 자꾸 부딪히는지, 왜 편한데 불안한지 — 사주가 정확하게 설명해줍니다."},
        {"name": "2인 종합 사주", "emoji": "👫", "price": 60000,
         "desc": "두 사람 각자 사주 풀이 + 궁합까지 한번에 (커플·부부·동업자)",
         "teaser": "각자의 사주를 먼저 보고, 두 사람이 만났을 때 어떤 시너지와 충돌이 생기는지까지 분석합니다. 함께 가도 되는 사람인지 — 사주가 가장 솔직하게 말해줍니다."},
        {"name": "재회운", "emoji": "🕊️", "price": 9900,
         "desc": "헤어진 연인과의 재회 가능성, 시기, 다시 만나도 되는지 사주로 분석",
         "teaser": "두 사람의 인연이 끊어진 것인지 이어진 것인지, 사주는 알고 있습니다. 재회 가능성이 있는 시기는 ○○이며, 다시 만났을 때 이전과 같은 패턴이 반복될지도 미리 볼 수 있어요."},
    ],
    "🌱 특별·건강": [
        {"name": "임신운", "emoji": "🤱", "price": 9900,
         "desc": "자녀 인연, 임신 가능 시기, 자녀운의 흐름 분석",
         "teaser": "당신의 사주에서 자녀 인연이 가장 강하게 들어오는 시기는 ○○년 전후입니다. 자녀와의 인연이 있는지, 어떤 방식으로 찾아오는지 — 준비가 되어 있을 때 기회를 놓치지 않을 수 있어요."},
        {"name": "건강운", "emoji": "🌿", "price": 9900,
         "desc": "사주로 보는 타고난 건강 약점, 조심해야 할 시기, 건강 관리 방향",
         "teaser": "당신의 사주에서 건강상 가장 취약한 부분은 ○○입니다. 특히 조심해야 할 시기가 있으며, 미리 알고 관리하면 큰 문제를 예방할 수 있어요."},
        {"name": "고난·변화운", "emoji": "⚡", "price": 9900,
         "desc": "힘든 시기는 언제인지, 어떻게 대비해야 하는지, 변화가 오는 시기 분석",
         "teaser": "당신의 사주에서 가장 힘든 시기는 ○○이며, 이 시기엔 특정 유형의 고난이 반복됩니다. 알고 지나가는 것과 모르고 지나가는 것은 완전히 달라요."},
        {"name": "고민 1가지 집중 상담", "emoji": "💬", "price": 9900,
         "desc": "지금 가장 큰 고민 1가지를 사주로 집중 분석 — 연애·직장·가족·결정장애 모두 가능",
         "teaser": "지금 머릿속을 가장 많이 차지하는 고민이 뭔가요? DM으로 고민 내용 1가지를 보내주시면 그 상황을 사주 관점에서 집중 분석해드립니다. 결정이 흔들릴 때, 사주가 방향을 잡아줘요."},
    ],
}


위험신호 = {
    "쥐띠": ("충동적 결정 주의", "5~6월 사이 판단력이 흐려지는 기운이 있습니다. 이 시기 중요한 결정을 내리면 후회할 확률이 높아요."),
    "소띠": ("배신 주의", "믿었던 사람이 돌아서는 기운이 감지됩니다. 가까운 사이일수록 더 조심해야 하는 시기입니다."),
    "호랑이띠": ("과욕 경고", "상반기에 큰 손실을 부를 수 있는 기운이 있습니다. 누군가 투자나 사업을 권유한다면 각별히 조심하세요."),
    "토끼띠": ("관계 갈등 주의", "오래된 관계에서 갈등이 생기거나 믿었던 사람이 돌아서는 상황이 생길 수 있습니다."),
    "용띠": ("결정의 기로", "하반기에 중요한 선택의 순간이 옵니다. 잘못 선택하면 3년은 고생할 수 있는 기운이 있어요."),
    "뱀띠": ("건강·가족 변수", "예상치 못한 건강 문제나 가족 관련 변수가 생길 수 있습니다. 하반기 특히 조심하세요."),
    "말띠": ("타이밍 실수 주의", "이직·이사 등 변화를 고려하고 있다면 타이밍이 핵심입니다. 잘못 움직이면 오히려 독이 됩니다."),
    "양띠": ("멘탈 붕괴 주의", "감정 기복이 심해지는 시기입니다. 멘탈이 흔들리면 좋은 기회도 스스로 날려버릴 수 있어요."),
    "원숭이띠": ("집중력 분산 경고", "여러 가지를 동시에 벌이다 아무것도 못 이루는 패턴에 빠질 수 있습니다. 선택과 집중이 필요합니다."),
    "닭띠": ("기회 실기 주의", "망설이다가 좋은 기회를 놓치는 상황이 생깁니다. 언제 뛰어야 하는지 판단이 올해의 핵심이에요."),
    "개띠": ("의리에 손해", "의리 때문에 손해를 보는 상황이 생깁니다. 돈 문제로 소중한 관계가 틀어질 수 있어요."),
    "돼지띠": ("함정 주의", "좋아 보이는 것이 함정일 수 있습니다. 재물운이 좋은 시기에 오히려 큰 손실이 생기는 기운이 있어요."),
}

def get_띠(year):
    return 띠_맵[year % 12]


def get_season(month):
    if month in [3, 4, 5]:
        return "봄"
    elif month in [6, 7, 8]:
        return "여름"
    elif month in [9, 10, 11]:
        return "가을"
    else:
        return "겨울"


def get_운의온도(year, month, day):
    today = datetime.now()
    seed = year * 10000 + month * 100 + day + today.year * 1000 + today.month * 31 + today.day
    random.seed(seed)
    return random.randint(28, 98)


def draw_text_center(draw, x, y, text, fill):
    bbox = draw.textbbox((0, 0), text)
    w = bbox[2] - bbox[0]
    draw.text((x - w // 2, y), text, fill=fill)


def draw_text_left(draw, x, y, text, fill):
    draw.text((x, y), text, fill=fill)


def wrap_text(text, max_chars):
    lines = []
    while len(text) > max_chars:
        lines.append(text[:max_chars])
        text = text[max_chars:]
    if text:
        lines.append(text)
    return lines


def create_instagram_card(name, 띠, gender, 성향, 운세, 재물):
    W, H = 1080, 1350
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)

    # 그라데이션 배경
    for y in range(H):
        r = int(15 + 15 * y / H)
        g = int(8 + 15 * y / H)
        b = int(45 + 35 * y / H)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # 별 장식
    random.seed(77)
    for _ in range(120):
        x = random.randint(0, W)
        sy = random.randint(0, int(H * 0.4))
        r = random.randint(1, 3)
        a = random.randint(100, 255)
        draw.ellipse([x - r, sy - r, x + r, sy + r], fill=(a, a, min(a + 50, 255)))

    # 상단 헤더
    draw.rectangle([0, 0, W, 150], fill=(10, 5, 40))
    draw_text_center(draw, W // 2, 30, "[ 사주 운세 ]", (255, 215, 0))
    draw_text_center(draw, W // 2, 90, datetime.now().strftime("%Y년 %m월 %d일"), (180, 180, 210))

    # 이름 + 띠
    draw_text_center(draw, W // 2, 190, f"{name}님  ({띠})", (255, 255, 255))
    draw_text_center(draw, W // 2, 260, f"{'여성' if gender == '여' else '남성'}", (180, 180, 210))

    # 구분선
    draw.rectangle([60, 310, W - 60, 313], fill=(255, 215, 0))

    def draw_section(title, content, y_start):
        draw_text_left(draw, 80, y_start, title, (255, 215, 0))
        y = y_start + 45
        for line in wrap_text(content[:130], 28):
            draw_text_left(draw, 80, y, line, (220, 220, 245))
            y += 40
        return y + 40

    y = 360
    y = draw_section("[기본 성향]", 성향, y)
    y = draw_section("[올해 운세]", 운세, y)
    y = draw_section("[간단 재물운]", 재물, y)

    # 잠금 힌트
    draw.rectangle([0, y + 10, W, y + 70], fill=(60, 45, 10))
    draw_text_center(draw, W // 2, y + 25, "대운 / 연애 / 커리어 / 궁합 더 보기 (유료)", (255, 215, 0))

    # 하단 CTA
    draw.rectangle([0, H - 110, W, H], fill=(10, 5, 40))
    draw_text_center(draw, W // 2, H - 85, f"DM 문의  |  {INSTA_ID}", (255, 215, 0))
    draw_text_center(draw, W // 2, H - 40, f"#사주  #운세  #{띠}  #2026운세", (160, 160, 190))

    return img


# ─── UI ───────────────────────────────────────────────────────────────────────

st.set_page_config(page_title="사주포커스 | 팀장님이 제 귀인이라고요?", page_icon="🔮", layout="centered")

st.markdown("""
<style>
/* 전체 배경 */
.stApp { background-color: #f5f3ff; }

/* 히어로 섹션 */
.hero {
    background: linear-gradient(135deg, #ffffff 0%, #ede9fe 100%);
    border: 1.5px solid #ddd6fe;
    border-radius: 24px;
    padding: 48px 32px 40px;
    text-align: center;
    margin-bottom: 32px;
    box-shadow: 0 4px 24px rgba(124,58,237,0.08);
}
.hero-tag {
    display: inline-block;
    background: #ede9fe;
    border: 1px solid #c4b5fd;
    color: #7c3aed;
    font-size: 0.78rem;
    letter-spacing: 0.12em;
    padding: 4px 14px;
    border-radius: 20px;
    margin-bottom: 20px;
    font-weight: 700;
}
.hero-title {
    font-size: 2.2rem;
    font-weight: 900;
    color: #1e1e2e;
    line-height: 1.3;
    margin: 0 0 14px;
    letter-spacing: -0.02em;
}
.hero-title span { color: #7c3aed; }
.hero-sub {
    font-size: 1rem;
    color: #6b6b8a;
    margin: 0 0 28px;
    line-height: 1.7;
}
.hero-badges {
    display: flex;
    justify-content: center;
    gap: 10px;
    flex-wrap: wrap;
}
.badge {
    background: #ffffff;
    border: 1.5px solid #ddd6fe;
    border-radius: 30px;
    padding: 6px 16px;
    font-size: 0.82rem;
    color: #7c3aed;
    font-weight: 600;
}

/* 폼 카드 */
.form-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 28px 24px;
    margin-bottom: 8px;
}
.form-title {
    font-size: 0.85rem;
    font-weight: 700;
    color: #7c3aed;
    letter-spacing: 0.08em;
    margin-bottom: 18px;
    text-transform: uppercase;
}

/* 버튼 */
.stButton > button, .stFormSubmitButton > button {
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    padding: 14px !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
    opacity: 0.88 !important;
}

/* 구분선 */
hr { border-color: #e5e7eb !important; }

/* 결과 배너 */
.result-banner {
    background: linear-gradient(135deg, #ede9fe, #e0e7ff);
    border: 1.5px solid #c4b5fd;
    border-radius: 16px;
    padding: 24px 28px;
    margin: 16px 0 24px;
}
.result-banner h2 { color: #1e1e2e; margin: 0 0 6px; font-size: 1.8rem; }
.result-banner p { color: #6b6b8a; margin: 0; font-size: 0.88rem; }
</style>
""", unsafe_allow_html=True)

# 히어로 섹션
st.markdown("""
<div class="hero">
    <div class="hero-tag">✦ SAJUFOCUS · 사주포커스 ✦</div>
    <h1 class="hero-title">"팀장님이 제 귀인이라고요?<br><span>제 퇴사 사유인데요?"</span></h1>
    <p class="hero-sub">억울하면 사주나 봐봐 — 진짜 이유 알려줌 😤<br>내 인생이 왜 이런지, 사주가 다 설명해줌</p>
    <div class="hero-badges">
        <span class="badge">🔮 기본 운세 무료</span>
        <span class="badge">🛡️ 부적 이미지 990원</span>
        <span class="badge">🔄 월구독 4,900원</span>
    </div>
</div>
""", unsafe_allow_html=True)

# 990원 차단법 배너
st.markdown("""
<div style="
    background: linear-gradient(135deg, #ede9fe 0%, #e0e7ff 100%);
    border: 1.5px solid #7c3aed;
    border-radius: 16px;
    padding: 24px 28px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    gap: 16px;
">
    <div style="font-size:2.2rem;">🛡️</div>
    <div style="flex:1;">
        <div style="color:#7c3aed; font-size:0.78rem; font-weight:700; letter-spacing:0.1em; margin-bottom:4px;">지금 가장 많이 찾는 서비스</div>
        <div style="color:#1e1e2e; font-size:1.15rem; font-weight:800; margin-bottom:4px;">나쁜 기운 소멸 부적 이미지 — <span style="color:#7c3aed;">990원</span></div>
        <div style="color:#6b6b8a; font-size:0.85rem;">내 사주에서 지금 나를 막고 있는 기운에 맞춘 부적 이미지를 DM으로 발송해드립니다<br>
        지갑·휴대폰·배경화면에 저장하는 것만으로 기운을 차단할 수 있어요<br>
        <span style="color:#7c3aed; font-weight:600;">✓ 월구독 시 매달 새 부적 이미지 업데이트 포함</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

with st.form("saju_form"):
    st.markdown('<div class="form-title">내 정보 입력</div>', unsafe_allow_html=True)
    name = st.text_input("이름 또는 닉네임", placeholder="홍길동")

    col1, col2, col3 = st.columns(3)
    with col1:
        year = st.number_input("출생년도", min_value=1930, max_value=2010, value=1995, step=1)
    with col2:
        month = st.selectbox("월", list(range(1, 13)))
    with col3:
        day = st.selectbox("일", list(range(1, 32)))

    col4, col5 = st.columns(2)
    with col4:
        gender = st.radio("성별", ["여", "남"], horizontal=True)
    with col5:
        hour = st.selectbox("출생시간 (모르면 '모름')", [
            "모름", "자시(23~01시)", "축시(01~03시)", "인시(03~05시)",
            "묘시(05~07시)", "진시(07~09시)", "사시(09~11시)",
            "오시(11~13시)", "미시(13~15시)", "신시(15~17시)",
            "유시(17~19시)", "술시(19~21시)", "해시(21~23시)"
        ])

    submitted = st.form_submit_button("✦ 내 사주 보기", use_container_width=True, type="primary")

if submitted:
    if not name.strip():
        st.error("이름을 입력해주세요.")
        st.stop()

    띠 = get_띠(year)
    season = get_season(month)
    이모지 = 띠_이모지[띠]

    st.markdown(f"""
<div class="result-banner">
    <h2>{이모지} {name}님은 <span style="color:#a78bfa">{띠}</span> 입니다</h2>
    <p>{year}년 {month}월 {day}일생 &nbsp;·&nbsp; {'여성' if gender == '여' else '남성'} &nbsp;·&nbsp; {hour}</p>
</div>
""", unsafe_allow_html=True)

    st.divider()

    # ── 무료 운세 ──────────────────────────────────────────────────────────────
    st.markdown("### ✨ 무료 운세")

    성향 = 기본_성향[띠][season]
    운세 = 올해_운세[띠]
    재물 = 재물운[띠]

    with st.expander("🌟 기본 성향", expanded=True):
        st.write(성향)

    with st.expander("⭐ 올해 운세 (2026년)", expanded=True):
        st.write(운세)

    with st.expander("💰 간단 재물운", expanded=True):
        st.write(재물)

    # ── 위험신호 ───────────────────────────────────────────────────────────────
    신호_제목, 신호_내용 = 위험신호[띠]
    st.markdown(f"""
<div style="
    background: #fff7ed;
    border: 1.5px solid #f97316;
    border-radius: 14px;
    padding: 20px 24px;
    margin: 20px 0;
">
    <div style="color:#ea580c; font-weight:800; font-size:1rem; margin-bottom:8px;">
        ⚠️ 올해 {name}님 사주에서 발견된 위험신호
    </div>
    <div style="color:#9a3412; font-weight:700; margin-bottom:6px;">🔴 {신호_제목}</div>
    <div style="color:#7c2d12; font-size:0.92rem; line-height:1.6;">{신호_내용}</div>
    <div style="margin-top:12px; color:#ea580c; font-size:0.85rem; font-weight:600;">
        👇 이 위험을 어떻게 피해야 하는지, 정확한 시기와 대처법은 프리미엄 분석에서 알려드립니다
    </div>
</div>
""", unsafe_allow_html=True)

    st.divider()

    # ── 프리미엄 운세 ──────────────────────────────────────────────────────────────
    st.markdown("### 🔒 프리미엄 운세")
    st.caption("결제 후 스레드 DM으로 영수증 스크린샷 전송 → 상세 결과 전달  |  스레드: @사주포커스")

    # 주요 추천 서비스 3종
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        st.markdown("""<div style="background:#fff8f0;border:1.5px solid #f97316;border-radius:12px;padding:16px;text-align:center;min-height:130px;">
            <div style="font-size:1.8rem;">🛡️</div>
            <div style="font-weight:800;color:#ea580c;font-size:0.88rem;margin:6px 0;">나쁜 기운 소멸<br>부적 이미지</div>
            <div style="font-size:1.2rem;font-weight:900;color:#ea580c;">990원</div>
        </div>""", unsafe_allow_html=True)
    with col_f2:
        st.markdown("""<div style="background:#f5f3ff;border:1.5px solid #7c3aed;border-radius:12px;padding:16px;text-align:center;min-height:130px;">
            <div style="font-size:1.8rem;">🔄</div>
            <div style="font-weight:800;color:#7c3aed;font-size:0.88rem;margin:6px 0;">월간 운세 구독</div>
            <div style="color:#6b6b8a;font-size:0.78rem;margin-bottom:4px;">이후 4,900원/월</div>
            <div style="font-size:1.2rem;font-weight:900;color:#7c3aed;">첫달 990원</div>
        </div>""", unsafe_allow_html=True)
    with col_f3:
        st.markdown("""<div style="background:#f5f3ff;border:1.5px solid #4f46e5;border-radius:12px;padding:16px;text-align:center;min-height:130px;">
            <div style="font-size:1.8rem;">📖</div>
            <div style="font-weight:800;color:#1e1e2e;font-size:0.88rem;margin:6px 0;">종합 사주 풀이</div>
            <div style="color:#6b6b8a;font-size:0.78rem;margin-bottom:4px;">대운+세운+전체분석</div>
            <div style="font-size:1.2rem;font-weight:900;color:#4f46e5;">35,000원</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 더 자세히 보고 싶은 항목을 골라보세요")

    탭_레이블 = list(프리미엄_탭.keys())
    탭_목록 = st.tabs(탭_레이블)

    for 탭, 레이블 in zip(탭_목록, 탭_레이블):
        with 탭:
            for item in 프리미엄_탭[레이블]:
                with st.container(border=True):
                    col_a, col_b = st.columns([5, 1])
                    with col_a:
                        st.markdown(f"**{item['emoji']} {item['name']}**")
                        st.caption(item["desc"])
                        st.markdown(f"> 🔒 *{item['teaser']}*")
                    with col_b:
                        st.markdown(f"**{item['price']:,}원**")

    st.markdown("<br>", unsafe_allow_html=True)

    # 단일 결제 CTA
    st.markdown(f"""
<div style="
    background: linear-gradient(135deg, #1e1e2e 0%, #2d1b69 100%);
    border-radius: 20px;
    padding: 32px 28px;
    margin-top: 8px;
    text-align: center;
">
    <div style="color:#a78bfa; font-size:0.8rem; letter-spacing:0.15em; font-weight:700; margin-bottom:10px;">💳 결제 안내</div>
    <div style="color:#ffffff; font-size:1.05rem; font-weight:800; margin-bottom:6px;">
        원하는 항목 확인 후 아래 계좌로 입금해주세요
    </div>
    <div style="color:#c4b5fd; font-size:0.88rem; margin-bottom:20px;">
        영수증 스크린샷 + 원하는 항목명을 DM으로 보내주시면 바로 전달해드립니다
    </div>
    <div style="background:rgba(255,255,255,0.1); border-radius:12px; padding:18px 24px; margin-bottom:20px; display:inline-block; min-width:260px;">
        <div style="color:#a78bfa; font-size:0.82rem; margin-bottom:8px;">입금 계좌</div>
        <div style="color:#ffffff; font-size:1.15rem; font-weight:800;">{BANK_NAME}</div>
        <div style="color:#e0e7ff; font-size:1.1rem; font-family:monospace; margin:6px 0;">{BANK_ACCOUNT}</div>
        <div style="color:#a78bfa; font-size:0.85rem;">예금주: {BANK_HOLDER}</div>
    </div>
    <div style="color:#c4b5fd; font-size:0.88rem;">
        📩 입금 후 스레드 DM 전송 →
        <a href="https://www.threads.net/@사주포커스" target="_blank"
           style="color:#a78bfa; font-weight:700; text-decoration:none;">@사주포커스</a>
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()
st.markdown("""
<div style="text-align:center; padding: 24px 0 8px; color:#6060a0; font-size:0.85rem;">
    <div style="font-size:1rem; font-weight:700; color:#a78bfa; margin-bottom:8px;">🔮 SAJUFOCUS · 사주포커스</div>
    <a href="https://www.threads.net/@사주포커스" target="_blank"
       style="color:#a78bfa; text-decoration:none; font-weight:600;">스레드 @사주포커스</a>
    &nbsp;·&nbsp; 문의 및 결제는 스레드 DM으로
</div>
""", unsafe_allow_html=True)
