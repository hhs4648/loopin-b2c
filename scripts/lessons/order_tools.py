"""순서 유형 공용 — 마지막 「순서 잇기」 스텝 (docs/tutor/templates/order.md)"""


def card(id, label, first=None, last=None):
    """단락 카드 — first·last는 (영어 단서, 한국어 뜻)"""
    c = {"id": id, "label": label}
    if first:
        c["first"] = {"en": first[0], "ko": first[1]}
    if last:
        c["last"] = {"en": last[0], "ko": last[1]}
    return c


def order_link(given, cards, answer, explain, wrong_by=None):
    """학생이 단락 카드를 끌어 주어진 글 아래에 순서대로 놓는다. 틀리면 처음 어긋난 칸을 짚는다(순서를 말하지 않는다)"""
    return {
        "id": "order_link", "type": "pick", "interaction": "word_pick", "tag": "순서 잇기",
        "candidates": [c["id"] for c in cards], "answers": list(answer),
        "order": {"given": given, "cards": cards},
        "brief": {
            "ask": "이제 직접 이어 봐요. 앞 카드의 끝과 다음 카드의 첫머리가 이어지게 카드를 순서대로 놓아 볼까요?",
            "wrong": "앞 카드의 끝과 다음 카드의 첫머리가 이어지는지 다시 봐요.",
            "wrong_by": wrong_by or {
                "0": "주어진 글의 끝을 다시 봐요. 그 바로 뒤에 이어질 첫머리를 찾아봐요.",
                "1": "두 번째 칸의 첫머리가 바로 위 카드의 끝을 받는지 다시 봐요.",
            },
            "more": "좋아요! {n}개 남았어요.",
            "praise": "다 이었어요! 끝과 첫머리가 딱딱 이어지죠.",
            "explain": explain,
            "point": "순서: 앞 단락의 끝 ↔ 다음 단락의 첫머리(This, the, in this manner, Nor …)가 이어지는지",
        },
        "method": 1,
    }
