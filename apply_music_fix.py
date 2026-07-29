"""
Fix the music play/pause button in index.html.

Root cause: The <script> block tries to get document.getElementById('bgm')
but the <audio id="bgm"> element appears AFTER the </script> tag.
So bgm is null and the button silently does nothing.

Fix: Wrap the music JS in a DOMContentLoaded listener so the DOM
is fully parsed before we look up elements. Expose toggleMusic on
window so the button's onclick="toggleMusic()" still works.
"""

filepath = r'c:\Users\SOUMYADIP\Desktop\THE VISIONARIES\index.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"Loaded: {len(content):,} characters")

# ── What we're replacing ──────────────────────────────────────────────────────
OLD = """    // ===== background music: play/pause button =====
    const bgm = document.getElementById('bgm');
    const musicBtn = document.getElementById('musicBtn');
    const playIcon = document.getElementById('playIcon');
    const pauseIcon = document.getElementById('pauseIcon');
    const musicLabel = document.getElementById('musicLabel');

    function setPlayingUI(isPlaying) {
      musicBtn.classList.toggle('paused', !isPlaying);
      playIcon.style.display = isPlaying ? 'none' : 'block';
      pauseIcon.style.display = isPlaying ? 'flex' : 'none';
      musicLabel.textContent = isPlaying ? 'Pause "Sabashiyaan"' : 'Play "Sabashiyaan"';
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
      // Try to autoplay \u2014 browsers may block this until user interaction.
      // The play/pause button in the corner always works.
      bgm.play().then(() => setPlayingUI(true)).catch(() => setPlayingUI(false));
    });"""

NEW = """    // ===== background music: play/pause button =====
    // Wrapped in DOMContentLoaded so <audio id="bgm"> exists when this runs.
    document.addEventListener('DOMContentLoaded', function() {
      var bgm = document.getElementById('bgm');
      var musicBtn = document.getElementById('musicBtn');
      var playIcon = document.getElementById('playIcon');
      var pauseIcon = document.getElementById('pauseIcon');
      var musicLabel = document.getElementById('musicLabel');

      if (!bgm || !musicBtn) {
        console.error('[Music] Elements not found!');
        return;
      }

      bgm.currentTime = 0;

      function setPlayingUI(isPlaying) {
        musicBtn.classList.toggle('paused', !isPlaying);
        playIcon.style.display = isPlaying ? 'none' : 'block';
        pauseIcon.style.display = isPlaying ? 'flex' : 'none';
        musicLabel.textContent = isPlaying ? 'Pause "Sabashiyaan"' : 'Play "Sabashiyaan"';
      }

      // Expose globally so onclick="toggleMusic()" works from HTML
      window.toggleMusic = function() {
        if (bgm.paused) {
          bgm.play()
            .then(function() { setPlayingUI(true); })
            .catch(function(err) {
              console.error('[Music] Play failed:', err);
              setPlayingUI(false);
            });
        } else {
          bgm.pause();
          setPlayingUI(false);
        }
      };

      // Try autoplay on page load (browsers may block until user gesture)
      bgm.play()
        .then(function() { setPlayingUI(true); })
        .catch(function() { setPlayingUI(false); });
    });"""

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("[OK] Fixed! Music JS now wrapped in DOMContentLoaded.")
    print("     toggleMusic() is exposed on window so the button works.")
else:
    # Check if already fixed
    if 'DOMContentLoaded' in content and 'window.toggleMusic' in content:
        print("[OK] Already fixed — no changes needed.")
    else:
        print("[FAIL] Could not locate the original music script block.")
        print("       The code may have been modified already.")
        # Show what's near the music section for debugging
        idx = content.find('background music')
        if idx >= 0:
            print("\nNearby content:")
            print(content[idx:idx+600])
