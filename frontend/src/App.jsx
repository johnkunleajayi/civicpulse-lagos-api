import { useState } from "react"

const API_URL = "https://civicpulse-lagos-api.onrender.com"

function App() {
  const [question, setQuestion] = useState("")
  const [answer, setAnswer] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  const askCivicPulse = async () => {
    if (!question.trim()) {
      return
    }

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
          question: question.trim(),
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

  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      askCivicPulse()
    }
  }

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-5">
          <div>
            <h1 className="text-2xl font-bold tracking-tight text-slate-950">
              CivicPulse Lagos
            </h1>
            <p className="text-sm text-slate-500">
              Know. Verify. Act.
            </p>
          </div>

          <div className="hidden items-center gap-2 text-sm text-slate-500 sm:flex">
            <span className="h-2 w-2 rounded-full bg-emerald-500"></span>
            Verified civic information
          </div>
        </div>
      </header>

      <main>
        <section className="mx-auto max-w-4xl px-6 pb-16 pt-20 text-center sm:pt-28">
          <div className="mb-5 inline-flex items-center rounded-full border border-blue-200 bg-blue-50 px-4 py-2 text-sm font-medium text-blue-700">
            Lagos public information, made understandable
          </div>

          <h2 className="text-4xl font-bold tracking-tight text-slate-950 sm:text-6xl">
            Public information shouldn't require a government insider to
            understand.
          </h2>

          <p className="mx-auto mt-6 max-w-2xl text-lg leading-8 text-slate-600">
            Ask questions about Lagos State public spending and projects.
            CivicPulse finds verified government information and shows you
            where the answer came from.
          </p>

          <div className="mx-auto mt-10 max-w-3xl rounded-2xl border border-slate-200 bg-white p-3 shadow-sm">
            <div className="flex flex-col gap-3 sm:flex-row">
              <input
                type="text"
                value={question}
                onChange={(event) => setQuestion(event.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Ask about Lagos public spending..."
                className="min-h-14 flex-1 rounded-xl border border-slate-200 bg-slate-50 px-5 text-base text-slate-900 outline-none transition focus:border-blue-500 focus:bg-white focus:ring-2 focus:ring-blue-100"
              />

              <button
                type="button"
                onClick={askCivicPulse}
                disabled={loading}
                className="min-h-14 rounded-xl bg-slate-950 px-7 font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-60"
              >
                {loading ? "Checking..." : "Ask CivicPulse"}
              </button>
            </div>
          </div>

          <div className="mt-5 flex flex-wrap justify-center gap-2">
            <button
              type="button"
              onClick={() =>
                setQuestion(
                  "How much did Lagos spend on rail projects in Q1 2026?"
                )
              }
              className="rounded-full border border-slate-200 bg-white px-4 py-2 text-sm text-slate-600 transition hover:border-blue-300 hover:text-blue-700"
            >
              Rail spending
            </button>

            <button
              type="button"
              onClick={() =>
                setQuestion(
                  "What percentage of the health project budget was spent in Q1 2026?"
                )
              }
              className="rounded-full border border-slate-200 bg-white px-4 py-2 text-sm text-slate-600 transition hover:border-blue-300 hover:text-blue-700"
            >
              Health spending
            </button>

            <button
              type="button"
              onClick={() =>
                setQuestion(
                  "What are the largest Lagos State projects by 2026 budget?"
                )
              }
              className="rounded-full border border-slate-200 bg-white px-4 py-2 text-sm text-slate-600 transition hover:border-blue-300 hover:text-blue-700"
            >
              Largest projects
            </button>
          </div>
        </section>

        {error && (
          <section className="mx-auto max-w-4xl px-6 pb-12">
            <div className="rounded-2xl border border-red-200 bg-red-50 p-6 text-red-700">
              <p className="font-semibold">Unable to answer</p>
              <p className="mt-1 text-sm">{error}</p>
            </div>
          </section>
        )}

        {answer && (
          <section className="mx-auto max-w-4xl px-6 pb-16">
            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8">
              <div className="mb-6 flex items-center gap-2">
                <span className="flex h-8 w-8 items-center justify-center rounded-full bg-emerald-100 font-semibold text-emerald-700">
                  ✓
                </span>
                <span className="text-sm font-semibold uppercase tracking-wide text-emerald-700">
                  Verified answer
                </span>
              </div>

              <h3 className="text-xl font-semibold text-slate-950">
                Answer
              </h3>

              <p className="mt-3 whitespace-pre-line text-lg leading-8 text-slate-700">
                {answer.answer}
              </p>

              {answer.evidence && answer.evidence.length > 0 && (
                <div className="mt-8 border-t border-slate-200 pt-8">
                  <div className="flex items-center justify-between gap-4">
                    <div>
                      <h3 className="text-xl font-semibold text-slate-950">
                        Evidence
                      </h3>
                      <p className="mt-1 text-sm text-slate-500">
                        Official information used to support this answer
                      </p>
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
                                    Q1 Expenditure
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

        <section className="border-y border-slate-200 bg-white">
          <div className="mx-auto grid max-w-6xl gap-8 px-6 py-14 md:grid-cols-3">
            <div>
              <div className="mb-4 flex h-11 w-11 items-center justify-center rounded-xl bg-blue-50 text-xl">
                🔎
              </div>
              <h3 className="text-lg font-semibold text-slate-950">
                Ask
              </h3>
              <p className="mt-2 leading-7 text-slate-600">
                Ask straightforward questions about Lagos State budgets and
                public projects.
              </p>
            </div>

            <div>
              <div className="mb-4 flex h-11 w-11 items-center justify-center rounded-xl bg-emerald-50 text-xl">
                ✓
              </div>
              <h3 className="text-lg font-semibold text-slate-950">
                Verify
              </h3>
              <p className="mt-2 leading-7 text-slate-600">
                Answers are grounded in published government documents and
                official sources.
              </p>
            </div>

            <div>
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
        </section>

        <section className="bg-slate-50">
          <div className="mx-auto max-w-6xl px-6 py-16">
            <div className="mx-auto max-w-3xl text-center">
              <p className="text-sm font-semibold uppercase tracking-wide text-blue-700">
                How CivicPulse verifies information
              </p>

              <h2 className="mt-3 text-3xl font-bold tracking-tight text-slate-950 sm:text-4xl">
                Don't just trust the answer. Check the evidence.
              </h2>

              <p className="mt-4 text-lg leading-8 text-slate-600">
                CivicPulse is designed to make the path from public data to
                civic understanding visible.
              </p>
            </div>

            <div className="mt-10 grid gap-6 md:grid-cols-3">
              <div className="rounded-2xl border border-slate-200 bg-white p-6">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-blue-50 text-xl font-bold text-blue-700">
                  1
                </div>

                <h3 className="mt-5 text-lg font-semibold text-slate-950">
                  Find official sources
                </h3>

                <p className="mt-2 leading-7 text-slate-600">
                  CivicPulse uses published government information as the
                  foundation for its answers.
                </p>
              </div>

              <div className="rounded-2xl border border-slate-200 bg-white p-6">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-emerald-50 text-xl font-bold text-emerald-700">
                  2
                </div>

                <h3 className="mt-5 text-lg font-semibold text-slate-950">
                  Match the evidence
                </h3>

                <p className="mt-2 leading-7 text-slate-600">
                  Relevant budget and project records are matched to the
                  citizen's question before an answer is presented.
                </p>
              </div>

              <div className="rounded-2xl border border-slate-200 bg-white p-6">
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

      <footer className="bg-slate-950 px-6 py-8 text-center text-sm text-slate-400">
        CivicPulse Lagos · Information you can trust
      </footer>
    </div>
  )
}

export default App