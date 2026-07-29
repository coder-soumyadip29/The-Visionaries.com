import re

filepath = r'c:\Users\SOUMYADIP\Desktop\THE VISIONARIES\index.html'

with open(filepath, 'rb') as f:
    content = f.read()

print(f"Loaded: {len(content):,} bytes")

# ── THE ROOT CAUSE ────────────────────────────────────────────────────────────
# The JS runs `const bgm = document.getElementById('bgm')` but the <audio> tag
# comes AFTER the </script>. So bgm = null → button does nothing.
#
# THE FIX: Wrap all music JS in DOMContentLoaded so it runs AFTER full DOM parse.
# ─────────────────────────────────────────────────────────────────────────────

OLD_MUSIC_SCRIPT = b"""    // ===== background music: play/pause button =====
    const bgm = document.getElementById('bgm');
    const musicBtn = document.getElementById('musicBtn');
    const playIcon = document.getElementById('playIcon');
    const pauseIcon = document.getElementById('pauseIcon');
    const musicLabel = document.getElementById('musicLabel');

    function setPlayingUI(isPlaying) {
      musicBtn.classList.toggle('paused', !isPlaying);
      playIcon.style.display = isPlaying ? 'none' : 'block';
      pauseIcon.style.display = isPlaying ? 'flex' : 'none';
      musicLabel.textContent = isPlaying ? 'Pause \\"Sabashiyaan\\"' : 'Play \\"Sabashiyaan\\"';
    }

    function toggleMusic() {
      if (bgm.paused) {
        bgm.play().then(() => setPlayingUI(true)).catch(() => setPlayingUI(false));
      } else {
        bgm.pause();
        setPlayingUI(false);
      }
    }

    // Always reset to the beginning on every page load (fresh start on refresh).
    window.addEventListener('load', () => {
      bgm.currentTime = 0;
      // Try to autoplay \xe2\x80\x94 browsers may block this until user interaction.
      // The play/pause button in the corner always works.
      bgm.play().then(() => setPlayingUI(true)).catch(() => setPlayingUI(false));
    });"""

NEW_MUSIC_SCRIPT = b"""    // ===== background music: play/pause button =====
    // Wrapped in DOMContentLoaded so bgm element exists when this runs.
    document.addEventListener('DOMContentLoaded', function() {
      const bgm = document.getElementById('bgm');
      const musicBtn = document.getElementById('musicBtn');
      const playIcon = document.getElementById('playIcon');
      const pauseIcon = document.getElementById('pauseIcon');
      const musicLabel = document.getElementById('musicLabel');

      bgm.currentTime = 0; // always start fresh

      function setPlayingUI(isPlaying) {
        musicBtn.classList.toggle('paused', !isPlaying);
        playIcon.style.display = isPlaying ? 'none' : 'block';
        pauseIcon.style.display = isPlaying ? 'flex' : 'none';
        musicLabel.textContent = isPlaying ? 'Pause \\"Sabashiyaan\\"' : 'Play \\"Sabashiyaan\\"';
      }

      // Expose toggleMusic globally so onclick="toggleMusic()" works
      window.toggleMusic = function() {
        if (bgm.paused) {
          bgm.currentTime = 0;
          bgm.play().then(() => setPlayingUI(true)).catch(err => {
            console.error('Audio play failed:', err);
            setPlayingUI(false);
          });
        } else {
          bgm.pause();
          setPlayingUI(false);
        }
      };
    });"""

if OLD_MUSIC_SCRIPT in content:
    content = content.replace(OLD_MUSIC_SCRIPT, NEW_MUSIC_SCRIPT)
    print("[OK] Fixed: Wrapped music JS in DOMContentLoaded")
    print("     toggleMusic is now global so the button onclick works.")
else:
    print("[WARN] Exact block not found, trying regex approach...")
    # Regex fallback: find the music script block and replace it
    pattern = rb'(// ===== background music.*?window\.addEventListener\(\'load\'.*?\}\);)'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        content = content[:match.start()] + NEW_MUSIC_SCRIPT + content[match.end():]
        print("[OK] Fixed via regex")
    else:
        print("[FAIL] Could not locate music script block.")
        print("Showing nearby content...")
        idx = content.find(b'background music')
        if idx >= 0:
            print(content[idx:idx+500].decode('utf-8', errors='replace'))
        input("Press Enter to close...")
        exit(1)

with open(filepath, 'wb') as f:
    f.write(content)

print("\n[DONE] Saved. Refresh index.html in your browser and click Play!")
input("Press Enter to close...")
