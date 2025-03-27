import spacy
import random
import re  # regex model for spacing issues

nlp = spacy.load("en_core_web_sm")  # load spacy nlp model

def enhance_sentence(sentence):
    """
    Enhance the sentence by replacing words with synonyms for variety and fixing spacing issues.
    """
    doc = nlp(sentence)
    new_sentence = []

    # replace words with synonyms for variety
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

    # removes extra spaces near punctuation
    improved_sentence = re.sub(r'\s([,.!?;’])', r'\1', improved_sentence)

    # fix spacing between integers and percentage sign (%)
    improved_sentence = re.sub(r'(\d+)\s%', r'\1%', improved_sentence)

    # capitalize first letter properly
    improved_sentence = improved_sentence[0].upper() + improved_sentence[1:]

    return improved_sentence

def generate_feedback(criteria_list):
    """
    Generates structured feedback based on the given criteria list.
    """
    feedback = []

    # classify scores
    high = [(entry["criterion"].capitalize(), entry["score"], entry["justification"]) for entry in criteria_list if entry["score"] >= 70]
    mid = [(entry["criterion"].capitalize(), entry["score"], entry["justification"]) for entry in criteria_list if 40 <= entry["score"] < 70]
    low = [(entry["criterion"].capitalize(), entry["score"], entry["justification"]) for entry in criteria_list if entry["score"] < 40]

    # majority rule to determine feedback structure
    if len(high) >= len(mid) + len(low):
        sections = [high, mid, low]
    else:
        sections = [low, mid, high]

    # feedback templates
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

    # different connectors
    contrastive_connectors = ["However,", "On the other hand,", "That being said,", "Nevertheless,", "Yet,", "Despite this,"]
    additive_connectors = ["Moreover,", "Furthermore,", "Additionally,", "Also,", "Not to mention,", "What's more,"]

    # shuffle transition words to ensure variety and not have repeated words
    random.shuffle(contrastive_connectors)
    random.shuffle(additive_connectors)

    last_category = None

    for section in sections:
        if not section:
            continue

        category = "high" if section == high else "mid" if section == mid else "low"

        # contrastive connector if transitioning to a different category
        if last_category and last_category != category:
            if contrastive_connectors:
                feedback.append(contrastive_connectors.pop(0))  
            else:
                random.shuffle(contrastive_connectors)
                feedback.append(contrastive_connectors.pop(0))

        # generate feedback
        for i, (criterion, score, justification) in enumerate(section):
            # picks a shuffled sentence
            template = templates[category][i % len(templates[category])]  
            # use spacy to refine
            improved_sentence = enhance_sentence(template.format(criterion=criterion, score=score))  

            # append justification naturally
            if justification:
                improved_sentence += f" {justification}"

            feedback.append(improved_sentence)

            # add additive connector for same section
            if i < len(section) - 1:
                if additive_connectors:
                    feedback.append(additive_connectors.pop(0))  
                else:
                    random.shuffle(additive_connectors)
                    feedback.append(additive_connectors.pop(0))

        # update last category
        last_category = category  

    return " ".join(feedback)

