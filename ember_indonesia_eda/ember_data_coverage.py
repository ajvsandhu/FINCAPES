import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import date

import pandas as pd

from ember_indonesia_eda import (
    DATASETS,
    OUTPUT_DIR,
    api_get,
    dictionary_sections,
    html_table,
    load_api_key,
    print_section,
    write_html_page,
)


FIRST_MONTHLY_YEAR = 1998


def fetch_all_entities(api_key, dataset):
    params = {"start_date": "1900"} if dataset.endswith("/yearly") else {}
    try:
        return api_get(api_key, dataset, params)
    except RuntimeError:
        if dataset.endswith("/yearly"):
            raise

    years = range(FIRST_MONTHLY_YEAR, date.today().year + 1)
    with ThreadPoolExecutor(max_workers=4) as pool:
        chunks = pool.map(
            lambda year: api_get(api_key, dataset, {"start_date": f"{year}-01", "end_date": f"{year}-12"}),
            years,
        )
        return pd.concat(list(chunks), ignore_index=True)


def summarise(dataset, data):
    date_length = 4 if dataset.endswith("/yearly") else 7
    data = data.assign(period=data["date"].str[:date_length])
    return (
        data.groupby("entity")
        .agg(
            entity_code=("entity_code", "first"),
            is_aggregate_entity=("is_aggregate_entity", "first"),
            rows=("period", "size"),
            first_date=("period", "min"),
            last_date=("period", "max"),
        )
        .reset_index()
        .assign(dataset=dataset)
    )


def main():
    api_key = load_api_key()
    if not api_key:
        sys.exit("Put EMBER_API_KEY=<your key> in the .env file next to this script.")
    OUTPUT_DIR.mkdir(exist_ok=True)

    summaries = []
    status = []
    for dataset in DATASETS:
        print(f"Fetching {dataset} for all countries...")
        try:
            data = fetch_all_entities(api_key, dataset)
        except RuntimeError as error:
            status.append({"dataset": dataset, "note": str(error)})
            continue
        summary = summarise(dataset, data)
        summaries.append(summary)
        status.append(
            {
                "dataset": dataset,
                "rows": len(data),
                "columns": data.shape[1],
                "entities": data["entity"].nunique(),
                "first_date": summary["first_date"].min(),
                "last_date": summary["last_date"].max(),
                "note": "",
            }
        )

    status = pd.DataFrame(status).reindex(
        columns=["dataset", "rows", "columns", "entities", "first_date", "last_date", "note"]
    )
    status = status.astype({"rows": "Int64", "columns": "Int64", "entities": "Int64"})
    details = pd.concat(summaries, ignore_index=True)
    entities = details.groupby("entity")[["entity_code", "is_aggregate_entity"]].first()
    details = details.drop(columns=["entity_code", "is_aggregate_entity"]).join(entities, on="entity")

    matrix = details.pivot(index="entity", columns="dataset", values="rows").reindex(columns=DATASETS)
    fetched = [dataset for dataset in DATASETS if dataset in details["dataset"].unique()]
    matrix[fetched] = matrix[fetched].fillna(0)
    matrix = entities.join(matrix.astype("Int64")).reset_index()
    matrix = matrix.sort_values(["is_aggregate_entity", "entity"]).reset_index(drop=True)
    details = details.sort_values(["is_aggregate_entity", "entity", "dataset"])[
        ["entity", "entity_code", "is_aggregate_entity", "dataset", "rows", "first_date", "last_date"]
    ]

    status.to_csv(OUTPUT_DIR / "ember_coverage_by_dataset.csv", index=False)
    matrix.to_csv(OUTPUT_DIR / "ember_coverage_rows_by_country.csv", index=False)
    details.to_csv(OUTPUT_DIR / "ember_coverage_date_ranges_by_country.csv", index=False)

    print_section("Datasets across all countries")
    print(status.to_string(index=False))
    countries = int((~matrix["is_aggregate_entity"].astype(bool)).sum())
    print(f"\n{countries} countries and {len(matrix) - countries} regions")

    sections = [
        f"<h2>Datasets across all countries and regions</h2>{html_table(status)}",
        f"<h2>Rows per dataset for each country and region ({len(matrix)} entities; "
        f"blank = dataset could not be fetched)</h2>{html_table(matrix)}",
        f"<h2>Date range per dataset for each country and region</h2>{html_table(details)}",
    ]
    sections += dictionary_sections()
    write_html_page("Ember API coverage for all countries", sections, "ember_data_coverage.html")


if __name__ == "__main__":
    main()
