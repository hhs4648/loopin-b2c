/**
 * 계정 삭제 안내. Google Play 스토어 등록정보에 이 주소(`/delete-account`)를 넣는다.
 * 앱 이름, 삭제 절차, 지워지는 데이터와 보관 기간이 이 화면에 바로 보여야 한다.
 */

type Props = {
  onBack: () => void;
};

export function AccountDeletion({ onBack }: Props) {
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
        <h1 className="saved-title">Loopin 계정 삭제</h1>
        <p>Loopin 계정과 그에 연결된 데이터를 삭제하는 방법입니다.</p>

        <section>
          <h2>앱에서 삭제하기</h2>
          <ol>
            <li>Loopin 앱을 엽니다.</li>
            <li>홈 화면 오른쪽 위의 설정을 누릅니다.</li>
            <li>로그인한 계정에서 회원 탈퇴를 누릅니다.</li>
            <li>탈퇴하기를 누르면 삭제가 완료됩니다.</li>
          </ol>
        </section>

        <section>
          <h2>앱을 열 수 없을 때</h2>
          <p>
            가입한 이메일과 함께 계정 삭제를 요청해 주세요.
            <br />
            <a href="mailto:contact@haksup.com">contact@haksup.com</a>
          </p>
        </section>

        <section>
          <h2>삭제되는 데이터</h2>
          <p>탈퇴가 끝나면 아래 데이터를 서버에 더 보관하지 않고 바로 삭제합니다.</p>
          <ul>
            <li>계정 식별자, 이메일, 이름, 최근 등급, 학습 목표</li>
            <li>학습 기록, 입력한 해석, 단어장, 노트</li>
          </ul>
        </section>

        <section>
          <h2>삭제되지 않는 데이터</h2>
          <ul>
            <li>로그아웃만 한 경우 서버의 계정과 학습 기록은 남습니다. 계정 삭제가 아닙니다.</li>
            <li>로그인하지 않고 만든 기록은 계정에 연결되어 있지 않습니다. 그 기록은 이 기기의 브라우저에 남으며, 사이트 데이터를 지우면 기기에서 삭제됩니다.</li>
          </ul>
        </section>
      </div>
    </div>
  );
}
