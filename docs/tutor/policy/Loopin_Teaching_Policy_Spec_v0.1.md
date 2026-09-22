# Loopin Teaching Policy Spec v0.1

## 0. 목적과 적용 전제

이 문서는 기존 Loopin 앱에 **Teaching Policy Engine**을 이식하기 위한
구현 명세다.

기존 앱에 이미 구현된 다음 요소는 최대한 유지한다.

-   선생님 캐릭터 이미지와 애니메이션
-   상냥쌤 등 캐릭터별 말투
-   화면/UI 구성
-   단어 클릭 시 뜻을 보여주는 사전 기능
-   기존 콘텐츠 표시/전환 로직

Teaching Policy는 캐릭터 대사를 직접 담당하기보다 **무엇을, 언제, 어느
깊이로, 어떤 상호작용을 통해 가르칠지**를 결정한다.

``` text
Student State
+ Learning Context
+ Passage / Item Property
+ Current Observation
        ↓
Teaching Policy Engine
        ↓
Teaching Action
        ↓
Existing Presentation Layer
(캐릭터 말투 / 대사 / UI / 애니메이션)
```

예:

``` json
{
  "action": "EXPLAIN_SENTENCE_STRUCTURE",
  "target": "long_subject",
  "intensity": "brief"
}
```

Presentation Layer는 위 행동을 상냥쌤 말투에 맞게 다음처럼 표현할 수
있다.

> 맞아! 그런데 이 문장은 주어가 조금 길지? 구조도 한번 보고 가자 😊

즉 **Teaching Logic과 Character Dialogue를 분리한다.**

------------------------------------------------------------------------

## 1. 시스템 목표와 핵심 원칙

``` yaml
SYSTEM_GOAL:
  primary:
    - maximize_actual_learning
    - preserve_student_agency
    - minimize_unnecessary_intervention
    - allocate_limited_attention_to_high_value_learning

  principles:
    - observation_is_not_intervention
    - observed_behavior_is_not_latent_state
    - correct_answer_is_not_mastery
    - immediate_performance_is_not_delayed_retention
    - hint_assisted_success_is_not_independent_success
    - unknown_word_is_not_automatically_teaching_target
    - student_difficulty_is_not_the_only_reason_to_teach
    - high_value_content_can_receive_brief_teaching_even_after_correct_answer
    - do_not_explain_everything
    - preserve_space_for_student_thinking
    - prefer_minimum_necessary_support
```

최상위 원칙:

> **제한된 시간·집중력·인지용량 안에서 지금 가장 가치 있는 학습 기회를
> 선택하고, 필요한 만큼만 개입한다.**

``` typescript
nextAction =
  minimumIntervention(
    highestValueLearningOpportunity(
      studentState,
      learningContext,
      itemProperty,
      observation
    )
  );
```

------------------------------------------------------------------------

## 2. 역할 분리

``` yaml
PRESENTATION_LAYER:
  owns:
    - teacher_character
    - teacher_tone
    - dialogue_copy
    - animation
    - UI
    - visual_assets
    - vocabulary_popup
    - transitions

TEACHING_POLICY_ENGINE:
  owns:
    - what_to_teach
    - whether_to_intervene
    - intervention_depth
    - interaction_type
    - hint_timing
    - review_schedule
    - student_state_update
    - mistake_tracking
    - next_learning_action
```

기존 앱의 말투와 단어 클릭 기능을 다시 만들지 말고 재사용한다.

------------------------------------------------------------------------

## 3. 기본 의사결정 구조

``` typescript
TeachingDecision = f(
  StudentState,
  LearningContext,
  ItemProperty,
  Observation
);
```

반복 루프:

``` text
Observe
→ Infer cautiously
→ Update State
→ Decide
→ Act
→ Recheck
→ Update
```

중요:

``` text
State Update != Immediate Teaching Action
```

학생이 어떤 약점을 드러냈다는 사실과 **지금 당장 그것을 깊게 가르쳐야
하는가**는 별개의 판단이다.

------------------------------------------------------------------------

## 4. Student State

``` yaml
StudentState:

  knowledge:
    skill_id:
      status: stable | uncertain | weak | unknown
      confidence: 0.0-1.0

  mistake_history:
    skill_id:
      count: integer
      repeated: boolean

  retention:
    skill_id:
      immediate_success: boolean | null
      delayed_success: boolean | null

  performance_history:
    skill_id:
      independent_success_count: integer
      hint_assisted_success_count: integer
      failure_count: integer

  behavior:
    hint_dependency: low | medium | high
    exploratory_style: low | medium | high
    review_compliance: low | medium | high

  reading:
    current_speed: optional
    target_speed: optional
```

### Knowledge State와 Mistake State는 분리한다

예:

``` yaml
knowledge:
  relative_clause:
    status: stable

mistake_history:
  relative_clause:
    count: 2
    repeated: true
```

이 학생은 개념을 모르기보다 **알지만 반복적으로 실수하는 상태**일 수
있다.

``` yaml
IF knowledge_status == stable
AND unexpected_error == true:

  action:
    - GIVE_SELF_CORRECTION_OPPORTUNITY
    - RECORD_MISTAKE
```

반복되면 재설명보다 자기수정·반복연습 중심의 복습 대상으로 전환할 수
있다.

------------------------------------------------------------------------

## 5. Learning Context

``` yaml
LearningContext:

  mode:
    - first_attempt
    - paper_review
    - regular_learning
    - exam_review
    - weakness_review
    - spaced_review

  exam_relevance:
    low | medium | high

  student_level:
    low | mid | high

  time_budget:
    short | normal | deep
```

현재 고3 2025년 3월 21번 샘플은 기본적으로:

``` yaml
mode: paper_review
time_budget: deep
```

학생이 종이로 한 번 문제를 풀어본 뒤 앱에서 **복습/학습**하는 상황을
가정한다. 앱이 긴 시험지 자체를 대체할 필요는 없다.

------------------------------------------------------------------------

## 6. Passage / Item Property

학생의 정오답만으로 개입 깊이를 정하지 않는다.

``` yaml
ItemProperty:

  english_difficulty:
    low | medium | high

  conceptual_difficulty:
    low | medium | high

  background_knowledge_required:
    low | medium | high

  exam_importance:
    low | medium | high

  teaching_value:
    low | medium | high

  intervention_density:
    minimal | normal | deep
```

현재 Q21 예시:

``` yaml
english_difficulty: high
conceptual_difficulty: high
background_knowledge_required: high
exam_importance: high
teaching_value: high
intervention_density: deep
```

### High-value correct-answer rule

``` yaml
IF answer == correct
AND teaching_value == high
AND sentence_establishes_core_passage_structure == true:

  action:
    BRIEF_CORE_ANALYSIS
```

객관식 정답은 찍어서 맞힐 수도 있고, 구조·개념 이해를 보장하지 않는다.

다만 이미 충분히 이해한 학생에게 장황한 설명을 반복하지 않는다.

------------------------------------------------------------------------

## 7. Observation: 앱이 관찰 가능한 신호만 사용

``` yaml
Observation:

  answer:
    correct | incorrect | skipped

  response_latency_ms: integer
  selected_option: optional
  answer_changes: integer

  hint_used: boolean
  hint_count: integer

  vocabulary_clicks:
    - word

  help_clicks:
    - help_id

  revisit_count: integer
  completed: boolean
  dropout: boolean
```

직접 관찰하지 못한 내적 상태를 사실처럼 저장하지 않는다.

``` yaml
DO_NOT_ASSUME:
  - student_is_confused
  - student_is_not_concentrating
  - student_understands
  - student_is_lazy
```

예:

``` text
rapid_submission = observable
possible_attention_lapse = hypothesis

help_click = observable
student_does_not_know = hypothesis
```

------------------------------------------------------------------------

## 8. Observation ≠ Intervention

``` yaml
EVENT:
  student_makes_grammar_error

STATE_UPDATE:
  grammar_skill:
    status: uncertain

DECISION:
  IF grammar_error_blocks_current_goal:
    intervene_now
  ELSE:
    continue_current_learning
    schedule_future_recheck
```

핵심:

> **학생이 모르는 것과 지금 가르쳐야 하는 것은 별개의 판단이다.**

------------------------------------------------------------------------

## 9. Vocabulary Policy

``` yaml
VocabularyItem:

  support_type:
    lookup_only
    | teaching_target
    | concept_support
```

예:

``` yaml
roots:
  support_type: lookup_only

trunk:
  support_type: lookup_only

correspond_to:
  support_type: teaching_target

metaphysics:
  support_type: concept_support

applied_science:
  support_type: concept_support
```

기본 규칙:

``` yaml
IF word_can_be_resolved_by_dictionary
AND word_is_not_structurally_or_conceptually_important:

  action:
    ALLOW_VOCABULARY_CLICK

  do_not:
    FORCE_TEACHER_EXPLANATION
```

즉:

> **학생이 모를 가능성이 높은 단어 ≠ 선생님이 적극적으로 가르쳐야 하는
> 단어**

일반적인 어휘 공백은 기존 클릭 사전으로 해결하고, 지문의 논리·개념·구조
이해에 중요한 표현에 수업 자원을 사용한다.

------------------------------------------------------------------------

## 10. Intervention Escalation

``` yaml
support_escalation:

  1: independent_attempt
  2: light_hint
  3: stronger_hint
  4: explanation
  5: worked_solution
  6: similar_practice
```

학생이 바로 "몰라요"를 눌러도 기본적으로:

``` yaml
IF first_failure_or_immediate_dont_know:
  prefer:
    HINT
  over:
    FULL_EXPLANATION
```

흐름:

``` text
problem
→ attempt
→ stuck
→ hint 1
→ retry
→ hint 2
→ retry
→ explanation
→ worked solution if needed
→ similar practice
```

단:

``` yaml
IF teaching_value == high
AND core_concept_requires_instruction:
  explanation_allowed: true
```

목표는 설명을 피하는 것이 아니라 **학생이 생각할 공간을 없앨 만큼 과잉
개입하지 않는 것**이다.

------------------------------------------------------------------------

## 11. Hint Policy

``` yaml
IF solved_with_hint:
  performance_status: hint_assisted_success
```

이는 다음과 다르다.

``` yaml
performance_status: independent_success
```

평가해야 할 흐름:

``` text
Hint use
→ reattempt
→ later independent performance
```

힌트를 많이 썼다는 이유만으로 즉시 막거나 벌점을 주지 않는다. 탐색형
학생은 상호작용을 통해 학습할 수도 있다.

나중에 독립적으로 수행할 수 있다면 힌트 사용 자체가 문제는 아니다.
반대로 힌트가 답 찾기로만 사용되고 독립 수행이 개선되지 않으면 개입한다.

------------------------------------------------------------------------

## 12. Exploratory Learners

모든 학생이 다음 순서로 배우는 것은 아니다.

``` text
설명 → 이해 → 적용
```

일부 학생은:

``` text
클릭 → 결과 → 다시 시도 → 패턴 파악 → 점진적 이해
```

로 배울 수 있다.

``` yaml
RULE:
  allow_learning_through_interaction: true
```

모든 학생에게 긴 주관식/자유응답을 강제하지 않는다. 필요한 곳에 짧은
산출을 사용한다.

다만:

``` text
exploratory_or_random_success != mastery
```

나중의 독립 수행으로 학습을 확인한다.

------------------------------------------------------------------------

## 13. Progressive Disclosure

정보량이 많은 문장은 모든 정보를 처음부터 동시에 처리시키지 않는다.

``` yaml
IF sentence_information_load == high:

  sequence:
    1: temporarily_hide_supplementary_information
    2: expose_core_structure
    3: teach_or_check_core_meaning
    4: restore_supplementary_information
    5: integrate_full_sentence
```

괄호, 삽입구, 부가설명 등이 대상이 될 수 있다.

이는 단순한 문장 분할이 아니라 **정보의 교수 순서를 설계하는 전략**이다.
모바일 화면에 특히 적합하다.

------------------------------------------------------------------------

## 14. Interaction Type Selection

모든 문장을 같은 문제 유형으로 만들지 않는다.

``` yaml
InteractionTypes:

  - meaning_choice
  - translation_choice
  - chunk_arrangement
  - structure_highlight
  - visual_mapping
  - prediction
  - contrast_reasoning
  - clickable_question
  - vocabulary_lookup
  - hint_then_retry
  - read_and_continue
```

``` typescript
interactionType = chooseInteraction({
  sentenceProperty,
  predictedMisconception,
  teachingGoal,
  studentState
});
```

문장 배열을 모든 문장에 반복하지 않는다.

------------------------------------------------------------------------

## 15. Previous Representation Retrieval

이전 문장에서 만든 유용한 표상을 다음 문장의 해석 도구로 재사용한다.

``` yaml
RULE_REUSE_PREVIOUS_REPRESENTATION:

  IF previous_sentence_created_useful_representation
  AND current_sentence_depends_on_it:

    action:
      RETRIEVE_PREVIOUS_REPRESENTATION_BEFORE_NEW_EXPLANATION
```

예:

``` text
Sentence 2
roots → metaphysics
trunk → physics
branches & fruit → applied science

        ↓ retrieval

Sentence 3
"fruits"가 여기서 무엇을 의미할까?
```

이렇게 하면 복습과 지문 연결관계 이해가 동시에 일어난다.

------------------------------------------------------------------------

## 16. Repeated Error / Review Policy

``` yaml
IF same_error_repeats:

  actions:
    - INFORM_STUDENT_THAT_ERROR_IS_REPEATING
    - DO_NOT_NECESSARILY_INTERRUPT_CURRENT_LESSON
    - ADD_TARGETED_REVIEW
```

현재 경험 기반 baseline:

``` yaml
review_schedule:
  questions_per_session: 5
  frequency: weekly
  duration_weeks: 3

delayed_check:
  after: 1_month
  cumulative_question: 1
```

이 수치는 검증된 최적값이 아니라 현재 경험 기반 출발점이다.

복습 미수행:

``` yaml
IF assigned_review_not_completed:
  action:
    REMIND

IF repeatedly_not_completed:
  action:
    INSERT_REVIEW_INTO_REGULAR_LEARNING_FLOW
```

Knowledge State와 Behavior State를 분리한다.

------------------------------------------------------------------------

## 17. Immediate Performance ≠ Retention

``` yaml
IF immediate_success == true:
  do_not_assume:
    mastery
```

기본 해석:

``` yaml
repeated_success:
  state: stable

mixed_success_and_failure:
  state: uncertain

repeated_failure:
  state: weak
```

즉시 수행과 지연 인출을 별도로 기록한다.

------------------------------------------------------------------------

# 18. Reference Implementation: 2025년 3월 고3 영어 Q21 첫 3문장

이 샘플은 긴 지문 전체를 모바일 화면에 한꺼번에 보여주지 않는다.

각 문장을 짧은 학습 단위로 변환하고, 문장마다 다른 interaction을
사용한다.

------------------------------------------------------------------------

## 18-1. Sentence 1

> The unity of science and philosophy in the old classical sense was
> perhaps best described by the famous tree of Descartes:

``` yaml
Sentence1:

  teaching_value: high

  goals:
    - understand_science_philosophy_unity
    - identify_long_subject
    - understand_classical_in_context
    - prepare_tree_metaphor

  predicted_difficulties:
    - unity
    - classical_in_context
    - long_subject
    - Descartes_background
```

### Step 1: Meaning choice = 진단

``` yaml
first_interaction:
  type: meaning_choice
  purpose: diagnostic
```

3지선다는 찍어서 맞힐 수 있으므로 정답을 맞혔다고 바로 다음 문장으로
넘어가지 않는다.

``` yaml
IF answer == correct:
  do_not_immediately_skip_sentence: true
```

### Step 2: 정답 후 짧은 문장 분석

``` yaml
after_correct_answer:
  action: BRIEF_SENTENCE_ANALYSIS

  reasons:
    - high_teaching_value
    - multiple_choice_can_be_guessed
    - sentence_establishes_passage_framework
```

화면 예:

``` text
[The unity of science and philosophy]
[in the old classical sense]
[was perhaps best described]
[by the famous tree of Descartes]
```

``` yaml
subject:
  "The unity of science and philosophy in the old classical sense"

predicate:
  "was perhaps best described"

by_phrase:
  "by the famous tree of Descartes"
```

문법 강의를 길게 하는 것이 아니라 긴 주어와 문장 뼈대를 보이게 한다.

### unity

기존 사전은:

``` text
unity → 통합 / 통일성
```

을 보여줄 수 있다.

하지만 이 지문에서는 맥락 의미도 짧게 제공할 가치가 있다.

``` yaml
unity:
  contextual_meaning:
    "과학과 철학이 지금처럼 완전히 분리된 분야로 여겨지지 않았던 관점"
```

### classical

``` yaml
classical:
  contextual_meaning:
    "여기서는 옛날의 전통적인 관점"
```

### Descartes

``` yaml
optional_help:
  - id: who_is_descartes
    label: "Descartes가 누구인가요?"
    depth: minimal
```

지문 이해에 필요한 정도만 제공한다.

### Sentence 1 → Sentence 2 bridge

``` yaml
NEXT_SENTENCE_BRIDGE:
  question:
    "그런데 과학과 철학이 하나라는 걸 왜 '나무'로 설명했을까?"
```

Sentence 2가 이 질문의 답이 되게 한다.

------------------------------------------------------------------------

## 18-2. Sentence 2

> The roots of this tree corresponded to metaphysics (the intelligible
> principles), the trunk to physics (statements of intermediate
> generality), and the branches and fruit to what we would call applied
> science.

정보량이 많으므로 Progressive Disclosure를 사용한다.

### Step 1: 괄호를 잠시 제거

먼저:

``` text
The roots of this tree corresponded to metaphysics,
the trunk to physics,
and the branches and fruit to what we would call applied science.
```

``` yaml
goal:
  establish_core_parallel_mapping_before_supplementary_information
```

### Step 2: 어휘 지원 분리

``` yaml
lookup_only:
  - roots
  - trunk

teaching_targets:
  - correspond_to

concept_support:
  - metaphysics
  - applied_science
```

`roots`, `trunk`는 기존 클릭 사전으로 충분하다.

### Step 3: what 지원

중위권 이하에게 필요하면:

``` yaml
what_clause:
  target:
    "what we would call applied science"

  support:
    "what = '~하는 것'"

  depth:
    brief
```

이 문장의 핵심 목표가 what 문법 자체는 아니므로 길게 확장하지 않는다.

### Step 4: 병렬 대응 구조

``` yaml
mapping:
  roots: metaphysics
  trunk: physics
  branches_and_fruit: applied_science
```

생략된 반복:

``` yaml
parallel_structure:

  explicit:
    "roots corresponded to metaphysics"

  ellipsis_1:
    "trunk [corresponded] to physics"

  ellipsis_2:
    "branches and fruit [corresponded] to applied science"
```

### Step 5: Visual Mapping

``` yaml
interaction:
  type: visual_mapping
```

예:

``` text
ROOTS              → metaphysics
TRUNK              → physics
BRANCHES & FRUIT   → applied science
```

전체 문장을 다시 번역시키지 않고 핵심 의미를 확인한다.

### Step 6: 괄호 복원

핵심 구조를 이해한 뒤:

``` yaml
action:
  RESTORE_SUPPLEMENTARY_INFORMATION
```

다시 보여준다.

``` text
metaphysics (the intelligible principles)
physics (statements of intermediate generality)
```

전체 흐름:

``` text
괄호 제거
→ 핵심 구조
→ 대응관계 확인
→ 괄호 복원
→ 전체 문장 통합
```

------------------------------------------------------------------------

## 18-3. Sentence 3

> He regarded the whole system of science and philosophy as we today
> regard science alone; he felt that the metaphysical principles were
> ultimately justified by their "fruits," not merely by their
> self-evidence.

### Step 1: 형이상학 선택형 도움

``` yaml
optional_help:

  metaphysics:
    label: "형이상학이란?"
    behavior: click_to_open
    explanation_depth: minimal
```

``` yaml
background_explanation_depth:
  minimum_needed_for_passage_comprehension
```

철학 강의를 길게 하지 않는다.

### Step 2: `as` 예상 오류

학생은 `regard A as B`를 떠올려 이 as를 잘못 분석할 수 있다.

실제 구조:

``` yaml
correct_structure:

  main:
    "He regarded the whole system of science and philosophy"

  comparison:
    "as we today regard science alone"

  as_meaning:
    "~하듯이 / ~와 같은 방식으로"
```

자연스러운 의미:

``` text
오늘날 우리가 과학만을 하나의 체계로 바라보듯,
그는 과학과 철학의 전체 체계를 바라보았다.
```

필요하면 이 예상 오류를 짧게 짚는다.

### Step 3: `"fruits"` 따옴표에 주목

``` yaml
UI_ACTION:
  highlight:
    '"fruits"'

teacher_prompt:
  "왜 fruits에 따옴표가 있을까?"
```

따옴표는 일반적인 과일이 아니라 특별한/비유적 의미라는 단서를 준다.

정답은 바로 말하지 않는다.

### Step 4: Sentence 2 표상 회상

``` yaml
previous_representation:

  roots: metaphysics
  trunk: physics
  branches_and_fruit: applied_science
```

그 다음 추론시킨다.

``` yaml
interaction:
  type: meaning_choice

question:
  "여기서 'fruits'가 의미하는 것은?"

options:
  A:
    "과학 이론의 뿌리가 되는 철학적 원리"

  B:
    "과학과 철학을 통해 실제로 얻어지는 응용·결과"

  C:
    "과학자가 관찰한 자연 그 자체"

correct:
  B
```

### Step 5: fruits vs self-evidence

바로 설명하지 않는다.

``` yaml
interaction:
  type: contrast_reasoning

prompt:
  "글에서는 'fruits'와 'self-evidence'를 대비하고 있어.
   둘은 어떻게 다른 걸까? 한번 생각해보자."
```

필요하면 힌트:

``` yaml
hint:
  "하나는 밖으로 나타나는 결과와 관련 있고,
   다른 하나는 원리 자체가 얼마나 당연하고
   설득력 있어 보이는지와 관련 있어."
```

그 뒤 정리:

``` yaml
concepts:

  fruits:
    meaning:
      "실제로 나오는 결과·응용"

  self_evidence:
    meaning:
      "다른 결과로 증명하지 않아도 원리 자체가 자명하고 그럴듯해 보이는 것"
```

핵심 대비:

``` text
결과를 통해 정당화되는 것
vs
원리 자체가 자명해 보이는 것
```

------------------------------------------------------------------------

## 19. 세 문장의 Interaction Pattern

``` yaml
Sentence1:
  interaction:
    - meaning_choice
    - brief_sentence_analysis
    - optional_clickable_help
    - curiosity_bridge

Sentence2:
  interaction:
    - progressive_disclosure
    - vocabulary_lookup
    - visual_mapping
    - parallel_structure
    - restore_supplementary_information

Sentence3:
  interaction:
    - optional_concept_help
    - predicted_grammar_error_support
    - metaphor_inference
    - retrieve_previous_representation
    - contrast_reasoning
    - conditional_hint
```

같은 지문에서도 문장 특성에 따라 interaction type을 바꾼다.

------------------------------------------------------------------------

## 20. Response-Dependent Branching

``` yaml
IF answer == incorrect:

  update:
    knowledge_status: uncertain

  action:
    choose_minimum_necessary_support

ELSE_IF answer == correct
AND item.teaching_value == high
AND core_structure_has_not_been_checked:

  action:
    BRIEF_CORE_ANALYSIS

ELSE:
  action:
    CONTINUE
```

도움 클릭은 기록하되 과도하게 해석하지 않는다.

``` yaml
IF help_clicked:
  log:
    help_id
    timestamp
    sentence_id
```

`help_clicked`를 곧바로 `student_does_not_know`로 변환하지 않는다.

------------------------------------------------------------------------

## 21. Teaching Action Output Schema

``` typescript
type TeachingAction = {
  action:
    | "CONTINUE"
    | "ALLOW_LOOKUP"
    | "ASK_MEANING_CHOICE"
    | "ASK_TRANSLATION_CHOICE"
    | "SHOW_STRUCTURE"
    | "SHOW_VISUAL_MAPPING"
    | "ASK_PREDICTION"
    | "ASK_CONTRAST"
    | "GIVE_LIGHT_HINT"
    | "GIVE_STRONG_HINT"
    | "EXPLAIN"
    | "SHOW_WORKED_SOLUTION"
    | "ASSIGN_SIMILAR_PRACTICE"
    | "SCHEDULE_REVIEW"
    | "RETRIEVE_PREVIOUS_REPRESENTATION";

  target?: string;

  intensity?: "minimal" | "brief" | "normal" | "deep";

  interactionId?: string;

  reason?: string[];

  stateUpdates?: Record<string, unknown>;

  nextReviewAt?: string;
};
```

예:

``` json
{
  "action": "SHOW_STRUCTURE",
  "target": "sentence_1_long_subject",
  "intensity": "brief",
  "reason": [
    "high_teaching_value",
    "multiple_choice_can_be_guessed",
    "sentence_establishes_passage_framework"
  ]
}
```

------------------------------------------------------------------------

## 22. Example Decision Function

``` typescript
function decideNextTeachingAction({
  studentState,
  learningContext,
  itemProperty,
  observation
}) {
  updateStudentStateFromObservation(
    studentState,
    observation
  );

  if (needsDictionaryOnly({
    itemProperty,
    observation
  })) {
    return {
      action: "ALLOW_LOOKUP"
    };
  }

  if (
    itemProperty.teaching_value === "high" &&
    coreTeachingStillNeeded({
      studentState,
      itemProperty,
      observation
    })
  ) {
    return chooseHighValueInteraction({
      studentState,
      learningContext,
      itemProperty,
      observation
    });
  }

  if (observation.answer === "incorrect") {
    return chooseMinimumNecessarySupport({
      studentState,
      learningContext,
      itemProperty,
      observation
    });
  }

  if (observation.hint_used) {
    markHintAssistedSuccess(studentState);
    scheduleIndependentRecheck({
      studentState,
      itemProperty
    });
  }

  if (observation.answer === "correct") {
    if (
      itemProperty.teaching_value === "high" &&
      coreStructureNotYetChecked({
        studentState,
        itemProperty
      })
    ) {
      return {
        action: "SHOW_STRUCTURE",
        intensity: "brief"
      };
    }

    return {
      action: "CONTINUE"
    };
  }

  return {
    action: "CONTINUE"
  };
}
```

------------------------------------------------------------------------

## 23. Policy Priority

규칙이 충돌할 경우 대략 다음 순서를 우선한다.

``` yaml
PRIORITY:

  1:
    preserve_core_learning_goal

  2:
    correct_major_misunderstanding_that_blocks_current_learning

  3:
    teach_high_value_structure_or_concept

  4:
    preserve_student_attempt_and_agency

  5:
    use_minimum_necessary_intervention

  6:
    defer_low_value_side_issues

  7:
    schedule_future_review_when_immediate_intervention_is_not_worth_the_cost
```

예를 들어 `trunk`를 모르는 학생에게 클릭 사전만으로 문제가 해결된다면
선생님 대사로 길게 가르치지 않는다. 그 시간은
`roots → metaphysics / trunk → physics / fruit → applied science`라는
핵심 구조에 쓴다.

------------------------------------------------------------------------

## 24. Product Philosophy

Loopin의 목표는 AI가 설명을 최대한 많이 생성하는 것이 아니다.

좋은 튜터는 제한된 학습 자원을 배분한다.

``` text
limited time
+ limited attention
+ limited cognitive capacity
        ↓
choose what matters most now
        ↓
intervene only enough
        ↓
let the student think / try / retrieve
        ↓
observe outcome
        ↓
update future teaching
```

시스템은 다음 중 무엇이 필요한지 결정할 수 있어야 한다.

``` text
teach now
hint now
let the student try
give only a word meaning
save it for later
schedule review
or do nothing
```

좋은 AI Tutor는 **잘 설명하는 능력뿐 아니라, 설명하지 않아야 할 때
설명하지 않는 능력**도 필요하다.

------------------------------------------------------------------------

## 25. ML-compatible Long-term Structure

초기에는 명시적 규칙으로 시작한다.

``` text
Human teaching experience
→ explicit policy
→ deterministic/rule-based implementation
→ interaction data
→ outcome data
→ identify where rules fail
→ learn/optimize selected policy decisions
```

추천 이벤트 구조:

``` yaml
LearningEvent:

  student_state_before: ...
  context: ...
  item_property: ...
  observation: ...
  action_taken: ...
  immediate_outcome: ...
  delayed_outcome: ...
  student_state_after: ...
```

핵심 데이터 구조:

``` text
State + Context + Item
→ Action
→ Outcome
```

장기적으로 중요한 질문은:

``` text
"AI가 좋은 설명을 생성했는가?"
```

보다:

``` text
"이 학생의 이 상태와 맥락에서,
어떤 teaching action이 실제 학습·retention·transfer·continued engagement를 더 좋게 만들었는가?"
```

이다.

------------------------------------------------------------------------

## 26. 다른 AI / 개발자에게 주는 구현 지침

1.  기존 캐릭터/UI/단어 클릭 사전 시스템을 기술적으로 필요한 경우가
    아니면 교체하지 않는다.
2.  현재 앱에서 다음 화면·대사·interaction을 결정하는 지점을 찾는다.
3.  그 지점에 `TeachingPolicyEngine` 또는 동등한 decision layer를
    삽입한다.
4.  교육적 판단을 캐릭터 대사에 직접 하드코딩하기보다 structured
    action으로 표현한다.
5.  기존 character/presentation layer가 structured action을 캐릭터별
    말투로 변환하게 한다.
6.  이 문서의 정책은 우선 deterministic rule / if-else / state
    machine으로 구현한다.
7.  학생의 관찰 가능한 행동, 선택된 Teaching Action, immediate/delayed
    outcome을 로그로 남긴다.
8.  첫 reference implementation으로 Q21 첫 세 문장의 흐름을 구현한다.
9.  새로운 teaching case를 발견할 때마다 기존 UI 전체를 다시
    설계하기보다 `state`, `rule`, `action`, `interaction type`을
    확장한다.
10. 추후 데이터가 충분히 쌓이면 규칙 전체를 ML로 대체하기보다, 규칙이
    불확실하거나 성능 차이가 나는 decision point부터 학습 대상으로
    검토한다.

------------------------------------------------------------------------

# 최종 구현 원칙

> **현재 학생과 학습 맥락에서 가장 가치 있는 학습 기회를 선택하고,
> 학생이 앞으로 나아가는 데 필요한 최소한의 개입을 적용한다.**

``` typescript
nextAction =
  minimumIntervention(
    highestValueLearningOpportunity(
      studentState,
      learningContext,
      itemProperty,
      observation
    )
  );
```
