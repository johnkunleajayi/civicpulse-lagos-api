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

        {/* Stronger image visibility */}
        <div className="absolute inset-0 bg-white/30"></div>

        <div className="absolute inset-0 bg-gradient-to-b from-white/55 via-white/25 to-blue-50/55"></div>

        {/* Subtle readability layer */}
        <div className="absolute inset-0 bg-slate-950/[0.03]"></div>
      </div>

      {/* Header */}
      <header className="sticky top-0 z-30 border-b border-white/60 bg-white/80 shadow-sm backdrop-blur-xl">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-3">
          <div>
            <img
              src={civicPulseLogo}
              alt="CivicPulse Lagos"
              className="h-14 w-auto object-contain sm:h-16"
            />
          </div>

          <div className="hidden items-center gap-2 rounded-full border border-emerald-200/80 bg-emerald-50/90 px-3 py-1.5 text-sm font-medium text-emerald-700 shadow-sm sm:flex">
            <span className="h-2 w-2 rounded-full bg-emerald-500 shadow-sm"></span>
            Lagos civic information
          </div>
        </div>
      </header>

      <main>

        {/* Hero */}
        <section className="relative overflow-hidden">
          <div className="absolute left-1/2 top-10 h-72 w-72 -translate-x-1/2 rounded-full bg-blue-400/10 blur-3xl"></div>

          <div className="relative mx-auto max-w-5xl px-6 pb-16 pt-14 text-center sm:pb-20 sm:pt-20">

            {/* Scope badge */}
            <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-blue-200/90 bg-white/85 px-4 py-2 text-sm font-semibold text-blue-700 shadow-lg shadow-blue-900/5 backdrop-blur-md">
              <span className="h-2 w-2 rounded-full bg-blue-600 shadow-sm"></span>
              2026 Lagos civic data
            </div>

            {/* Main heading */}
            <h1 className="mx-auto max-w-4xl text-4xl font-bold tracking-tight text-slate-950 drop-shadow-sm sm:text-6xl lg:text-7xl">
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

            {/* Search */}
            <div className="mx-auto mt-9 max-w-3xl">
              <div className="rounded-3xl border border-white/90 bg-white/90 p-2 shadow-2xl shadow-slate-900/15 backdrop-blur-xl">

                <div className="flex flex-col gap-2 sm:flex-row">
                  <div className="relative flex-1">
                    <span className="pointer-events-none absolute left-5 top-1/2 -translate-y-1/2 text-lg text-slate-400">
                      🔎
                    </span>

                    <input
                      type="text"
                      value={question}
                      onChange={(event) => setQuestion(event.target.value)}
                      onKeyDown={handleKeyDown}
                      placeholder="Ask about Lagos public spending..."
                      className="min-h-14 w-full rounded-2xl border border-transparent bg-slate-50 pl-12 pr-5 text-base text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-blue-300 focus:bg-white focus:ring-4 focus:ring-blue-50"
                    />
                  </div>

                  <button
                    type="button"
                    onClick={() => askCivicPulse()}
                    disabled={loading}
                    className="min-h-14 rounded-2xl bg-slate-950 px-7 font-semibold text-white shadow-lg shadow-slate-950/15 transition hover:bg-blue-700 hover:shadow-blue-900/20 disabled:cursor-not-allowed disabled:opacity-60"
                  >
                    {loading ? "Checking..." : "Ask CivicPulse →"}
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

            {/* Suggested questions */}
            <div className="mt-6 flex flex-wrap justify-center gap-2">
              <button
                type="button"
                onClick={() =>
                  setQuestion(
                    "How much has Lagos spent on waterways?"
                  )
                }
                className="rounded-full border border-white/90 bg-white/85 px-4 py-2 text-sm font-medium text-slate-700 shadow-sm backdrop-blur-md transition hover:border-blue-300 hover:bg-blue-50 hover:text-blue-700 hover:shadow-md"
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
                className="rounded-full border border-white/90 bg-white/85 px-4 py-2 text-sm font-medium text-slate-700 shadow-sm backdrop-blur-md transition hover:border-emerald-300 hover:bg-emerald-50 hover:text-emerald-700 hover:shadow-md"
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
                className="rounded-full border border-white/90 bg-white/85 px-4 py-2 text-sm font-medium text-slate-700 shadow-sm backdrop-blur-md transition hover:border-amber-300 hover:bg-amber-50 hover:text-amber-700 hover:shadow-md"
              >
                Lagos largest projects
              </button>
            </div>

            {/* Metadata */}
            <div className="mt-9 flex flex-wrap items-center justify-center gap-x-5 gap-y-2 text-xs font-semibold uppercase tracking-wide text-slate-500">
              <span>2026 Data Coverage</span>

              <span className="hidden h-1 w-1 rounded-full bg-slate-400 sm:block"></span>

              <span>Q2 2026 Performance</span>

              <span className="hidden h-1 w-1 rounded-full bg-slate-400 sm:block"></span>

              <span>Official Sources</span>
            </div>
          </div>
        </section>

        {/* Error */}
        {error && (
          <section className="mx-auto max-w-4xl px-6 pb-12 pt-8">
            <div className="rounded-2xl border border-red-200 bg-red-50/95 p-6 text-red-700 shadow-xl shadow-red-900/5 backdrop-blur-md">
              <p className="font-semibold">Unable to answer</p>
              <p className="mt-1 text-sm">{error}</p>
            </div>
          </section>
        )}

        {/* Answer */}
        {answer && (
          <section
            ref={answerSectionRef}
            className="scroll-mt-6 mx-auto max-w-4xl px-6 pb-16 pt-8"
          >
            <div className="overflow-hidden rounded-3xl border border-white/90 bg-white/95 shadow-2xl shadow-slate-900/15 backdrop-blur-xl">

              {/* Answer header */}
              <div
                className={
                  isClarification
                    ? "border-b border-blue-100 bg-gradient-to-r from-blue-50/90 to-white px-6 py-5 sm:px-8"
                    : "border-b border-emerald-100 bg-gradient-to-r from-emerald-50/90 to-white px-6 py-5 sm:px-8"
                }
              >
                {isClarification ? (
                  <div className="flex items-center gap-3">
                    <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-100 text-lg text-blue-700 shadow-sm">
                      🔎
                    </span>

                    <div>
                      <p className="text-xs font-bold uppercase tracking-[0.16em] text-blue-700">
                        Let's clarify
                      </p>

                      <p className="mt-0.5 text-sm text-slate-500">
                        Help me understand what you're looking for
                      </p>
                    </div>
                  </div>
                ) : (
                  <div className="flex items-center gap-3">
                    <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-100 text-lg font-bold text-emerald-700 shadow-sm">
                      ✓
                    </span>

                    <div>
                      <p className="text-xs font-bold uppercase tracking-[0.16em] text-emerald-700">
                        Verified answer
                      </p>

                      <p className="mt-0.5 text-sm text-slate-500">
                        Supported by official Lagos State information
                      </p>
                    </div>
                  </div>
                )}
              </div>

              <div className="p-6 sm:p-8">

                <h3 className="text-xl font-semibold text-slate-950">
                  {isClarification
                    ? "I need a little more detail"
                    : "Answer"}
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
                          <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-white text-xs font-semibold text-slate-500 shadow-sm group-hover:bg-blue-100 group-hover:text-blue-700">
                            {index + 1}
                          </span>

                          <span>{suggestedQuestion}</span>
                        </button>
                      ))}
                    </div>
                  </div>
                ) : (
                  <div className="mt-4 rounded-2xl bg-slate-50/80 p-5 ring-1 ring-slate-100">
                    <p className="whitespace-pre-line text-lg leading-8 text-slate-700">
                      {answer.answer}
                    </p>
                  </div>
                )}

                {/* Evidence */}
                {hasEvidence && (
                  <div className="mt-8 border-t border-slate-200 pt-8">

                    <div className="flex items-center justify-between gap-4">
                      <div className="flex items-center gap-3">
                        <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-emerald-50 text-emerald-700 shadow-sm">
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

                      <span className="hidden rounded-full border border-emerald-200 bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-700 sm:inline-flex">
                        Source verified
                      </span>
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
                            className="overflow-hidden rounded-2xl border border-slate-200 bg-slate-50/80 shadow-sm"
                          >
                            {project && (
                              <div className="p-5">

                                <div className="mb-5 flex items-start gap-3">
                                  <span className="mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-emerald-100 text-sm font-bold text-emerald-700">
                                    ✓
                                  </span>

                                  <div>
                                    <p className="text-xs font-bold uppercase tracking-wide text-emerald-700">
                                      Verified from official source
                                    </p>

                                    <p className="mt-1 font-semibold leading-6 text-slate-950">
                                      {project.project_description}
                                    </p>
                                  </div>
                                </div>

                                <div className="grid gap-3 sm:grid-cols-2">
                                  <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
                                    <p className="text-xs font-medium uppercase tracking-wide text-slate-500">
                                      2026 Budget
                                    </p>

                                    <p className="mt-1 text-xl font-bold text-slate-900">
                                      ₦
                                      {Number(
                                        project.original_budget
                                      ).toLocaleString("en-NG", {
                                        minimumFractionDigits: 2,
                                      })}
                                    </p>
                                  </div>

                                  <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
                                    <p className="text-xs font-medium uppercase tracking-wide text-slate-500">
                                      YTD Expenditure
                                    </p>

                                    <p className="mt-1 text-xl font-bold text-slate-900">
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
                              <div className="px-5 pb-5">
                                <p className="font-semibold text-slate-950">
                                  {item.metric}
                                </p>
                              </div>
                            )}

                            {source && (
                              <div className="border-t border-slate-200 bg-white p-5">
                                <div className="flex items-start gap-3">
                                  <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-blue-50 text-blue-700">
                                    📄
                                  </div>

                                  <div className="min-w-0">
                                    <p className="text-xs font-bold uppercase tracking-wide text-slate-500">
                                      Official source
                                    </p>

                                    <p className="mt-1 text-sm font-semibold leading-6 text-slate-900">
                                      {source.title}
                                    </p>
                                  </div>
                                </div>

                                <div className="mt-5 grid gap-4 text-sm sm:grid-cols-3">
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

                                    <p className="mt-1 font-medium text-slate-700">
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
                                  className="mt-5 inline-flex items-center rounded-xl bg-slate-950 px-5 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-blue-700"
                                >
                                  View official source
                                  <span className="ml-2">→</span>
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
            </div>
          </section>
        )}

        {/* Built for Lagos */}
        <section className="border-y border-white/70 bg-white/70 backdrop-blur-xl">
          <div className="mx-auto max-w-6xl px-6 py-14">

            <div className="mx-auto max-w-3xl text-center">
              <p className="text-xs font-bold uppercase tracking-[0.18em] text-blue-700">
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

            <div className="mt-10 grid gap-5 md:grid-cols-3">

              <div className="rounded-2xl border border-slate-200/90 bg-white/90 p-6 shadow-sm transition hover:-translate-y-1 hover:shadow-lg">
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

              <div className="rounded-2xl border border-slate-200/90 bg-white/90 p-6 shadow-sm transition hover:-translate-y-1 hover:shadow-lg">
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

              <div className="rounded-2xl border border-slate-200/90 bg-white/90 p-6 shadow-sm transition hover:-translate-y-1 hover:shadow-lg">
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

        {/* Verification */}
        <section className="bg-white/55 backdrop-blur-xl">
          <div className="mx-auto max-w-6xl px-6 py-14">

            <div className="mx-auto max-w-3xl text-center">
              <p className="text-xs font-bold uppercase tracking-[0.18em] text-blue-700">
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

            <div className="mt-10 grid gap-5 md:grid-cols-3">

              <div className="rounded-2xl border border-slate-200/90 bg-white/90 p-6 shadow-sm">
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

              <div className="rounded-2xl border border-slate-200/90 bg-white/90 p-6 shadow-sm">
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

              <div className="rounded-2xl border border-slate-200/90 bg-white/90 p-6 shadow-sm">
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

      {/* Footer */}
      <footer className="bg-slate-950/95 px-6 py-8 text-center text-sm text-slate-400 backdrop-blur-xl">
        <p className="font-medium text-slate-300">
          CivicPulse Lagos · Information you can trust
        </p>

        <p className="mt-2 text-xs text-slate-500">
          Current coverage: Lagos State public budget and project information
          for 2026, including Q2 2026 performance data.
        </p>
      </footer>
    </div>
  )
}

export default App