import './App.css'
import FileDropzone from './components/ImportBox/FileDropzone'


function App() {
  return (
    <>
      <section id="center">
        <div className="hero">
          <img src="/hero.png" className="base" width="170" height="179" alt="" />
          <img src="react.svg" className="framework" alt="React logo" />
          <img src="/vite.svg" className="vite" alt="Vite logo" />
        </div>
        <div>
          <h1>Get started</h1>
          <FileDropzone />
        </div>
      </section>

      <div className="ticks"></div>

      <section id="next-steps">
        <div id="social" style={{ justifyContent: 'center', display: 'flex', flexDirection: 'column'}}>
          <svg className="icon" role="presentation" aria-hidden="true">
            <use href="/icons.svg#social-icon"></use>
          </svg>
          <h2>Projekt von Nils und Sam</h2>
          <p>Schau dir unseren Code an!</p>
          <ul>
            <li>
              <a href="https://github.com/Nils1024/user-story-api" target="_blank">
                <svg
                  className="button-icon"
                  role="presentation"
                  aria-hidden="true"
                >
                  <use href="/icons.svg#github-icon"></use>
                </svg>
                GitHub
              </a>
            </li>
          </ul>
        </div>
      </section>

      <div className="ticks"></div>
      <section id="spacer"></section>
    </>
  )
}

export default App