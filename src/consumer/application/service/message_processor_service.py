from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

knowledge_base = {
    "O que é Python?": "Python é uma linguagem de programação de alto nível, conhecida por sua simplicidade e legibilidade.",
    "Para que serve o machine learning?": "Machine learning é usado para criar modelos que aprendem com dados e fazem previsões.",
    "O que é inteligência artificial?": "Inteligência artificial é a simulação de processos de inteligência humana por máquinas."
}

vectorizer = TfidfVectorizer()
questions = list(knowledge_base.keys())
tfidf_matrix = vectorizer.fit_transform(questions)

def get_answer(question: str) -> str:
    question_tfidf = vectorizer.transform([question])
    similarities = cosine_similarity(question_tfidf, tfidf_matrix)
    max_similarity = similarities.max()
    best_match_index = similarities.argmax()
    if max_similarity > 0.3:
        return list(knowledge_base.values())[best_match_index]
    return "Desculpe, não sei responder essa pergunta."