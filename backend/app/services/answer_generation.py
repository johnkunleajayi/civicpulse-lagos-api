from app.services.question_intent import extract_ranking_limit


def generate_summary_answer(question: str, summary: dict):
    if not summary:
        return "I could not find verified Lagos State budget summary data for Q1 2026."

    question_lower = question.lower()

    if "percentage" in question_lower or "percent" in question_lower:
        return (
            f"Lagos State spent "
            f"{summary['performance_percentage']:.1f}% of its 2026 capital budget "
            f"in Q1 2026."
        )

    if "capital budget" in question_lower:
        return (
            f"Lagos State's total 2026 capital budget is "
            f"₦{summary['original_budget']:,.2f}."
        )

    amount = summary["q1_performance"]

    return (
        f"Lagos State recorded ₦{amount:,.2f} in total capital expenditure "
        f"for Q1 2026, representing "
        f"{summary['performance_percentage']:.1f}% of the "
        f"₦{summary['original_budget']:,.2f} capital budget."
    )


def generate_ranking_answer(
    question: str,
    projects: list[dict],
    category: str | None = None,
):
    if not projects:
        if category:
            return (
                f"I could not find verified Lagos State {category} "
                f"project data for 2026."
            )

        return "I could not find verified Lagos State project data for 2026."

    limit = extract_ranking_limit(question)
    result_count = len(projects)

    if category:
        category_label = category

        if limit and result_count < limit:
            heading = (
                f"I found {result_count} verified Lagos State "
                f"{category_label} projects with the highest 2026 budgets:"
            )
        elif limit:
            heading = (
                f"The top {limit} Lagos State {category_label} "
                f"projects by 2026 budget are:"
            )
        else:
            heading = (
                f"The Lagos State {category_label} projects "
                f"with the highest 2026 budgets are:"
            )

    elif limit and result_count < limit:
        heading = (
            f"I found {result_count} verified Lagos State projects "
            f"with the highest 2026 budgets:"
        )

    elif limit:
        heading = (
            f"The top {limit} Lagos State projects by 2026 budget are:"
        )

    else:
        heading = (
            "The Lagos State projects with the highest 2026 budgets are:"
        )

    lines = [heading]

    for index, project in enumerate(projects, start=1):
        lines.append(
            f"{index}. {project['project_description']} — "
            f"₦{project['original_budget']:,.2f}"
        )

    return "\n".join(lines)


def generate_category_answer(
    question: str,
    category: str,
    projects: list[dict],
):
    if not projects:
        return (
            f"I could not find verified Lagos State {category} "
            f"project data for 2026."
        )

    total_budget = sum(
        project["original_budget"]
        for project in projects
        if project["original_budget"] is not None
    )

    total_spending = sum(
        project["ytd_performance"]
        for project in projects
        if project["ytd_performance"] is not None
    )

    question_lower = question.lower()

    if "percentage" in question_lower or "percent" in question_lower:
        percentage = (
            (total_spending / total_budget) * 100
            if total_budget
            else 0
        )

        return (
            f"Lagos State spent {percentage:.1f}% of the verified "
            f"{category} project budget in Q1 2026."
        )

    if (
        "spend" in question_lower
        or "spent" in question_lower
        or "spending" in question_lower
        or "expenditure" in question_lower
        or "expenditures" in question_lower
        or "money went into" in question_lower
        or "performance" in question_lower
    ):
        lines = [
            f"Lagos State recorded ₦{total_spending:,.2f} in "
            f"expenditure across {len(projects)} verified "
            f"{category} projects in Q1 2026.",
            "",
            "Project breakdown:",
        ]

        for index, project in enumerate(projects, start=1):
            spending = project["ytd_performance"] or 0

            lines.append(
                f"{index}. {project['project_description']} — "
                f"₦{spending:,.2f}"
            )

        return "\n".join(lines)

    if "project" in question_lower and (
        "which" in question_lower
        or "what" in question_lower
        or "list" in question_lower
    ):
        lines = [
            f"I found {len(projects)} verified Lagos State "
            f"{category} projects in the 2026 budget:"
        ]

        for index, project in enumerate(projects, start=1):
            lines.append(
                f"{index}. {project['project_description']} — "
                f"₦{project['original_budget']:,.2f}"
            )

        return "\n".join(lines)

    return (
        f"Lagos State has ₦{total_budget:,.2f} budgeted across "
        f"{len(projects)} verified {category} projects in 2026."
    )


def generate_answer(question: str, projects: list[dict]):
    if not projects:
        return "I could not find a verified Lagos State project matching your question."

    project = projects[0]
    question_lower = question.lower()
    project_name = project["project_description"]

    if "percentage" in question_lower or "percent" in question_lower:
        percentage = project["performance_percentage"]

        return (
            f"{project_name} has used "
            f"{percentage:.1f}% of its original 2026 budget "
            f"as reported for Q1 2026."
        )

    if "spent" in question_lower or "performance" in question_lower:
        amount = project["ytd_performance"]

        return (
            f"{project_name} has recorded "
            f"₦{amount:,.2f} in 2026 year-to-date expenditure "
            f"as reported for Q1 2026."
        )

    if "left" in question_lower or "balance" in question_lower:
        amount = project["balance"]

        return (
            f"The remaining balance for {project_name} "
            f"is ₦{amount:,.2f} against its original 2026 budget."
        )

    budget = project["original_budget"]

    return (
        f"{project_name} has an original 2026 budget "
        f"of ₦{budget:,.2f}."
    )