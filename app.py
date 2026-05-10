import streamlit as st
from datetime import datetime
from PIL import Image, ImageDraw
import random
import os
from dotenv import load_dotenv

load_dotenv()

INSTA_ID = os.getenv("INSTA_ID", "@내인스타계정")
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
    "쥐띠": "2026년 쥐띠는 새로운 도전과 기회의 해입니다. 상반기에는 인간관계에서 좋은 인연이 찾아오며 하반기에는 그동안 준비해온 일들이 결실을 맺기 시작합니다. 재물운은 안정적이며 노력한 만큼 돌아오는 해입니다.",
    "소띠": "2026년 소띠는 묵묵히 쌓아온 노력이 빛을 발하는 해입니다. 직장과 사업에서 안정적인 성장이 이어지며 주변의 신뢰가 높아집니다. 상반기 중요한 결정이 하반기 성과로 이어집니다.",
    "호랑이띠": "2026년 호랑이띠는 강한 에너지로 목표를 향해 돌진하는 해입니다. 새로운 분야에 도전하면 좋은 결과를 얻을 수 있으며 리더십을 발휘할 기회가 많아집니다.",
    "토끼띠": "2026년 토끼띠는 조화롭고 안정적인 한 해입니다. 인간관계에서 귀인이 나타나고 오래 고민하던 문제들이 자연스럽게 해결됩니다.",
    "용띠": "2026년 용띠는 큰 그림을 그리고 실행하는 해입니다. 강한 카리스마로 주변을 이끌며 중요한 프로젝트에서 두각을 나타냅니다. 하반기에 특히 큰 기회가 찾아옵니다.",
    "뱀띠": "2026년 뱀띠는 직관과 지혜로 중요한 결정을 내리는 해입니다. 조용히 준비해온 것들이 드디어 수면 위로 떠오르며 결실을 맺는 시기입니다.",
    "말띠": "2026년 말띠는 활발한 활동과 도전의 해입니다. 새로운 환경이나 인연이 찾아오며 변화를 두려워하지 않을 때 더 큰 기회가 열립니다.",
    "양띠": "2026년 양띠는 창의성과 감수성이 빛나는 해입니다. 예술적 감각이나 창의적 아이디어로 새로운 기회를 만들 수 있으며 인간관계에서 따뜻한 인연이 더해집니다.",
    "원숭이띠": "2026년 원숭이띠는 다양한 가능성을 탐색하는 해입니다. 새로운 분야에 관심을 가지면 예상치 못한 성과로 이어집니다. 빠른 적응력을 살려 변화하는 상황에서 기회를 포착하세요.",
    "닭띠": "2026년 닭띠는 준비와 실행이 완벽하게 맞아떨어지는 해입니다. 꼼꼼하게 준비해온 것들이 드디어 인정받으며 직업적으로 중요한 기회가 찾아옵니다.",
    "개띠": "2026년 개띠는 신뢰와 의리가 큰 복이 되는 해입니다. 오래된 인연이 새로운 기회를 가져오고 진심 어린 노력이 반드시 결실로 돌아옵니다.",
    "돼지띠": "2026년 돼지띠는 풍요롭고 기회가 많은 해입니다. 재물운이 상승하며 새로운 수익원이 생길 수 있습니다. 긍정적인 에너지를 유지하면 더 많은 기회가 자연스럽게 찾아옵니다.",
}

재물운 = {
    "쥐띠": "2026년 쥐띠의 재물운은 꾸준한 상승세입니다. 큰 지출보다는 저축과 안정적 투자가 유리하며 상반기 예상치 못한 소득이 생길 수 있습니다.",
    "소띠": "2026년 소띠의 재물운은 안정적입니다. 노력한 만큼 정직하게 돌아오는 재물운이며 무리한 투자보다는 본업에 집중하는 것이 더 큰 재물을 불러옵니다.",
    "호랑이띠": "2026년 호랑이띠의 재물운은 적극적인 도전에서 열립니다. 새로운 수익 기회가 찾아오며 과감한 결정이 좋은 결과로 이어질 수 있습니다.",
    "토끼띠": "2026년 토끼띠의 재물운은 인간관계에서 시작됩니다. 주변의 귀인이 경제적 기회를 가져오며 협력과 파트너십에서 수익이 발생할 수 있습니다.",
    "용띠": "2026년 용띠의 재물운은 강하게 상승하는 시기입니다. 큰 투자나 사업 결정에 좋은 시기이며 장기적인 재물 계획을 세우면 좋은 결과를 얻습니다.",
    "뱀띠": "2026년 뱀띠의 재물운은 직관을 믿는 것이 핵심입니다. 평소 관심 있던 분야에서 예상치 못한 수익 기회가 생깁니다.",
    "말띠": "2026년 말띠의 재물운은 활발한 활동에 비례합니다. 여러 채널에서 수익이 생기는 다양한 재물운이며 하반기에 특히 좋은 재물 기운이 들어옵니다.",
    "양띠": "2026년 양띠의 재물운은 창의적인 활동에서 열립니다. 부업이나 새로운 시도에서 예상보다 큰 수익이 생길 수 있습니다.",
    "원숭이띠": "2026년 원숭이띠의 재물운은 아이디어에서 시작됩니다. 창의적인 접근이 수익으로 이어지며 네트워크를 잘 활용하면 더 큰 경제적 기회가 열립니다.",
    "닭띠": "2026년 닭띠의 재물운은 꼼꼼한 관리에서 나옵니다. 지출을 체계적으로 관리하면 생각보다 많은 것이 쌓이며 상반기 예상치 못한 추가 수입이 생길 수 있습니다.",
    "개띠": "2026년 개띠의 재물운은 신뢰에서 옵니다. 오래 쌓아온 신뢰와 관계가 경제적 기회로 연결됩니다.",
    "돼지띠": "2026년 돼지띠의 재물운은 매우 좋습니다. 여러 방면에서 수익 기회가 생기며 긍정적인 마인드가 더 많은 재물을 불러옵니다.",
}

유료_항목 = [
    {
        "name": "월운세 정기구독 (매월 1일)",
        "emoji": "📅",
        "price": 990,
        "desc": "첫 달 990원 → 이후 매월 4,900원 | 매월 1일 월운세 상세 분석 | 🌡️ 오늘 내 운의 온도 매일 확인 | 🧧 구독 첫 달 부적 이미지 1회 증정 | 언제든 해지 가능",
        "teaser": "구독하시면 매월 1일 월운세 + 매일 내 운의 온도를 확인할 수 있어요. 첫 달엔 부적 이미지도 함께 드립니다...",
        "badge": "정기구독",
    },
    {
        "name": "종합 사주 풀이",
        "emoji": "🌟",
        "price": 35000,
        "desc": "아래 모든 항목을 한번에 — 기질·대운·재물·애정·건강 전체 분석",
        "teaser": "당신의 사주 전체 흐름과 지금 이 시기가 의미하는 것은...",
        "badge": "BEST",
    },
    {
        "name": "2인 종합 사주",
        "emoji": "👫",
        "price": 60000,
        "desc": "두 사람의 사주를 함께 분석 — 각자의 운세 + 두 사람의 궁합까지 한번에 (커플·부부·동업자)",
        "teaser": "두 사람의 사주를 함께 보면 보이지 않던 것들이 보입니다...",
        "badge": "커플추천",
    },
    {
        "name": "궁합 분석",
        "emoji": "🤝",
        "price": 18900,
        "desc": "친구 / 직장동료 / 동업자 / 부모자식 — 원하는 관계를 선택해서 궁합 분석",
        "teaser": "상대방의 생년월일을 함께 보내주시면 두 사람 사이의 궁합을...",
        "badge": "",
    },
    {
        "name": "타고난 기질",
        "emoji": "✨",
        "price": 9900,
        "desc": "사주로 보는 진짜 내 성격, 타고난 강점과 약점, 에너지 유형 분석",
        "teaser": "당신의 사주 원국에서 가장 강한 기운은 ○○이며...",
        "badge": "",
    },
    {
        "name": "대운 분석",
        "emoji": "🌊",
        "price": 9900,
        "desc": "10년 단위 대운의 흐름, 현재 대운이 내 삶에 미치는 영향 상세 분석",
        "teaser": "현재 당신은 ○○대운의 흐름 위에 있습니다. 이 시기는...",
        "badge": "",
    },
    {
        "name": "세운 (올해 상세)",
        "emoji": "📆",
        "price": 9900,
        "desc": "2026년 세운이 내 사주와 어떻게 작용하는지, 월별 흐름 포함 상세 분석",
        "teaser": "2026년 세운은 당신의 사주에서 ○○의 역할을 합니다...",
        "badge": "",
    },
    {
        "name": "인생 흐름",
        "emoji": "🔮",
        "price": 9900,
        "desc": "과거·현재·미래의 큰 흐름, 인생 전환점과 중요한 결정 시기 분석",
        "teaser": "당신의 인생은 ○○대에 가장 큰 변화를 겪으며...",
        "badge": "",
    },
    {
        "name": "재물운 상세",
        "emoji": "💰",
        "price": 9900,
        "desc": "타고난 재물 그릇, 돈이 들어오는 방식, 재물운이 좋은 시기 상세 분석",
        "teaser": "당신의 재물 그릇은 ○○형이며, 돈이 들어오는 통로는...",
        "badge": "",
    },
    {
        "name": "적성 · 직업운",
        "emoji": "💼",
        "price": 9900,
        "desc": "타고난 직업 적성, 잘 맞는 직종, 커리어 방향이 맞는지 분석",
        "teaser": "당신의 사주에서 가장 빛나는 직업 기질은 ○○이며...",
        "badge": "",
    },
    {
        "name": "애정 · 연애운",
        "emoji": "💕",
        "price": 9900,
        "desc": "타고난 연애 패턴, 이상형 유형, 2026년 만남의 시기 분석",
        "teaser": "당신의 연애 기질은 ○○형입니다. 2026년 애정운은...",
        "badge": "",
    },
    {
        "name": "결혼운",
        "emoji": "💍",
        "price": 9900,
        "desc": "결혼 시기, 배우자 인연의 특징, 결혼 후 운의 변화 분석",
        "teaser": "당신의 배우자 인연은 ○○한 기운을 가진 사람이며...",
        "badge": "",
    },
    {
        "name": "임신운",
        "emoji": "🤱",
        "price": 9900,
        "desc": "자녀 인연, 임신 가능 시기, 자녀운의 흐름 분석",
        "teaser": "당신의 사주에서 자녀 인연은 ○○년 전후에 가장 강하게...",
        "badge": "",
    },
    {
        "name": "이직운",
        "emoji": "🚀",
        "price": 9900,
        "desc": "이직·창업에 유리한 시기, 지금 움직여도 되는지 사주로 판단",
        "teaser": "지금 이직을 고민 중이라면, 사주상 가장 유리한 시기는...",
        "badge": "",
    },
    {
        "name": "고난 · 변화운",
        "emoji": "⚡",
        "price": 9900,
        "desc": "힘든 시기는 언제인지, 어떻게 대비해야 하는지, 변화가 오는 시기 분석",
        "teaser": "당신의 사주에서 조심해야 할 시기는 ○○이며...",
        "badge": "",
    },
    {
        "name": "건강운",
        "emoji": "🌿",
        "price": 9900,
        "desc": "사주로 보는 타고난 건강 약점, 조심해야 할 시기, 건강 관리 방향",
        "teaser": "당신의 사주에서 건강상 주의해야 할 부분은 ○○이며...",
        "badge": "",
    },
    {
        "name": "재회운",
        "emoji": "🕊️",
        "price": 9900,
        "desc": "헤어진 연인과의 재회 가능성, 시기, 다시 만나도 되는지 사주로 분석",
        "teaser": "두 사람의 인연이 끊어진 것인지 이어진 것인지, 사주는 알고 있습니다...",
        "badge": "",
    },
    {
        "name": "고민 1가지 집중 상담",
        "emoji": "💬",
        "price": 9900,
        "desc": "지금 가장 큰 고민 1가지를 사주로 집중 분석 — 연애·직장·가족·결정장애 모두 가능",
        "teaser": "DM으로 고민 내용 1가지를 보내주시면 사주 관점에서 집중 분석해드립니다...",
        "badge": "",
    },
]


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

st.set_page_config(page_title="사주 운세 | 내 운명을 알아보세요", page_icon="🔮", layout="centered")

st.markdown("""
<style>
/* 전체 배경 */
.stApp { background-color: #0f0f1a; }

/* 기본 텍스트 */
.stApp, .stMarkdown, label, .stRadio label { color: #e8e8f0 !important; }

/* 히어로 섹션 */
.hero {
    background: linear-gradient(135deg, #1a0533 0%, #0d1b3e 50%, #0f0f1a 100%);
    border: 1px solid #2d2d4e;
    border-radius: 20px;
    padding: 48px 32px 40px;
    text-align: center;
    margin-bottom: 32px;
}
.hero-tag {
    display: inline-block;
    background: rgba(167, 139, 250, 0.15);
    border: 1px solid rgba(167, 139, 250, 0.4);
    color: #a78bfa;
    font-size: 0.78rem;
    letter-spacing: 0.12em;
    padding: 4px 14px;
    border-radius: 20px;
    margin-bottom: 20px;
    font-weight: 600;
}
.hero-title {
    font-size: 2.6rem;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.2;
    margin: 0 0 14px;
    letter-spacing: -0.02em;
}
.hero-title span { color: #a78bfa; }
.hero-sub {
    font-size: 1rem;
    color: #9090b0;
    margin: 0 0 28px;
    line-height: 1.6;
}
.hero-badges {
    display: flex;
    justify-content: center;
    gap: 12px;
    flex-wrap: wrap;
}
.badge {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 30px;
    padding: 6px 16px;
    font-size: 0.82rem;
    color: #c0c0d8;
}

/* 폼 카드 */
.form-card {
    background: #16162a;
    border: 1px solid #2a2a45;
    border-radius: 16px;
    padding: 28px 24px;
    margin-bottom: 8px;
}
.form-title {
    font-size: 0.85rem;
    font-weight: 700;
    color: #a78bfa;
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
    letter-spacing: 0.02em !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
    opacity: 0.88 !important;
}

/* 입력 필드 */
.stTextInput input, .stNumberInput input, .stSelectbox select {
    background: #0f0f1a !important;
    border: 1px solid #2a2a45 !important;
    border-radius: 10px !important;
    color: #e8e8f0 !important;
}

/* 구분선 */
hr { border-color: #2a2a45 !important; }

/* expander */
.streamlit-expanderHeader {
    background: #16162a !important;
    border: 1px solid #2a2a45 !important;
    border-radius: 10px !important;
    color: #e8e8f0 !important;
}

/* 결과 배너 */
.result-banner {
    background: linear-gradient(135deg, #1a0533, #0d1b3e);
    border: 1px solid #3d2d6e;
    border-radius: 16px;
    padding: 24px 28px;
    margin: 16px 0 24px;
}
.result-banner h2 { color: #ffffff; margin: 0 0 6px; font-size: 1.8rem; }
.result-banner p { color: #9090b0; margin: 0; font-size: 0.88rem; }
</style>
""", unsafe_allow_html=True)

# 히어로 섹션
st.markdown("""
<div class="hero">
    <div class="hero-tag">✦ 무료 사주 분석 ✦</div>
    <h1 class="hero-title">생년월일로 보는<br><span>나의 운명</span></h1>
    <p class="hero-sub">기질 · 재물 · 연애 · 커리어 · 건강까지<br>사주 하나로 내 인생의 흐름을 읽어드립니다</p>
    <div class="hero-badges">
        <span class="badge">🔮 기본 운세 무료</span>
        <span class="badge">⚡ 바로 확인</span>
        <span class="badge">🔒 프리미엄 상세 분석</span>
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


    st.divider()

    # ── 유료 운세 ──────────────────────────────────────────────────────────────
    st.markdown("### 🔒 프리미엄 운세")
    st.caption("결제 후 인스타 DM으로 영수증 스크린샷 전송 → 상세 결과 전달")

    for item in 유료_항목:
        with st.container(border=True):
            col_a, col_b = st.columns([3, 1])
            with col_a:
                badge = (
                    " 🏆 BEST" if item["badge"] == "BEST"
                    else " 💑 커플추천" if item["badge"] == "커플추천"
                    else " 🔄 정기구독" if item["badge"] == "정기구독"
                    else ""
                )
                st.markdown(f"**{item['emoji']} {item['name']}**{badge}")
                st.caption(item["desc"])
                st.markdown(f"> 🔒 *{item['teaser']}*")
            with col_b:
                if item["badge"] == "정기구독":
                    st.markdown("**첫 달 990원**")
                    st.caption("이후 4,900원/월")
                else:
                    st.markdown(f"**{item['price']:,}원**")
                with st.popover("💳 결제하기", use_container_width=True):
                    if item["badge"] == "정기구독":
                        st.markdown(f"**{item['name']}**")
                        st.markdown("🎁 **첫 달 990원** → 이후 매월 4,900원")
                        st.caption("🧧 구독 첫 달 부적 이미지 1회 증정")
                    else:
                        st.markdown(f"**{item['name']}** — {item['price']:,}원")
                    st.divider()
                    st.markdown(f"🏦 **{BANK_NAME}**")
                    st.code(BANK_ACCOUNT, language=None)
                    st.caption(f"예금주: {BANK_HOLDER}")
                    st.warning("입금 후 인스타 DM으로 영수증 전송해주세요 📩")
