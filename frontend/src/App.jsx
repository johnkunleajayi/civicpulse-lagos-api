import { useEffect, useRef, useState } from "react"
import civicPulseLogo from "./assets/civic-logo.png"
import lagosBridgeBackground from "./assets/civic-bg.png"

const API_URL = "https://civicpulse-lagos-api.onrender.com"

function App() {
  const [question, setQuestion] = useState("")
  const [answer, setAnswer] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  const answerSectionRef = useRef(null)

  const askCivicPulse = async (questionText = question) => {
    if (!questionText.trim()) {
      return
    }

    setQuestion(questionText)
    setLoading(true)
    setError("")
    setAnswer(null)

    try {
      const response = await fetch(`${API_URL}/questions/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: questionText.trim(),
        }),
      })

      if (!response.ok) {
        throw new Error("Unable to get an answer from CivicPulse.")
      }

      const data = await response.json()

      setAnswer(data)
    } catch (err) {
      setError(
        err.message ||
          "Something went wrong while connecting to CivicPulse."
      )
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    if (!answer) {
      return
    }

    requestAnimationFrame(() => {
      answerSectionRef.current?.scrollIntoView({
        behavior: "smooth",
        block: "start",
      })
    })
  }, [answer])

  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      askCivicPulse()
    }
  }

  const handleSuggestedQuestion = (suggestedQuestion) => {
    askCivicPulse(suggestedQuestion)
  }

  const getSuggestedQuestions = () => {
    if (!isClarification || !answer?.answer) {
      return []
    }

    return answer.answer
      .split("\n")
      .map((line) => {
        const match = line.match(/^\s*\d+\.\s+(.+)$/)
        return match ? match[1].trim() : null
      })
      .filter(Boolean)
  }

  const hasEvidence =
    answer?.evidence && answer.evidence.length > 0

  const isClarification = answer && !hasEvidence

  const suggestedQuestions = getSuggestedQuestions()

  return (
    <div className="relative min-h-screen overflow-x-hidden text-slate-900">
      {/* Full-page Lagos background */}
      <div className="pointer-events-none fixed inset-0 -z-10">
        <img
          src={lagosBridgeBackground}
          alt=""
          aria-hidden="true"
          className="h-full w-full object-cover"
        />

        <div className="absolute inset-0 bg-white/45"></div>

        <div className="absolute inset-0 bg-gradient-to-b from-white/65 via-white/40 to-blue-50/65"></div>
      </div>

      <header className="border-b border-white/70 bg-white/85 backdrop-blur-md">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <div>
            <img
              src={civicPulseLogo}
              alt="CivicPulse Lagos"
              className="h-16 w-auto object-contain sm:h-20"
            />
          </div>

          <div className="hidden items-center gap-2 rounded-full border border-emerald-100 bg-emerald-50/95 px-3 py-1.5 text-sm font-medium text-emerald-700 sm:flex">
            <span className="h-2 w-2 rounded-full bg-emerald-500"></span>
            Lagos civic information
          </div>
        </div>
      </header>

      <main>
        {/* Lagos Hero */}
        <section className="relative overflow-hidden">
          <div className="relative mx-auto max-w-5xl px-6 pb-20 pt-16 text-center sm:pb-24 sm:pt-24">
            <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-blue-200 bg-white/90 px-4 py-2 text-sm font-semibold text-blue-700 shadow-sm backdrop-blur-sm">
              <span className="h-2 w-2 rounded-full bg-blue-600"></span>
              2026 Lagos civic data
            </div>

            <h1 className="mx-auto max-w-4xl text-4xl font-bold tracking-tight text-slate-950 sm:text-6xl lg:text-7xl">
              Understand Lagos.
              <span className="block text-blue-700">
                Verify the facts.
              </span>
              <span className="block">
                Make Lagos more transparent.
              </span>
            </h1>

            <p className="mx-auto mt-6 max-w-2xl text-lg leading-8 text-slate-700 sm:text-xl">
              Ask questions about Lagos State public spending, budgets, and
              projects. CivicPulse connects the answer to official government
              evidence so you can check it yourself.
            </p>

            <div className="mx-auto mt-10 max-w-3xl">
              <div className="rounded-2xl border border-white/80 bg-white/95 p-2 shadow-xl shadow-slate-900/10 backdrop-blur-sm">
                <div className="flex flex-col gap-2 sm:flex-row">
                  <input
                    type="text"
                    value={question}
                    onChange={(event) => setQuestion(event.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Ask about Lagos public spending..."
                    className="min-h-14 flex-1 rounded-xl border border-transparent bg-slate-50 px-5 text-base text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-blue-300 focus:bg-white focus:ring-4 focus:ring-blue-50"
                  />

                  <button
                    type="button"
                    onClick={() => askCivicPulse()}
                    disabled={loading}
                    className="min-h-14 rounded-xl bg-slate-950 px-7 font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
                  >
                    {loading ? "Checking..." : "Ask CivicPulse"}
                  </button>
                </div>
              </div>

              <p className="mt-3 text-sm font-medium text-slate-600">
                Ask about Lagos State budgets, projects, spending, and
                infrastructure.
              </p>

              <p className="mt-4 text-sm font-medium text-slate-500">
                <span className="font-semibold text-slate-700">
                  Current data coverage:
                </span>{" "}
                Lagos State's 2026 budget and Q2 2026 performance data.
              </p>
            </div>

            <div className="mt-6 flex flex-wrap justify-center gap-2">
              <button
                type="button"
                onClick={() =>
                  setQuestion(
                    "How much has Lagos spent on waterways?"
                  )
                }
                className="rounded-full border border-white/90 bg-white/90 px-4 py-2 text-sm font-medium text-slate-700 shadow-sm backdrop-blur-sm transition hover:border-blue-300 hover:bg-blue-50 hover:text-blue-700"
              >
                Lagos waterways
              </button>

              <button
                type="button"
                onClick={() =>
                  setQuestion(
                    "What percentage of the health project budget was spent?"
                  )
                }
                className="rounded-full border border-white/90 bg-white/90 px-4 py-2 text-sm font-medium text-slate-700 shadow-sm backdrop-blur-sm transition hover:border-emerald-300 hover:bg-emerald-50 hover:text-emerald-700"
              >
                Lagos health projects
              </button>

              <button
                type="button"
                onClick={() =>
                  setQuestion(
                    "What are the largest Lagos State projects by 2026 budget?"
                  )
                }
                className="rounded-full border border-white/90 bg-white/90 px-4 py-2 text-sm font-medium text-slate-700 shadow-sm backdrop-blur-sm transition hover:border-amber-300 hover:bg-amber-50 hover:text-amber-700"
              >
                Lagos largest projects
              </button>
            </div>

            <div className="mt-10 flex flex-wrap items-center justify-center gap-x-6 gap-y-2 text-xs font-semibold uppercase tracking-wide text-slate-500">
              <span>2026 Data Coverage</span>
              <span className="hidden h-1 w-1 rounded-full bg-slate-400 sm:block"></span>
              <span>Q2 2026 Performance</span>
              <span className="hidden h-1 w-1 rounded-full bg-slate-400 sm:block"></span>
              <span>Official Sources</span>
            </div>
          </div>
        </section>

        {error && (
          <section className="mx-auto max-w-4xl px-6 pb-12 pt-8">
            <div className="rounded-2xl border border-red-200 bg-red-50/95 p-6 text-red-700 shadow-sm backdrop-blur-sm">
              <p className="font-semibold">Unable to answer</p>
              <p className="mt-1 text-sm">{error}</p>
            </div>
          </section>
        )}

        {answer && (
          <section
            ref={answerSectionRef}
            className="scroll-mt-6 mx-auto max-w-4xl px-6 pb-16 pt-10"
          >
            <div className="rounded-2xl border border-white/80 bg-white/95 p-6 shadow-xl shadow-slate-900/10 backdrop-blur-sm sm:p-8">
              {isClarification ? (
                <div className="mb-6 flex items-center gap-2">
                  <span className="flex h-8 w-8 items-center justify-center rounded-full bg-blue-100 font-semibold text-blue-700">
                    🔎
                  </span>
                  <span className="text-sm font-semibold uppercase tracking-wide text-blue-700">
                    Let's clarify
                  </span>
                </div>
              ) : (
                <div className="mb-6 flex items-center gap-2">
                  <span className="flex h-8 w-8 items-center justify-center rounded-full bg-emerald-100 font-semibold text-emerald-700">
                    ✓
                  </span>
                  <span className="text-sm font-semibold uppercase tracking-wide text-emerald-700">
                    Verified answer
                  </span>
                </div>
              )}

              <h3 className="text-xl font-semibold text-slate-950">
                {isClarification ? "I need a little more detail" : "Answer"}
              </h3>

              {isClarification && suggestedQuestions.length > 0 ? (
                <div className="mt-3">
                  <p className="text-lg leading-8 text-slate-700">
                    I can help you explore verified Lagos State budget and
                    project information, but I need a little more detail.
                  </p>

                  <p className="mt-6 text-sm font-semibold uppercase tracking-wide text-slate-500">
                    Try one of these questions
                  </p>

                  <div className="mt-3 space-y-2">
                    {suggestedQuestions.map((suggestedQuestion, index) => (
                      <button
                        key={index}
                        type="button"
                        onClick={() =>
                          handleSuggestedQuestion(suggestedQuestion)
                        }
                        disabled={loading}
                        className="group flex w-full items-start gap-3 rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-left text-sm leading-6 text-slate-700 transition hover:border-blue-300 hover:bg-blue-50 hover:text-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
                      >
                        <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-white text-xs font-semibold text-slate-500 group-hover:bg-blue-100 group-hover:text-blue-700">
                          {index + 1}
                        </span>

                        <span>{suggestedQuestion}</span>
                      </button>
                    ))}
                  </div>
                </div>
              ) : (
                <p className="mt-3 whitespace-pre-line text-lg leading-8 text-slate-700">
                  {answer.answer}
                </p>
              )}

              {hasEvidence && (
                <div className="mt-8 border-t border-slate-200 pt-8">
                  <div>
                    <div className="flex items-center gap-3">
                      <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-50 text-emerald-700">
                        ✓
                      </div>

                      <div>
                        <h3 className="text-xl font-semibold text-slate-950">
                          Evidence
                        </h3>

                        <p className="mt-1 text-sm text-slate-500">
                          Official information used to support this answer
                        </p>
                      </div>
                    </div>
                  </div>

                  <div className="mt-5 space-y-4">
                    {answer.evidence.map((item, index) => {
                      const project = item.project
                      const source = item.source

                      const sourcePage = project
                        ? project.source_page
                        : item.source_page

                      return (
                        <div
                          key={index}
                          className="rounded-xl border border-slate-200 bg-slate-50 p-5"
                        >
                          {project && (
                            <div>
                              <div className="mb-4 flex items-start gap-3">
                                <span className="mt-0.5 flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-emerald-100 text-sm font-bold text-emerald-700">
                                  ✓
                                </span>

                                <div>
                                  <p className="text-xs font-semibold uppercase tracking-wide text-emerald-700">
                                    Verified from official source
                                  </p>

                                  <p className="mt-1 font-semibold leading-6 text-slate-950">
                                    {project.project_description}
                                  </p>
                                </div>
                              </div>

                              <div className="grid gap-3 sm:grid-cols-2">
                                <div className="rounded-lg border border-slate-200 bg-white p-4">
                                  <p className="text-xs font-medium uppercase tracking-wide text-slate-500">
                                    2026 Budget
                                  </p>

                                  <p className="mt-1 text-lg font-semibold text-slate-900">
                                    ₦
                                    {Number(
                                      project.original_budget
                                    ).toLocaleString("en-NG", {
                                      minimumFractionDigits: 2,
                                    })}
                                  </p>
                                </div>

                                <div className="rounded-lg border border-slate-200 bg-white p-4">
                                  <p className="text-xs font-medium uppercase tracking-wide text-slate-500">
                                    YTD Expenditure
                                  </p>

                                  <p className="mt-1 text-lg font-semibold text-slate-900">
                                    ₦
                                    {Number(
                                      project.ytd_performance
                                    ).toLocaleString("en-NG", {
                                      minimumFractionDigits: 2,
                                    })}
                                  </p>
                                </div>
                              </div>
                            </div>
                          )}

                          {item.metric && (
                            <div>
                              <p className="font-semibold text-slate-950">
                                {item.metric}
                              </p>
                            </div>
                          )}

                          {source && (
                            <div className="mt-5 border-t border-slate-200 pt-5">
                              <div className="flex items-start gap-3">
                                <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-blue-50 text-blue-700">
                                  📄
                                </div>

                                <div>
                                  <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
                                    Source
                                  </p>

                                  <p className="mt-1 text-sm font-semibold leading-6 text-slate-900">
                                    {source.title}
                                  </p>
                                </div>
                              </div>

                              <div className="mt-4 grid gap-4 text-sm sm:grid-cols-3">
                                <div>
                                  <p className="text-xs font-medium uppercase tracking-wide text-slate-400">
                                    Publisher
                                  </p>

                                  <p className="mt-1 text-slate-700">
                                    {source.publisher}
                                  </p>
                                </div>

                                <div>
                                  <p className="text-xs font-medium uppercase tracking-wide text-slate-400">
                                    Reporting period
                                  </p>

                                  <p className="mt-1 text-slate-700">
                                    {source.reporting_period}
                                  </p>
                                </div>

                                <div>
                                  <p className="text-xs font-medium uppercase tracking-wide text-slate-400">
                                    Source page
                                  </p>

                                  <p className="mt-1 font-semibold text-slate-900">
                                    Page {sourcePage}
                                  </p>
                                </div>
                              </div>

                              <a
                                href={source.url}
                                target="_blank"
                                rel="noreferrer"
                                className="mt-5 inline-flex rounded-lg border border-blue-200 bg-blue-50 px-4 py-2 text-sm font-semibold text-blue-700 transition hover:bg-blue-100 hover:text-blue-900"
                              >
                                View official source →
                              </a>
                            </div>
                          )}
                        </div>
                      )
                    })}
                  </div>
                </div>
              )}
            </div>
          </section>
        )}

        <section className="border-y border-white/70 bg-white/80 backdrop-blur-sm">
          <div className="mx-auto max-w-6xl px-6 py-16">
            <div className="mx-auto max-w-3xl text-center">
              <p className="text-sm font-semibold uppercase tracking-wide text-blue-700">
                Built for Lagos
              </p>

              <h2 className="mt-3 text-3xl font-bold tracking-tight text-slate-950 sm:text-4xl">
                From Lagos data to Lagos citizens.
              </h2>

              <p className="mt-4 text-lg leading-8 text-slate-600">
                Civic information should be understandable, verifiable, and
                accessible to everyone who cares about Lagos.
              </p>
            </div>

            <div className="mt-12 grid gap-6 md:grid-cols-3">
              <div className="rounded-2xl border border-slate-200 bg-white/90 p-6 transition hover:-translate-y-1 hover:shadow-md">
                <div className="mb-4 flex h-11 w-11 items-center justify-center rounded-xl bg-blue-50 text-xl">
                  🔎
                </div>

                <h3 className="text-lg font-semibold text-slate-950">
                  Ask
                </h3>

                <p className="mt-2 leading-7 text-slate-600">
                  Ask straightforward questions about Lagos State budgets,
                  spending, and public projects.
                </p>
              </div>

              <div className="rounded-2xl border border-slate-200 bg-white/90 p-6 transition hover:-translate-y-1 hover:shadow-md">
                <div className="mb-4 flex h-11 w-11 items-center justify-center rounded-xl bg-emerald-50 text-xl">
                  ✓
                </div>

                <h3 className="text-lg font-semibold text-slate-950">
                  Verify
                </h3>

                <p className="mt-2 leading-7 text-slate-600">
                  Answers are grounded in published Lagos State government
                  information and official sources.
                </p>
              </div>

              <div className="rounded-2xl border border-slate-200 bg-white/90 p-6 transition hover:-translate-y-1 hover:shadow-md">
                <div className="mb-4 flex h-11 w-11 items-center justify-center rounded-xl bg-amber-50 text-xl">
                  →
                </div>

                <h3 className="text-lg font-semibold text-slate-950">
                  Act
                </h3>

                <p className="mt-2 leading-7 text-slate-600">
                  See the source, reporting period, and page so you can check
                  the evidence yourself.
                </p>
              </div>
            </div>
          </div>
        </section>

        <section className="bg-white/65 backdrop-blur-sm">
          <div className="mx-auto max-w-6xl px-6 py-16">
            <div className="mx-auto max-w-3xl text-center">
              <p className="text-sm font-semibold uppercase tracking-wide text-blue-700">
                How CivicPulse verifies information
              </p>

              <h2 className="mt-3 text-3xl font-bold tracking-tight text-slate-950 sm:text-4xl">
                Don't just trust the answer. Check the evidence.
              </h2>

              <p className="mt-4 text-lg leading-8 text-slate-600">
                CivicPulse is designed to make the path from Lagos public data
                to civic understanding visible.
              </p>
            </div>

            <div className="mt-10 grid gap-6 md:grid-cols-3">
              <div className="rounded-2xl border border-slate-200 bg-white/90 p-6">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-blue-50 text-xl font-bold text-blue-700">
                  1
                </div>

                <h3 className="mt-5 text-lg font-semibold text-slate-950">
                  Find official sources
                </h3>

                <p className="mt-2 leading-7 text-slate-600">
                  CivicPulse uses published Lagos State government information
                  as the foundation for its answers.
                </p>
              </div>

              <div className="rounded-2xl border border-slate-200 bg-white/90 p-6">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-emerald-50 text-xl font-bold text-emerald-700">
                  2
                </div>

                <h3 className="mt-5 text-lg font-semibold text-slate-950">
                  Match the evidence
                </h3>

                <p className="mt-2 leading-7 text-slate-600">
                  Relevant Lagos budget and project records are matched to the
                  citizen's question before an answer is presented.
                </p>
              </div>

              <div className="rounded-2xl border border-slate-200 bg-white/90 p-6">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-amber-50 text-xl font-bold text-amber-700">
                  3
                </div>

                <h3 className="mt-5 text-lg font-semibold text-slate-950">
                  Show the proof
                </h3>

                <p className="mt-2 leading-7 text-slate-600">
                  Every supported result points back to the source, reporting
                  period, and page so citizens can verify it themselves.
                </p>
              </div>
            </div>
          </div>
        </section>
      </main>

      <footer className="bg-slate-950/95 px-6 py-8 text-center text-sm text-slate-400 backdrop-blur-sm">
        <p>CivicPulse Lagos · Information you can trust</p>
        <p className="mt-2 text-xs text-slate-500">
          Current coverage: Lagos State public budget and project information
          for 2026, including Q2 2026 performance data.
        </p>
      </footer>
    </div>
  )
}

export default App