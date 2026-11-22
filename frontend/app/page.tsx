import type { Metadata, Viewport } from "next";

import { HomeAccountLink } from "@/components/home/HomeAccountLink";
import { KitScripts } from "@/components/home/KitScripts";

/*
  Trang chủ dựng theo taste-skill (bộ kit nguyên văn ở public/assets, CSS riêng ở public/home.css).
  kind: software · deal: hero collage · palette teal-on-paper · type reddit · radius round · ground sage
  nav nav-split (nav-cards chia lại vì không có ảnh) · footer-dark · close-type · rhythm dark-band · buttons pill
  mark stack · effect silk-folds trong khung [data-visual] duy nhất (#so-sanh) · moment pinned-chapters (#cach-dat)
  Liên kết sang trang app dùng <a> (tải lại cả trang): trang app không nạp kit, trang chủ không nạp Tailwind.
*/

export const metadata: Metadata = {
  title: "MediFlow: đặt gói khám định kỳ ở Hà Nội, TP.HCM, Đà Nẵng",
  description: "So sánh 15 gói khám sức khỏe định kỳ của 3 bệnh viện, xem giờ còn trống trong 14 ngày tới và đặt lịch trên trang.",
  openGraph: {
    type: "website",
    title: "MediFlow: đặt gói khám định kỳ ở Hà Nội, TP.HCM, Đà Nẵng",
    description: "Lọc gói theo tuổi, giới và giá, so sánh tối đa 3 gói, đặt lịch khám trong vài bước.",
    images: ["/share.jpg"],
  },
  twitter: { card: "summary_large_image" },
  other: { "site-kind": "software", "page-type": "software" },
};

export const viewport: Viewport = { themeColor: "#f7f9f8" };

const KIT = [
  "system.css",
  "ui/cards.css",
  "motion/motion.css",
  "backgrounds/backgrounds.css",
  "layout/layout.css",
  "layout/demo.css",
  "icons/icon.css",
  "ui/base.css",
  "ui/window/fragment.css",
  "ui/calendar/fragment.css",
  "ui/checklist/fragment.css",
];

// :root đúng như start.mjs in ra (palette teal-on-paper, type reddit)
const TOKENS = `:root {
  --p-bg: #f7f9f8; --p-surface: #ebf0ee; --p-ink: #06525c; --p-muted: #2f737d;
  --p-accent: #06525c; --p-accent-ink: #f7f9f8; --p-action: #06525c; --p-action-ink: #f7f9f8;
  --p-inv-bg: #06525c; --p-inv-surface: #205d66; --p-inv-ink: #f7f9f8; --p-inv-muted: #c1d0d2;
  --p-inv-accent: #f7f9f8; --p-inv-accent-ink: #06525c; --p-inv-action: #f7f9f8; --p-inv-action-ink: #06525c;
  --font-display: "Reddit Sans", system-ui, sans-serif;
  --font-text: "Reddit Sans", system-ui, sans-serif;
  --font-mono: "JetBrains Mono", ui-monospace, "SFMono-Regular", Menlo, Consolas, monospace;
  --display-weight: 500;
  --display-tracking: -0.03em;
  --display-tracking-xl: -0.04em;
}`;

const css = (o: Record<string, string | number>) => o as React.CSSProperties;

const Arrow = () => (
  <svg className="m-arrow" viewBox="0 0 12 12" aria-hidden="true">
    <path className="m-arrow__stem" d="M1 6h8" />
    <path className="m-arrow__head" d="M4.5 2.5 8 6l-3.5 3.5" />
  </svg>
);

const Check = () => (
  <span className="ui-check__box">
    <svg viewBox="0 0 16 16">
      <path d="m4.5 8.2 2.3 2.3 4.7-5" />
    </svg>
  </span>
);

const PRICES = [
  { tag: "tong-quat", name: "Tổng quát", note: "7 gói ở 3 bệnh viện, có gói riêng nam, nữ", from: "từ 990.000đ" },
  { tag: "tim-mach", name: "Tim mạch", note: "2 gói từ 40 tuổi, có siêu âm tim, điện tim", from: "từ 4.600.000đ" },
  { tag: "ung-thu", name: "Tầm soát ung thư", note: "2 gói ung thư vú, cổ tử cung cho nữ từ 25", from: "từ 3.800.000đ" },
  { tag: "cao-tuoi", name: "Người cao tuổi", note: "2 gói từ 60 tuổi, có đo mật độ xương", from: "từ 4.100.000đ" },
  { tag: "tien-hon-nhan", name: "Tiền hôn nhân", note: "1 gói cho người 18 đến 45 tuổi", from: "2.500.000đ" },
  { tag: "doanh-nghiep", name: "Doanh nghiệp", note: "1 gói cho nhân viên 18 đến 60 tuổi", from: "900.000đ" },
];

const HOSPITALS = [
  { code: "ALP", name: "Bệnh viện Alpha (mô phỏng)", city: "Hà Nội", focus: "Tổng quát, tim mạch, người cao tuổi" },
  { code: "BET", name: "Bệnh viện Beta (mô phỏng)", city: "TP. Hồ Chí Minh", focus: "Tầm soát cho nữ, tiền hôn nhân" },
  { code: "GAM", name: "Bệnh viện Gamma (mô phỏng)", city: "Đà Nẵng", focus: "Người cao tuổi, doanh nghiệp" },
];

export default function Home() {
  return (
    <>
      <link rel="preconnect" href="https://fonts.googleapis.com" />
      <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="" />
      <link
        rel="stylesheet"
        precedence="kit"
        href="https://fonts.googleapis.com/css2?family=Reddit+Sans:wght@400..700&family=JetBrains+Mono:wght@400..500&display=swap"
      />
      {KIT.map((f) => (
        <link key={f} rel="stylesheet" precedence="kit" href={`/assets/${f}`} />
      ))}
      <style href="mf-tokens" precedence="kit">
        {TOKENS}
      </style>
      <link rel="stylesheet" precedence="kit" href="/home.css" />

      <header className="nav nav--split">
        <div className="wrap nav__bar">
          <a className="skip-link" href="#top">
            Bỏ qua tới nội dung
          </a>
          <a className="nav__logo" href="#top">
            <span className="mark" data-mark="stack" aria-hidden="true" />
            MediFlow
          </a>
          <nav className="nav__links" aria-label="Chính">
            <div className="nav__item">
              <a className="nav__link" href="/packages">
                Gói khám
              </a>
            </div>
            <div className="nav__item">
              <a className="nav__link" href="/hospitals">
                Bệnh viện
              </a>
            </div>
            <div className="nav__item">
              <a className="nav__link" href="#cach-dat">
                Cách đặt
              </a>
            </div>
            <div className="nav__item">
              <a className="nav__link" href="#faq">
                Hỏi đáp
              </a>
            </div>
          </nav>
          <div className="nav__actions">
            <HomeAccountLink />
            <a className="btn btn--primary" href="/packages">
              Đặt lịch khám
            </a>
          </div>
          <button className="nav__toggle" type="button" aria-expanded="false" aria-label="Mở menu">
            <svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true">
              <path d="M2 5h14M2 13h14" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" />
            </svg>
          </button>
        </div>
      </header>

      <main id="top">
        <section className="hero hero--collage" data-enter aria-labelledby="hero-h">
          <div className="wrap">
            <div className="hero-text grid hero__grid">
              <div className="hero__text span-5">
                <h1 id="hero-h">Đặt gói khám định kỳ ở Hà Nội, TP.HCM, Đà Nẵng</h1>
                <p className="hero__lead">
                  Lọc 15 gói khám của 3 bệnh viện theo tuổi, giới và giá, xem giờ còn trống trong 14 ngày tới rồi đặt lịch ngay trên trang.
                </p>
                <div className="btn-row">
                  <a className="btn btn--primary" href="/packages">
                    Đặt lịch khám
                    <Arrow />
                  </a>
                  <a className="btn btn--secondary" href="/hospitals">
                    Xem bệnh viện
                  </a>
                </div>
                <p className="hero__proof">Khám từ 07:00 đến 10:00, Thứ Hai đến Thứ Bảy.</p>
              </div>
              <div
                className="hero__art span-6 start-7"
                role="img"
                aria-label="Danh sách gói khám của MediFlow lọc theo thành phố, và lịch khám vừa đặt kèm việc cần chuẩn bị"
              >
                <div className="ly-piece ly-piece--main d-win" aria-hidden="true">
                  <div className="d-win__bar">
                    <span className="d-win__dots">
                      <i />
                      <i />
                      <i />
                    </span>
                    <span>MediFlow · Gói khám</span>
                  </div>
                  <div className="d-win__body">
                    <div className="d-side">
                      <span className="is-on">
                        <i />
                        Gói khám
                      </span>
                      <span>
                        <i />
                        Bệnh viện
                      </span>
                      <span>
                        <i />
                        So sánh
                      </span>
                      <span>
                        <i />
                        Lịch của tôi
                      </span>
                      <span className="d-side__label">Thành phố</span>
                      <span>
                        <i />
                        Hà Nội
                      </span>
                      <span>
                        <i />
                        TP.HCM
                      </span>
                      <span>
                        <i />
                        Đà Nẵng
                      </span>
                    </div>
                    <div className="d-main">
                      <div className="d-main__head">
                        <h4>Gói khám</h4>
                        <span className="d-btn">So sánh (2)</span>
                      </div>
                      <div className="d-tabs">
                        <span className="is-on">Tất cả 15</span>
                        <span>Tổng quát 7</span>
                        <span>Tim mạch 2</span>
                      </div>
                      <div className="d-rows">
                        <div className="d-row">
                          <span className="d-thumb" style={{ background: "#dce3d6" }} />
                          <div>
                            <b>Tổng quát cơ bản</b>
                            <small>Gamma · Đà Nẵng</small>
                          </div>
                          <span className="num">990.000đ</span>
                          <span className="d-chip">Từ 18 tuổi</span>
                        </div>
                        <div className="d-row">
                          <span className="d-thumb" style={{ background: "#d6e0e9" }} />
                          <div>
                            <b>Tổng quát cơ bản</b>
                            <small>Alpha · Hà Nội</small>
                          </div>
                          <span className="num">1.200.000đ</span>
                          <span className="d-chip">Từ 18 tuổi</span>
                        </div>
                        <div className="d-row">
                          <span className="d-thumb" style={{ background: "#d6e0e9" }} />
                          <div>
                            <b>Nâng cao nam</b>
                            <small>Alpha · Hà Nội</small>
                          </div>
                          <span className="num">3.500.000đ</span>
                          <span className="d-chip d-chip--low">Đang chọn</span>
                        </div>
                        <div className="d-row">
                          <span className="d-thumb" style={{ background: "#e9e0d2" }} />
                          <div>
                            <b>Tiền hôn nhân</b>
                            <small>Beta · TP.HCM</small>
                          </div>
                          <span className="num">2.500.000đ</span>
                          <span className="d-chip">18–45 tuổi</span>
                        </div>
                        <div className="d-row">
                          <span className="d-thumb" style={{ background: "#dce3d6" }} />
                          <div>
                            <b>Tim mạch</b>
                            <small>Gamma · Đà Nẵng</small>
                          </div>
                          <span className="num">4.600.000đ</span>
                          <span className="d-chip">Từ 40 tuổi</span>
                        </div>
                        <div className="d-row">
                          <span className="d-thumb" style={{ background: "#e9e0d2" }} />
                          <div>
                            <b>Ung thư vú</b>
                            <small>Beta · TP.HCM</small>
                          </div>
                          <span className="num">4.200.000đ</span>
                          <span className="d-chip">Nữ, từ 25</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div className="ly-piece ly-piece--note d-card" aria-hidden="true" data-ly-steps="700">
                  <div className="d-card__row">
                    <h5>Lịch khám ALP-TQNAM</h5>
                    <span className="d-chip" data-step data-step-at="4">
                      Đã đặt
                    </span>
                  </div>
                  <div className="d-note__line" data-step>
                    <i>✓</i>
                    <span>
                      <b>Tổng quát nâng cao nam</b>, Bệnh viện Alpha
                    </span>
                  </div>
                  <div className="d-note__line" data-step>
                    <i>✓</i>
                    <span>
                      <b>07:00 Thứ Hai</b>, còn 4 chỗ
                    </span>
                  </div>
                  <div className="d-note__line" data-step>
                    <i className="warn">!</i>
                    <span>
                      <b>Nhịn ăn 8 tiếng</b> trước giờ khám
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className="section" id="pricing" aria-labelledby="gia-h">
          <div className="wrap">
            <div className="section-head">
              <h2 id="gia-h">Giá gói khám theo nhu cầu</h2>
              <p>Giá ghi trên từng gói, lịch hẹn giữ đúng giá lúc bạn xác nhận.</p>
            </div>
            <div className="grid">
              <ul className="rows span-5">
                {PRICES.map((p) => (
                  <li key={p.tag}>
                    <a className="rows__name" href={`/packages?tag=${p.tag}`}>
                      {p.name}
                      <span className="muted">{p.note}</span>
                    </a>
                    <span className="rows__value">{p.from}</span>
                  </li>
                ))}
                <li>
                  <a className="rows__name" href="/packages">
                    Tất cả gói khám
                    <span className="muted">15 gói, lọc theo tuổi, giới và giá</span>
                  </a>
                  <span className="rows__value">từ 900.000đ</span>
                </li>
              </ul>
              <div className="frame frame--split span-6 start-7" role="img" aria-label="Trang chi tiết gói Tầm soát tim mạch của Bệnh viện Gamma: giá, hạng mục và nút đặt lịch">
                <div className="stage stage--fade-b">
                  <div className="at-corner to-edge" style={css({ "--ax": "56px", "--ay": "56px" })}>
                    <div className="ui ui-panel mf-win" aria-hidden="true">
                      <div className="mf-pkg">
                        <b>Tầm soát tim mạch</b>
                        <span className="num">4.600.000đ</span>
                        <small>Bệnh viện Gamma (mô phỏng) · Đà Nẵng · từ 40 tuổi</small>
                      </div>
                      <div className="mf-win__title">Hạng mục (5)</div>
                      {["Khám nội tổng quát", "Bộ mỡ máu (cholesterol, triglycerid, HDL, LDL)", "Điện tim (ECG)", "Siêu âm tim", "Chụp X-quang ngực thẳng"].map((i) => (
                        <div key={i} className="mf-item">{i}</div>
                      ))}
                      <div className="mf-win__title">Chuẩn bị trước khám</div>
                      <div className="mf-item">Nhịn ăn ít nhất 8 tiếng trước giờ khám (được uống nước lọc)</div>
                      <span className="ui-btn ui-btn--accent">Đặt lịch</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className="section" id="ung-dung" aria-labelledby="app-h">
          <div className="wrap">
            <div className="grid">
              <h2 id="app-h" className="span-5">
                Danh sách gói và giờ còn trống
              </h2>
              <p className="span-6 start-7">
                Chọn gói ở cột trái, lịch bên phải hiện ngày còn chỗ trong 14 ngày tới, mỗi ngày bốn khung giờ từ 07:00 đến 10:00.{" "}
                <a className="link" href="/packages">
                  Xem 15 gói khám
                </a>
              </p>
            </div>
            <div className="ui app fill" role="img" aria-label="Danh sách gói khám bên cạnh lịch còn chỗ của gói Tổng quát nâng cao nam" data-ui-pause-host>
              <div className="app__pane app__pane--list">
                <div className="ui ui-panel ui-win" data-ui="window" data-open="Còn chỗ" data-work="Đang xem" data-done="Đã đặt">
                  <div className="ui-win__bar">
                    <span className="ui-dots" aria-hidden="true">
                      <i />
                      <i />
                      <i />
                    </span>
                    <span className="ui-win__crumb">
                      MediFlow <i>/</i> <b>Gói khám</b>
                    </span>
                    <span className="ui-spacer" />
                    <span className="ui-win__search" aria-hidden="true">
                      <svg className="ui-icon" viewBox="0 0 16 16">
                        <circle cx="7" cy="7" r="4.5" />
                        <path d="m10.5 10.5 3 3" />
                      </svg>
                      <span className="ui-win__ph">Tìm gói</span>
                    </span>
                  </div>
                  <div className="ui-win__body">
                    <nav className="ui-win__side" aria-hidden="true">
                      <span className="ui-win__nav is-on">
                        Gói khám<em>15</em>
                      </span>
                      <span className="ui-win__nav">
                        Bệnh viện<em>3</em>
                      </span>
                      <span className="ui-win__nav">So sánh</span>
                      <span className="ui-win__label">Loại gói</span>
                      <span className="ui-win__nav">
                        <span className="ui-win__hash">#</span>Tổng quát
                      </span>
                      <span className="ui-win__nav">
                        <span className="ui-win__hash">#</span>Tim mạch
                      </span>
                    </nav>
                    <div className="ui-win__main">
                      <div className="ui-win__cols" aria-hidden="true">
                        <span>Bệnh viện</span>
                        <span>Gói</span>
                        <span>Đối tượng</span>
                        <span>Giá</span>
                      </div>
                      <ul className="ui-win__rows">
                        {[
                          ["G", 1, "Bệnh viện Gamma", "Khám doanh nghiệp", "18–60", "900k"],
                          ["G", 1, "Bệnh viện Gamma", "Tổng quát cơ bản", "Từ 18", "990k"],
                          ["A", 3, "Bệnh viện Alpha", "Tổng quát cơ bản", "Từ 18", "1,2 tr"],
                          ["B", 4, "Bệnh viện Beta", "Tổng quát cơ bản", "Từ 18", "1,45 tr"],
                          ["B", 4, "Bệnh viện Beta", "Tiền hôn nhân", "18–45", "2,5 tr"],
                          ["A", 3, "Bệnh viện Alpha", "Tổng quát nâng cao nam", "Nam, 30+", "3,5 tr"],
                          ["G", 1, "Bệnh viện Gamma", "Tầm soát ung thư vú", "Nữ, 25+", "3,8 tr"],
                          ["A", 3, "Bệnh viện Alpha", "Tổng quát nâng cao nữ", "Nữ, 30+", "3,9 tr"],
                          ["B", 4, "Bệnh viện Beta", "Tổng quát nâng cao nam", "Nam, 30+", "3,9 tr"],
                          ["G", 1, "Bệnh viện Gamma", "Người cao tuổi", "Từ 60", "4,1 tr"],
                        ].map(([av, tone, who, sub, st, price], i) => (
                          <li key={i} className={`ui-win__row${i === 5 ? " is-sel" : ""}`} data-row>
                            <span className="ui-avatar" data-tone={tone}>
                              {av}
                            </span>
                            <span className="ui-win__who">{who}</span>
                            <span className="ui-win__sub">{sub}</span>
                            <span className="ui-win__st" data-st>
                              {st}
                            </span>
                            <span className="ui-win__age">{price}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
              <div className="app__pane app__pane--open" data-ui-loop>
                <div className="ui ui-panel ui-calendar" data-ui="calendar" data-start="7" data-end="19" data-month="Th12">
                  <div className="ui-cal__head">
                    <div className="ui-cal__month">
                      Tháng 12 <span>2026</span>
                    </div>
                    <span className="ui-spacer" />
                    <span className="ui-chip ui-chip--plain ui-chip--ink" data-cal-range>
                      Th12 7 – 19
                    </span>
                  </div>
                  <div className="ui-cal__dow" aria-hidden="true">
                    {["T2", "T3", "T4", "T5", "T6", "T7", "CN"].map((d) => (
                      <span key={d}>{d}</span>
                    ))}
                  </div>
                  <div className="ui-cal__days">
                    {[30, ...Array.from({ length: 31 }, (_, i) => i + 1), 1, 2, 3].map((d, i) => {
                      const out = i === 0 || i > 31;
                      const cls = out ? "is-out" : d === 7 ? "is-start" : d === 19 ? "is-end" : d > 7 && d < 19 ? "is-in" : d === 9 ? "" : "";
                      return (
                        <span key={i} className={`ui-cal__d ${cls}${!out && d === 9 ? " is-mark" : ""}`.trim()} data-d={out ? undefined : d}>
                          <b>{d}</b>
                        </span>
                      );
                    })}
                  </div>
                  <div className="ui-cal__events">
                    {[
                      ["7", "07:00 · còn 4 chỗ", "Thứ Hai, Tổng quát nâng cao nam"],
                      ["9", "09:00 · còn 2 chỗ", "Thứ Tư, Bệnh viện Alpha"],
                      ["12", "10:00 · còn 5 chỗ", "Thứ Bảy, Bệnh viện Alpha"],
                      ["19", "08:00 · còn 5 chỗ", "Thứ Bảy, Bệnh viện Alpha"],
                    ].map(([d, title, sub]) => (
                      <div key={d} className="ui-cal__ev" data-ev={d}>
                        <span className="ui-cal__date">
                          <b>{d}</b>
                          <i>Th12</i>
                        </span>
                        <span className="ui-cal__evtext">
                          <span className="ui-cal__evtitle">{title}</span>
                          <span className="ui-cal__evsub">{sub}</span>
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className="section ground-inverse" id="cach-dat" style={css({ "--h": 2 })} data-moment="pinned-chapters" aria-labelledby="steps-h">
          <div className="wrap mo-pc__grid">
            <div className="mo-pc__text">
              <h2 id="steps-h">Đặt lịch khám trong 3 bước</h2>
              <ol className="mo-pc__steps">
                <li className="mo-pc__step">
                  <h3>Chọn gói theo tuổi và giới</h3>
                  <p>Lọc theo thành phố, loại gói, tuổi, giới và mức giá, rồi so sánh tối đa 3 gói trên một bảng.</p>
                  <figure className="mo-pc__visual">
                    <div className="ui ui-panel mf-win" role="img" aria-label="Bộ lọc Hà Nội, Tổng quát, Nam, 35 tuổi và hai gói khớp">
                      <div className="mf-win__title">Gói khám</div>
                      <div className="mf-chips">
                        <span className="ui-chip ui-chip--ink">Hà Nội</span>
                        <span className="ui-chip ui-chip--ink">Tổng quát</span>
                        <span className="ui-chip ui-chip--ink">Nam</span>
                        <span className="ui-chip ui-chip--ink">35 tuổi</span>
                      </div>
                      <div className="mf-pkg">
                        <b>Khám tổng quát cơ bản</b>
                        <span className="num">1.200.000đ</span>
                        <small>Bệnh viện Alpha · 6 hạng mục</small>
                      </div>
                      <div className="mf-pkg">
                        <b>Tổng quát nâng cao nam</b>
                        <span className="num">3.500.000đ</span>
                        <small>Bệnh viện Alpha · 12 hạng mục</small>
                      </div>
                      <span className="ui-btn ui-btn--accent">So sánh (2)</span>
                    </div>
                  </figure>
                </li>
                <li className="mo-pc__step">
                  <h3>Chọn giờ khám còn trống</h3>
                  <p>Ngày Thứ Hai đến Thứ Bảy trong 14 ngày tới, mỗi khung giờ ghi số chỗ còn lại.</p>
                  <figure className="mo-pc__visual">
                    <div className="ui ui-panel mf-win" role="img" aria-label="Bốn khung giờ ngày Thứ Hai, khung 07:00 đang được chọn">
                      <div className="mf-win__title">Thứ Hai, 07/12/2026</div>
                      <div className="mf-slots">
                        <span className="mf-slot is-on">
                          <b>07:00</b>
                          <span className="mf-muted">còn 4 chỗ</span>
                        </span>
                        <span className="mf-slot">
                          <b>08:00</b>
                          <span className="mf-muted">còn 5 chỗ</span>
                        </span>
                        <span className="mf-slot">
                          <b>09:00</b>
                          <span className="mf-muted">còn 2 chỗ</span>
                        </span>
                        <span className="mf-slot">
                          <b>10:00</b>
                          <span className="mf-muted">còn 5 chỗ</span>
                        </span>
                      </div>
                      <span className="ui-btn ui-btn--accent">Xác nhận đặt lịch</span>
                    </div>
                  </figure>
                </li>
                <li className="mo-pc__step">
                  <h3>Xác nhận lịch và chuẩn bị</h3>
                  <p>Lịch hẹn vào mục Lịch của tôi, kèm việc cần làm trước giờ khám và nút hủy.</p>
                  <figure className="mo-pc__visual">
                    <div className="ui ui-panel ui-checks" data-ui="checklist" role="img" aria-label="Danh sách chuẩn bị trước giờ khám, đã xong một trong ba việc">
                      <div className="ui-checks__head">
                        <div className="ui-title">Chuẩn bị trước khám</div>
                        <span className="ui-spacer" />
                        <div className="ui-meta" data-checks-count>
                          1/3 việc
                        </div>
                      </div>
                      <div className="ui-checks__bar">
                        <i data-checks-bar style={css({ "--k": 0.33 })} />
                      </div>
                      <ul className="ui-checks__list">
                        <li className="ui-check is-done">
                          <Check />
                          <span className="ui-check__label">Không đeo trang sức, đồ kim loại</span>
                        </li>
                        <li className="ui-check">
                          <Check />
                          <span className="ui-check__label">Nhịn ăn ít nhất 8 tiếng trước giờ khám</span>
                        </li>
                        <li className="ui-check">
                          <Check />
                          <span className="ui-check__label">Lấy nước tiểu giữa dòng buổi sáng</span>
                        </li>
                      </ul>
                    </div>
                  </figure>
                </li>
              </ol>
            </div>
            <div className="mo-pc__visuals frame" />
          </div>
        </section>

        <section className="section" id="benh-vien" style={css({ "--hm": 2 })} aria-labelledby="bv-h">
          <div className="wrap">
            <div className="section-head">
              <h2 id="bv-h">Bệnh viện ở Hà Nội, TP.HCM và Đà Nẵng</h2>
              <p>Ba bệnh viện đa khoa mô phỏng, mỗi nơi 5 gói. Tên, địa chỉ và số điện thoại đều hư cấu.</p>
            </div>
            <div className="grid">
              {HOSPITALS.map((h) => (
                <a key={h.code} className="card card--row card--open span-4" href={`/hospitals/${h.code}`}>
                  <h3>{h.name}</h3>
                  <p>
                    {h.city} · {h.focus}
                  </p>
                  <div className="panel">
                    <div className="stage stage--fade-b">
                      <div className="at-rise fit" style={css({ "--fit-max": "340px", "--ax": "max(24px, 50% - 170px)", "--ay": "40px", "--ay-sm": "16px" })}>
                        <div className="ui ui-panel mf-win" role="img" aria-label={`Các gói khám của ${h.name}`}>
                          <div className="mf-win__title">{h.city}</div>
                          {(h.code === "ALP"
                            ? [["Khám tổng quát cơ bản", "1.200.000đ"], ["Tổng quát nâng cao nữ", "3.900.000đ"], ["Tầm soát tim mạch", "5.200.000đ"]]
                            : h.code === "BET"
                              ? [["Khám tổng quát cơ bản", "1.450.000đ"], ["Khám tiền hôn nhân", "2.500.000đ"], ["Tầm soát ung thư vú", "4.200.000đ"]]
                              : [["Khám doanh nghiệp", "900.000đ"], ["Khám tổng quát cơ bản", "990.000đ"], ["Người cao tuổi", "4.100.000đ"]]
                          ).map(([n, p]) => (
                            <div key={n} className="mf-pkg">
                              <b>{n}</b>
                              <span className="num">{p}</span>
                              <small>07:00 đến 10:00</small>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>
                </a>
              ))}
            </div>
          </div>
        </section>

        <section className="section" id="so-sanh" aria-labelledby="ss-h">
          <div className="wrap">
            <div className="grid">
              <h2 id="ss-h" className="span-5">
                So sánh tối đa 3 gói trên một bảng
              </h2>
              <p className="span-6 start-7">
                Mỗi hàng là một hạng mục, mỗi cột là một gói. Ba gói tổng quát cơ bản giá từ 990.000đ đến 1.450.000đ khác nhau ở khám mắt và
                nước tiểu.{" "}
                <a className="link" href="/compare?codes=GAM-CB01,ALP-CB01,BET-CB01">
                  So sánh ba gói này
                </a>
              </p>
            </div>
            <div
              className="frame fill"
              data-visual
              data-fx="silk-folds"
              data-fx-seed="11"
              data-fx-palette='{"bg":"#cdd6c6","surface":"#dce3d6","ink":"#262d24","accent":"#6c8e63"}'
              data-fx-params='{"speed":0,"tone":1,"scale":1.3,"folds":0.55,"sheen":0.5,"angle":-28,"calm":0.2,"calmX":0.5,"calmY":0.9}'
              style={css({ "--calm-k": "0%", marginTop: "var(--s-7)" })}
            >
              <div className="stage stage--fade-b">
                <div className="at-corner fit" style={css({ "--fit-max": "760px", "--ax": "max(24px, 50% - 380px)", "--ay": "40px", "--ay-sm": "16px" })}>
                  <div className="ui ui-panel" role="img" aria-label="Bảng so sánh ba gói khám tổng quát cơ bản của Gamma, Alpha và Beta">
                    <table className="mf-table">
                      <thead>
                        <tr>
                          <th>Hạng mục</th>
                          <th>
                            <b>Gamma</b>990.000đ
                          </th>
                          <th>
                            <b>Alpha</b>1.200.000đ
                          </th>
                          <th>
                            <b>Beta</b>1.450.000đ
                          </th>
                        </tr>
                      </thead>
                      <tbody>
                        {[
                          ["Khám mắt", "—", "—", "✓"],
                          ["Tổng phân tích nước tiểu", "—", "✓", "✓"],
                          ["Khám nội tổng quát", "✓", "✓", "✓"],
                          ["Tổng phân tích tế bào máu", "✓", "✓", "✓"],
                          ["Đường huyết lúc đói", "✓", "✓", "✓"],
                          ["Chụp X-quang ngực thẳng", "✓", "✓", "✓"],
                          ["Siêu âm ổ bụng tổng quát", "✓", "✓", "✓"],
                        ].map(([item, ...cells]) => (
                          <tr key={item}>
                            <th>{item}</th>
                            {cells.map((c, i) => (
                              <td key={i}>{c}</td>
                            ))}
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className="section" id="faq" style={css({ "--hm": 2 })} aria-labelledby="faq-h">
          <div className="wrap">
            <div className="grid">
              <div className="section-head span-5">
                <h2 id="faq-h">Câu hỏi về đặt lịch khám</h2>
                <p>
                  Thông tin chỉ mang tính tham khảo, vui lòng tham vấn bác sĩ để cá nhân hóa tầm soát.{" "}
                  <a className="link" href="/packages">
                    Xem các gói khám
                  </a>
                </p>
                <div className="frame frame--split" role="img" aria-label="Một lịch hẹn trong Lịch của tôi với nút Xem chuẩn bị và Hủy" style={css({ marginTop: "var(--s-6)" })}>
                  <div className="stage">
                    <div className="at-rise fit" style={css({ "--fit-max": "380px", "--ax": "max(24px, 50% - 190px)", "--ay": "48px", "--ay-sm": "24px" })}>
                      <div className="ui ui-panel mf-win" aria-hidden="true">
                        <div className="mf-win__title">Lịch của tôi</div>
                        <div className="mf-pkg">
                          <b>Tổng quát nâng cao nam</b>
                          <span className="num">3.500.000đ</span>
                          <small>Bệnh viện Alpha · 07:00 Thứ Hai, 07/12/2026</small>
                        </div>
                        <div className="mf-chips">
                          <span className="ui-chip ui-chip--ink">Đã đặt</span>
                        </div>
                        <div className="mf-chips">
                          <span className="ui-btn">Xem chuẩn bị</span>
                          <span className="ui-btn ui-btn--ghost">Hủy</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div className="faq span-6 start-7">
                {[
                  ["Bệnh viện trên MediFlow có thật không?", "Không. Alpha, Beta và Gamma là bệnh viện mô phỏng của một đồ án học tập; tên, địa chỉ và số điện thoại đều hư cấu."],
                  ["Có cần tài khoản để đặt lịch không?", "Có. Xem và so sánh gói không cần đăng nhập, bước xác nhận đặt lịch thì cần tài khoản khách hàng."],
                  ["Giá gói có đổi sau khi đặt không?", "Không. Lịch hẹn giữ đúng giá của gói tại lúc bạn bấm Xác nhận đặt lịch."],
                  ["Hủy lịch như thế nào?", "Mở Lịch của tôi, bấm Hủy ở lịch hẹn rồi xác nhận. Chỉ hủy được khi chưa tới giờ khám."],
                  ["Cần chuẩn bị gì trước khi khám?", "Mỗi gói có danh sách riêng, ví dụ nhịn ăn ít nhất 8 tiếng nếu gói có xét nghiệm đường huyết lúc đói."],
                ].map(([q, a]) => (
                  <div key={q} className="faq__item">
                    <h3>{q}</h3>
                    <p>{a}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>
      </main>

      <footer className="footer closing footer--dark ground-inverse g2m" id="contact" aria-labelledby="close-h">
        <div className="wrap">
          <div className="closing__cta close--type">
            <div className="section-head">
              <h2 id="close-h">Chọn gói khám cho lần khám tới</h2>
              <p>Khám từ 07:00 đến 10:00, Thứ Hai đến Thứ Bảy.</p>
            </div>
            <a className="btn btn--primary btn--xl btn--wide" href="/packages">
              Đặt lịch khám
              <Arrow />
            </a>
          </div>
          <div className="closing__links">
            <div className="grid">
              <div className="span-4 stack-4">
                <a className="nav__logo" href="#top">
                  <span className="mark" data-mark="stack" aria-hidden="true" />
                  MediFlow
                </a>
                <p className="footer__lede">Đặt lịch gói khám sức khỏe định kỳ ở ba bệnh viện mô phỏng.</p>
              </div>
              <div className="span-2 footer__col">
                <h3>Gói khám</h3>
                <ul>
                  {PRICES.slice(0, 4).map((p) => (
                    <li key={p.tag}>
                      <a href={`/packages?tag=${p.tag}`}>{p.name}</a>
                    </li>
                  ))}
                </ul>
              </div>
              <div className="span-2 footer__col">
                <h3>Bệnh viện</h3>
                <ul>
                  {HOSPITALS.map((h) => (
                    <li key={h.code}>
                      <a href={`/hospitals/${h.code}`}>{h.city}</a>
                    </li>
                  ))}
                </ul>
              </div>
              <div className="span-2 footer__col">
                <h3>Tài khoản</h3>
                <ul>
                  <li>
                    <a href="/login">Đăng nhập</a>
                  </li>
                  <li>
                    <a href="/register">Đăng ký</a>
                  </li>
                  <li>
                    <a href="/bookings">Lịch của tôi</a>
                  </li>
                </ul>
              </div>
              <div className="span-2 footer__col">
                <h3>Trang</h3>
                <ul>
                  <li>
                    <a href="#cach-dat">Cách đặt</a>
                  </li>
                  <li>
                    <a href="#faq">Hỏi đáp</a>
                  </li>
                  <li>
                    <a href="/compare?codes=GAM-CB01,ALP-CB01,BET-CB01">So sánh</a>
                  </li>
                </ul>
              </div>
            </div>
            <div className="footer__legal">
              <span>&copy; 2026 MediFlow, đồ án học tập</span>
              <div className="socials" />
            </div>
          </div>
        </div>
      </footer>

      <KitScripts />
    </>
  );
}
