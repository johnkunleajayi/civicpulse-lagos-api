from decimal import Decimal

from app.database.connection import SessionLocal
from app.database.models import BudgetSummaryDB, ProjectDB


SOURCE_ID = 1


projects = [
    {
        "administrative_code": "011101000100",
        "administrative_description": "Lagos State Public Procurement Agency",
        "project_description": "Integration and set-up of E-Procurement system in 10 MDAs",
        "budget_year": 2026,
        "original_budget": Decimal("680410575"),
        "q1_performance": Decimal("0"),
        "ytd_performance": Decimal("0"),
        "performance_percentage": Decimal("0"),
        "balance": Decimal("680410575"),
        "source_id": SOURCE_ID,
        "source_page": 56,
    },
    {
        "administrative_code": "011113600100",
        "administrative_description": "Fire Service",
        "project_description": "Rehabilitation of Fire Service Security and Control Centre",
        "budget_year": 2026,
        "original_budget": Decimal("1043767965"),
        "q1_performance": Decimal("200000000"),
        "ytd_performance": Decimal("200000000"),
        "performance_percentage": Decimal("19.2"),
        "balance": Decimal("843767965"),
        "source_id": SOURCE_ID,
        "source_page": 56,
    },
    {
        "administrative_code": "011113600100",
        "administrative_description": "Fire Service",
        "project_description": "FIRE AND RESCUE SERVICE RESPONSE UNIT (HEAVY DUTY VEHICLE EQUIPMENT)",
        "budget_year": 2026,
        "original_budget": Decimal("2100000000"),
        "q1_performance": Decimal("610641815.77"),
        "ytd_performance": Decimal("610641815.77"),
        "performance_percentage": Decimal("29.1"),
        "balance": Decimal("1489358184.23"),
        "source_id": SOURCE_ID,
        "source_page": 56,
    },
    {
        "administrative_code": "011200300100",
        "administrative_description": "State House of Assembly",
        "project_description": "Construction of Permanent Legislative Quarters for Honourable Members of the Assembly, processing of documentation and ancillary works",
        "budget_year": 2026,
        "original_budget": Decimal("35473450844.04"),
        "q1_performance": Decimal("6500000000"),
        "ytd_performance": Decimal("6500000000"),
        "performance_percentage": Decimal("18.3"),
        "balance": Decimal("28973450844.04"),
        "source_id": SOURCE_ID,
        "source_page": 56,
    },
    {
        "administrative_code": "021500100100",
        "administrative_description": "Ministry of Agriculture Hqtrs",
        "project_description": "Infrastructural Development for Lagos Wholesale Market Hub",
        "budget_year": 2026,
        "original_budget": Decimal("27029451098"),
        "q1_performance": Decimal("3433775012.31"),
        "ytd_performance": Decimal("3433775012.31"),
        "performance_percentage": Decimal("12.7"),
        "balance": Decimal("23595676085.69"),
        "source_id": SOURCE_ID,
        "source_page": 57,
    },
    {
        "administrative_code": "021500100100",
        "administrative_description": "Ministry of Agriculture Hqtrs",
        "project_description": "Lagos Wholesale Produce Hub (Variation in the Cost of Construction of Idi-Oro Mid level)",
        "budget_year": 2026,
        "original_budget": Decimal("28000000000"),
        "q1_performance": Decimal("681412100"),
        "ytd_performance": Decimal("681412100"),
        "performance_percentage": Decimal("2.4"),
        "balance": Decimal("27318587900"),
        "source_id": SOURCE_ID,
        "source_page": 58,
    },
    {
        "administrative_code": "022900100100",
        "administrative_description": "Ministry of Transportation",
        "project_description": "Traffic Improvement Scheme (Outstanding Projects, Gridlock Resolution and Traffic improvement)",
        "budget_year": 2026,
        "original_budget": Decimal("22339519440"),
        "q1_performance": Decimal("216084060.36"),
        "ytd_performance": Decimal("216084060.36"),
        "performance_percentage": Decimal("1.0"),
        "balance": Decimal("22123435379.64"),
        "source_id": SOURCE_ID,
        "source_page": 59,
    },
    {
        "administrative_code": "022905300100",
        "administrative_description": "Lagos State Metropolitan Area Transport",
        "project_description": "Construction of the 2nd Phase of Blueline Rail",
        "budget_year": 2026,
        "original_budget": Decimal("67356513550"),
        "q1_performance": Decimal("5019458955.87"),
        "ytd_performance": Decimal("5019458955.87"),
        "performance_percentage": Decimal("7.5"),
        "balance": Decimal("62337054594.13"),
        "source_id": SOURCE_ID,
        "source_page": 59,
    },
    {
        "administrative_code": "022905300100",
        "administrative_description": "Lagos State Metropolitan Area Transport",
        "project_description": "Provision of Rail Transportation Infrastructure for Blue line Project",
        "budget_year": 2026,
        "original_budget": Decimal("105254164670"),
        "q1_performance": Decimal("19475356712.05"),
        "ytd_performance": Decimal("19475356712.05"),
        "performance_percentage": Decimal("18.5"),
        "balance": Decimal("85778807957.95"),
        "source_id": SOURCE_ID,
        "source_page": 59,
    },
    {
        "administrative_code": "022905300100",
        "administrative_description": "Lagos State Metropolitan Area Transport",
        "project_description": "Rail Transportation Infrastructure for Red line Rail (Agbado-National Theartre)",
        "budget_year": 2026,
        "original_budget": Decimal("35084721560"),
        "q1_performance": Decimal("0"),
        "ytd_performance": Decimal("0"),
        "performance_percentage": Decimal("0"),
        "balance": Decimal("35084721560"),
        "source_id": SOURCE_ID,
        "source_page": 59,
    },
    {
        "administrative_code": "022905300100",
        "administrative_description": "Lagos State Metropolitan Area Transport",
        "project_description": "Rail Transportation Infrastructure from Marina to Okokomiako",
        "budget_year": 2026,
        "original_budget": Decimal("33154432340"),
        "q1_performance": Decimal("0"),
        "ytd_performance": Decimal("0"),
        "performance_percentage": Decimal("0"),
        "balance": Decimal("33154432340"),
        "source_id": SOURCE_ID,
        "source_page": 59,
    },
    {
        "administrative_code": "022905700100",
        "administrative_description": "Lagos State Waterways Authority",
        "project_description": "Development of Lagos waterways (Omi-Eko)",
        "budget_year": 2026,
        "original_budget": Decimal("148800000000"),
        "q1_performance": Decimal("823608059.49"),
        "ytd_performance": Decimal("823608059.49"),
        "performance_percentage": Decimal("0.6"),
        "balance": Decimal("147976391940.51"),
        "source_id": SOURCE_ID,
        "source_page": 59,
    },
    {
        "administrative_code": "023400200100",
        "administrative_description": "Office of Infrastructure",
        "project_description": "THE REHABILITATION/RE-CONSTRUCTION OF ETI-OSA LEKKI-EPE EXPRESSWAY",
        "budget_year": 2026,
        "original_budget": Decimal("125794759964"),
        "q1_performance": Decimal("78998894883.23"),
        "ytd_performance": Decimal("78998894883.23"),
        "performance_percentage": Decimal("62.8"),
        "balance": Decimal("46795865080.77"),
        "source_id": SOURCE_ID,
        "source_page": 60,
    },
    {
        "administrative_code": "023400200100",
        "administrative_description": "Office of Infrastructure",
        "project_description": "State Infrastructure Intervention Fund (SIIF) for Ikeja, Ikorodu, Lagos Island, Epe and Badagry",
        "budget_year": 2026,
        "original_budget": Decimal("40000000000"),
        "q1_performance": Decimal("11877180977.27"),
        "ytd_performance": Decimal("11877180977.27"),
        "performance_percentage": Decimal("29.7"),
        "balance": Decimal("28122819022.73"),
        "source_id": SOURCE_ID,
        "source_page": 61,
    },
    {
        "administrative_code": "052100100100",
        "administrative_description": "Ministry of Health",
        "project_description": "Construction of Ojo General Hospital",
        "budget_year": 2026,
        "original_budget": Decimal("19550984161"),
        "q1_performance": Decimal("5611938260.67"),
        "ytd_performance": Decimal("5611938260.67"),
        "performance_percentage": Decimal("28.7"),
        "balance": Decimal("13939045900.33"),
        "source_id": SOURCE_ID,
        "source_page": 68,
    },
    {
        "administrative_code": "052100100100",
        "administrative_description": "Ministry of Health",
        "project_description": "Construction of Shomolu General Hospital",
        "budget_year": 2026,
        "original_budget": Decimal("29834819479"),
        "q1_performance": Decimal("4886500000"),
        "ytd_performance": Decimal("4886500000"),
        "performance_percentage": Decimal("16.9"),
        "balance": Decimal("24048319479"),
        "source_id": SOURCE_ID,
        "source_page": 68,
    },
    {
        "administrative_code": "052100100100",
        "administrative_description": "Ministry of Health",
        "project_description": "Construction of New Massey Children Hospital (ISPO II)",
        "budget_year": 2026,
        "original_budget": Decimal("17185208697.56"),
        "q1_performance": Decimal("3232511415.53"),
        "ytd_performance": Decimal("3232511415.53"),
        "performance_percentage": Decimal("18.8"),
        "balance": Decimal("13952697282.03"),
        "source_id": SOURCE_ID,
        "source_page": 68,
    },
]


db = SessionLocal()

try:
    added = 0
    skipped = 0

    for project in projects:
        existing = (
            db.query(ProjectDB)
            .filter(
                ProjectDB.administrative_code
                == project["administrative_code"],
                ProjectDB.project_description
                == project["project_description"],
                ProjectDB.budget_year
                == project["budget_year"],
            )
            .first()
        )

        if existing:
            skipped += 1
            continue

        db.add(ProjectDB(**project))
        added += 1

    summary = BudgetSummaryDB(
        metric="Total Capital Expenditure",
        budget_year=2026,
        reporting_period="Q1 2026",
        original_budget=Decimal("2337805210325.31"),
        q1_performance=Decimal("340762383816.67"),
        performance_percentage=Decimal("14.6"),
        source_id=SOURCE_ID,
        source_page=56,
    )

    existing_summary = (
        db.query(BudgetSummaryDB)
        .filter(
            BudgetSummaryDB.metric == summary.metric,
            BudgetSummaryDB.budget_year == summary.budget_year,
            BudgetSummaryDB.reporting_period == summary.reporting_period,
        )
        .first()
    )

    if not existing_summary:
        db.add(summary)
        print("Successfully added capital expenditure summary.")
    else:
        print("Capital expenditure summary already exists.")

    db.commit()

    print(f"Successfully added {added} projects.")
    print(f"Skipped {skipped} existing projects.")

finally:
    db.close()