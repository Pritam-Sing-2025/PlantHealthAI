import React, { useEffect, useState } from "react";

export default function Footer() {
  const [email, setEmail] = useState("");
  const [subscribed, setSubscribed] = useState(false);
  const [cookieAccepted, setCookieAccepted] = useState(false);
  const [showCookiePanel, setShowCookiePanel] = useState(false);
  const [msg, setMsg] = useState(null);

  useEffect(() => {
    const accepted = localStorage.getItem("plantai_cookies_accepted");
    setCookieAccepted(accepted === "true");
    setShowCookiePanel(accepted !== "true");
  }, []);

  const isValidEmail = (s) =>
    /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(s).toLowerCase());

  const handleSubscribe = (e) => {
    e.preventDefault();
    setMsg(null);

    if (!isValidEmail(email)) {
      setMsg({ type: "error", text: "Please enter a valid email address." });
      return;
    }

    setSubscribed(true);
    setMsg({ type: "success", text: "Thanks! You're subscribed." });
    setEmail("");
    console.log("Subscribed email (client-only):", email);
  };

  const acceptCookies = () => {
    localStorage.setItem("plantai_cookies_accepted", "true");
    setCookieAccepted(true);
    setShowCookiePanel(false);
  };

  const manageCookies = () => {
    alert(
      "Cookie preferences: this demo stores only a small local flag (no tracking). For production, show granular controls here."
    );
  };

  return (
    <>
      <footer className="site-footer">
        <div className="footer-inner">
          <div className="footer-col about">
            <h3>Almighty</h3>
            <p>
              Helping growers detect plant diseases quickly. Built with
              simplicity in mind. Stay in touch for updates and model
              improvements.
            </p>

            <div className="social-row" aria-label="Social links">
              <a
                href="https://twitter.com"
                target="_blank"
                rel="noopener noreferrer"
                aria-label="Twitter"
                className="social-link"
              >
                {/* Twitter */}
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                  <path
                    d="M22 5.92c-.64.29-1.33.49-2.05.58a3.56 3.56 0 001.57-1.97 7.1 7.1 0 01-2.26.86 3.53 3.53 0 00-6.02 3.22A10.03 10.03 0 013 4.9a3.52 3.52 0 001.09 4.72c-.53-.02-1.03-.16-1.47-.4v.04c0 1.7 1.21 3.12 2.82 3.45a3.5 3.5 0 01-1.47.06c.42 1.32 1.64 2.28 3.09 2.31A7.06 7.06 0 012 19.54a9.93 9.93 0 005.4 1.58c6.48 0 10.03-5.36 10.03-10.01v-.45A7 7 0 0022 5.92z"
                    fill="currentColor"
                  />
                </svg>
              </a>

              <a
                href="https://facebook.com"
                target="_blank"
                rel="noopener noreferrer"
                aria-label="Facebook"
                className="social-link"
              >
                {/* Facebook */}
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                  <path
                    d="M22 12a10 10 0 10-11.5 9.9v-7h-2.2V12h2.2V9.6c0-2.2 1.33-3.4 3.26-3.4.94 0 1.93.17 1.93.17v2.12h-1.09c-1.07 0-1.4.66-1.4 1.33V12h2.38l-.38 2.9h-2V21.9A10 10 0 0022 12z"
                    fill="currentColor"
                  />
                </svg>
              </a>

              <a
                href="https://instagram.com"
                target="_blank"
                rel="noopener noreferrer"
                aria-label="Instagram"
                className="social-link"
              >
                {/* Instagram */}
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                  <path
                    d="M7 2h10a5 5 0 015 5v10a5 5 0 01-5 5H7a5 5 0 01-5-5V7a5 5 0 015-5zm5 5.9a4.1 4.1 0 100 8.2 4.1 4.1 0 000-8.2zm5.2-.9a1.1 1.1 0 11-2.2 0 1.1 1.1 0 012.2 0zM12 9a3 3 0 110 6 3 3 0 010-6z"
                    fill="currentColor"
                  />
                </svg>
              </a>

              <a
                href="https://linkedin.com"
                target="_blank"
                rel="noopener noreferrer"
                aria-label="LinkedIn"
                className="social-link"
              >
                {/* LinkedIn */}
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                  <path
                    d="M4.98 3.5A2.5 2.5 0 004.98 8.5 2.5 2.5 0 004.98 3.5zM3 9.75h4v11H3v-11zM13 9.75h3.6v1.5h.05c.5-.95 1.73-1.95 3.56-1.95 3.8 0 4.5 2.5 4.5 5.75v6.7h-4v-5.95c0-1.42-.03-3.25-1.98-3.25-1.98 0-2.29 1.55-2.29 3.14v6.06h-4v-11z"
                    fill="currentColor"
                  />
                </svg>
              </a>

              <a
                href="https://github.com"
                target="_blank"
                rel="noopener noreferrer"
                aria-label="GitHub"
                className="social-link"
              >
                {/* GitHub */}
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                  <path
                    d="M12 .5a12 12 0 00-3.8 23.4c.6.1.8-.3.8-.6v-2.1c-3.3.7-4-1.6-4-1.6-.5-1.2-1.1-1.5-1.1-1.5-.9-.6.07-.6.07-.6 1 .06 1.5 1 1.5 1 .9 1.6 2.4 1.1 3 .8.1-.6.4-1.1.7-1.4-2.7-.3-5.5-1.3-5.5-5.9 0-1.3.5-2.3 1.2-3.1-.1-.3-.5-1.6.1-3.2 0 0 1-.3 3.3 1.2a11.4 11.4 0 016 0C17 3 18 3.3 18 3.3c.6 1.6.2 2.9.1 3.2.8.8 1.2 1.8 1.2 3.1 0 4.6-2.8 5.6-5.5 5.9.4.4.8 1.1.8 2.2v3.3c0 .3.2.7.8.6A12 12 0 0012 .5z"
                    fill="currentColor"
                  />
                </svg>
              </a>
            </div>
          </div>

          <div className="footer-col links">
            <h4>Quick Links</h4>
            <ul>
              <li>
                <a href="/how-it-works">How It Works</a>
              </li>
              <li>
                <a href="/about">About</a>
              </li>
              <li>
                <a href="/contact">Contact</a>
              </li>
              <li>
                <a href="/privacy">Privacy Policy</a>
              </li>
              <li>
                <a href="/terms">Terms &amp; Conditions</a>
              </li>
            </ul>
          </div>

          <div className="footer-col subscribe">
            <h4>Subscribe for updates</h4>
            <form onSubmit={handleSubscribe} className="subscribe-form">
              <input
                aria-label="Email"
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="subscribe-input"
              />
              <button type="submit" className="subscribe-btn">
                Subscribe
              </button>
            </form>

            {msg && (
              <div
                role="status"
                className={`subscribe-msg ${msg.type === "error" ? "err" : "ok"}`}
              >
                {msg.text}
              </div>
            )}

            <div className="small-note">
              By subscribing you agree to receive occasional updates. We don't
              spam.
            </div>
          </div>
        </div>

        <div className="footer-bottom">
          <span>© {new Date().getFullYear()} Almighty</span>
          <nav className="bottom-links" aria-label="Footer policy links">
            <a href="/privacy">Privacy</a>
            <a href="/cookies">Cookies</a>
            <a href="/terms">Terms</a>
          </nav>
        </div>
      </footer>

      {showCookiePanel && !cookieAccepted && (
        <div className="cookie-panel" role="dialog" aria-live="polite">
          <div className="cookie-text">
            We use a tiny cookie to remember your preferences. This demo does
            not track personal data. Learn more in our{" "}
            <a href="/privacy">Privacy Policy</a>.
          </div>
          <div className="cookie-actions">
            <button className="btn ghost" onClick={manageCookies}>
              Manage
            </button>
            <button className="btn primary" onClick={acceptCookies}>
              Accept Cookies
            </button>
          </div>
        </div>
      )}
    </>
  );
}
