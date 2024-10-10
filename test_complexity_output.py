from textblob_complexity import TextComplexityScorer

# Example text
text = ("The quick brown fox jumps over the lazy dog. Hoever,"
        " the dog was not amused and decided to take a nap instead.")


# Initialize the TextComplexityScorer with your text
scorer = TextComplexityScorer(text)

# Compute and print the various complexity scores
print(f"ARI (Automated Readability Index): {scorer.ari()}")
print(f"Flesch-Kincaid Grade Level: {scorer.flesch_kincaid_grade()}")
print(f"Gunning Fog Index: {scorer.gunning_fog()}")
print(f"SMOG Index: {scorer.smog_index()}")
print(f"All Scores: {scorer.compute_scores()}")
