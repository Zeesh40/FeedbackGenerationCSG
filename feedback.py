import spacy
import random
import re

nlp = spacy.load("en_core_web_sm")

def enhance_sentence(sentence):
    doc = nlp(sentence)
    new_sentence = []

    for token in doc:
        word = token.text
        if word.lower() in ["superb", "good", "fantastic", "remarkable"]:
            word = random.choice(["magnificent", "great", "brilliant"])
        elif word.lower() in ["improve", "refine", "focus"]:
            word = random.choice(["enhance", "strengthen"])
        elif word.lower() in ["performance", "skills", "abilities"]:
            word = random.choice(["capabilities", "expertise", "competence"])
        new_sentence.append(word)

    improved_sentence = " ".join(new_sentence)
    improved_sentence = re.sub(r'\s([,.!?;’])', r'\1', improved_sentence)
    improved_sentence = re.sub(r'(\d+)\s%', r'\1%', improved_sentence)
    improved_sentence = improved_sentence[0].upper() + improved_sentence[1:]
    improved_sentence = re.sub(r"\b([A-Za-z]+)\s+'(re|ve|ll|d|m|s|t)\b", r"\1'\2", improved_sentence)
    improved_sentence = re.sub(r"\b(well)\s+(detailed)\b", r"\1-\2", improved_sentence)

    return improved_sentence


def generate_feedback(criteria_data, order="adaptive"):
    standalone_starters = [
        "In particular", "Specifically", "Notably", "For instance", "To illustrate"
    ]
    flowing_starters = [
        "This is evident in how", "This was demonstrated by how", "This was reflected in how",
        "As highlighted by how"
    ]

    templates = {
        "high": [
            "You demonstrated superb abilities in {criterion}, earning {score}%.",
            "An outstanding score of {score}% in {criterion} highlights your remarkable grasp of the material.",
            "You did a great job for {criterion}, with a score of {score}%.",
            "You excelled in {criterion} with {score}% as your score.",
            "Your {criterion} score of {score}% highlights a strong understanding and performance.",
            "Great performance in {criterion}, with a score of {score}%.",
        ],
        "mid": [
            "In {criterion}, your score of {score}% demonstrates competence, though refining this further could benefit you.",
            "{criterion} was handled fairly well with a {score}% score, yet there’s definitely space to enhance your performance.",
            "Your performance in {criterion} was decent at {score}%, but there seems to be some room for improvement.",
            "A score of {score}% in {criterion} shows a solid grasp, yet there’s potential for growth and development.",
            "You're doing fairly well in {criterion}, scoring {score}%.",
            "A score of {score}% in {criterion} shows you’re on the right track, but there’s clear potential to improve.",
            "Your {criterion} result of {score}% reflects solid effort, but greater consistency would strengthen your overall performance.",
        ],
        "low": [
            "Your {criterion} score of {score}% shows that this is an area worth strengthening.",
            "A score of {score}% in {criterion} reflects a need to further develop your capabilities in this area.",
            "Your score in {criterion} was {score}%, indicating an area to focus.",
            "Scoring {score}% in {criterion} suggests the need for more attention and practice.",
            "There is room for improvement in {criterion}, as your score came out as {score}%.",
        ]
    }

    for cat in templates:
        random.shuffle(templates[cat])

    major_contrast = ["However,", "On the other hand,", "Despite this,", "Nevertheless,", "Alternatively,"]
    mild_contrast = ["That being said,", "Even so,", "Still,", "At the same time,"]
    additive_connectors = ["Moreover,", "Furthermore,", "Additionally,", "Also,", "Not to mention,", "What's more,"]

    random.shuffle(major_contrast)
    random.shuffle(mild_contrast)
    random.shuffle(additive_connectors)

    high = [(c["criterion"].capitalize(), c["score"]) for c in criteria_data if c["score"] >= 70]
    mid = [(c["criterion"].capitalize(), c["score"]) for c in criteria_data if 40 <= c["score"] < 70]
    low = [(c["criterion"].capitalize(), c["score"]) for c in criteria_data if c["score"] < 40]

    all_scores = [c["score"] for c in criteria_data]
    average_score = sum(all_scores) / len(all_scores)

    if order == "low-mid-high":
        sections = [low, mid, high]
    elif order == "high-mid-low":
        sections = [high, mid, low]
    else:
        sections = [high, mid, low] if average_score >= 50 else [low, mid, high]

    for section in sections:
        random.shuffle(section)

    def get_contrast_type(prev_cat, curr_cat):
        if (prev_cat == "low" and curr_cat == "high") or (prev_cat == "high" and curr_cat == "low"):
            return "major"
        return "mild"

    last_category = None
    connector_buffer = None
    all_sentences = []

    for section in sections:
        if not section:
            continue

        if set(section) == set(high):
            category = "high"
        elif set(section) == set(mid):
            category = "mid"
        else:
            category = "low"

        if last_category and last_category != category:
            contrast_type = get_contrast_type(last_category, category)
            if contrast_type == "major":
                connector_buffer = major_contrast.pop(0) if major_contrast else "However,"
            else:
                connector_buffer = mild_contrast.pop(0) if mild_contrast else "That being said,"

        for i, (criterion, score) in enumerate(section):
            template = templates[category][i % len(templates[category])]
            sentence = template.format(criterion=criterion, score=score)
            enhanced = enhance_sentence(sentence)

            if connector_buffer:
                enhanced = f"{connector_buffer} {enhanced[0].lower() + enhanced[1:]}"
                connector_buffer = None

            justification_text = next(
                (c.get("justification", "").strip() for c in criteria_data if c["criterion"].lower() == criterion.lower()),
                ""
            )

            if justification_text:
                if random.random() < 0.5:
                    starter = random.choice(standalone_starters) + ","
                else:
                    starter = random.choice(flowing_starters)
                justification_text = justification_text.strip(" .!?")
                justification_text = justification_text[0].lower() + justification_text[1:] if justification_text else ""
                justification_sentence = f"{starter} {justification_text}."
                enhanced += f" {justification_sentence}"


            all_sentences.append((category, enhanced))

            if i < len(section) - 1 and random.random() > 0.5:
                connector_buffer = additive_connectors.pop(0) if additive_connectors else "Also,"


        last_category = category

    # Separate sentences into strength/improvement groups
    improvement_sentences = [s for cat, s in all_sentences if cat in ["low", "mid"]]
    strength_sentences = [s for cat, s in all_sentences if cat == "high"]

    # Group paragraphs based on selected order
    paragraphs = []
    if order == "low-mid-high" or (order == "adaptive" and average_score < 50):
        if improvement_sentences:
            paragraphs.append(" ".join(improvement_sentences))
        if strength_sentences:
            paragraphs.append(" ".join(strength_sentences))
    else:
        if strength_sentences:
            paragraphs.append(" ".join(strength_sentences))
        if improvement_sentences:
            paragraphs.append(" ".join(improvement_sentences))


    # Add 'wrap-up' phrasing'
    if paragraphs:
        last_paragraph = paragraphs[-1].strip()
        sentences = re.split(r'(?<=[.!?]) +', last_paragraph)

        # Filter only appropriate sentences
        real_sentences = [
            s for s in sentences
            if not s.strip().startswith(
                tuple(["In particular", "Specifically", "Notably", "To illustrate", "For instance", "Moreover", "Furthermore", "Additionally", "Also", "What's more"])
            ) and not s.strip().startswith(("Lastly", "Finally"))
        ]

        if len(real_sentences) > 1:
            # Loop backwards to find the last actual feedback sentence
            for i in range(len(sentences) - 1, -1, -1):
                sentence = sentences[i].strip()
                if sentence and sentence not in real_sentences:
                    continue
                if not sentence.startswith(("Lastly", "Finally")):
                    sentence = re.sub(
                        r"^(However,|On the other hand,|Despite this,|Nevertheless,|That being said,|Even so,|Still,|At the same time,)\s*",
                        "",
                        sentence,
                        flags=re.IGNORECASE
                    )
                    intro = random.choice(["Lastly,", "Finally,"])
                    sentence = f"{intro} {sentence[0].lower() + sentence[1:]}" if sentence[0].isupper() else f"{intro} {sentence}"
                    sentences[i] = sentence
                    break

            paragraphs[-1] = " ".join(sentences)


    return "\n\n".join(paragraphs)


