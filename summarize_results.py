import pandas as pd

# Load the results
df = pd.read_csv(r"E:\signal-safe\AAPL_top_matches.csv")

# Convert Day column to datetime
df['Day'] = pd.to_datetime(df['Day'], dayfirst=True)

# Group by Day and get top 5 scores
summary = (
    df.sort_values(['Day', 'Score'], ascending=[True, False])
      .groupby('Day')
      .head(5)
)

# Print summary neatly
for day, group in summary.groupby('Day'):
    print(f"\n=== {day.date()} ===")
    for _, row in group.iterrows():
        print(f"- Score: {row['Score']:.3f} | {row['Headline'][:80]}... (Source: {row['Source']})")

# Optional: save summary to a new CSV
summary.to_csv(r"E:\signal-safe\AAPL_summary.csv", index=False)
print("\nSummary saved to AAPL_summary.csv")
