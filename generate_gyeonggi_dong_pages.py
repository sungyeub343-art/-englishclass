from pathlib import Path
import re


ROOT = Path(__file__).parent

# Administrative 읍면동 names for the 31 Gyeonggi municipalities.
MUNICIPALITIES = {
    "suwon": ("수원시", [
        "파장동", "율천동", "정자1동", "정자2동", "정자3동", "영화동", "송죽동", "조원1동", "조원2동", "연무동",
        "세류1동", "세류2동", "세류3동", "평동", "서둔동", "구운동", "금곡동", "호매실동", "권선1동", "권선2동", "곡선동", "입북동",
        "행궁동", "매교동", "매산동", "고등동", "화서1동", "화서2동", "지동", "우만1동", "우만2동", "인계동",
        "매탄1동", "매탄2동", "매탄3동", "매탄4동", "원천동", "광교1동", "광교2동", "영통1동", "영통2동", "영통3동", "망포1동", "망포2동",
    ]),
    "seongnam": ("성남시", ["수정구 신흥1동", "수정구 신흥2동", "수정구 신흥3동", "수정구 태평1동", "수정구 태평2동", "수정구 태평3동", "수정구 태평4동", "수정구 산성동", "수정구 양지동", "수정구 복정동", "수정구 위례동", "수정구 신촌동", "수정구 고등동", "수정구 시흥동", "중원구 성남동", "중원구 중앙동", "중원구 금광1동", "중원구 금광2동", "중원구 은행1동", "중원구 은행2동", "중원구 상대원1동", "중원구 상대원2동", "중원구 상대원3동", "중원구 하대원동", "중원구 도촌동", "분당구 분당동", "분당구 수내1동", "분당구 수내2동", "분당구 수내3동", "분당구 정자1동", "분당구 정자2동", "분당구 정자3동", "분당구 서현1동", "분당구 서현2동", "분당구 이매1동", "분당구 이매2동", "분당구 야탑1동", "분당구 야탑2동", "분당구 야탑3동", "분당구 판교동", "분당구 삼평동", "분당구 백현동", "분당구 운중동", "분당구 금곡동", "분당구 구미1동", "분당구 구미동"]),
    "goyang": ("고양시", ["덕양구 주교동", "덕양구 원신동", "덕양구 흥도동", "덕양구 성사1동", "덕양구 성사2동", "덕양구 효자동", "덕양구 삼송1동", "덕양구 삼송2동", "덕양구 창릉동", "덕양구 고양동", "덕양구 관산동", "덕양구 능곡동", "덕양구 화정1동", "덕양구 화정2동", "덕양구 행주동", "덕양구 행신1동", "덕양구 행신2동", "덕양구 행신3동", "덕양구 행신4동", "덕양구 대덕동", "일산동구 식사동", "일산동구 중산1동", "일산동구 중산2동", "일산동구 정발산동", "일산동구 풍산동", "일산동구 백석1동", "일산동구 백석2동", "일산동구 마두1동", "일산동구 마두2동", "일산동구 장항1동", "일산동구 장항2동", "일산동구 고봉동", "일산서구 일산1동", "일산서구 일산2동", "일산서구 일산3동", "일산서구 탄현1동", "일산서구 탄현2동", "일산서구 주엽1동", "일산서구 주엽2동", "일산서구 대화동", "일산서구 송포동", "일산서구 덕이동", "일산서구 가좌동"]),
    "yongin": ("용인시", ["처인구 포곡읍", "처인구 모현읍", "처인구 이동읍", "처인구 남사읍", "처인구 원삼면", "처인구 백암면", "처인구 중앙동", "처인구 역북동", "처인구 삼가동", "처인구 유림동", "처인구 동부동", "수지구 풍덕천1동", "수지구 풍덕천2동", "수지구 신봉동", "수지구 죽전1동", "수지구 죽전2동", "수지구 동천동", "수지구 상현1동", "수지구 상현2동", "수지구 성복동", "기흥구 신갈동", "기흥구 영덕1동", "기흥구 영덕2동", "기흥구 하갈동", "기흥구 보라동", "기흥구 상갈동", "기흥구 구갈동", "기흥구 상하동", "기흥구 동백1동", "기흥구 동백2동", "기흥구 동백3동", "기흥구 구성동", "기흥구 마북동", "기흥구 동탄동", "기흥구 보정동"]),
    "bucheon": ("부천시", ["심곡1동", "심곡2동", "심곡3동", "원미1동", "원미2동", "소사동", "역곡1동", "역곡2동", "춘의동", "도당동", "약대동", "중동", "중1동", "중2동", "중3동", "중4동", "상동", "상1동", "상2동", "상3동", "심곡본1동", "심곡본동", "소사본1동", "소사본동", "범박동", "옥길동", "괴안동", "역곡3동", "송내1동", "송내2동", "성곡동", "고강본동", "고강1동", "원종1동", "원종2동", "오정동", "신흥동"]),
    "ansan": ("안산시", ["상록구 일동", "상록구 이동", "상록구 사동", "상록구 사이동", "상록구 해양동", "상록구 본오1동", "상록구 본오2동", "상록구 본오3동", "상록구 부곡동", "상록구 월피동", "상록구 성포동", "상록구 반월동", "상록구 안산동", "단원구 와동", "단원구 고잔동", "단원구 중앙동", "단원구 호수동", "단원구 원곡동", "단원구 백운동", "단원구 신길동", "단원구 초지동", "단원구 선부1동", "단원구 선부2동", "단원구 선부3동", "단원구 대부동"]),
    "anyang": ("안양시", ["만안구 안양1동", "만안구 안양2동", "만안구 안양3동", "만안구 안양4동", "만안구 안양5동", "만안구 안양6동", "만안구 안양7동", "만안구 안양8동", "만안구 안양9동", "만안구 석수1동", "만안구 석수2동", "만안구 박달1동", "만안구 박달2동", "동안구 비산1동", "동안구 비산2동", "동안구 비산3동", "동안구 부흥동", "동안구 달안동", "동안구 관양1동", "동안구 관양2동", "동안구 부림동", "동안구 평촌동", "동안구 평안동", "동안구 귀인동", "동안구 호계1동", "동안구 호계2동", "동안구 호계3동", "동안구 범계동", "동안구 신촌동", "동안구 갈산동"]),
    "namyangju": ("남양주시", ["와부읍", "진접읍", "화도읍", "진건읍", "오남읍", "퇴계원읍", "별내면", "수동면", "조안면", "호평동", "평내동", "금곡동", "양정동", "다산1동", "다산2동", "별내동"]),
    "hwaseong": ("화성시", ["봉담읍", "우정읍", "향남읍", "남양읍", "매송면", "비봉면", "마도면", "송산면", "서신면", "팔탄면", "장안면", "양감면", "정남면", "진안동", "병점1동", "병점2동", "반월동", "기배동", "화산동", "동탄1동", "동탄2동", "동탄3동", "동탄4동", "동탄5동", "동탄6동", "동탄7동", "동탄8동"]),
    "pyeongtaek": ("평택시", ["팽성읍", "안중읍", "포승읍", "오성면", "청북읍", "현덕면", "진위면", "서탄면", "고덕면", "세교동", "배미동", "비전1동", "비전2동", "용이동", "동삭동", "신평동", "원평동", "통복동", "세교동", "송탄동", "지산동", "송북동", "신장1동", "신장2동", "서정동", "장당동", "고덕동", "중앙동"]),
    "siheung": ("시흥시", ["대야동", "신천동", "신현동", "은행동", "매화동", "목감동", "군자동", "정왕본동", "정왕1동", "정왕2동", "정왕3동", "정왕4동", "배곧1동", "배곧2동", "과림동", "연성동", "장곡동", "능곡동", "월곶동", "거북섬동"]),
    "gimpo": ("김포시", ["통진읍", "고촌읍", "양촌읍", "대곶면", "월곶면", "하성면", "김포본동", "장기본동", "사우동", "풍무동", "장기동", "구래동", "운양동", "마산동", "걸포동"]),
    "paju": ("파주시", ["문산읍", "파주읍", "법원읍", "조리읍", "월롱면", "탄현면", "광탄면", "파평면", "적성면", "군내면", "장단면", "진동면", "진서면", "금촌1동", "금촌2동", "금촌3동", "교하동", "운정1동", "운정2동", "운정3동", "운정4동", "운정5동", "운정6동"]),
    "gwangju-gyeonggi": ("광주시", ["오포읍", "초월읍", "곤지암읍", "도척면", "퇴촌면", "남종면", "남한산성면", "경안동", "송정동", "탄벌동", "광남1동", "광남2동"]),
    "gwangmyeong": ("광명시", ["광명1동", "광명2동", "광명3동", "광명4동", "광명5동", "광명6동", "광명7동", "철산1동", "철산2동", "철산3동", "철산4동", "하안1동", "하안2동", "하안3동", "하안4동", "소하1동", "소하2동", "일직동", "학온동"]),
    "gunpo": ("군포시", ["군포1동", "군포2동", "산본1동", "산본2동", "금정동", "재궁동", "오금동", "수리동", "궁내동", "광정동", "대야동", "송부동"]),
    "hanam": ("하남시", ["천현동", "신장1동", "신장2동", "덕풍1동", "덕풍2동", "덕풍3동", "풍산동", "감북동", "감일동", "위례동", "춘궁동", "초이동", "미사1동", "미사2동"]),
    "osan": ("오산시", ["중앙동", "대원동", "남촌동", "신장동", "세마동", "초평동", "청학동", "궐동", "금암동", "수청동"]),
    "icheon": ("이천시", ["장호원읍", "부발읍", "신둔면", "백사면", "호법면", "마장면", "대월면", "모가면", "설성면", "율면", "창전동", "증포동", "관고동", "중리동"]),
    "anseong": ("안성시", ["공도읍", "보개면", "금광면", "서운면", "미양면", "대덕면", "양성면", "원곡면", "일죽면", "죽산면", "삼죽면", "고삼면", "안성1동", "안성2동", "안성3동"]),
    "hwasong": ("화성시", ["봉담읍", "우정읍", "향남읍", "남양읍", "동탄1동", "동탄2동", "동탄3동", "동탄4동", "동탄5동", "동탄6동", "동탄7동", "동탄8동"]),
    "uijeongbu": ("의정부시", ["의정부1동", "의정부2동", "의정부3동", "호원1동", "호원2동", "장암동", "신곡1동", "신곡2동", "송산1동", "송산2동", "송산3동", "자금동", "가능동", "흥선동", "녹양동"]),
    "yangju": ("양주시", ["백석읍", "은현면", "남면", "광적면", "장흥면", "양주1동", "양주2동", "회천1동", "회천2동", "회천3동", "회천4동"]),
    "pocheon": ("포천시", ["소흘읍", "군내면", "내촌면", "가산면", "신북면", "창수면", "영중면", "일동면", "이동면", "영북면", "관인면", "화현면", "포천동", "선단동"]),
    "yeoju": ("여주시", ["가남읍", "점동면", "세종대왕면", "흥천면", "금사면", "산북면", "대신면", "북내면", "강천면", "여흥동", "중앙동", "오학동"]),
    "dongducheon": ("동두천시", ["생연1동", "생연2동", "중앙동", "보산동", "불현동", "송내동", "소요동", "상패동"]),
    "gwacheon": ("과천시", ["중앙동", "갈현동", "별양동", "부림동", "과천동", "문원동"]),
    "guri": ("구리시", ["갈매동", "동구동", "인창동", "교문1동", "교문2동", "수택1동", "수택2동", "수택3동"]),
    "uiwang": ("의왕시", ["고천동", "부곡동", "오전동", "내손1동", "내손2동", "청계동"]),
    "gapyeong": ("가평군", ["가평읍", "설악면", "청평면", "상면", "조종면", "북면"]),
    "yangpyeong": ("양평군", ["양평읍", "강상면", "강하면", "양서면", "옥천면", "서종면", "단월면", "청운면", "용문면", "개군면", "지평면"]),
    "yeoncheon": ("연천군", ["연천읍", "전곡읍", "군남면", "청산면", "백학면", "미산면", "왕징면", "신서면", "중면", "장남면"]),
}

# Correct the municipality slug used by the existing parent page.
MUNICIPALITIES["hwaseong"] = MUNICIPALITIES.pop("hwasong")

CSS = ".subdistricts{margin-top:24px;padding-top:20px;border-top:1px solid var(--line)}.subdistricts h2{margin:0 0 12px;font-size:19px}.subdistrict-links{display:flex;flex-wrap:wrap;gap:8px}.subdistrict-links a{padding:9px 12px;border:1px solid var(--line);border-radius:999px;background:#fff;color:#2f3f61;font-size:13px;font-weight:700}"


def child_from_parent(base: str, city_name: str, dong: str, filename: str, parent_filename: str) -> str:
    label = f"경기 {city_name} {dong}"
    text = base.replace("경기 수원시", label)
    text = re.sub(r"<title>.*?</title>", f"<title>{label} 영어회화 1:1 화상회화 무료상담 | 파워잉글리쉬</title>", text, count=1, flags=re.S)
    text = re.sub(r'<link rel="canonical" href=".*?">', f'<link rel="canonical" href="https://englishclass.kr/{filename}">', text, count=1)
    text = re.sub(r'<meta property="og:url" content=".*?">', f'<meta property="og:url" content="https://englishclass.kr/{filename}">', text, count=1)
    text = text.replace('<span>수원시</span>', f'<a href="{parent_filename}">{city_name}</a><span>›</span><span>{dong}</span>')
    text = text.replace('href="english-gyeonggi.html">경기', 'href="english-gyeonggi.html">경기')
    text = text.replace('href="english-gyeonggi.html">경기</a>\n      <span>수원시</span>', f'href="english-gyeonggi.html">경기</a>\n      <a href="{parent_filename}">{city_name}</a>\n      <span>{dong}</span>')
    text = text.replace('href="english-gyeonggi-suwon.html">경기 시·군·구 전체 보기', 'href="english-gyeonggi.html">경기 시·군·구 전체 보기')
    text = text.replace('href="english-gyeonggi-suwon.html">수원시 전체 동 보기', f'href="{parent_filename}">{city_name} 전체 읍면동 보기')
    return text


def update_parent(slug: str, city_name: str, dongs: list[str]) -> None:
    parent = ROOT / f"english-gyeonggi-{slug}.html"
    if not parent.exists():
        raise FileNotFoundError(parent)
    text = parent.read_text(encoding="utf-8")
    if "subdistricts" not in text:
        text = text.replace(".photo-strip{", CSS + ".photo-strip{", 1)
    parent_filename = parent.name
    links = "\n".join(
        f'          <a href="english-gyeonggi-{slug}-{index}.html">{dong}</a>'
        for index, dong in enumerate(dongs, 1)
    )
    block = f'''  <div class="subdistricts">\n    <h2>경기 {city_name} 읍면동 영어회화</h2>\n    <div class="subdistrict-links">\n{links}\n    </div>\n  </div>\n'''
    if "<div class=\"subdistricts\">" in text:
        text = re.sub(r'  <div class="subdistricts">.*?  </div>\n', block, text, count=1, flags=re.S)
    else:
        marker = "  </div>\n</section>\n</main>"
        text = text.replace(marker, block + marker, 1)
    parent.write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    base = (ROOT / "english-gyeonggi-suwon.html").read_text(encoding="utf-8")
    generated = 0
    for slug, (city_name, dongs) in MUNICIPALITIES.items():
        update_parent(slug, city_name, dongs)
        parent_filename = f"english-gyeonggi-{slug}.html"
        expected = {f"english-gyeonggi-{slug}-{index}.html" for index in range(1, len(dongs) + 1)}
        for old in ROOT.glob(f"english-gyeonggi-{slug}-*.html"):
            if old.name not in expected:
                old.unlink()
        for index, dong in enumerate(dongs, 1):
            filename = f"english-gyeonggi-{slug}-{index}.html"
            (ROOT / filename).write_text(
                child_from_parent(base, city_name, dong, filename, parent_filename),
                encoding="utf-8",
                newline="\n",
            )
            generated += 1
    print(f"Updated {len(MUNICIPALITIES)} parent pages")
    print(f"Generated {generated} 읍면동 pages")


if __name__ == "__main__":
    main()
