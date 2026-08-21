from pathlib import Path
import re


ROOT = Path(__file__).parent

DISTRICTS = {
    "jongno": ("종로구", ["청운효자동", "사직동", "삼청동", "부암동", "평창동", "무악동", "교남동", "가회동", "종로1·2·3·4가동", "종로5·6가동", "이화동", "혜화동", "창신제1동", "창신제2동", "창신제3동", "숭인제1동", "숭인제2동"]),
    "jung": ("중구", ["소공동", "회현동", "명동", "필동", "장충동", "광희동", "을지로동", "신당동", "다산동", "약수동", "청구동", "동화동", "황학동", "중림동"]),
    "yongsan": ("용산구", ["후암동", "용산2가동", "남영동", "청파동", "원효로제1동", "원효로제2동", "효창동", "용문동", "한강로동", "이촌제1동", "이촌제2동", "이태원제1동", "이태원제2동", "한남동", "서빙고동", "보광동"]),
    "seongdong": ("성동구", ["왕십리도선동", "왕십리제2동", "마장동", "사근동", "행당제1동", "행당제2동", "응봉동", "금호1가동", "금호2·3가동", "금호4가동", "옥수동", "성수1가제1동", "성수1가제2동", "성수2가제1동", "성수2가제3동", "송정동", "용답동"]),
    "gwangjin": ("광진구", ["중곡제1동", "중곡제2동", "중곡제3동", "중곡제4동", "능동", "구의제1동", "구의제2동", "구의제3동", "광장동", "자양제1동", "자양제2동", "자양제3동", "자양제4동", "화양동", "군자동"]),
    "dongdaemun": ("동대문구", ["용신동", "제기동", "전농제1동", "전농제2동", "답십리제1동", "답십리제2동", "장안제1동", "장안제2동", "청량리동", "회기동", "휘경제1동", "휘경제2동", "이문제1동", "이문제2동"]),
    "jungnang": ("중랑구", ["면목본동", "면목제2동", "면목제3·8동", "면목제4동", "면목제5동", "면목제7동", "상봉제1동", "상봉제2동", "중화제1동", "중화제2동", "묵제1동", "묵제2동", "망우본동", "망우제3동", "신내1동", "신내2동"]),
    "seongbuk": ("성북구", ["성북동", "삼선동", "동선동", "돈암제1동", "돈암제2동", "안암동", "보문동", "정릉제1동", "정릉제2동", "정릉제3동", "정릉제4동", "길음제1동", "길음제2동", "종암동", "월곡제1동", "월곡제2동", "장위제1동", "장위제2동", "장위제3동", "석관동"]),
    "gangbuk": ("강북구", ["삼양동", "미아동", "송중동", "송천동", "삼각산동", "번1동", "번2동", "번3동", "수유1동", "수유2동", "수유3동", "우이동", "인수동"]),
    "dobong": ("도봉구", ["쌍문1동", "쌍문2동", "쌍문3동", "쌍문4동", "방학1동", "방학2동", "방학3동", "창1동", "창2동", "창3동", "창4동", "창5동", "도봉1동", "도봉2동"]),
    "nowon": ("노원구", ["월계1동", "월계2동", "월계3동", "공릉1동", "공릉2동", "하계1동", "하계2동", "중계본동", "중계1동", "중계2·3동", "중계4동", "상계1동", "상계2동", "상계3·4동", "상계5동", "상계6·7동", "상계8동", "상계9동", "상계10동"]),
    "eunpyeong": ("은평구", ["녹번동", "불광제1동", "불광제2동", "갈현제1동", "갈현제2동", "구산동", "대조동", "응암제1동", "응암제2동", "응암제3동", "역촌동", "신사제1동", "신사제2동", "증산동", "수색동", "진관동"]),
    "seodaemun": ("서대문구", ["충현동", "천연동", "북아현동", "신촌동", "연희동", "홍제제1동", "홍제제2동", "홍제제3동", "홍은제1동", "홍은제2동", "남가좌제1동", "남가좌제2동", "북가좌제1동", "북가좌제2동"]),
    "mapo": ("마포구", ["공덕동", "아현동", "도화동", "용강동", "대흥동", "염리동", "신수동", "서강동", "서교동", "합정동", "망원제1동", "망원제2동", "연남동", "성산제1동", "성산제2동", "상암동"]),
    "yangcheon": ("양천구", ["목1동", "목2동", "목3동", "목4동", "목5동", "신월1동", "신월2동", "신월3동", "신월4동", "신월5동", "신월6동", "신월7동", "신정1동", "신정2동", "신정3동", "신정4동", "신정6동", "신정7동"]),
    "gangseo": ("강서구", ["염창동", "등촌제1동", "등촌제2동", "등촌제3동", "화곡본동", "화곡제1동", "화곡제2동", "화곡제3동", "화곡제4동", "화곡제6동", "화곡제8동", "우장산동", "가양제1동", "가양제2동", "가양제3동", "발산1동", "공항동", "방화제1동", "방화제2동", "방화제3동"]),
    "guro": ("구로구", ["신도림동", "구로제1동", "구로제2동", "구로제3동", "구로제4동", "구로제5동", "가리봉동", "고척제1동", "고척제2동", "개봉제1동", "개봉제2동", "개봉제3동", "오류제1동", "오류제2동", "수궁동", "항동"]),
    "geumcheon": ("금천구", ["가산동", "독산제1동", "독산제2동", "독산제3동", "독산제4동", "시흥제1동", "시흥제2동", "시흥제3동", "시흥제4동", "시흥제5동"]),
    "yeongdeungpo": ("영등포구", ["영등포본동", "영등포동", "여의동", "당산제1동", "당산제2동", "도림동", "문래동", "양평제1동", "양평제2동", "신길제1동", "신길제3동", "신길제4동", "신길제5동", "신길제6동", "신길제7동", "대림제1동", "대림제2동", "대림제3동"]),
    "dongjak": ("동작구", ["노량진제1동", "노량진제2동", "상도제1동", "상도제2동", "상도제3동", "상도제4동", "흑석동", "사당제1동", "사당제2동", "사당제3동", "사당제4동", "사당제5동", "대방동", "신대방제1동", "신대방제2동"]),
    "gwanak": ("관악구", ["보라매동", "은천동", "성현동", "청림동", "행운동", "낙성대동", "청룡동", "남현동", "신림동", "신사동", "조원동", "미성동", "난곡동", "난향동", "삼성동", "대학동", "서원동", "신원동", "서림동"]),
    "seocho": ("서초구", ["서초1동", "서초2동", "서초3동", "서초4동", "잠원동", "반포본동", "반포1동", "반포2동", "반포3동", "반포4동", "방배본동", "방배1동", "방배2동", "방배3동", "방배4동", "양재1동", "양재2동", "내곡동"]),
    "gangnam": ("강남구", ["신사동", "논현1동", "논현2동", "압구정동", "청담동", "삼성1동", "삼성2동", "대치1동", "대치2동", "대치4동", "역삼1동", "역삼2동", "도곡1동", "도곡2동", "개포1동", "개포2동", "개포3동", "개포4동", "일원본동", "일원1동", "일원2동", "수서동", "세곡동"]),
    "songpa": ("송파구", ["풍납1동", "풍납2동", "거여1동", "거여2동", "마천1동", "마천2동", "방이1동", "방이2동", "오륜동", "오금동", "송파1동", "송파2동", "석촌동", "삼전동", "가락본동", "가락1동", "가락2동", "문정1동", "문정2동", "장지동", "위례동", "잠실본동", "잠실2동", "잠실3동", "잠실4동", "잠실6동", "잠실7동"]),
    "gangdong": ("강동구", ["강일동", "상일제1동", "상일제2동", "명일제1동", "명일제2동", "고덕제1동", "고덕제2동", "암사제1동", "암사제2동", "암사제3동", "천호제1동", "천호제2동", "천호제3동", "성내제1동", "성내제2동", "성내제3동", "길동", "둔촌제1동", "둔촌제2동"]),
}

def make_slug(dong, index):
    known = {
        "청운효자동": "cheongunhyoja", "사직동": "sajik", "삼청동": "samcheong", "부암동": "buam",
        "평창동": "pyeongchang", "무악동": "muak", "교남동": "gyonam", "가회동": "gahoe",
        "종로1·2·3·4가동": "jongno-1-2-3-4-ga", "종로5·6가동": "jongno-5-6-ga", "이화동": "ihwa",
        "혜화동": "hyehwa", "창신제1동": "changsin-1", "창신제2동": "changsin-2", "창신제3동": "changsin-3",
        "숭인제1동": "sungin-1", "숭인제2동": "sungin-2",
    }
    return known.get(dong, str(index))


def child_template():
    return (ROOT / "english-seoul-jongno-cheongunhyoja.html").read_text(encoding="utf-8")


def update_parent(district_slug, district_name, dongs):
    path = ROOT / f"english-seoul-{district_slug}.html"
    text = path.read_text(encoding="utf-8")
    css = ".subdistricts{margin-top:24px;padding-top:20px;border-top:1px solid var(--line)}.subdistricts h2{margin:0 0 12px;font-size:19px}.subdistrict-links{display:flex;flex-wrap:wrap;gap:8px}.subdistrict-links a{padding:9px 12px;border:1px solid var(--line);border-radius:999px;background:#fff;color:#2f3f61;font-size:13px;font-weight:700}"
    if "subdistricts" not in text:
        text = text.replace(".photo-strip{", css + ".photo-strip{", 1)
    links = "\n".join(f'          <a href="english-seoul-{district_slug}-{make_slug(dong, i)}.html">{dong}</a>' for i, dong in enumerate(dongs, 1))
    block = f'''      <div class="subdistricts">\n        <h2>서울 {district_name} 동별 영어회화</h2>\n        <div class="subdistrict-links">\n{links}\n        </div>\n      </div>\n'''
    text = re.sub(r'      <div class="subdistricts">.*?      </div>\n', block, text, count=1, flags=re.S)
    if "subdistricts" not in text:
        marker = "    </div>\n  </div>\n</section>\n</main>"
        text = text.replace(marker, "    </div>\n" + block + "  </div>\n</section>\n</main>", 1)
    path.write_text(text, encoding="utf-8", newline="\n")


def main():
    base = child_template()
    generated = 0
    for district_slug, (district_name, dongs) in DISTRICTS.items():
        update_parent(district_slug, district_name, dongs)
        expected = {
            f"english-seoul-{district_slug}-{make_slug(dong, index)}.html"
            for index, dong in enumerate(dongs, 1)
        }
        prefix = f"english-seoul-{district_slug}-"
        for path in ROOT.glob(f"{prefix}*.html"):
            if path.name not in expected:
                path.unlink()
        for index, dong in enumerate(dongs, 1):
            slug = make_slug(dong, index)
            filename = f"english-seoul-{district_slug}-{slug}.html"
            text = base.replace("서울 종로구 청운효자동", f"서울 {district_name} {dong}")
            text = text.replace("종로구 전체 동 보기", f"{district_name} 전체 동 보기")
            text = text.replace("english-seoul-jongno.html", f"english-seoul-{district_slug}.html")
            text = text.replace("english-seoul-jongno-cheongunhyoja.html", filename)
            text = text.replace("english-seoul-jongno-", f"english-seoul-{district_slug}-")
            (ROOT / filename).write_text(text, encoding="utf-8", newline="\n")
            generated += 1
    print(f"Generated {generated} Seoul dong pages")


if __name__ == "__main__":
    main()
