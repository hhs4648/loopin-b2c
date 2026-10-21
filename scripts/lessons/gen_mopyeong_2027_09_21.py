"""2026년 9월 모의평가(2027학년도, 평가원) 21번 레슨 + 대사를 만든다 (밑줄 의미 추론, 3점). 오답률 46% · Top 5 (메가스터디).

    PYTHONUTF8=1 py scripts/lessons/gen_mopyeong_2027_09_21.py   (→ npm run policy:copy stamp <id> → npm run build)

선생님이 확인할 점 (Claude 초안, 2026-10-21):
- 두 그룹 축: 왼쪽 「personalized 쪽 (나에게 맞춤)」 ↔ 오른쪽 「massive 쪽 (수많은 사용자)」. 5문장 but 앞뒤에서 둘이 처음 함께 나와
  칠판을 5문장에서 처음 연다(빈 칠판 금지). 1~4문장은 칠판 정리(story)만
- 5문장에 해석 맞추기(add_match, 앞 절 The outputs are personalized, but the data sets are massive만)를 넣었다 — but 대조를 손으로 맞춰 보게
- 밑줄 문장에 3지 「거울이 비춰 보이는 것」(s7_q)을 두었다: 많은 사용자가 함께 하는 검색 / 한 사람의 개인 정보 / 회사가 몰래 바꾼 결과.
  오답 두 개는 많이 고른 ③(개인 데이터 검열, 22%)·①(결과 조작, 11%) 쪽 오독이다. 보기 ②와 너무 가까워 답을 거의 주는 셈이면 빼 주세요
  (밑줄 틀 「아직 정할 것: 밑줄 뜻 3지 화면을 따로 둘지」)
- 1문장 핵심어 고르기: 답 Social media companies · keep you on site · results useful to you, 함정 are working · attempting
  (「~하려고 애쓰다」 — 무엇을 하려는지가 핵심). 함정 고르기가 어색하면 바꿔 주세요
- 2문장 bakery 예시·3문장 cats 예시는 묻지 않고 넘겼다(3문장은 한 줄 show)
- 헷갈리는 단어(trap): return(돌아오다 ✕ → 결과를 내놓다), look(look to = ~하려고 하다), prompt(신속한 ✕ → 제시하다),
  key(열쇠 ✕ → 주요한), mining(광산 ✕ → 캐내다·탐색하다), account(계좌 ✕ → take ~ into account = 고려하다), sense(감각 ✕ → in a sense = 어떤 의미에서)
  — 해설 번역(내놓아야 한다·최대화하려고 하는데·제시할지도·주요·채굴하고·고려하고·어떤 의미에서)과 대조함
- hold a mirror up to = 「~을 거울에 비추다, ~을 그대로 반영하다」, refinement = 「다듬어진 검색어」, derive = 「도출하다」 — 해설 Words and Phrases와 대조함
- 21번엔 시험지 아래 * 풀이 단어가 없다
- 4문장의 대시(―)는 하나뿐이라 흐리지 않았다. 원문의 ―(가로줄)는 다른 레슨과 같게 —로 적었다
- 평가 뒤집기(+/−)는 넣지 않았다 — 글쓴이가 자동 완성을 좋게/나쁘게 평가하는 글이 아님
- S·V 찾기 스텝은 만들지 않았다(2026-10-20 삭제), 끊어읽기 roles·slashes·modifiers만
반영한 규칙: README §0-1(2026-10-20~21), underline.md v1, 칠판은 읽은 데까지만·화면마다 X, 대사 핵심만, 칭찬 분리(엔진), 화면 중계 말 없음.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, r, choice, show, tip, groups, rows, sense, sc, keywords, topic_svg,  # noqa: E402
                      base_lesson, exam_brief, review, finish, METHOD_IMAGES)
from beginner import add_match, add_refers, m  # noqa: E402

ID = "mopyeong-2027-09-21-autocomplete-mirror"

S = [
    "Social media companies are working to keep you on site or attempting to deliver results useful to you.",
    "You can see this personalization reflected in the results of search engines, which try to maximize relevance: "
    "searching for “bakery” in New York should return different results than searching in Paris.",
    "Features like the little predictive-text cues of autocomplete also look to maximize relevance by suggesting refinements: "
    "typing in “cats” might prompt the user with “cats movie” or “cats that don’t shed.”",
    "Autocomplete suggestions offer a look into the algorithm’s understanding of accumulated user behavior — an immensely "
    "important part of how key social media algorithms work.",
    "The outputs are personalized, but the data sets are massive, and the platforms are mining for similarities across vast "
    "quantities of user information.",
    "If a whole lot of users near you or similar to you complete the search that you’ve begun with specific words, the "
    "autocomplete algorithm takes that into account and may be more likely to suggest them to you.",
    "Since the results are derived from data related to millions of searches, autocomplete is, in a sense, holding a mirror up "
    "to society.",
]
# 해설지 번역
KO = [
    "소셜 미디어 기업들은 여러분을 사이트에 머물게 하려고 노력하거나 여러분에게 유용한 결과를 제공하려고 시도한다.",
    "여러분은 관련성을 최대화하려고 노력하는 검색 엔진의 결과에 반영된 이러한 개인화를 볼 수 있는데, 뉴욕에서 '빵집(bakery)'을 검색하는 것은 파리에서 검색하는 것과 다른 결과를 내놓아야 한다.",
    "자동 완성의 작은 예측 입력 단서와 같은 기능들 또한 다듬어진 검색어들을 제안함으로써 관련성을 최대화하려고 하는데, '고양이(cats)'를 입력하면 사용자에게 '고양이 영화(cats movie)' 또는 '털 안 빠지는 고양이(cats that don’t shed)'를 제시할지도 모른다.",
    "자동 완성 제안 검색어는 누적된 사용자 행동에 대한 알고리즘의 이해를 들여다볼 수 있게 해 주는데, 이는 주요 소셜 미디어 알고리즘이 작동하는 방식의 매우 중요한 부분이다.",
    "결과물은 개인화되지만, 데이터 세트는 거대하며 플랫폼은 방대한 양의 사용자 정보 전체에서 유사성을 채굴하고 있다.",
    "여러분 근처에 있거나 여러분과 유사한 수많은 사용자가 여러분이 특정 단어를 가지고 시작한 검색을 완료한다면, 자동 완성 알고리즘은 그 점을 고려하고 그것들을 여러분에게 제안할 가능성이 더 높을 수 있다.",
    "그 결과는 수백만 건의 검색과 관련된 데이터에서 도출되기 때문에, 자동 완성은 어떤 의미에서 사회에 거울을 비추고 있는 것이다.",
]
UNDER = "holding a mirror up to society"

LEFT = "personalized 쪽 (나에게 맞춤)"
RIGHT = "massive 쪽 (수많은 사용자)"
SORT_LEFT = "왼쪽 · personalized (나에게 맞춤)"
SORT_RIGHT = "오른쪽 · massive (수많은 사용자)"


def board(left, right, fresh=(), sort=None):
    """단어 지도 — 읽은 데까지만, 단어만. sort = 학생이 끌어 넣을 말(맞는 쪽에 fresh로 넣어 두면 답하기 전엔 숨는다)"""
    return groups("자동 완성", LEFT, left, RIGHT, right, fresh=fresh, between="↔",
                  sort={"words": sort, "left": SORT_LEFT, "right": SORT_RIGHT} if sort else None)


L5 = [("personalized", "나에게 맞춘"), ("results useful to you", "나에게 쓸모 있는 결과")]
R5 = [("massive", "거대한"), ("accumulated user behavior", "쌓인 사용자 행동")]
R5B = R5 + [("similarities", "비슷한 점")]
R6 = R5B + [("a whole lot of users", "아주 많은 사용자")]
R7 = R6 + [("society", "사회")]

sentences = [
    {
        "id": 1, "text": S[0], "model_translation": KO[0], "teaching_value": "high",
        "glosses": [g("Social media companies", "소셜 미디어 기업들"), g("social", "사회의, 사회적인"), g("media", "매체"),
                    g("companies", "기업들"), g("are working", "애쓰고 있다 · work to ~ = ~하려고 노력하다"), g("working", "일하는, 노력하는"),
                    g("keep you on site", "여러분을 사이트에 머물게 하다"), g("site", "(웹)사이트"),
                    g("attempting", "시도하는 · attempt to ~ = ~하려고 시도하다"), g("deliver", "전달하다, 제공하다"),
                    g("results useful to you", "여러분에게 유용한 결과"), g("results", "결과"), g("useful", "유용한")],
        "slashes": ["are working", "on site", "or attempting", "deliver results"],
        "roles": [r("Social media companies", "S"), r("are working", "V"), r("attempting", "V")],
        "emphasis": ["keep you on site", "results useful to you"],
        "steps": [
            keywords("s1_keys", ["Social media companies", "are working", "keep you on site", "attempting", "results useful to you"],
                     ["Social media companies", "keep you on site", "results useful to you"],
                     "그건 '~하려고 애쓰다'라는 말이에요. 무엇을 하려는지가 핵심이에요.",
                     "핵심어는 Social media companies, keep you on site, results useful to you예요. 소셜 미디어 기업은 나를 사이트에 붙잡아 두고, 나에게 쓸모 있는 결과를 주려 해요.",
                     ask="이 문장을 빠르게 이해하려면 모든 단어를 읽지 않아도 돼요. 핵심어 3개를 찾아볼까요?",
                     tips=[tip("work to ~ / attempt to ~", "둘 다 '~하려고 애쓰다'예요. 뒤의 to ~가 하려는 일이에요.", "attempting"),
                           tip("results useful to you", "명사 뒤에서 useful to you가 꾸며요. '여러분에게 유용한 결과'예요.", "useful")]),
        ],
    },
    {
        "id": 2, "text": S[1], "model_translation": KO[1], "teaching_value": "high",
        "glosses": [g("You can see", "여러분은 볼 수 있다"), g("this personalization", "이러한 개인화"),
                    g("personalization", "개인화 · 사람마다 맞춰 주는 것"), g("reflected", "반영된"),
                    g("in the results of search engines", "검색 엔진의 결과에"), g("search", "검색"), g("engines", "엔진"),
                    g("try to maximize relevance", "관련성을 최대화하려고 하다"), g("maximize", "최대화하다"),
                    g("relevance", "관련성 · 나에게 맞는 정도"), g("searching for “bakery”", "'빵집'을 검색하는 것"),
                    g("searching", "검색하는 것"), g("bakery", "빵집"), g("in New York", "뉴욕에서"),
                    g("should return", "내놓아야 한다"), g("return", "돌아오다 · 여기서는 (결과를) '내놓다'"),
                    g("different results", "다른 결과"), g("different", "다른"), g("in Paris", "파리에서")],
        "slashes": ["this personalization", "of search engines,", "maximize relevance:", "in New York", "different results"],
        "roles": [r("You", "S"), r("can see", "V"), r("this personalization", "O"), r("reflected", "C"),
                  r("searching for “bakery” in New York", "S"), r("should return", "V"), r("different results", "O")],
        "modifiers": ["which try to maximize relevance"],
        "emphasis": ["this personalization", "different results"],
        "steps": [
            choice("s2_this",
                   "this personalization(이러한 개인화)은 무엇을 가리킬까요?",
                   [("o0", "나에게 쓸모 있는 결과를 주는 것", True), ("o1", "모든 사람에게 같은 결과를 주는 것", False),
                    ("o2", "회사 광고를 먼저 보여 주는 것", False)],
                   "this가 가리키는 것은 앞 문장에서 찾아요. 1문장 끝 results useful to you를 봐요.",
                   why="this는 앞 문장을 가리켜요. 1문장의 results useful to you, 나에게 쓸모 있게 맞춰 준 결과예요.",
                   highlight=["this personalization"],
                   tips=[tip("see A reflected in B", "'A가 B에 반영된 것을 보다'예요.", "reflected"),
                         tip("return", "이 글에서는 → (결과를) 내놓다  ('돌아오다' 아님)", "return", trap=True)],
                   point="this personalization = 나에게 맞춘 결과 (뉴욕과 파리에서 bakery 검색 결과가 다름)"),
        ],
    },
    {
        "id": 3, "text": S[2], "model_translation": KO[2], "teaching_value": "low",
        "glosses": [g("Features", "기능들"), g("like the little predictive-text cues", "작은 예측 입력 단서 같은"),
                    g("little", "작은"), g("predictive-text", "예측 입력"), g("cues", "단서, 신호"), g("of autocomplete", "자동 완성의"),
                    g("autocomplete", "자동 완성"), g("also look to maximize relevance", "또한 관련성을 최대화하려고 한다"),
                    g("look", "보다 · 여기서는 look to ~ = ~하려고 하다"), g("by suggesting refinements", "다듬어진 검색어를 제안함으로써"),
                    g("suggesting", "제안하는 것"), g("refinements", "다듬어진 검색어"), g("typing in “cats”", "'cats'를 입력하는 것"),
                    g("typing", "입력하는 것"), g("cats", "고양이"), g("might prompt", "제시할지도 모른다"),
                    g("prompt", "신속한 · 여기서는 '제시하다, 유도하다'"), g("the user", "사용자"), g("user", "사용자"),
                    g("movie", "영화"), g("shed", "(털이) 빠지다")],
        "slashes": ["Features", "cues of autocomplete", "maximize relevance", "refinements:", "typing in “cats”", "prompt the user",
                    "“cats movie”"],
        "roles": [r("Features like the little predictive-text cues of autocomplete", "S"), r("look to maximize", "V"),
                  r("relevance", "O"), r("typing in “cats”", "S"), r("might prompt", "V"), r("the user", "O")],
        "modifiers": ["that don’t shed"],
        "steps": [
            show("s3_skim",
                 "자동 완성(autocomplete)도 나에게 맞는 검색어를 골라 제안해요. cats를 치면 cats movie를 띄우는 식이에요.",
                 highlight=["autocomplete"], button="다음 문장",
                 tips=[tip("look", "이 글에서는 → look to ~ = ~하려고 하다  ('보다' 아님)", "look", trap=True),
                       tip("prompt", "이 글에서는 → (사용자에게) 제시하다  ('신속한' 아님)", "prompt", trap=True),
                       tip("A: 예시", "콜론(:) 뒤는 앞말의 예시예요. cats 예시는 가볍게 읽고 넘어가요.", "refinements:")]),
        ],
    },
    {
        "id": 4, "text": S[3], "model_translation": KO[3], "teaching_value": "high",
        "glosses": [g("Autocomplete suggestions", "자동 완성 제안 검색어"), g("autocomplete", "자동 완성"), g("suggestions", "제안"),
                    g("offer a look into", "~을 들여다볼 수 있게 해 주다"), g("offer", "제공하다"), g("look", "봄, 살펴봄"),
                    g("the algorithm’s understanding", "알고리즘의 이해"), g("algorithm’s", "알고리즘의"),
                    g("understanding", "이해"), g("accumulated user behavior", "누적된 사용자 행동"), g("accumulated", "누적된"),
                    g("user", "사용자"), g("behavior", "행동"), g("an immensely important part", "매우 중요한 부분"),
                    g("immensely", "매우, 엄청나게"), g("important", "중요한"), g("part", "부분"),
                    g("how key social media algorithms work", "주요 소셜 미디어 알고리즘이 작동하는 방식"),
                    g("key", "열쇠 · 여기서는 '주요한'"), g("social", "사회의"), g("media", "매체"), g("algorithms", "알고리즘"),
                    g("work", "작동하다")],
        "slashes": ["offer a look", "algorithm’s understanding", "user behavior", "important part"],
        "roles": [r("Autocomplete suggestions", "S"), r("offer", "V"), r("a look", "O")],
        "emphasis": ["accumulated user behavior"],
        "steps": [
            choice("s4_look",
                   "자동 완성 제안을 보면 무엇을 들여다볼 수 있대요?",
                   [("o0", "쌓인 사용자 행동을 알고리즘이 어떻게 이해하는지", True), ("o1", "나 한 사람이 숨긴 개인 정보", False),
                    ("o2", "회사가 광고로 번 돈", False)],
                   "offer a look into 뒤를 봐요. accumulated user behavior는 '누적된 사용자 행동'이에요.",
                   why="'the algorithm’s understanding of accumulated user behavior', 사용자들이 쌓아 온 행동을 알고리즘이 어떻게 이해하는지 보여 준대요.",
                   highlight=["accumulated user behavior"],
                   tips=[tip("offer a look into ~", "'~을 들여다볼 수 있게 해 주다'예요. 여기서 look은 명사 '살펴봄'이에요.", "offer a look"),
                         tip("대시(—) 하나", "대시(—) 뒤는 앞말을 다시 설명해요. 그만큼 아주 중요한 부분이라는 말이에요.", "immensely"),
                         tip("key", "이 글에서는 → 주요한  ('열쇠' 아님)", "key", trap=True)],
                   point="자동 완성 제안 = 누적된 사용자 행동(accumulated user behavior)을 보여 준다"),
        ],
    },
    {
        "id": 5, "text": S[4], "model_translation": KO[4], "teaching_value": "high",
        "glosses": [g("The outputs", "결과물"), g("outputs", "결과물"), g("personalized", "개인화된, 나에게 맞춘"),
                    g("the data sets", "데이터 세트"), g("data", "데이터"), g("sets", "세트, 묶음"), g("massive", "거대한"),
                    g("the platforms", "플랫폼"), g("platforms", "플랫폼"), g("are mining", "채굴하고 있다, 캐내고 있다"),
                    g("mining", "광산 · 여기서는 '캐내는, 탐색하는'"), g("similarities", "유사성, 비슷한 점"),
                    g("across vast quantities", "방대한 양 전체에서"), g("vast", "방대한"), g("quantities", "양"),
                    g("of user information", "사용자 정보의"), g("information", "정보")],
        "slashes": ["are personalized,", "are massive,", "are mining", "for similarities"],
        "roles": [r("The outputs", "S"), r("are … are", "V"), r("personalized", "C"), r("the data sets", "S"), r("massive", "C"),
                  r("the platforms", "S"), r("are mining", "V")],
        "emphasis": ["personalized", "massive", "similarities"],
        "steps": [
            choice("s5_mine",
                   "플랫폼은 방대한 사용자 정보 전체에서 무엇을 캐낸대요?",
                   [("o0", "사용자들 사이의 비슷한 점", True), ("o1", "한 사람만의 특별한 점", False),
                    ("o2", "틀린 정보", False)],
                   "are mining for 뒤를 봐요. similarities는 similar(비슷한)의 명사예요.",
                   why="'mining for similarities across vast quantities of user information', 수많은 사용자 정보에서 비슷한 점을 찾는대요.",
                   highlight=["mining", "similarities"],
                   tips=[tip("mining", "이 글에서는 → 캐내는, 탐색하는  ('광산' 아님)", "mining", trap=True)],
                   point="플랫폼 = 수많은 사용자 정보에서 비슷한 점(similarities)을 캐낸다"),
            show("s5_board", "but을 기준으로 두 그룹으로 나눠 봐요.\n결과는 나에게 맞춤(personalized)이지만, 데이터는 수많은 사용자의 것(massive)이에요.",
                 button="다음", highlight=["but"],
                 panel=board(L5, R5, fresh=("personalized", "results useful to you", "massive", "accumulated user behavior"))),
            choice("s5_sort",
                   "similarities(비슷한 점)는 칠판 어느 쪽 말일까요?",
                   [("o0", SORT_LEFT, False), ("o1", SORT_RIGHT, True)],
                   "누구와 누구 사이의 비슷한 점인지 봐요. across vast quantities of user information이에요.",
                   why="수많은 사용자 정보 전체에서 찾는 비슷한 점이에요. 나 한 사람이 아니라 많은 사용자 쪽이에요.",
                   highlight=["similarities"],
                   panel=board(L5, R5B, fresh=("similarities",), sort=["similarities"]),
                   point="similarities → massive(수많은 사용자) 쪽"),
        ],
    },
    {
        "id": 6, "text": S[5], "model_translation": KO[5], "teaching_value": "high",
        "glosses": [g("a whole lot of users", "아주 많은 사용자"), g("whole", "전체의 · a whole lot of = 아주 많은"),
                    g("lot", "많음"), g("users", "사용자들"), g("near you", "여러분 근처에 있는"), g("near", "~ 근처에"),
                    g("similar to you", "여러분과 비슷한"), g("similar", "비슷한"), g("complete", "완료하다"),
                    g("the search", "검색"), g("you’ve begun", "여러분이 시작한"), g("begun", "시작된"),
                    g("with specific words", "특정 단어로"), g("specific", "특정한"), g("words", "단어"),
                    g("the autocomplete algorithm", "자동 완성 알고리즘"), g("autocomplete", "자동 완성"), g("algorithm", "알고리즘"),
                    g("takes that into account", "그 점을 고려한다"), g("takes", "가지다"), g("account", "계좌 · 여기서는 take ~ into account = 고려하다"),
                    g("may be", "~일 수도 있다"), g("more likely", "~할 가능성이 더 높은"), g("likely", "~할 것 같은"),
                    g("suggest", "제안하다")],
        "slashes": ["of users", "similar to you", "the search", "you’ve begun", "specific words,", "the autocomplete algorithm",
                    "into account", "more likely"],
        "roles": [r("a whole lot of users near you or similar to you", "S"), r("complete", "V"),
                  r("the search that you’ve begun with specific words", "O"), r("the autocomplete algorithm", "S"), r("takes", "V"),
                  r("may be", "V"), r("more likely", "C")],
        "modifiers": ["near you or similar to you", "that you’ve begun with specific words"],
        "emphasis": ["a whole lot of users"],
        "steps": [
            choice("s6_suggest",
                   "자동 완성은 나에게 어떤 검색어를 띄울 가능성이 더 높대요?",
                   [("o0", "나와 가깝거나 비슷한 많은 사용자가 쓴 검색어", True), ("o1", "내가 예전에 딱 한 번 쓴 검색어", False),
                    ("o2", "회사가 광고하려는 검색어", False)],
                   "If 덩어리를 봐요. 누가 검색을 완료하면 알고리즘이 그걸 고려한대요.",
                   why="'If a whole lot of users near you or similar to you complete the search', 나와 가깝거나 비슷한 사용자들이 많이 쓴 검색어를 더 띄울 수 있대요.",
                   highlight=["a whole lot of users", "suggest"],
                   tips=[tip("take ~ into account", "'~을 고려하다'예요. that은 앞의 If 덩어리 내용이에요.", "into account"),
                         tip("account", "이 글에서는 → take ~ into account = 고려하다  ('계좌' 아님)", "account", trap=True),
                         tip("a whole lot of ~", "'아주 많은 ~'예요.", "whole")],
                   point="나와 비슷한 많은 사용자가 쓴 검색어 → 자동 완성이 나에게 제안"),
            choice("s6_sort",
                   "a whole lot of users(아주 많은 사용자)는 칠판 어느 쪽 말일까요?",
                   [("o0", SORT_LEFT, False), ("o1", SORT_RIGHT, True)],
                   "나 한 사람인지, 많은 사람인지 봐요.",
                   why="나 한 사람이 아니라 많은 사용자예요. massive 쪽이에요.",
                   highlight=["a whole lot of users"],
                   panel=board(L5, R6, fresh=("a whole lot of users",), sort=["a whole lot of users"]),
                   point="a whole lot of users → massive(수많은 사용자) 쪽"),
        ],
    },
    {
        "id": 7, "text": S[6], "model_translation": KO[6], "teaching_value": "high",
        "glosses": [g("Since", "~ 때문에"), g("the results", "그 결과"), g("results", "결과"), g("are derived from", "~에서 도출된다"),
                    g("derived", "도출된, 얻어진"), g("data", "데이터"), g("related to", "~와 관련된"), g("millions of searches", "수백만 건의 검색"),
                    g("related", "관련된"), g("millions", "수백만"), g("searches", "검색"), g("autocomplete", "자동 완성"),
                    g("in a sense", "어떤 의미에서"), g("sense", "감각 · 여기서는 in a sense = 어떤 의미에서"),
                    g("holding a mirror up to society", "사회에 거울을 비추고 있는"), g("holding", "들고 있는"), g("mirror", "거울"),
                    g("society", "사회")],
        "slashes": ["are derived", "from data", "of searches,", "autocomplete is,", "in a sense,", "holding a mirror"],
        "roles": [r("the results", "S"), r("are derived", "V"), r("autocomplete", "S"), r("is … holding", "V"), r("a mirror", "O")],
        "modifiers": ["related to millions of searches"],
        "emphasis": ["millions of searches"],
        "steps": [
            choice("s7_since",
                   "Since 덩어리를 보면, 자동 완성 결과는 어디에서 나올까요?",
                   [("o0", "수백만 건의 검색 데이터", True), ("o1", "나 한 사람의 검색 기록", False), ("o2", "회사가 고른 인기 검색어", False)],
                   "are derived from 뒤를 봐요. derive from ~은 '~에서 얻다'예요.",
                   why="'derived from data related to millions of searches', 수백만 건의 검색과 관련된 데이터에서 나온대요.",
                   highlight=["millions of searches"],
                   tips=[tip("be derived from ~", "'~에서 도출되다, ~에서 나오다'예요.", "derived"),
                         tip("sense", "이 글에서는 → in a sense = 어떤 의미에서  ('감각' 아님)", "sense", trap=True)],
                   point="자동 완성 결과 = 수백만 건의 검색 데이터에서 나옴"),
            choice("s7_sort",
                   "드디어 밑줄이에요. 거울이 비추는 society(사회)는 칠판 어느 쪽 말일까요?",
                   [("o0", SORT_LEFT, False), ("o1", SORT_RIGHT, True)],
                   "사회는 나 한 사람인지, 많은 사람인지 봐요.",
                   why="사회는 나 한 사람이 아니라 수많은 사람이에요. massive 쪽이에요.",
                   highlight=["society"],
                   panel=board(L5, R7, fresh=("society",), sort=["society"]),
                   point="society → massive(수많은 사용자) 쪽"),
            choice("s7_q",
                   "그럼 자동 완성이라는 거울에 비치는 것은 무엇일까요?",
                   [("o0", "많은 사용자가 함께 검색하는 것", True), ("o1", "한 사람이 숨기고 싶은 개인 정보", False),
                    ("o2", "회사가 몰래 바꾼 검색 결과", False)],
                   "거울은 앞에 있는 것을 그대로 비춰요. 자동 완성 결과가 무엇에서 나왔는지 떠올려 봐요.",
                   why="자동 완성은 수백만 건의 검색에서 비슷한 점을 찾아 보여 줘요. 개인 정보를 숨기거나 결과를 바꾼다는 말은 글에 없어요.",
                   highlight=["holding a mirror up to society"],
                   point="거울에 비치는 것 = 많은 사용자의 검색 (개인 정보·조작 이야기 X)"),
            show("s7_map",
                 "hold a mirror up to ~는 '~을 거울에 비추다', 그대로 보여 준다는 말이에요. 자동 완성은 수많은 사람이 무엇을 검색하는지 그대로 보여 줘요.\n이 뜻을 바꿔 쓴 보기를 골라 봐요.",
                 button="문제 풀러 갈게요",
                 tips=[tip("hold a mirror up to ~", "'~을 거울에 비추다, ~을 그대로 반영하다'예요.", "holding a mirror"),
                       tip("in a sense", "'어떤 의미에서'예요. 진짜 거울이 아니라 비유라는 표시예요.", "in a sense")]),
        ],
    },
]

add_match(sentences, 5, [m("The outputs", "결과물은"), " ", m("are personalized", "개인화되지만"), ", ",
                         m("the data sets", "데이터 세트는"), " ", m("are massive", "거대하다"), "."],
          display="The outputs are personalized, but the data sets are massive")
add_refers(sentences, 6, {"them": "them = specific words(특정 단어들)"})

SENSES = {
    1: [sense("to", "are working to keep", "~하려고", "work to + 동사원형 = ~하려고 노력하다"),
        sense("to", "attempting to deliver", "~하려고", "attempt to + 동사원형 = ~하려고 시도하다"),
        sense("to", "useful to you", "~에게", "useful to ~ = ~에게 유용한")],
    2: [sense("which", "search engines, which try", "(그런데) 그것은", "콤마 + which — 앞의 search engines를 덧붙여 설명"),
        sense("to", "try to maximize", "~하려고", "try to + 동사원형 = ~하려고 노력하다"),
        sense("for", "searching for “bakery”", "~을", "search for ~ = ~을 검색하다")],
    3: [sense("to", "look to maximize", "~하려고", "look to + 동사원형 = ~하려고 하다"),
        sense("that", "cats that don’t shed", "(앞 명사를 꾸밈)", "관계대명사 that + 동사 — 앞의 cats를 꾸밈")],
    5: [sense("but", "are personalized, but the data sets", "하지만", "앞뒤를 맞세우는 but"),
        sense("for", "mining for similarities", "~을 찾아", "mine for ~ = ~을 캐내다, 찾다")],
    6: [sense("if", "If a whole lot of users", "만약 ~라면", "접속사 if + 주어·동사"),
        sense("to", "similar to you", "~와", "similar to ~ = ~와 비슷한"),
        sense("that", "the search that you’ve begun", "(앞 명사를 꾸밈)", "관계대명사 that — 앞의 the search를 꾸밈"),
        sense("that", "takes that into account", "그것", "지시대명사 that — 앞의 If 덩어리 내용"),
        sense("to", "likely to suggest", "~할", "be likely to + 동사원형 = ~할 가능성이 있다"),
        sense("to", "suggest them to you", "~에게", "suggest A to B = A를 B에게 제안하다")],
    7: [sense("since", "Since the results are derived", "~ 때문에", "접속사 since + 주어·동사 = ~ 때문에"),
        sense("to", "related to millions", "~와", "related to ~ = ~와 관련된"),
        sense("to", "up to society", "~에", "hold a mirror up to ~ = ~에 거울을 비추다")],
}

WORDS = {
    "social": "사회의", "media": "매체", "companies": "기업들", "working": "노력하는", "keep": "유지하다, 머물게 하다", "site": "사이트",
    "attempting": "시도하는", "deliver": "제공하다", "results": "결과", "useful": "유용한", "can": "~할 수 있다", "see": "보다",
    "personalization": "개인화", "reflected": "반영된", "search": "검색", "engines": "엔진", "try": "노력하다", "maximize": "최대화하다",
    "relevance": "관련성", "searching": "검색하는 것", "bakery": "빵집", "new": "새로운 · New York = 뉴욕", "york": "요크 · New York = 뉴욕",
    "should": "~해야 한다", "return": "내놓다", "different": "다른", "paris": "파리", "features": "기능들", "little": "작은",
    "predictive-text": "예측 입력", "cues": "단서", "autocomplete": "자동 완성", "look": "~하려고 하다, 봄", "suggesting": "제안하는 것",
    "refinements": "다듬어진 검색어", "typing": "입력하는 것", "cats": "고양이", "prompt": "제시하다", "user": "사용자",
    "movie": "영화", "shed": "(털이) 빠지다", "suggestions": "제안", "offer": "제공하다", "algorithm’s": "알고리즘의",
    "understanding": "이해", "accumulated": "누적된", "behavior": "행동", "immensely": "매우", "important": "중요한", "part": "부분",
    "key": "주요한", "algorithms": "알고리즘", "work": "작동하다", "outputs": "결과물", "personalized": "개인화된", "data": "데이터",
    "sets": "세트", "massive": "거대한", "platforms": "플랫폼", "mining": "캐내는", "similarities": "비슷한 점", "vast": "방대한",
    "quantities": "양", "information": "정보", "whole": "전체의", "lot": "많음", "users": "사용자들", "near": "~ 근처에",
    "similar": "비슷한", "complete": "완료하다", "you’ve": "너는 ~했다 (= you have)", "begun": "시작된", "specific": "특정한",
    "words": "단어", "algorithm": "알고리즘", "takes": "가지다 · take ~ into account = 고려하다", "account": "고려 · take ~ into account",
    "likely": "~할 것 같은", "suggest": "제안하다", "derived": "도출된", "related": "관련된", "millions": "수백만", "searches": "검색",
    "sense": "의미 · in a sense = 어떤 의미에서", "holding": "들고 있는", "mirror": "거울", "society": "사회", "may": "~일 수도 있다",
}

# 칠판 정리 — 2~3문장마다, 밑줄 문장 앞에서 멈춘다(요약이 곧 답). 5문장부터는 단어 지도가 대신한다
STORIES = [
    (2, [sc("문장 1", "📱", "keep you on site · results useful to you", "소셜 미디어 기업은 나에게 쓸모 있는 결과를 주려 해요"),
         sc("문장 2", "🥐", "personalization · different results", "같은 bakery 검색도 뉴욕과 파리에서 결과가 달라요")]),
    (4, [sc("문장 3~4", "⌨️", "autocomplete · accumulated user behavior", "자동 완성 제안에는 쌓인 사용자 행동이 담겨 있어요")]),
]

OPTIONS = [
    ("1", "manipulating search results in favor of the socially influential", ["manipulating", "the socially influential"],
     "사회적으로 영향력 있는 사람들에게 유리하도록 검색 결과를 조작하는 것", False),
    ("2", "revealing commonalities in users and their shared interests", ["revealing commonalities", "shared interests"],
     "사용자들의 공통점과 그들의 공유된 관심사를 드러내는 것", True),
    ("3", "censoring personal data utilizing social media algorithms", ["censoring", "personal data"],
     "소셜 미디어 알고리즘을 활용하여 개인 데이터를 검열하는 것", False),
    ("4", "collecting information useful for building user networks", ["collecting information", "user networks"],
     "사용자 네트워크를 구축하는 데 유용한 정보를 수집하는 것", False),
    ("5", "examining apparently random data to find regularity", ["apparently random data", "regularity"],
     "규칙성을 찾기 위해 겉보기에 무작위인 것 같은 데이터를 조사하는 것", False),
]
exam = {
    "question": "밑줄 친 holding a mirror up to society가 다음 글에서 의미하는 바로 가장 적절한 것은? [3점]",
    "underline": UNDER, "analysis_first": True, "wrong_rate": 46.0, "wrong_rank": 5,
    "wrong_rate_source": "메가스터디 풀서비스 채점 기준 — 전체 응시자 공개 오답률과 다를 수 있다",
    "glosses": [g("manipulating", "조작하는 것"), g("search results", "검색 결과"), g("in favor of", "~에게 유리하도록"),
                g("the socially influential", "사회적으로 영향력 있는 사람들"), g("revealing", "드러내는 것"),
                g("commonalities", "공통점"), g("users", "사용자들"), g("shared interests", "공유된 관심사"), g("censoring", "검열하는 것"),
                g("personal data", "개인 데이터"), g("utilizing", "활용하여"), g("collecting", "수집하는 것"), g("information", "정보"),
                g("building", "구축하는 것"), g("user networks", "사용자 네트워크"), g("examining", "조사하는 것"),
                g("apparently", "겉보기에"), g("random", "무작위의"), g("regularity", "규칙성")],
    "options": [{"id": o[0], "label": o[1], "keywords": o[2], "ko": o[3], **({"correct": True} if o[4] else {})} for o in OPTIONS],
    "brief": exam_brief(
        "보기도 다 해석할 필요 없어요. 색칠된 단어만 보고, 거울이 칠판 어느 쪽을 비추는지 떠올리며 골라 봐요.",
        "정답이에요! 자동 완성은 수백만 건의 검색에서 나와요. 많은 사용자의 공통점과 관심사를 거울처럼 그대로 보여 준다는 말이에요.",
        "정답은 ②예요. 자동 완성은 수많은 사용자 정보에서 비슷한 점을 찾아 보여 줘요. 그래서 사회를 비추는 거울이에요.",
        {"1": "누구에게 유리하게 결과를 조작한다는 말은 글에 없어요. 많은 사용자의 검색을 그대로 비춰요.",
         "3": "personal data, algorithms는 글에 나온 말이지만, 데이터를 검열한다(censoring)는 이야기는 없어요.",
         "4": "사용자 네트워크를 만든다는 말은 글에 없어요. 많은 사용자의 검색을 보여 주는 거예요.",
         "5": "데이터가 무작위처럼 보인다는 말은 글에 없어요. 거울은 사용자들의 비슷한 점을 그대로 비춰요."},
        {"3": review(22,
                     "③에는 personal data, social media algorithms처럼 글에 나온 말이 많아서 그럴듯해 보여요. "
                     "하지만 글에 검열(censoring), 즉 무언가를 막거나 지운다는 말은 없어요. 거울은 수많은 사용자의 비슷한 점을 그대로 비춰요.",
                     panel=rows(("5문장", "mining for similarities across vast quantities of user information", "수많은 사용자 정보에서 비슷한 점을 찾음", "hl"),
                                ("7문장", "holding a mirror up to society", "사회를 거울처럼 그대로 비춤", "hl"),
                                ("③", "censoring", "검열하다 — 글에 없는 말", "hl2")),
                     rank_word="가장 많이 고른")}),
}

lesson = base_lesson(
    ID, source="2026년 9월 모의평가(2027학년도, 한국교육과정평가원) 영어 21번 (밑줄 의미 추론, 3점)",
    topic="밑줄 문제 푸는 법: 핵심 단어 → 관계(personalized 쪽 ↔ massive 쪽) → 밑줄 뜻",
    method={"type": "underline_meaning", "labels": ["핵심 단어 찾기", "관계 잡기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-autocomplete-mirror.svg", ("Autocomplete", "자동 완성"), "→", ("Mirror", "거울"),
                                       "자동 완성은 무엇을 비출까?", "2026년 9월 모의평가 21번 도입 칠판"),
                      "alt": "칠판: Autocomplete(자동 완성) → Mirror(거울) — 자동 완성은 무엇을 비출까?", "kind": "drawing"},
            "method": METHOD_IMAGES["underline"]},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "검색창에 글자를 치면 검색어가 저절로 뜨죠? 이번 글은 그 자동 완성(autocomplete)을 다뤄요."}},
           {"id": "method1", "type": "say", "button": "네", "brief": {"say": "수능 문제는 시간 싸움이에요."}},
           {"id": "method2", "type": "say", "button": "좋아요",
            "brief": {"say": "밑줄 문제는 핵심 단어 위주로 지문의 요지를 빠르게 파악하면 좋아요."}}],
    exam=exam,
    key_words={"passage": [g("personalization", "개인화"), g("reflect", "반영하다"), g("maximize", "최대화하다"), g("relevance", "관련성"),
                           g("predictive", "예측의"), g("autocomplete", "자동 완성"), g("refinement", "다듬어진 검색어"),
                           g("prompt", "제시하다"), g("accumulated", "누적된"), g("immensely", "매우, 엄청나게"),
                           g("massive", "거대한"), g("mine", "채굴하다, 탐색하다"), g("similarity", "유사성"), g("vast", "방대한"),
                           g("take ~ into account", "~을 고려하다"), g("derive", "도출하다, 얻다"), g("in a sense", "어떤 의미에서"),
                           g("hold a mirror up to", "~을 거울에 비추다, ~을 그대로 반영하다")],
               "options": [g("manipulate", "조작하다"), g("commonality", "공통점"), g("censor", "검열하다"), g("apparently", "겉보기에"),
                           g("regularity", "규칙성")]},
    sentences=sentences)

finish(ID, lesson, senses=SENSES, words=WORDS, stories=STORIES, topic_intro="밑줄 문제 푸는 법")
