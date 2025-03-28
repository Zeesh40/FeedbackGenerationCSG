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

    # Fix spacing near punctuation
    improved_sentence = re.sub(r'\s([,.!?;’])', r'\1', improved_sentence)
    improved_sentence = re.sub(r'(\d+)\s%', r'\1%', improved_sentence)
    improved_sentence = improved_sentence[0].upper() + improved_sentence[1:]

    # Contraction fix
    improved_sentence = re.sub(r"\b([A-Za-z]+)\s+'(re|ve|ll|d|m|s|t)\b", r"\1'\2", improved_sentence)

    # Common phrase cleanup
    improved_sentence = re.sub(r"\b(well)\s+(detailed)\b", r"\1-\2", improved_sentence)

    return improved_sentence


def generate_feedback(criteria_data):
    feedback = []

    # Starters for justification
    starters = ["In particular", "Specifically", "For instance", "To illustrate", "Notably"]
    random.shuffle(starters)

    # Feedback templates
    templates = {
        "high": [
            "You did a great job for {criterion}, with a score of {score}%.",
            "You excelled in {criterion} with {score}% as your score.",
            "Your {criterion} score of {score}% highlights a strong understanding and performance.",
            "Great performance in {criterion}, with a score of {score}%."
        ],
        "mid": [
            "Your performance in {criterion} was decent at {score}%, but there seems to be some room for improvement.",
            "A score of {score}% in {criterion} shows a solid grasp, yet there’s potential for growth and development.",
            "You're doing fairly well in {criterion}, scoring {score}%."
        ],
        "low": [
            "Your score in {criterion} was {score}%, indicating an area to focus.",
            "Scoring {score}% in {criterion} suggests the need for more attention and practice.",
            "There is room for improvement in {criterion}, as your score came out as {score}%."
        ]
    }

    for cat in templates:
        random.shuffle(templates[cat])

    # Transition words
    major_contrast = ["However,", "On the other hand,", "Despite this,", "Nevertheless,"]
    mild_contrast = ["That being said,", "Even so,", "Still,", "At the same time,"]
    additive_connectors = ["Moreover,", "Furthermore,", "Additionally,", "Also,", "Not to mention,", "What's more,"]

    random.shuffle(major_contrast)
    random.shuffle(mild_contrast)
    random.shuffle(additive_connectors)

    # Grouping criteria
    high = [(c["criterion"].capitalize(), c["score"]) for c in criteria_data if c["score"] >= 70]
    mid = [(c["criterion"].capitalize(), c["score"]) for c in criteria_data if 40 <= c["score"] < 70]
    low = [(c["criterion"].capitalize(), c["score"]) for c in criteria_data if c["score"] < 40]

    # Average-based ordering
    all_scores = [c["score"] for c in criteria_data]
    average_score = sum(all_scores) / len(all_scores)

    if average_score >= 50:
        sections = [high, mid, low]
    else:
        sections = [low, mid, high]

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

        category = "high" if section == high else "mid" if section == mid else "low"

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
                starter = starters.pop(0).capitalize() if starters else "In particular"
                justification_text = justification_text.strip(" .!?")
                justification_sentence = f"{starter}, {justification_text}."
                enhanced += f" {justification_sentence}"

            all_sentences.append((category, enhanced))

            if i < len(section) - 1 and random.random() > 0.5:
                connector = additive_connectors.pop(0) if additive_connectors else "Also,"
                all_sentences.append((category, connector))

        last_category = category

    # Group into paragraphs
    improvement_sentences = []
    strength_sentences = []

    for idx, (cat, sentence) in enumerate(all_sentences):
        if cat in ["low", "mid"]:
            improvement_sentences.append(sentence)
        else:
            strength_sentences.append(sentence)

    # Add "Lastly," to final strength sentence
    if strength_sentences:
        last = strength_sentences[-1]
        if not last.strip().startswith(("Lastly", "Finally")):
            strength_sentences[-1] = f"Lastly, {last[0].lower() + last[1:]}" if last[0].isupper() else f"Lastly, {last}"

    paragraphs = []
    if improvement_sentences:
        paragraphs.append(" ".join(improvement_sentences))
    if strength_sentences:
        paragraphs.append(" ".join(strength_sentences))

    return "\n\n".join(paragraphs)
