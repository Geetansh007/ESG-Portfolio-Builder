def calculate_esg_score(row, preference):
    if preference == "Environmental":
        return (0.6 * row["E_score"] +
                0.2 * row["S_score"] +
                0.2 * row["G_score"])
    elif preference == "Social":
        return (0.2 * row["E_score"] +
                0.6 * row["S_score"] +
                0.2 * row["G_score"])
    elif preference == "Governance":
        return (0.2 * row["E_score"] +
                0.2 * row["S_score"] +
                0.6 * row["G_score"])
    else:
        return (row["E_score"] +
                row["S_score"] +
                row["G_score"]) / 3
