"""Example usage for the outlier utilities."""

from outliers import detect_outliers, modified_z_scores


def main() -> None:
    values = [10, 12, 12, 13, 12, 11, 12, 100]
    scores = modified_z_scores(values)
    flags = detect_outliers(values)

    print("Values:", values)
    print("Modified z-scores:", [round(score, 2) for score in scores])
    print("Outlier flags:", flags)


if __name__ == "__main__":
    main()
