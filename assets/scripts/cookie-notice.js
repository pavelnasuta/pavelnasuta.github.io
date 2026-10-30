(() => {
  const notice = document.querySelector('[data-cookie-notice]');
  const dismiss = notice?.querySelector('[data-cookie-notice-dismiss]');
  const storageKey = 'nasuta-cookie-notice-dismissed-until';
  const sixMonths = 180 * 24 * 60 * 60 * 1000;

  if (!notice || !dismiss) return;

  try {
    if (Number(localStorage.getItem(storageKey)) > Date.now()) {
      notice.hidden = true;
    }
  } catch (_) {
    // Privacy settings can block storage; keep the informational notice visible.
  }

  dismiss.addEventListener('click', () => {
    notice.hidden = true;
    try {
      localStorage.setItem(storageKey, String(Date.now() + sixMonths));
    } catch (_) {
      // The click should still dismiss the notice in the current page view.
    }
  });
})();
