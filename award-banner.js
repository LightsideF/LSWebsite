(function () {
  var SHOW = true;
  var SHOW_BADGE = true;
  var AWARD_TEXT = 'Best Personal & Business Solutions Firm 2026 \u2014 England & Wales';
  var AWARD_BODY = 'UK Enterprise Awards';

  if (!SHOW) return;

  var css = `
#ls-award-banner {
  background: #f7f8f9;
  border-top: 3px solid #e8a020;
  border-bottom: 3px solid #e8a020;
  padding: 10px 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}
#ls-award-banner .ls-award-svg {
  flex-shrink: 0;
  width: 44px;
  height: 44px;
}
#ls-award-banner .ls-award-text {
  font-family: 'Lato', sans-serif;
  font-size: 0.875rem;
  color: #1e3a5f;
  line-height: 1.3;
}
#ls-award-banner .ls-award-text strong {
  font-weight: 700;
  display: block;
}
#ls-award-banner .ls-award-text span {
  color: #6b7a8d;
  font-size: 0.78rem;
}
@media (max-width: 680px) {
  #ls-award-banner {
    padding: 7px 16px;
    gap: 10px;
  }
  #ls-award-banner .ls-award-svg {
    width: 32px;
    height: 32px;
  }
  #ls-award-banner .ls-award-text {
    font-size: 0.78rem;
  }
  #ls-award-banner .ls-award-text span {
    font-size: 0.72rem;
  }
}
`;

  var svgBadge = SHOW_BADGE ? `<svg class="ls-award-svg" viewBox="0 0 56 56" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <circle cx="28" cy="28" r="26" fill="#1e3a5f"/>
  <circle cx="28" cy="28" r="22" fill="none" stroke="#e8a020" stroke-width="1.5"/>
  <path d="M28 10 L30.5 20 L41 20 L32.5 26 L35 36 L28 30 L21 36 L23.5 26 L15 20 L25.5 20 Z" fill="#e8a020"/>
  <text x="28" y="45" text-anchor="middle" font-family="'Lato',sans-serif" font-size="6" font-weight="700" fill="#e8a020" letter-spacing="0.5">AWARD</text>
</svg>` : '';

  var html = `<div id="ls-award-banner" role="complementary" aria-label="Award recognition">
  ${svgBadge}
  <div class="ls-award-text">
    <strong>${AWARD_TEXT}</strong>
    <span>${AWARD_BODY}</span>
  </div>
</div>`;

  var style = document.createElement('style');
  style.textContent = css;
  document.head.appendChild(style);

  var header = document.querySelector('header.site-header');
  if (header && header.parentNode) {
    var div = document.createElement('div');
    div.innerHTML = html;
    header.parentNode.insertBefore(div.firstElementChild, header.nextSibling);
  }
})();
