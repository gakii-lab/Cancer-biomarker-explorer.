import csv

def load_biomarkers(input_file='biomarkers.csv'):
    with open(input_file, newline='', encoding='utf-8') as csvfile:
        return list(csv.DictReader(csvfile))

def filter_biomarkers(data, cancer=None, category=None, method=None):
    results = []
    for row in data: 
        if cancer and cancer.lower() not in row['Cancer Type'].lower():
            continue
        if category and category.lower() not in row['Biomarker Category'].lower():
            continue
        if method and method.lower() not in row['Testing Method'].lower():
            continue
        results.append(row)
    return results

def display_biomarkers(results):
    print(f"\n🔬 {len(results)} biomarkers found:\n")
    for b in results:
        print(f"- {b['Biomarker']} ({b['Gene/Symbol']}): {b['Biomarker Category']}, via {b['Testing Method']} → {b['Clinical Interpretation']} | Therapy: {b['Associated Therapy']}")

def export_results(results, output_file='filtered_biomarkers.csv'):
    if not results:
        print("No data to export.")
        return
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    print(f"\n📁 Results saved to {output_file}")

def summarize_categories(results):
    summary = {}
    for r in results:
        key = r['Biomarker Category']
        summary[key] = summary.get(key, 0) + 1
    print("\n📊 Category Summary:")
    for k, v in summary.items():
        print(f"  - {k}: {v} marker(s)")

if __name__ == "__main__":
    data = load_biomarkers()

    print("🔎 Cancer Biomarker Explorer")
    cancer = input("Filter by Cancer Type (or leave blank): ")
    category = input("Filter by Biomarker Category (e.g. Predictive, Diagnostic): ")
    method = input("Filter by Testing Method (e.g. IHC, PCR): ")

    filtered = filter_biomarkers(data, cancer, category, method)
    display_biomarkers(filtered)
    summarize_categories(filtered)

    save = input("\n💾 Export results to CSV? (y/n): ")
    if save.lower() == 'y':
        export_results(filtered)
