"""Shared floating back-to-top control for public static routes."""

STYLESHEET = '<link rel="stylesheet" href="/assets/styles/back-to-top.css?v=1">'
SCRIPT = '<script defer src="/assets/scripts/back-to-top.js?v=1"></script>'
LEGACY_SCRIPT = '<script defer src="/assets/scripts/back-to-top.js"></script>'
MARKER = 'data-back-to-top'

BACK_TO_TOP = '''<a class="back-to-top" href="#top" data-back-to-top aria-label="Наверх">
  <svg class="lucide lucide-arrow-up" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m5 12 7-7 7 7"/><path d="M12 19V5"/></svg>
  <span>Наверх</span>
</a>'''
