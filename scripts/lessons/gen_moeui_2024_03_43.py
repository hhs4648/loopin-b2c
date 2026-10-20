"""2024년 3월 고3 43번 레슨 + 대사를 만든다 (43~45 장문 중 43번 — 글의 순서, 2점). 오답률 자료 없음(Top 15 밖).

    python3 scripts/lessons/gen_moeui_2024_03_43.py   (→ stamp → 44·45번도 다시 돌린다 → npm run build)

이야기 글 순서는 처음 — Claude 초안(2026-10-18, 미니 모의고사 연결용). 틀: docs/tutor/templates/order.md, 단 이야기라
단서가 these/However 같은 말이 아니라 '사건의 순서'다: 카드 발견 → 살펴봄(examined the card) → 할아버지께 보여 줌 → 할아버지가
받아 듦(took the card) → 가르쳐 달라 부탁 → 함께 연습. 주어진 글이 (A)이고 (B)(C)(D)를 잇는다. 정답 ④ (D)-(B)-(C).
44·45번은 이 레슨의 문장·뜻을 가져다 쓴다(이 파일을 고치면 둘 다 다시 돌린다). 해설지 해석과 대조함. twinkle은 *풀이 단어.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, r, choice, show, tip, rows, sense, topic_svg, base_lesson, exam_brief, finish)  # noqa: E402
from order_tools import card, order_link  # noqa: E402

ID = "moeui-2024-03-43-baseball-card"

S = [
    "(A) Once upon a time in the small town of Meadowville, there lived a curious boy named Tommy.",
    "Tommy’s grandfather, affectionately known as Grandpa Joe, had always been a mysterious figure to (a)him.",
    "Grandpa Joe was a man of few words, but his eyes lit up from stories untold.",
    "One lazy summer afternoon, while searching the garage, Tommy found an old, forgotten box.",
    "As (b)he opened it, the treasure of memories spilled out, including an old baseball card featuring a young Grandpa Joe.",
    "(B) A spark of nostalgia lit up Grandpa Joe’s eyes as he took the card.",
    "Memories flooded back, and he told stories of his youthful days on the baseball field.",
    "Grandpa Joe spoke of the thrill of the game and the joy of hitting a home run.",
    "Tommy, fascinated by these stories, felt more connected to his grandfather.",
    "Eager to learn more, (c)he asked Grandpa Joe to teach him about baseball.",
    "(C) They spent afternoons in the backyard as (d)he shared the wisdom of the game with his grandson.",
    "Together, they practiced hitting, catching, and even laughed over the mistakes.",
    "As they bonded over baseball, the gap between generations closed.",
    "Grandpa Joe’s eyes no longer held just the twinkle of untold stories; they now radiated warmth and shared memories.",
    "(D) Tommy’s eyes widened with excitement as he examined the card.",
    "In the card, Grandpa Joe stood proudly in a baseball uniform.",
    "He was not the quiet person Tommy knew.",
    "Intrigued by this discovery, Tommy rushed inside the house to find Grandpa Joe.",
    "“Hey, Grandpa! I found this cool baseball card of you. Were you a baseball player?” (e)he asked, eyes filled with curiosity.",
]
KO = [
    "(A) 옛날 옛적 Meadowville의 작은 마을에 Tommy라는 이름의 호기심 많은 소년이 살고 있었다.",
    "애정 어린 표현으로 Grandpa Joe로 알려진 Tommy의 할아버지는 항상 그에게 신비로운 인물이었다.",
    "Grandpa Joe는 말수가 적은 사람이었지만, 그의 눈은 말하지 않은 이야기들로 빛이 났다.",
    "어느 나른한 여름 오후, 차고를 탐색하던 중, Tommy는 오래되고 잊혀진 상자를 발견했다.",
    "그가 그것을 열었을 때, 젊은 Grandpa Joe가 등장하는 오래된 야구 카드를 포함한 추억의 보물이 쏟아졌다.",
    "(B) 그가 카드를 가져가면서 노스탤지어의 반짝임이 Grandpa Joe의 눈을 밝혔다.",
    "기억들이 다시 밀려 들어왔고, 그는 야구장에서 보낸 그의 젊은 시절 이야기를 했다.",
    "Grandpa Joe는 경기의 전율과 홈런을 치는 기쁨에 관해 이야기했다.",
    "Tommy는 이러한 이야기들에 매료되어 할아버지와 더 연결되어졌다고 느꼈다.",
    "더 배우기를 열망하여, 그는 Grandpa Joe에게 야구를 가르쳐 달라고 부탁했다.",
    "(C) 그들은 뒷마당에서 오후를 보내며, 그는 그의 손자에게 경기의 지혜를 나누어 주었다.",
    "함께, 그들은 공 치기, 잡기를 연습하였고 심지어 실수들을 웃어 넘겼다.",
    "그들이 야구를 통해 유대감을 형성하며, 세대 간의 격차가 줄어들었다.",
    "Grandpa Joe의 눈은 더 이상 말하지 않은 이야기들의 반짝임을 지니지 않았고, 이제는 따뜻함과 함께 나눈 기억으로 반짝였다.",
    "(D) 그가 카드를 살펴보면서 Tommy의 눈이 흥분으로 커졌다.",
    "카드 속에서, Grandpa Joe는 야구 유니폼을 입고 당당하게 서 있었다.",
    "그는 Tommy가 알던 조용한 사람이 아니었다.",
    "이 발견으로 호기심이 불러일으켜져서, Tommy는 Grandpa Joe를 찾아 집 안으로 서둘러 들어갔다.",
    "“할아버지! 제가 할아버지의 이 멋진 야구 카드를 찾았어요. 야구 선수셨어요?” 그는 호기심으로 가득찬 눈으로 물어보았다.",
]
GLOSSES = [
    [g("Once upon a time", "옛날 옛적에"), g("in the small town of Meadowville", "메도우빌이라는 작은 마을에"), g("there lived", "~가 살았다"),
     g("a curious boy", "호기심 많은 소년"), g("named Tommy", "토미라는 이름의")],
    [g("Tommy’s grandfather", "토미의 할아버지"), g("affectionately known as Grandpa Joe", "다정하게 '조 할아버지'라고 불리는"),
     g("had always been", "늘 ~였다"), g("a mysterious figure", "신비로운 인물"), g("to (a)him", "그에게")],
    [g("Grandpa Joe", "조 할아버지"), g("was a man of few words", "말수가 적은 사람이었다"), g("but", "하지만"), g("his eyes", "그의 눈은"),
     g("lit up", "빛났다"), g("from stories untold", "말하지 않은 이야기들로")],
    [g("One lazy summer afternoon", "어느 나른한 여름 오후"), g("while searching the garage", "차고를 뒤지다가"), g("Tommy", "토미"),
     g("found", "발견했다"), g("an old, forgotten box", "오래되고 잊혀진 상자")],
    [g("As (b)he opened it", "그가 그것을 열자"), g("the treasure of memories", "추억의 보물"), g("spilled out", "쏟아져 나왔다"),
     g("including", "~을 포함해"), g("an old baseball card", "오래된 야구 카드"), g("featuring a young Grandpa Joe", "젊은 조 할아버지가 나오는")],
    [g("A spark of nostalgia", "그리움의 불꽃"), g("lit up Grandpa Joe’s eyes", "조 할아버지의 눈을 밝혔다"), g("as he took the card", "그가 카드를 받아 들며")],
    [g("Memories", "기억들"), g("flooded back", "다시 밀려왔다"), g("he told stories", "그는 이야기를 했다"),
     g("of his youthful days", "그의 젊은 시절의"), g("on the baseball field", "야구장에서")],
    [g("Grandpa Joe", "조 할아버지"), g("spoke of", "~에 대해 이야기했다"), g("the thrill of the game", "경기의 짜릿함"),
     g("the joy of hitting a home run", "홈런을 치는 기쁨")],
    [g("Tommy", "토미"), g("fascinated by these stories", "이 이야기들에 매료되어"), g("felt more connected", "더 가까워졌다고 느꼈다"),
     g("to his grandfather", "그의 할아버지와")],
    [g("Eager to learn more", "더 배우고 싶어서"), g("(c)he", "그는"), g("asked Grandpa Joe", "조 할아버지에게 부탁했다"),
     g("to teach him about baseball", "그에게 야구를 가르쳐 달라고")],
    [g("They", "그들은"), g("spent afternoons", "오후를 보냈다"), g("in the backyard", "뒷마당에서"), g("as (d)he shared", "그가 나누어 주며"),
     g("the wisdom of the game", "경기의 지혜"), g("with his grandson", "그의 손자에게")],
    [g("Together", "함께"), g("they practiced", "그들은 연습했다"), g("hitting, catching", "치기, 잡기"),
     g("even laughed over the mistakes", "실수도 웃어넘겼다")],
    [g("As they bonded over baseball", "그들이 야구로 가까워지면서"), g("the gap between generations", "세대 간의 차이"), g("closed", "좁혀졌다")],
    [g("Grandpa Joe’s eyes", "조 할아버지의 눈은"), g("no longer held", "더 이상 담고 있지 않았다"), g("just the twinkle of untold stories", "말하지 않은 이야기의 반짝임만"),
     g("they now radiated", "이제 ~으로 빛났다"), g("warmth and shared memories", "따뜻함과 함께 나눈 기억")],
    [g("Tommy’s eyes", "토미의 눈이"), g("widened", "커졌다"), g("with excitement", "흥분으로"), g("as he examined the card", "그가 카드를 살펴보며")],
    [g("In the card", "카드 속에서"), g("Grandpa Joe", "조 할아버지는"), g("stood proudly", "당당하게 서 있었다"), g("in a baseball uniform", "야구 유니폼을 입고")],
    [g("He", "그는"), g("was not the quiet person", "조용한 사람이 아니었다"), g("Tommy knew", "토미가 알던")],
    [g("Intrigued by this discovery", "이 발견에 호기심이 생겨"), g("Tommy", "토미는"), g("rushed inside the house", "집 안으로 서둘러 들어갔다"),
     g("to find Grandpa Joe", "조 할아버지를 찾으려고")],
    [g("Hey, Grandpa", "할아버지"), g("I found this cool baseball card of you", "할아버지의 멋진 야구 카드를 찾았어요"),
     g("Were you a baseball player", "야구 선수셨어요"), g("(e)he asked", "그가 물었다"), g("eyes filled with curiosity", "호기심 가득한 눈으로")],
]
SENSES = {
    2: [sense("as", "known as Grandpa Joe", "~로", "be known as + 이름"), sense("to", "to (a)him", "~에게", "전치사 to + 사람")],
    3: [sense("but", "but his eyes", "하지만", "접속사 but (대조)")],
    4: [sense("while", "while searching", "~하는 동안, ~하다가", "while + -ing")],
    5: [sense("as", "As (b)he opened it", "~할 때, ~하자", "접속사 as + 주어·동사 (때)")],
    6: [sense("as", "as he took the card", "~하면서", "접속사 as + 주어·동사 (동시)")],
    9: [sense("to", "connected to his grandfather", "~와", "connected to + 사람")],
    10: [sense("to", "Eager to learn", "~하기를 (간절히)", "eager to + 동사원형"),
         sense("to", "to teach him", "~해 달라고", "ask + 사람 + to 동사원형")],
    11: [sense("as", "as (d)he shared", "~하면서", "접속사 as + 주어·동사 (동시)")],
    13: [sense("as", "As they bonded", "~하면서", "접속사 as + 주어·동사 (동시)")],
    15: [sense("as", "as he examined", "~하면서", "접속사 as + 주어·동사 (동시)")],
    18: [sense("to", "to find Grandpa Joe", "~하려고", "to부정사 (목적)")],
}
WORDS = {"once": "옛날, 한때", "upon": "~에", "small": "작은", "town": "마을", "meadowville": "메도우빌(마을 이름)", "lived": "살았다",
         "curious": "호기심 많은", "boy": "소년", "named": "~라는 이름의", "tommy": "토미", "tommy’s": "토미의", "grandfather": "할아버지",
         "affectionately": "다정하게", "known": "알려진", "grandpa": "할아버지", "joe": "조", "joe’s": "조의", "always": "늘",
         "mysterious": "신비로운", "figure": "인물", "him": "그를, 그에게", "man": "사람", "few": "거의 없는", "words": "말",
         "eyes": "눈", "lit": "빛났다(light의 과거)", "stories": "이야기들", "untold": "말하지 않은", "lazy": "나른한", "summer": "여름",
         "afternoon": "오후", "searching": "뒤지는", "garage": "차고", "found": "발견했다", "old": "오래된", "forgotten": "잊혀진",
         "box": "상자", "opened": "열었다", "treasure": "보물", "memories": "기억들, 추억", "spilled": "쏟아졌다", "including": "~을 포함해",
         "baseball": "야구", "card": "카드", "featuring": "~이 나오는", "young": "젊은", "spark": "불꽃, 반짝임", "nostalgia": "그리움, 향수",
         "took": "받아 들었다", "flooded": "밀려왔다", "told": "말했다", "youthful": "젊은", "days": "시절", "field": "경기장",
         "spoke": "이야기했다", "thrill": "짜릿함", "game": "경기", "joy": "기쁨", "hitting": "치는 것", "home": "집, 홈", "run": "달리기, 득점",
         "fascinated": "매료된", "felt": "느꼈다", "connected": "연결된, 가까운", "eager": "간절히 바라는", "learn": "배우다", "asked": "부탁했다, 물었다",
         "teach": "가르치다", "spent": "보냈다", "afternoons": "오후들", "backyard": "뒷마당", "shared": "나누었다, 함께한", "wisdom": "지혜",
         "grandson": "손자", "together": "함께", "practiced": "연습했다", "catching": "잡기", "laughed": "웃었다", "mistakes": "실수들",
         "bonded": "가까워졌다", "gap": "차이, 틈", "generations": "세대", "closed": "좁혀졌다", "longer": "더 이상 (no longer)",
         "held": "담았다", "twinkle": "반짝임", "radiated": "빛났다, 내뿜었다", "warmth": "따뜻함", "widened": "커졌다",
         "excitement": "흥분", "examined": "살펴보았다", "stood": "서 있었다", "proudly": "당당하게", "uniform": "유니폼", "quiet": "조용한",
         "person": "사람", "knew": "알았다", "intrigued": "호기심이 생긴", "discovery": "발견", "rushed": "서둘러 갔다", "inside": "안으로",
         "house": "집", "find": "찾다", "hey": "저기요, 이봐", "cool": "멋진", "player": "선수", "filled": "가득한", "curiosity": "호기심",
         "he": "그는", "a)him": "(a) 그에게", "b)he": "(b) 그는", "d)he": "(d) 그는", "e)he": "(e) 그는", "they": "그들은", "even": "심지어", "now": "이제", "just": "~만", "no": "아니"}


def story(*done):
    r = {"A": ("(A)", "Tommy found … an old baseball card", "토미가 상자에서 할아버지의 옛 야구 카드를 찾음"),
         "D": ("(D)", "examined the card → rushed to find Grandpa Joe", "카드를 살펴봄 → 할아버지께 달려가 물음", "hl"),
         "B": ("(B)", "he took the card → asked to teach him", "할아버지가 카드를 받아 듦 → 가르쳐 달라 부탁", "hl"),
         "C": ("(C)", "They spent afternoons … practiced", "함께 야구 연습, 세대 차가 좁혀짐", "hl")}
    return rows(*[r[d] for d in done])


STEPS = {
    1: [show("g_story", "이야기 글이에요. 이야기는 사건이 일어난 차례대로 이어져요. 누가 무엇을 했는지 따라가 봐요.",
             button="다음 문장",
             tips=[tip("이야기 순서 요령", "단락 첫머리 사건이 바로 앞 단락 끝 사건에 이어지는지 봐요. the card처럼 the가 붙은 말은 앞에서 이미 나온 것이에요.")])],
    2: [choice("g_figure", "Tommy에게 할아버지는 어떤 사람이었나요?",
               [("o0", "늘 신비로운 사람", True), ("o1", "늘 같이 노는 친한 사람", False)],
               "a mysterious figure를 봐요. mysterious는 '신비로운'이에요.", highlight=["a mysterious figure"])],
    5: [show("g_end", "(A)는 Tommy가 상자에서 젊은 할아버지가 나오는 야구 카드를 찾으며 끝나요.",
             highlight=["an old baseball card"], panel=story("A"), button="다음"),
        show("paper_order", "이제 (B)·(C)·(D)를 시험지 순서대로 읽어요. 단락마다 첫 사건과 끝 사건을 봐 두면 좋아요.",
             button="(B)부터 읽어 볼게요")],
    6: [choice("b_before", "할아버지가 카드를 받아 들며(took the card) 눈이 반짝여요. (B) 앞에는 어떤 장면이 있어야 할까요?",
               [("o0", "Tommy가 할아버지를 찾아가 카드를 보여 주는 장면", True),
                ("o1", "두 사람이 뒷마당에서 야구를 연습하는 장면", False)],
               "카드는 Tommy가 찾았어요. 할아버지가 받아 들려면 누가 건네야 할까요.",
               why="카드는 Tommy가 차고에서 찾았어요. 할아버지가 그 카드를 받아 들려면, 앞에서 Tommy가 카드를 들고 할아버지를 찾아가야 해요.",
               highlight=["as he took the card"],
               point="(B) he took the card ← 앞에서 Tommy가 카드를 할아버지께 보여 줘야 한다")],
    10: [choice("b_next", "(B)는 Tommy가 야구를 가르쳐 달라고 부탁하며 끝나요. 다음엔 어떤 장면이 오기 쉬울까요?",
                [("o0", "할아버지가 야구를 가르쳐 주는 장면", True), ("o1", "Tommy가 카드를 처음 살펴보는 장면", False)],
                "부탁을 했으니, 그 부탁이 어떻게 됐는지가 이어지기 쉬워요.",
                why="가르쳐 달라고 부탁했으니 다음엔 할아버지가 가르쳐 주는 장면이 와요. 카드를 처음 살펴보는 건 할아버지께 보여 주기 전 일이에요.",
                highlight=["asked Grandpa Joe to teach him"], panel=story("B"),
                point="(B) 끝: 가르쳐 달라 부탁 → 다음은 가르쳐 주는 장면")],
    11: [show("c_first", "(C)는 함께 오후를 보내며 할아버지가 손자에게 야구의 지혜를 나눠 주는 장면으로 시작해요.",
              highlight=["shared the wisdom of the game"], button="다음 문장")],
    14: [show("c_end", "(C)는 세대 차가 좁혀지고 할아버지 눈이 따뜻하게 빛났다는, 이야기의 마무리예요.",
              highlight=["radiated warmth"], panel=story("B", "C"), button="다음 문장")],
    15: [choice("d_before", "Tommy가 카드를 살펴보며(examined the card) 눈이 커져요. (D) 앞에는 어떤 장면이 있어야 할까요?",
                [("o0", "Tommy가 카드를 막 찾은 장면", True), ("o1", "할아버지가 카드를 받아 든 장면", False)],
                "the card는 앞에서 이미 나온 카드예요. Tommy가 카드를 처음 보고 놀라는 장면이에요.",
                why="the card는 앞에 나온 그 카드예요. Tommy가 카드를 처음 살펴보며 놀라는 장면이니, 바로 앞엔 카드를 찾은 장면이 있어야 해요.",
                highlight=["as he examined the card"],
                point="(D) he examined the card ← 카드를 막 찾은 (A) 끝 바로 뒤")],
    19: [show("d_end", "(D)는 Tommy가 할아버지를 찾아가 '야구 선수셨어요?' 하고 묻는 장면으로 끝나요.",
              highlight=["Were you a baseball player"], panel=story("A", "D"), button="다음"),
         order_link(
             card("given", "(A) 주어진 글", last=("… an old baseball card featuring a young Grandpa Joe", "젊은 할아버지가 나오는 옛 야구 카드")),
             [card("B", "(B)", first=("A spark of nostalgia lit up Grandpa Joe’s eyes as he took the card.", "할아버지가 카드를 받아 들며 눈이 반짝임"),
                   last=("… he asked Grandpa Joe to teach him about baseball.", "야구를 가르쳐 달라고 부탁")),
              card("C", "(C)", first=("They spent afternoons in the backyard …", "뒷마당에서 함께 오후를 보냄"),
                   last=("… they now radiated warmth and shared memories.", "따뜻함과 함께 나눈 기억으로 빛남")),
              card("D", "(D)", first=("Tommy’s eyes widened with excitement as he examined the card.", "카드를 살펴보며 눈이 커짐"),
                   last=("“… Were you a baseball player?” he asked …", "'야구 선수셨어요?' 하고 물음"))],
             ["D", "B", "C"],
             "(A) 카드 발견 → (D) 카드를 살펴보고 할아버지께 물음 → (B) 할아버지가 카드를 받아 들고 옛이야기, 가르쳐 달라 부탁 → (C) 함께 연습 순서예요.",
             wrong_by={"0": "(A) 끝에서 Tommy가 카드를 막 찾았어요. 그 바로 뒤에 이어질 첫 사건을 찾아봐요.",
                       "1": "두 번째 칸의 첫 사건이 바로 위 카드의 끝 사건에 이어지는지 다시 봐요."}),
         show("c_go", "직접 이어 봤어요. 실제 시험 보기에서는 몇 번일지 볼까요?", button="문제 풀러 갈게요")],
}

sentences = [{"id": i + 1, "text": S[i], "model_translation": KO[i], "teaching_value": "high" if i + 1 in STEPS else "low",
              "glosses": GLOSSES[i], "steps": STEPS.get(i + 1, []), **({"label": "주어진 글"} if i == 0 else {})} for i in range(len(S))]

# 끊어읽기 자리와, 켜면 같이 보이는 S·V·O·C(메인 문장 + because·if 같은 절 안의 S·V, 같은 진하기)·[ ] 수식어 — 2026-10-20 선생님 전체 규칙
SLASHES = {
    1: ["Once upon a time", "Meadowville,", "there lived"],
    2: ["Tommy’s grandfather,", "Grandpa Joe,", "a mysterious figure"],
    3: ["few words,", "lit up"],
    4: ["summer afternoon,", "the garage,"],
    5: ["opened it,", "spilled out,", "baseball card"],
    6: ["A spark of nostalgia", "Joe’s eyes"],
    7: ["flooded back,", "told stories", "youthful days"],
    8: ["spoke of", "the thrill of the game"],
    9: ["Tommy,", "these stories,", "more connected"],
    10: ["learn more,", "asked Grandpa Joe"],
    11: ["spent afternoons", "the backyard", "the wisdom of the game"],
    12: ["Together,", "hitting, catching,"],
    13: ["over baseball,", "between generations"],
    14: ["Grandpa Joe’s eyes", "no longer held", "untold stories;", "radiated warmth"],
    15: ["widened with excitement"],
    16: ["In the card,", "stood proudly"],
    17: ["the quiet person"],
    18: ["this discovery,", "inside the house"],
    19: ["Hey, Grandpa!", "baseball card of you.", "a baseball player?”", "he asked,"],
}
ROLES = {
    1: [r("lived", "V"), r("a curious boy", "S")],
    2: [r("Tommy’s grandfather", "S"), r("had always been", "V"), r("a mysterious figure", "C")],
    3: [r("Grandpa Joe", "S"), r("was", "V"), r("a man", "C"), r("his eyes", "S"), r("lit up", "V")],
    4: [r("Tommy", "S"), r("found", "V"), r("an old, forgotten box", "O")],
    5: [r("he", "S"), r("opened", "V"), r("it", "O"), r("the treasure of memories", "S"), r("spilled out", "V")],
    6: [r("A spark of nostalgia", "S"), r("lit up", "V"), r("Grandpa Joe’s eyes", "O"), r("he", "S"), r("took", "V"), r("the card", "O")],
    7: [r("Memories", "S"), r("flooded back", "V"), r("he", "S"), r("told", "V"), r("stories", "O")],
    8: [r("Grandpa Joe", "S"), r("spoke of", "V")],
    9: [r("Tommy", "S"), r("felt", "V"), r("more connected", "C")],
    10: [r("he", "S"), r("asked", "V"), r("Grandpa Joe", "O")],
    11: [r("They", "S"), r("spent", "V"), r("afternoons", "O"), r("he", "S"), r("shared", "V"), r("the wisdom of the game", "O")],
    12: [r("they", "S"), r("practiced", "V"), r("laughed", "V")],
    13: [r("they", "S"), r("bonded", "V"), r("the gap", "S"), r("closed", "V")],
    14: [r("Grandpa Joe’s eyes", "S"), r("no longer held", "V"), r("the twinkle", "O"), r("they", "S"), r("now radiated", "V"),
         r("warmth and shared memories", "O")],
    15: [r("Tommy’s eyes", "S"), r("widened", "V"), r("he", "S"), r("examined", "V"), r("the card", "O")],
    16: [r("Grandpa Joe", "S"), r("stood", "V")],
    17: [r("He", "S"), r("was not", "V"), r("the quiet person", "C")],
    18: [r("Tommy", "S"), r("rushed", "V")],
    19: [r("I", "S"), r("found", "V"), r("this cool baseball card", "O"), r("he", "S"), r("asked", "V")],
}
MODIFIERS = {  # 끊어읽기 때 [ ]로 묶는 수식어 — 관계대명사절·분사 덩어리 (안의 S·V는 안 적는다)
    2: ["affectionately known as Grandpa Joe"],
    5: ["featuring a young Grandpa Joe"],
    9: ["fascinated by these stories"],
    17: ["Tommy knew"],
}
for _s in sentences:
    for _c in SLASHES.get(_s["id"], []):
        assert _s["text"].count(_c) == 1, (_s["id"], _c)  # 한 번만 나오는 말로 — 끊을 자리가 하나로 정해지게
    if SLASHES.get(_s["id"]):
        _s["slashes"] = SLASHES[_s["id"]]
    if ROLES.get(_s["id"]):
        _s["roles"] = ROLES[_s["id"]]
    if MODIFIERS.get(_s["id"]):
        _s["modifiers"] = MODIFIERS[_s["id"]]

OPTIONS = [("1", "(B)-(D)-(C)", False), ("2", "(C)-(B)-(D)", False), ("3", "(C)-(D)-(B)", False), ("4", "(D)-(B)-(C)", True), ("5", "(D)-(C)-(B)", False)]
exam = {
    "question": "주어진 글 (A)에 이어질 내용을 순서에 맞게 배열한 것으로 가장 적절한 것은?",
    "sentence": 1, "analysis_first": True, "glosses": [],
    "options": [{"id": o[0], "label": o[1], "keywords": [], **({"correct": True} if o[2] else {})} for o in OPTIONS],
    "brief": exam_brief(
        "사건 순서(카드 발견 → 살펴봄 → 받아 듦 → 함께 연습)를 떠올리며 골라 봐요.",
        "정답이에요! 카드 발견 → (D) 살펴보고 할아버지께 물음 → (B) 할아버지가 받아 들고 가르쳐 달라는 부탁 → (C) 함께 연습, 순서예요.",
        "정답은 ④ (D)-(B)-(C)예요.",
        {"1": "(B)에서 할아버지가 카드를 받아 들려면, 먼저 Tommy가 카드를 보여 줘야 해요. 그건 (D)예요.",
         "2": "(C)의 함께 연습은 가르쳐 달라는 부탁(B 끝) 뒤에 와요.",
         "3": "(C)는 이야기의 마무리예요. 카드를 보여 주기도 전에 연습할 수 없어요.",
         "5": "(D) 뒤에 바로 (C)가 오면, 가르쳐 달라는 부탁(B) 없이 연습부터 하게 돼요."}),
}

lesson = base_lesson(
    ID, source="2024년 3월 고3 전국연합학력평가 영어 43~45번 중 43번 (글의 순서, 2점)",
    topic="이야기 순서 푸는 법: 단락마다 첫 사건과 끝 사건 → 앞 단락 끝 사건에 이어지는 첫 사건 찾기 → 순서 잇기",
    method={"type": "order", "labels": ["첫 사건 · 끝 사건", "순서 잇기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-baseball-card.svg", ("Old Card", "옛 야구 카드"), "→", ("Grandpa", "할아버지"),
                                       "낡은 카드 한 장이 무엇을 바꿀까?", "2024년 3월 43번 도입 칠판"),
                      "alt": "칠판: Old Card(옛 야구 카드) → Grandpa(할아버지)", "kind": "drawing"}},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "말수 적은 할아버지의 옛 사진을 찾은 적 있나요? 이번 글은 오래된 야구 카드 한 장에서 시작하는 이야기예요."}},
           {"id": "method1", "type": "say", "button": "좋아요",
            "brief": {"say": "이야기 순서 문제는 사건이 일어난 차례를 따라가요. 단락마다 첫 사건과 끝 사건을 보고 이어 볼게요."}}],
    exam=exam,
    key_words={"passage": [g("curious", "호기심 많은"), g("affectionately", "다정하게"), g("mysterious", "신비로운"), g("garage", "차고"),
                           g("nostalgia", "그리움, 향수"), g("youthful", "젊은"), g("fascinated", "매료된"), g("eager", "간절히 바라는"),
                           g("wisdom", "지혜"), g("radiate", "빛나다"), g("examine", "살펴보다"), g("proudly", "당당하게"),
                           g("intrigued", "호기심이 생긴"), g("discovery", "발견")],
               "options": []},
    sentences=sentences, english="medium", concept="medium")

finish(ID, lesson, senses=SENSES, words=WORDS, topic_intro="이야기 순서 푸는 법")
