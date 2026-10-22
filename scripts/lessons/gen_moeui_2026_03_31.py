"""2026년 3월 고3 31번 레슨 + 대사를 만든다 (빈칸 추론, 2점). 오답률 59.8%(EBS) · Top 8.

    PYTHONUTF8=1 py scripts/lessons/gen_moeui_2026_03_31.py   (→ npm run policy:copy stamp <id> → npm run build)

틀: docs/tutor/templates/blank.md — 빈칸이 마지막 문장(33번 꼴). 정답 ⑤ capitalist.
선택률(EBS): ① 13.9 ② 19.1 ③ 15.4 ④ 11.4 ⑤ 40.2 — 많이 고른 오답 ② individualist(개인주의적).
② 짐작: 글에 the artist · their ability · 「교수의 말」처럼 예술가 한 사람이 나와서. 7문장이 「교수 혼자 생각이 아니라
문화의 규범(cultural norms)」이라고 짚으니 s7_q 오답 보기와 option_review에서 같이 짚는다.
③ romantic은 글(5문장)에 나온 단어 — 칠판 without commerce 쪽에 넣어 둔다(반대 쪽 말).
열쇠: 두 쪽 — commerce 쪽(commerce · professional · productive · money · the only marker of success · commercial · earn money)
↔ without commerce 쪽(hobby · for art’s sake · romantic). 빈칸 문장은 then(그렇다면)으로 8문장의 결론 → 같은 쪽.
시험지 아래 *풀이 단어 없음. 해설지(해설-pymupdf.txt) 해석과 대조함 — 단어 뜻·Tip은 해설 번역을 따랐다.
규칙 반영: 2026-10-21까지 — S·V 찾기 스텝 없음(svo-finding), 핵심어 나열형 translate 없음, 끊어읽기(slashes·roles·modifiers),
화면 중계 말 없음, 칭찬과 질문 분리(엔진), option_review는 review()(되묻기 없음). Claude 초안 — 선생님 검토 전.

선생님이 확인할 점
1. 「같은 쪽? 반대 쪽?」의 기준 — 글쓴이는 7문장에서 교수의 말을 의심(But … merely … mindlessly?)하지만, 빈칸 문장은
   8문장(서양 문화에서 전문 = 상업)의 결론(then)이다. 그래서 s9_side는 「글쓴이 주장」이 아니라 「앞 문장과 같은 쪽?」으로 물었다.
2. ② individualist를 많이 고른 이유는 추측이다(예술가 개인 · 교수 한 사람). 다른 이유로 보시면 option_review 문구를 고쳐야 한다.
3. 칠판 묶음 이름을 「commerce 쪽 / without commerce 쪽」(1문장 말)으로 했다. 5문장의 for art’s sake · romantic도 without commerce 쪽에 넣었다.
4. romantic은 시험 보기 ③이라 헷갈리는 단어(trap)로 두지 않고 s5_seen에서 「좋게 보는 말이 아니에요」로만 짚었다.
   평소와 반대 평가(evaluation-flip)로 2지를 따로 묻지 않은 것은 글쓴이가 아니라 문화의 평가라서.
5. 헷갈리는 단어(trap) 후보: senior(졸업반) · nature(본질) · marker(지표) · title(직함) · then(그렇다면) — 엑셀(함정단어.xlsx)에는 안 넣었다.
6. 해석 맞추기는 1문장(짧은 문장)에만 넣었다. 나머지 짧은 문장(5·9)은 뜻 질문·빈칸 뜻 질문과 겹쳐서 뺐다.
7. 3문장 끊어읽기 roles에 if절 안 주어 we 다섯 개와 동사(are not engaged in · are not … are not · can … call)를 「…」로 차례로 잡았다 — 화면에서 자리가 맞는지 눌러 볼 것.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, r, choice, show, pick, tip, groups, rows, sense, sc, m, topic_svg,  # noqa: E402
                      base_lesson, exam_brief, review, finish)
from beginner import add_match, add_refers  # noqa: E402

ID = "moeui-2026-03-31-art-and-commerce"

BLANK = "Professional art, then, is inherently ________."
S = [
    "“Art without commerce is a hobby.”",
    "These words, spoken with much authority to senior fine arts majors, are the kind that those who create art are unable to ignore.",
    "We worry about this idea that if we are not engaged in commerce, then we are not professional; and if we are not professional, "
    "can we even call ourselves artists?",
    "Art of any form, by its very nature, cannot or should not be quantified, and yet writers measure pages and words; visual artists "
    "measure canvases completed all in an effort to appear “productive,” to perhaps justify this urge to create.",
    "The notion of creating for art’s sake is then seen as hopelessly romantic and nearly indefensible.",
    "Of course one can engage in art, but it better be for money, for that is the only marker of success.",
    "But was that professor’s declaration merely an old talker with a title mindlessly repeating the cultural norms and expectations "
    "that had, in fact, labeled him as “successful”?",
    "In Western culture, it is almost impossible to separate professional from commercial, and so the artist is legitimized by their "
    "ability to earn money.",
    BLANK,
]
# 해설지 해석 (2026-03-고3/해설-pymupdf.txt 31번)
KO = [
    "“상업이 없는 예술은 취미이다.”",
    "졸업반 미술 전공생들에게 큰 권위를 가지고 전달된 이 말은 예술을 창조하는 이들이 무시할 수 없는 종류의 말이다.",
    "우리는 만약 상업에 종사하지 않으면 전문가가 아니라는 이 생각에 대해 걱정하며, 그러면 만약 우리가 전문가가 아니라면 자신을 예술가라고 심지어 부를 수 있겠는가?",
    "어떤 형태의 예술이든 바로 그 본질상 수량화될 수 없거나 되어서는 안 되는 것임에도 불구하고, 작가들은 쪽수와 단어 수를 세고, "
    "시각 예술가는 완성된 캔버스 개수를 세는데, (이는) 모두 ‘생산적’으로 보이기 위한, 어쩌면 창작하고자 하는 이 충동을 정당화하기 위한 노력이다.",
    "예술을 위한 창작이라는 개념은 그러면 어찌할 도리가 없을 정도로 낭만적이고 거의 옹호의 여지가 없는 것으로 보인다.",
    "물론 한 사람은 예술에 종사할 수 있지만, 그것은 돈을 위한 것인 편이 나은데, 돈이 성공의 유일한 지표이기 때문이다.",
    "하지만 그 교수의 선언은, 직함을 가진 나이 든 수다쟁이가 사실상 그에게 ‘성공한’ 사람이라는 명칭을 붙여 준 문화적 규범과 기대를 아무 생각 없이 되풀이하는 것에 불과한가?",
    "서양 문화권에서는 상업성에서 전문성을 분리하는 것이 거의 불가능하며, 따라서 예술가는 돈을 버는 능력에 의해 정당성을 부여받는다.",
    "그렇다면, 전문 예술은 본질적으로 ________이다.",
]

LEFT = "왼쪽 · commerce 쪽"
RIGHT = "오른쪽 · without commerce 쪽"


def board(left, right, fresh=(), sort=None):
    """단어 지도 — 묶음 이름은 1문장에 나온 말까지만(commerce / without commerce). 빈칸 말(자본주의)은 쓰지 않는다"""
    return groups("예술과 commerce", "commerce 쪽", left, "without commerce 쪽", right, fresh=fresh, between="↔",
                  sort={"words": sort, "left": LEFT, "right": RIGHT} if sort else None)


L1 = [("commerce", "상업")]
R1 = [("hobby", "취미")]
L3 = L1 + [("professional", "전문가")]
L4 = L3 + [("productive", "생산적인")]
R5 = R1 + [("for art’s sake", "예술을 위해"), ("romantic", "낭만적일 뿐")]
L8 = L4 + [("money", "돈"), ("the only marker of success", "성공의 유일한 지표"), ("commercial", "상업적인"), ("earn money", "돈을 벌다")]

SIDE_TIP = tip("같은 쪽? 반대 쪽?", "빈칸 문장에 But, However, not 같은 반전 단서가 있으면 반대 의견이 들어가요. "
               "then(그렇다면)처럼 앞 내용을 받아 결론을 내면 앞과 같은 말이 들어가요.")

sentences = [
    {
        "id": 1, "text": S[0], "model_translation": KO[0], "teaching_value": "high",
        "glosses": [g("Art without commerce", "상업이 없는 예술"), g("Art", "예술"), g("without commerce", "상업이 없는"),
                    g("commerce", "상업 · 사고팔아 돈을 버는 일"), g("is", "~이다"), g("a hobby", "취미"), g("hobby", "취미"),
                    g("Professional art", "전문 예술"), g("Professional", "전문적인, 직업으로 하는"), g("then", "그렇다면"),
                    g("inherently", "본질적으로, 원래부터")],
        "roles": [r("Art without commerce", "S"), r("is", "V"), r("a hobby", "C")],
        "steps": [
            show("s1_passage", "빈칸은 마지막 문장에 있어요. 이 문장을 잠깐 볼까요?",
                 button="네", before_read=True, show_passage=[BLANK], method=0),
            choice("s1_blank_meaning",
                   "핵심어만 칠해 뒀어요. 이 문장은 무슨 뜻일까요?",
                   [("o0", "그래서 전문 예술은 가끔 ____일 수도 있다", False),
                    ("o1", "그렇다면 전문 예술은 본질적으로 ____이다", True),
                    ("o2", "하지만 전문 예술은 결코 ____이 아니다", False)],
                   "콤마 사이 then은 '그렇다면'이에요. inherently는 '본질적으로, 원래부터'예요.",
                   why="'then'은 '그렇다면', 'inherently'는 '본질적으로'예요. not 같은 부정어도 없어요.",
                   before_read=True, display=BLANK, tag="빈칸 문장", method=0,
                   highlight=["Professional art", "then", "inherently", "________"],
                   tips=[tip("then (콤마 사이)", "문장 가운데 콤마 사이의 then은 '그렇다면, 그러니까'예요. 앞 내용을 받아 결론을 말해요.")]),
            show("s1_where", "then(그렇다면)이 있으니 앞 내용의 결론이에요. 전문 예술(Professional art)이 어떤 성질인지 생각하며 처음부터 읽어 봐요.",
                 button="처음부터 읽어 볼게요", before_read=True, display=BLANK, tag="빈칸 문장", method=0),
            show("s1_board", "상업(commerce)이 없는 예술은 취미(hobby)일 뿐이래요. 이 두 말이 글의 두 쪽이에요.",
                 panel=board(L1, R1, fresh=("commerce", "hobby")), highlight=["commerce", "hobby"], button="다음 문장"),
        ],
    },
    {
        "id": 2, "text": S[1], "model_translation": KO[1], "teaching_value": "low",
        "glosses": [g("These words", "이 말"), g("spoken with much authority", "큰 권위를 가지고 전달된"), g("authority", "권위"),
                    g("to senior fine arts majors", "졸업반 미술 전공생들에게"), g("senior", "졸업반의, 최고 학년의"),
                    g("fine arts", "미술"), g("majors", "전공생"), g("are", "~이다"), g("the kind", "종류"),
                    g("those who create art", "예술을 창조하는 이들"), g("create", "창조하다, 창작하다"),
                    g("are unable to ignore", "무시할 수 없다"), g("unable", "~할 수 없는"), g("ignore", "무시하다")],
        "slashes": ["These words,", "fine arts majors,", "the kind", "create art"],
        "roles": [r("These words", "S"), r("are", "V"), r("the kind", "C")],
        "modifiers": ["spoken with much authority to senior fine arts majors", "that those who create art are unable to ignore"],
        "steps": [
            show("s2_note", "These words는 앞의 그 말이에요. 예술을 하는 사람들은 이 말을 무시할 수 없대요.",
                 highlight=["unable to ignore"], faded=["spoken with much authority to senior fine arts majors,"], button="다음 문장",
                 tips=[tip("those who ~", "'~하는 사람들'이에요. those who create art = 예술을 창조하는 이들.", "those who")]),
        ],
    },
    {
        "id": 3, "text": S[2], "model_translation": KO[2], "teaching_value": "high",
        "glosses": [g("We", "우리는"), g("worry about", "~에 대해 걱정하다"), g("this idea", "이 생각"), g("idea", "생각"),
                    g("are not engaged in", "~에 종사하지 않다"), g("engaged in", "~에 종사하는"), g("engaged", "종사하는, 관여하는"),
                    g("commerce", "상업"), g("professional", "전문가인, 전문적인"), g("call ourselves", "자신을 ~라고 부르다"),
                    g("ourselves", "우리 자신"), g("even", "심지어"), g("artists", "예술가")],
        "slashes": ["this idea", "in commerce,", "not professional;", "not professional,"],
        "roles": [r("We … we … we … we … we", "S"), r("worry about", "V"), r("this idea", "O"), r("are not engaged in", "V"),
                  r("are not … are not", "V"), r("can … call", "V")],
        "steps": [
            choice("s3_chain",
                   "this idea(이 생각)는 어떤 생각일까요?",
                   [("o0", "상업을 안 하면 전문가가 아니고, 전문가가 아니면 예술가라고 부를 수도 없다", True),
                    ("o1", "전문가가 되면 상업을 하지 않아도 된다", False),
                    ("o2", "예술가는 누구나 스스로 전문가라고 부를 수 있다", False)],
                   "that 뒤가 그 생각이에요. if A, then B(A라면 B)가 두 번 이어져요.",
                   why="'if we are not engaged in commerce, then we are not professional', 상업을 안 하면 전문가가 아니래요. 그럼 예술가라고 부를 수 있을지 걱정해요.",
                   highlight=["commerce", "not professional;", "artists"],
                   tips=[tip("this idea that ~", "'~라는 이 생각'이에요. that 뒤가 idea의 내용이에요.", "this idea"),
                         tip("be engaged in ~", "'~에 종사하다, ~을 하다'예요. engaged in commerce = 상업에 종사하는.", "engaged in")]),
            pick("s3_same", "commerce와 같은 쪽 말을 이 문장에서 하나 더 찾아 눌러 볼까요?",
                 ["this idea", "professional", "artists"], ["professional"],
                 "그건 commerce와 같은 쪽 말이 아니에요.",
                 "상업을 해야 professional(전문가)이래요. commerce와 같은 쪽이에요.",
                 wrong_by={"this idea": "this idea는 that 뒤 생각 전체를 가리켜요.",
                           "artists": "artists는 마지막에 걱정하는 말이에요. 상업을 안 하면 무엇이 아니라고 했는지 봐요."}),
        ],
    },
    {
        "id": 4, "text": S[3], "model_translation": KO[3], "teaching_value": "high",
        "glosses": [g("Art of any form", "어떤 형태의 예술이든"), g("form", "형태"), g("by its very nature", "바로 그 본질상"),
                    g("nature", "본질, 본성"), g("cannot or should not be quantified", "수량화될 수 없거나 되어서는 안 된다"),
                    g("quantified", "수량화된, 수로 세어진"), g("and yet", "그런데도"), g("writers", "작가들"),
                    g("measure", "세다, 재다"), g("pages and words", "쪽수와 단어 수"), g("visual artists", "시각 예술가"),
                    g("visual", "시각의"), g("canvases completed", "완성된 캔버스"), g("canvases", "캔버스"),
                    g("completed", "완성된"), g("in an effort to", "~하려는 노력으로"), g("effort", "노력"),
                    g("appear", "~처럼 보이다"), g("productive", "생산적인 · 결과물을 많이 내는"),
                    g("to perhaps justify", "어쩌면 정당화하기 위해"), g("justify", "정당화하다"), g("perhaps", "어쩌면"),
                    g("this urge to create", "창작하고자 하는 이 충동"), g("urge", "충동")],
        "slashes": ["of any form,", "very nature,", "be quantified,", "pages and words;", "canvases completed", "in an effort",
                    "“productive,”", "perhaps justify"],
        "roles": [r("Art of any form", "S"), r("cannot or should not be quantified", "V"), r("writers", "S"),
                  r("measure … measure", "V"), r("pages and words", "O"), r("visual artists", "S"), r("canvases completed", "O")],
        "steps": [
            choice("s4_yet",
                   "and yet 앞뒤를 이으면 무슨 뜻일까요?",
                   [("o0", "예술은 수로 셀 수 없는데도, 작가들은 쪽수와 단어 수를 센다", True),
                    ("o1", "예술은 수로 셀 수 없어서, 작가들은 아무것도 세지 않는다", False),
                    ("o2", "예술은 수로 세야 해서, 작가들은 쪽수와 단어 수를 센다", False)],
                   "quantified는 '수량화된, 수로 세어진'이에요. and yet은 앞과 어긋나는 일을 이어요.",
                   why="'cannot or should not be quantified', 예술은 수로 셀 수 없대요. 'and yet writers measure pages and words', 그런데도 작가들은 쪽수와 단어 수를 세요.",
                   highlight=["quantified", "and yet", "measure"], faded=["by its very nature,"],
                   tips=[tip("and yet", "'그런데도, 그럼에도'예요. 앞 내용과 어긋나는 일을 이어요.", "and yet")]),
            choice("s4_sort",
                   "'in an effort to appear productive', 생산적으로 보이려고 센대요. productive는 칠판 어느 쪽일까요?",
                   [("o0", LEFT, True), ("o1", RIGHT, False)],
                   "productive(생산적인)는 결과물을 많이 내 보이는 거예요. 상업을 해야 전문가라는 말을 떠올려 봐요.",
                   why="productive는 결과물을 많이 내서 보여 주는 말이에요. 상업·전문가와 함께 가는 말이에요.",
                   panel=board(L3, R1, sort=["productive"]), highlight=["productive"],
                   tips=[tip("in an effort to ~", "'~하려는 노력으로'예요. all in an effort to appear productive = 모두 생산적으로 보이려는 노력이에요.",
                             "in an effort")]),
        ],
    },
    {
        "id": 5, "text": S[4], "model_translation": KO[4], "teaching_value": "high",
        "glosses": [g("The notion", "개념"), g("notion", "개념, 생각"), g("of creating", "창작한다는"), g("creating", "창작하는 것"),
                    g("for art’s sake", "예술을 위한 · 돈이 아니라 예술 그 자체를 위해"), g("sake", "위함, 목적"),
                    g("is then seen as", "그러면 ~로 보인다"), g("seen", "보이는, 여겨지는"),
                    g("hopelessly romantic", "어찌할 도리가 없을 정도로 낭만적인"), g("hopelessly", "어찌할 도리가 없을 정도로"),
                    g("romantic", "낭만적인"), g("nearly indefensible", "거의 옹호의 여지가 없는"), g("nearly", "거의"),
                    g("indefensible", "옹호의 여지가 없는")],
        "slashes": ["for art’s sake", "then seen", "hopelessly romantic"],
        "roles": [r("The notion of creating for art’s sake", "S"), r("is then seen as", "V"),
                  r("hopelessly romantic and nearly indefensible", "C")],
        "steps": [
            choice("s5_seen",
                   "'creating for art’s sake(예술을 위한 창작)'는 어떻게 여겨진대요?",
                   [("o0", "어찌할 도리 없이 낭만적이고, 거의 옹호할 수 없다", True),
                    ("o1", "가장 전문적이고 훌륭하다", False),
                    ("o2", "돈을 가장 많이 버는 길이다", False)],
                   "is seen as A는 'A로 여겨지다'예요. as 뒤 두 말을 봐요.",
                   why="'hopelessly romantic and nearly indefensible', 어찌할 도리 없이 낭만적이고 거의 옹호의 여지가 없대요. 좋게 보는 말이 아니에요.",
                   highlight=["romantic", "indefensible"],
                   tips=[tip("for art’s sake", "'예술을 위해'예요. for one’s sake = ~을 위해. 돈이 아니라 예술 그 자체가 목적이에요.", "art’s sake"),
                         tip("be seen as ~", "'~로 보이다, ~로 여겨지다'예요.", "seen as")]),
            show("s5_map", "돈이 안 되는 '예술을 위한 창작'은 낭만적일 뿐(romantic)이라고 여겨진대요. 상업이 없는 쪽 말이에요.",
                 panel=board(L4, R5, fresh=("for art’s sake", "romantic")), highlight=["for art’s sake", "romantic"],
                 button="다음 문장"),
        ],
    },
    {
        "id": 6, "text": S[5], "model_translation": KO[5], "teaching_value": "high",
        "glosses": [g("Of course", "물론"), g("one", "한 사람, 누구나"), g("can engage in", "~에 종사할 수 있다"),
                    g("engage in art", "예술에 종사하다"), g("engage", "종사하다, 참여하다"), g("art", "예술"),
                    g("better be", "~인 편이 낫다"), g("for money", "돈을 위한"), g("money", "돈"),
                    g("the only marker of success", "성공의 유일한 지표"), g("marker", "지표, 표시"), g("success", "성공"),
                    g("only", "유일한")],
        "slashes": ["Of course", "engage in art,", "for money,"],
        "roles": [r("one", "S"), r("can engage in", "V"), r("art", "O"), r("it", "S"), r("better be", "V"), r("that", "S"),
                  r("is", "V"), r("the only marker of success", "C")],
        "steps": [
            choice("s6_meaning",
                   "이 문장은 무슨 뜻일까요?",
                   [("o0", "예술을 해도 되지만 돈을 위해서여야 한다, 돈이 성공의 유일한 지표니까", True),
                    ("o1", "예술은 돈을 위해서 하면 안 된다, 돈은 성공의 지표가 아니니까", False),
                    ("o2", "누구나 예술을 하면 돈을 벌 수 있다, 성공은 쉬우니까", False)],
                   "but 뒤 'it better be for money'를 봐요. 콤마 뒤 for는 '왜냐하면'이에요.",
                   why="'it better be for money'는 돈을 위한 것인 편이 낫다는 말이에요. 'for that is the only marker of success', 돈이 성공의 유일한 지표이기 때문이래요.",
                   highlight=["but", "money", "marker of success"],
                   tips=[tip("it better be ~", "it had better be ~에서 had가 빠진 말이에요. '~인 편이 낫다'예요.", "better be"),
                         tip("for + 문장", "콤마 뒤 for가 문장을 이끌면 '왜냐하면 ~이니까'예요. for that is … = 그것(돈)이 …이기 때문이다.", "for that")]),
            pick("s6_same", "commerce 쪽 말 두 개를 이 문장에서 찾아 눌러 볼까요?",
                 ["engage in art", "money", "the only marker of success"], ["money", "the only marker of success"],
                 "그건 commerce 쪽 말이 아니에요.",
                 "money(돈), the only marker of success(성공의 유일한 지표)예요. 돈이 성공을 재는 유일한 잣대래요.",
                 praise="다 찾았어요!",
                 wrong_by={"engage in art": "engage in art는 '예술에 종사하다'예요. 무엇을 위해서여야 한다고 했는지 봐요."}),
        ],
    },
    {
        "id": 7, "text": S[6], "model_translation": KO[6], "teaching_value": "high",
        "glosses": [g("was", "~이었다"), g("that professor’s declaration", "그 교수의 선언"), g("professor’s", "교수의"),
                    g("declaration", "선언"), g("merely", "~에 불과한, 단지"), g("an old talker", "나이 든 수다쟁이"),
                    g("talker", "수다쟁이, 말하는 사람"), g("with a title", "직함을 가진"), g("title", "직함"),
                    g("mindlessly repeating", "아무 생각 없이 되풀이하는"), g("mindlessly", "아무 생각 없이"), g("repeating", "되풀이하는"),
                    g("the cultural norms and expectations", "문화적 규범과 기대"), g("cultural norms", "문화적 규범"),
                    g("cultural", "문화적인"), g("norms", "규범"), g("expectations", "기대"), g("in fact", "사실상"),
                    g("labeled", "명칭을 붙였다"), g("him", "그를(그 교수)"), g("successful", "성공한")],
        "slashes": ["professor’s declaration", "with a title", "mindlessly repeating", "and expectations", "in fact,"],
        "roles": [r("was", "V"), r("that professor’s declaration", "S"), r("an old talker", "C")],
        "modifiers": ["with a title", "mindlessly repeating the cultural norms and expectations",
                      "that had, in fact, labeled him as “successful”"],
        "steps": [
            choice("s7_q",
                   "But으로 시작하는 질문이에요. 글쓴이는 교수의 말을 어떻게 볼까요?",
                   [("o0", "문화의 규범을 생각 없이 되풀이한 말일 수 있다", True),
                    ("o1", "누구나 따라야 할 옳은 말이다", False),
                    ("o2", "교수 혼자만의 특별한 생각이다", False)],
                   "merely(~에 불과한), mindlessly repeating(아무 생각 없이 되풀이하는) 뒤를 봐요.",
                   why="'mindlessly repeating the cultural norms and expectations', 문화적 규범과 기대를 생각 없이 되풀이했다는 거예요. 교수 혼자 만든 생각이 아니에요.",
                   highlight=["merely", "repeating", "cultural norms"],
                   tips=[tip("But + 질문", "But으로 시작하는 질문은 '정말 그럴까?' 하고 앞의 말을 의심하는 경우가 많아요.", "But was")]),
            show("s7_note", "교수의 말은 혼자 생각이 아니라 문화적 규범(cultural norms)을 되풀이한 거래요. 그 규범이 교수를 '성공한' 사람이라고 불러 줬어요.",
                 highlight=["cultural norms", "successful"], button="다음 문장"),
        ],
    },
    {
        "id": 8, "text": S[7], "model_translation": KO[7], "teaching_value": "high",
        "glosses": [g("In Western culture", "서양 문화권에서는"), g("Western", "서양의"), g("culture", "문화"),
                    g("Western culture", "서양 문화"), g("is", "~이다"), g("almost impossible", "거의 불가능한"),
                    g("impossible", "불가능한"), g("almost", "거의"), g("separate", "분리하다, 떼어 놓다"),
                    g("professional", "전문적인 것, 전문성"), g("from commercial", "상업성에서"), g("commercial", "상업적인 것, 상업성"),
                    g("and so", "따라서, 그래서"), g("the artist", "예술가"), g("artist", "예술가"),
                    g("is legitimized", "정당성을 부여받다"), g("legitimized", "정당성을 부여받은"),
                    g("their ability", "그들의 능력"), g("ability", "능력"), g("earn money", "돈을 벌다"), g("earn", "벌다")],
        "slashes": ["In Western culture,", "almost impossible", "separate professional", "from commercial,", "and so the artist",
                    "is legitimized", "their ability"],
        "roles": [r("it", "S"), r("is", "V"), r("almost impossible", "C"), r("the artist", "S"), r("is legitimized", "V")],
        "steps": [
            choice("s8_sep",
                   "'it is almost impossible to separate professional from commercial'은 무슨 뜻일까요?",
                   [("o0", "전문적인 것을 상업적인 것에서 떼어 놓기가 거의 불가능하다", True),
                    ("o1", "전문적인 것과 상업적인 것은 거의 상관이 없다", False),
                    ("o2", "전문가는 상업적인 일을 하면 안 된다", False)],
                   "separate A from B는 'A를 B에서 떼어 놓다'예요. it은 뒤의 to separate …를 가리켜요.",
                   why="'separate professional from commercial'은 전문성을 상업성에서 떼어 놓는 거예요. 그게 거의 불가능하대요.",
                   highlight=["impossible", "separate", "commercial"],
                   tips=[tip("it ~ to …", "it은 뒤의 to 덩어리를 가리켜요. it is impossible to separate … = …을 떼어 놓는 것은 불가능하다.", "it is"),
                         tip("separate A from B", "'A를 B에서 분리하다, 떼어 놓다'예요.", "separate")]),
            pick("s8_same", "professional 말고 commerce 쪽 말 두 개를 더 찾아 눌러 볼까요?",
                 ["Western culture", "commercial", "the artist", "earn money"], ["commercial", "earn money"],
                 "그건 commerce 쪽 말이 아니에요.",
                 "commercial(상업적인 것), earn money(돈을 벌다)예요. 예술가는 돈 버는 능력으로 정당성을 부여받는대요.",
                 praise="다 찾았어요!",
                 wrong_by={"Western culture": "Western culture는 '서양 문화'예요. 어디 이야기인지 알려 주는 말이에요.",
                           "the artist": "the artist는 정당성을 부여받는 사람이에요. 무엇으로 받는지 봐요."}),
            show("s8_map", "서양 문화에서는 전문과 상업을 떼어 놓을 수 없어요. 그래서 예술가는 돈 버는 능력으로 인정받아요.",
                 panel=board(L8, R5, fresh=("money", "the only marker of success", "commercial", "earn money")),
                 highlight=["commercial", "earn money"], button="다음 문장",
                 tips=[tip("legitimize", "'정당성을 부여하다'예요. is legitimized by ~ = ~로 정당성을 부여받는다.", "legitimized")]),
        ],
    },
    {
        "id": 9, "text": BLANK, "model_translation": KO[8], "teaching_value": "high",
        "glosses": [g("Professional art", "전문 예술"), g("Professional", "전문적인, 직업으로 하는"), g("art", "예술"),
                    g("then", "그렇다면"), g("is", "~이다"), g("inherently", "본질적으로, 원래부터")],
        "roles": [r("Professional art", "S"), r("is", "V")],
        "steps": [
            choice("s9_side",
                   "앞 문장은 '전문과 상업은 떼어 놓을 수 없다'예요. 빈칸 문장은 이 말과 같은 쪽일까요, 반대 쪽일까요?",
                   [("o0", "같은 쪽 (commerce 쪽)", True), ("o1", "반대 쪽 (without commerce 쪽)", False)],
                   "then(그렇다면)은 앞 내용을 받아 결론을 내요. But이나 not 같은 반전 단서도 없어요.",
                   why="then은 '그렇다면'이라 앞 문장의 결론이에요. 반전 단서가 없고, Professional art는 칠판의 professional 쪽 말이에요.",
                   highlight=["Professional art", "then"], tips=[SIDE_TIP],
                   point="빈칸 = then(그렇다면)으로 8문장(전문 = 상업)의 결론 = commerce 쪽 = 같은 쪽"),
            choice("s9_fill",
                   "빈칸에는 어떤 말이 와야 할까요?",
                   [("o0", "돈과 상관없이 예술 그 자체를 위한", False),
                    ("o1", "예술가 한 사람 한 사람의 개성을 따르는", False),
                    ("o2", "돈을 버는 일(상업)과 떼어 놓을 수 없는", True)],
                   "앞 문장 'separate professional from commercial'과 'ability to earn money'를 떠올려 봐요.",
                   why="전문 예술은 상업과 떼어 놓을 수 없고, 돈 버는 능력으로 인정받아요. 그 성질이 빈칸에 들어가요.",
                   highlight=["inherently", "________"]),
            show("s9_go", "빈칸은 commerce 쪽, 돈벌이와 떼어 놓을 수 없는 성질이에요. 이 말을 한 단어로 바꿔 쓴 보기를 찾아봐요.",
                 button="문제 풀러 갈게요"),
        ],
    },
]

# 해석 맞추기 — 짧은 1문장만 (모두에게). 덩어리는 문장에 그대로 있는 구절
add_match(sentences, 1, [m("Art without commerce", "상업이 없는 예술은"), " ", m("a hobby", "취미"), m("is", "이다"), "."])
# 가리키는 말
add_refers(sentences, 2, {"These words": "“Art without commerce is a hobby.”(상업이 없는 예술은 취미이다)"})
add_refers(sentences, 6, {"that": "money(돈)"})
add_refers(sentences, 7, {"him": "that professor(그 교수)"})
add_refers(sentences, 8, {"it": "to separate professional from commercial(상업성에서 전문성을 분리하는 것)"})

SENSES = {
    2: [sense("to", "to senior fine arts majors", "~에게", "전치사 to (spoken to + 사람 = ~에게 전달된)"),
        sense("that", "the kind that", "~하는 (종류)", "관계대명사 that — 앞의 the kind를 꾸민다"),
        sense("to", "unable to ignore", "~할 (수 없는)", "be unable to + 동사원형 = ~할 수 없다")],
    3: [sense("that", "this idea that", "~라는 (생각)", "동격 that — this idea의 내용"),
        sense("if", "if we are not engaged", "만약 ~라면", "조건 if (if A, then B)"),
        sense("if", "if we are not professional", "만약 ~라면", "조건 if")],
    4: [sense("yet", "and yet", "그런데도", "접속사 yet (and yet = 그런데도)"),
        sense("to", "in an effort to appear", "~하려는 (노력)", "in an effort to + 동사원형 = ~하려는 노력으로"),
        sense("to", "to perhaps justify", "~하기 위한", "앞의 effort에 이어지는 둘째 to부정사"),
        sense("to", "urge to create", "~하고자 하는 (충동)", "명사 + to부정사 (urge to ~ = ~하고자 하는 충동)")],
    5: [sense("for", "for art’s sake", "~을 위한", "for one’s sake = ~을 위해"),
        sense("as", "seen as", "~로", "be seen as A = A로 보이다, 여겨지다")],
    6: [sense("but", "but it better be", "하지만", "접속사 but"),
        sense("for", "for money", "~을 위한", "전치사 for (목적)"),
        sense("for", "for that is", "왜냐하면 ~이니까", "접속사 for (콤마 뒤 이유)"),
        sense("that", "that is the only marker", "그것(돈)", "지시대명사 that — 앞의 money")],
    7: [sense("but", "But was", "하지만", "접속사 But (의심하는 질문을 이끈다)"),
        sense("that", "that professor’s", "그 (교수의)", "지시형용사 that"),
        sense("that", "that had labeled", "~한 (규범과 기대)", "관계대명사 that — the cultural norms and expectations를 꾸민다"),
        sense("as", "labeled him as", "~라고", "label A as B = A에게 B라는 명칭을 붙이다")],
    8: [sense("to", "to separate", "~하는 것은", "가주어 it … to부정사 (진주어)"),
        sense("so", "and so", "따라서, 그래서", "접속사 so (결과)"),
        sense("to", "ability to earn", "~할 (능력)", "명사 + to부정사 (ability to ~ = ~할 능력)")],
}

WORDS = {"words": "말", "spoken": "전달된, 말해진", "much": "많은, 큰", "fine": "미술의 · fine arts = 미술", "arts": "예술",
         "kind": "종류", "those": "~하는 이들", "create": "창조하다", "worry": "걱정하다", "call": "부르다",
         "any": "어떤", "very": "바로 그", "writers": "작가들", "pages": "쪽수", "words;": "단어 수", "artists": "예술가",
         "notion": "개념", "creating": "창작하는 것", "art’s": "예술의", "old": "나이 든", "talker": "수다쟁이",
         "norms": "규범", "expectations": "기대", "fact": "사실", "western": "서양의", "culture": "문화",
         "almost": "거의", "ability": "능력", "earn": "벌다", "money": "돈", "success": "성공", "course": "과정 · of course = 물론",
         "art": "예술", "commerce": "상업", "hobby": "취미", "professional": "전문적인", "inherently": "본질적으로",
         "authority": "권위", "senior": "졸업반의", "majors": "전공생", "unable": "~할 수 없는", "ignore": "무시하다",
         "idea": "생각", "engaged": "종사하는", "ourselves": "우리 자신", "form": "형태", "nature": "본질",
         "quantified": "수량화된", "measure": "세다", "visual": "시각의", "canvases": "캔버스", "completed": "완성된",
         "effort": "노력", "appear": "~처럼 보이다", "productive": "생산적인", "justify": "정당화하다", "urge": "충동",
         "sake": "위함", "seen": "보이는", "hopelessly": "어찌할 도리가 없을 정도로", "romantic": "낭만적인", "nearly": "거의",
         "indefensible": "옹호의 여지가 없는", "engage": "종사하다", "better": "~하는 편이 낫다", "marker": "지표",
         "professor’s": "교수의", "declaration": "선언", "merely": "~에 불과한", "title": "직함", "mindlessly": "아무 생각 없이",
         "repeating": "되풀이하는", "cultural": "문화적인", "labeled": "명칭을 붙였다", "successful": "성공한",
         "impossible": "불가능한", "separate": "분리하다", "commercial": "상업적인", "artist": "예술가",
         "legitimized": "정당성을 부여받은", "perhaps": "어쩌면"}

STORIES = [
    (3, [sc("문장 1~2", "💰", "Art without commerce = a hobby", "상업이 없는 예술은 취미일 뿐 — 예술가들이 무시할 수 없는 말이에요"),
         sc("문장 3", "😟", "not commerce → not professional", "상업을 안 하면 전문가가 아니고, 그럼 예술가도 아닐까 걱정해요")]),
    (7, [sc("문장 4", "📏", "measure → appear productive", "셀 수 없는 예술인데도 쪽수·캔버스 수를 세며 생산적으로 보이려 해요"),
         sc("문장 5~6", "💵", "money = the only marker of success", "예술을 위한 창작은 낭만적일 뿐, 돈이 성공의 유일한 지표래요"),
         sc("문장 7", "🤔", "repeating the cultural norms?", "교수의 말은 문화적 규범을 생각 없이 되풀이한 게 아닐까요")]),
]

OPTIONS = [("1", "universal", "보편적인", False), ("2", "individualist", "개인주의적인", False), ("3", "romantic", "낭만적인", False),
           ("4", "collective", "집단적인", False), ("5", "capitalist", "자본주의적인", True)]
exam = {
    "question": "다음 빈칸에 들어갈 말로 가장 적절한 것을 고르시오.",
    "underline": "________", "sentence": 9, "analysis_first": True, "wrong_rate": 59.8, "wrong_rank": 8,
    "wrong_rate_source": "EBS 공개 오답률",
    "glosses": [g("universal", "보편적인"), g("individualist", "개인주의적인"), g("romantic", "낭만적인"),
                g("collective", "집단적인"), g("capitalist", "자본주의적인")],
    "options": [{"id": o[0], "label": o[1], "keywords": [o[1]], "ko": o[2], **({"correct": True} if o[3] else {})} for o in OPTIONS],
    "brief": exam_brief(
        "칠판의 commerce 쪽 말을 한 단어로 바꾼 보기를 골라 봐요.",
        "정답이에요! 서양 문화에서 전문은 상업과 떼어 놓을 수 없고, 예술가는 돈 버는 능력으로 인정받아요. 그러니 전문 예술은 본질적으로 자본주의적(capitalist)이에요.",
        "정답은 ⑤ capitalist(자본주의적인)예요. 전문 = 상업이고, 돈이 성공의 유일한 지표였어요.",
        {"1": "universal(보편적인)은 어디서나 누구에게나 같다는 말이에요. 글은 서양 문화(Western culture)의 이야기예요.",
         "2": "예술가 한 사람(the artist)이 나와서 끌리지만, 빈칸은 돈 버는 능력, 상업과 묶인 성질이에요.",
         "3": "romantic은 글에 나온 단어지만, 돈과 상관없는 '예술을 위한 창작' 쪽 말이에요. 빈칸과 반대 쪽이에요.",
         "4": "collective(집단적인)는 여럿이 함께한다는 말이에요. 글에 함께 만든다는 이야기는 없어요."},
        {"2": review(19.1,
                     "individualist(개인주의적인)는 개인을 중요하게 여긴다는 말이에요. 글에 the artist, their ability처럼 예술가 한 사람이 나와서 끌리지만, 그 능력은 돈 버는 능력(earn money)이에요.\n교수의 말도 혼자 생각이 아니라 문화적 규범(cultural norms)이었어요.",
                     panel=rows(("8문장", "separate professional from commercial", "전문을 상업에서 떼어 놓을 수 없다", "hl"),
                                ("8문장", "their ability to earn money", "돈 버는 능력으로 인정받는다", "hl"),
                                ("7문장", "the cultural norms", "개인 생각이 아니라 문화적 규범", "hl2")),
                     rank_word="가장 많이 고른")}),
}

# ── 10분 모의고사·분석 화면의 「핵심어」(emphasis) — 지문당 10개 안팎, 주장이 서는 문장(8·9)과 1문장만 ──
EMPHASIS = {
    1: ["without commerce", "hobby"],
    8: ["impossible", "separate", "professional", "commercial", "earn money"],
    9: ["Professional art", "then", "inherently"],
}
for _s in sentences:
    for _c in _s.get("slashes", []):
        assert _s["text"].count(_c) == 1, (_s["id"], _c)  # 한 번만 나오는 말로 — 끊을 자리가 하나로 정해지게
    if EMPHASIS.get(_s["id"]):
        _s["emphasis"] = EMPHASIS[_s["id"]]
assert set(EMPHASIS) <= {_s["id"] for _s in sentences}, "EMPHASIS에 없는 문장 번호"

lesson = base_lesson(
    ID, source="2026년 3월 고3 전국연합학력평가 영어 31번 (빈칸 추론, 2점)",
    topic="빈칸 푸는 법: 빈칸 문장부터 → 처음부터 읽으며 같은 말 모으기 → 빈칸이 같은 쪽인지 반대 쪽인지 → 바꿔 쓴 보기",
    method={"type": "blank", "labels": ["빈칸 문장 먼저 보기", "요지 잡기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-art-commerce.svg", ("Art", "예술"), "+", ("Commerce", "상업"),
                                       "돈을 벌지 않는 예술은 취미일까?", "2026년 3월 31번 도입 칠판"),
                      "alt": "칠판: Art(예술) + Commerce(상업)", "kind": "drawing"}},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "돈을 벌지 않아도 예술가라고 할 수 있을까요? 이번 글은 예술과 상업(commerce) 이야기예요."}},
           {"id": "method1", "type": "say", "button": "좋아요",
            "brief": {"say": "빈칸 문제는 빈칸 위치를 살펴보고 가면 좋아요. 빈칸은 글쓴이 의견과 동일할 수도 있고, 반대일 수도 있어요."}}],
    exam=exam,
    key_words={"passage": [g("commerce", "상업"), g("authority", "권위"), g("senior", "졸업반"), g("major", "전공생"),
                           g("ignore", "무시하다"), g("be engaged in", "~에 종사하다"), g("professional", "전문적인, 전문가"),
                           g("by nature", "본질상"), g("quantify", "수량화하다"), g("in an effort to", "~하려는 노력으로"),
                           g("productive", "생산적인"), g("justify", "정당화하다"), g("urge", "충동"), g("notion", "개념"),
                           g("for one’s sake", "~을 위해"), g("hopelessly", "어찌할 도리가 없을 정도로"), g("romantic", "낭만적인"),
                           g("indefensible", "옹호의 여지가 없는"), g("marker", "지표"), g("declaration", "선언"),
                           g("title", "직함"), g("mindlessly", "아무 생각 없이"), g("norm", "규범"), g("label", "명칭을 붙이다"),
                           g("separate A from B", "A를 B에서 분리하다"), g("commercial", "상업적인"),
                           g("legitimize", "정당성을 부여하다"), g("inherently", "본질적으로")],
               "options": [g("universal", "보편적인"), g("individualist", "개인주의적인"), g("collective", "집단적인"),
                           g("capitalist", "자본주의적인")]},
    sentences=sentences)

# 헷갈리는 단어(trap) — 평소 아는 뜻과 이 글의 뜻이 다른 단어. 해설 번역과 대조함:
# senior 졸업반 · nature 본질 · marker 지표 · title 직함 · then 그렇다면.
# 그 문장의 첫 스텝에 붙이면 처음 읽는 화면부터 물결 밑줄로 보인다. 숙어·문법 요령은 헷갈리는 단어가 아니라 Tip이다
TRAPS = {
    2: [tip("senior", "이 글에서는 → 졸업반의  ('노인' 아님)", "senior", trap=True)],
    4: [tip("nature", "이 글에서는 → 본질  ('자연' 아님)", "nature", trap=True)],
    6: [tip("marker", "이 글에서는 → 지표  ('마커 펜' 아님)", "marker", trap=True)],
    7: [tip("title", "이 글에서는 → 직함  ('제목' 아님)", "title", trap=True)],
    9: [tip("then", "이 글에서는 → 그렇다면  ('그때' 아님)", "then", trap=True)],
}
for _s in lesson["sentences"]:
    if _s["id"] in TRAPS:
        _first = _s["steps"][0]
        _first["tips"] = [*_first.get("tips", []), *TRAPS[_s["id"]]]

finish(ID, lesson, senses=SENSES, words=WORDS, stories=STORIES, topic_intro="빈칸 푸는 법")
