document.querySelectorAll('[data-copy-prompt]').forEach((button) => {
  button.addEventListener('click', async () => {
    const code = button.parentElement.querySelector('pre code');
    const text = code.innerText;
    const previous = button.textContent;
    try {
      await navigator.clipboard.writeText(text);
      button.textContent = 'Скопировано';
      if (typeof window.ym === 'function') window.ym(27865374, 'reachGoal', 'copy_create_med_prompt');
    } catch {
      const range = document.createRange();
      range.selectNodeContents(code);
      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      button.textContent = 'Выделено — ⌘C';
    }
    window.setTimeout(() => { button.textContent = previous; }, 1800);
  });
});
