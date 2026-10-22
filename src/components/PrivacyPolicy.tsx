/**
 * 개인정보 처리방침.
 *
 * 심사·로그인 동의 화면에서 주소로 열릴 수 있게 `/privacy` 에서도 이 화면이 뜬다.
 * 적힌 항목은 앱이 실제로 저장하는 것만 (`auth.ts`, `records.ts`, `cloud.ts`).
 */

type Props = {
  onBack: () => void;
};

export function PrivacyPolicy({ onBack }: Props) {
  return (
    <div className="stage-fill saved privacy">
      <header className="saved-top">
        <button type="button" className="icon-btn light" title="뒤로" onClick={onBack}>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
            <path d="M15 6l-6 6 6 6" />
          </svg>
        </button>
      </header>
      <div className="saved-body-scroll">
        <h1 className="saved-title">개인정보 처리방침</h1>
        <p className="privacy-date">시행일: 2026년 10월 22일</p>
        <p>
          Loopin(이하 “서비스”)은 이용자의 개인정보를 관련 법령에 따라 다음과 같이 처리합니다.
        </p>

        <section>
          <h2>1. 수집하는 개인정보 항목</h2>
          <ul>
            <li>소셜 로그인(카카오, Google, Apple) 시 계정 식별자와 이메일. 카카오 계정은 이메일이 제공되지 않을 수 있습니다.</li>
            <li>이용자가 직접 입력하는 이름, 최근 등급, 학습 목표.</li>
            <li>서비스 이용 중 생성되는 학습 기록. 학습한 문제, 정답과 오답, 입력한 해석, 단어장, 노트.</li>
            <li>로그인하지 않은 경우 학습 기록이 익명 식별자와 함께 서버에 저장될 수 있습니다. 이 경우 이메일과 이름은 수집하지 않습니다.</li>
            <li>서비스 이용 경로와 화면 진행. 어느 링크에서 들어왔는지, 로그인 방법, 학습자 구분, 등급, 어디까지 보고 나갔는지. 이 기록에는 이름, 이메일, 입력한 해석을 넣지 않습니다.</li>
          </ul>
        </section>

        <section>
          <h2>2. 개인정보의 이용 목적</h2>
          <ul>
            <li>수업 제공과 학습 진행 상태의 저장.</li>
            <li>로그인한 계정에서 다른 기기의 학습 기록 조회.</li>
            <li>문제 난이도 집계. 집계 자료에는 이름과 이메일을 포함하지 않습니다.</li>
            <li>이용자가 어디에서 들어오고 어느 화면에서 멈추는지 살펴 서비스를 개선.</li>
          </ul>
          <p>수집한 개인정보는 광고에 이용하지 않으며 판매하지 않습니다.</p>
        </section>

        <section>
          <h2>3. 개인정보의 보유 및 이용 기간</h2>
          <ul>
            <li>회원 탈퇴 시 계정, 학습 기록, 노트, 단어장, 이용 경로를 지체 없이 파기합니다. 탈퇴는 설정의 회원 탈퇴에서 할 수 있습니다.</li>
            <li>로그아웃은 해당 기기에 저장된 기록만 삭제합니다. 서버에 저장된 기록은 다시 로그인하면 확인할 수 있습니다.</li>
            <li>로그인하지 않은 이용자의 기기 내 기록은 해당 브라우저에 저장됩니다. 사이트 데이터를 삭제하면 기기에서 삭제됩니다.</li>
          </ul>
        </section>

        <section>
          <h2>4. 개인정보 처리의 위탁</h2>
          <p>서비스 제공을 위해 다음과 같이 개인정보 처리를 위탁합니다.</p>
          <ul>
            <li>Supabase: 계정 및 학습 기록의 보관.</li>
            <li>Vercel: 웹사이트 호스팅.</li>
            <li>카카오, Google, Apple: 로그인 인증 및 계정 정보 확인.</li>
            <li>Google Fonts: 화면 글꼴 제공. 글꼴을 불러오는 과정에서 이용자 기기가 해당 서버에 접속할 수 있습니다.</li>
          </ul>
        </section>

        <section>
          <h2>5. 만 14세 미만 아동의 개인정보</h2>
          <p>
            서비스는 만 14세 이상만 이용할 수 있습니다. 만 14세 미만 아동의 개인정보가 수집된 사실을 확인하면 해당 정보를 지체 없이 파기합니다.
          </p>
        </section>

        <section>
          <h2>6. 이용자의 권리와 문의</h2>
          <p>
            이용자는 자신의 개인정보에 대한 열람, 정정, 삭제, 처리정지를 요청할 수 있습니다. 요청은 아래로 보내 주시기 바랍니다.
            <br />
            <a href="mailto:contact@haksup.com">contact@haksup.com</a>
          </p>
        </section>
      </div>
    </div>
  );
}
