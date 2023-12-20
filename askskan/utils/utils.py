import re
from app.configurations.development.settings import SCHEMA_COLS_PATTERN


def extract_pattern(pattern, text):
    """
    Extracts the pattern from the text.
    """
    return re.search(pattern, text, re.DOTALL)


def pretty_print_docs(docs):
    pattern = SCHEMA_COLS_PATTERN
    print(
        [
            extract_pattern(pattern, d.page_content).group(1).strip()
            for i, d in enumerate(docs)
        ]
    )


def get_columns_from_docs(docs):
    pattern = SCHEMA_COLS_PATTERN
    embed_docs = [
        extract_pattern(pattern, d.page_content).group(1).strip()
        for i, d in enumerate(docs)
    ]
    return embed_docs


def get_embeds_with_scores(embeds_with_similarities):
    embeds = []
    sim_scores = []
    embed_ranks = []
    embed_rank_sim = []
    for rank, embed_with_similarity in enumerate(embeds_with_similarities):
        embeds.append(embed_with_similarity[0])
        sim_scores.append(embed_with_similarity[1])
        embed_ranks.append(rank + 1)
        embed_rank_sim.append((rank + 1, embed_with_similarity[1]))
    return embeds, embed_ranks, sim_scores, embed_rank_sim
