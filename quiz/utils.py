from .models import QuestionType, Answer

def check_answer(question, response):
    """
    Reusable logic for checking correctness, computing score, and collecting feedback.
    """
    is_correct = False
    awarded_score = 0
    feedback = []
    correct_ids = list(
        question.answers.filter(is_correct=True).values_list("id", flat=True)
    )

    if question.question_type == QuestionType.SINGLE_CHOICE:
        selected_answer = Answer.objects.filter(id=response[0], question=question).first()
        if selected_answer:
            is_correct = selected_answer.is_correct
            awarded_score = selected_answer.score if is_correct else 0
            feedback_text = selected_answer.feedback_if_correct if is_correct else selected_answer.feedback_if_wrong
            if feedback_text:
                feedback.append(feedback_text)

    elif question.question_type == QuestionType.MULTI_SELECT:
        selected_answers = Answer.objects.filter(id__in=response, question=question)
        selected_ids = [str(ans.id) for ans in selected_answers]
        is_correct = sorted(selected_ids) == sorted([str(cid) for cid in correct_ids])
        awarded_score = sum(a.score for a in selected_answers if a.id in correct_ids)
        for ans in selected_answers:
            fb = ans.feedback_if_correct if ans.is_correct else ans.feedback_if_wrong
            if fb:
                feedback.append(fb)

    elif question.question_type == QuestionType.FREE_TEXT:
        correct_answer = question.answers.first().text.strip().lower()
        is_correct = response.strip().lower() == correct_answer
        awarded_score = question.answers.first().score if is_correct else 0
        feedback_text = question.answers.first().feedback_if_correct if is_correct else question.answers.first().feedback_if_wrong
        if feedback_text:
            feedback.append(feedback_text)

    elif question.question_type == QuestionType.ORDER:
        correct_order = list(question.answers.order_by('order').values_list('id', flat=True))
        is_correct = response == list(correct_order)
        for idx, ans_id in enumerate(response):
            if ans_id == str(correct_order[idx]):
                answer = Answer.objects.get(id=ans_id)
                awarded_score += answer.score
                if answer.feedback_if_correct:
                    feedback.append(answer.feedback_if_correct)
            else:
                answer = Answer.objects.filter(id=ans_id).first()
                if answer and answer.feedback_if_wrong:
                    feedback.append(answer.feedback_if_wrong)

    elif question.question_type == QuestionType.MATCH:
        match_data = {a.text.strip(): a.match_pair.strip() for a in question.answers.all() if a.match_pair}
        is_correct = True
        for term, user_match in response.items():
            expected_match = match_data.get(term)
            answer = question.answers.filter(text=term).first()
            if expected_match and user_match.strip() == expected_match:
                awarded_score += answer.score
                if answer.feedback_if_correct:
                    feedback.append(answer.feedback_if_correct)
            else:
                is_correct = False
                if answer and answer.feedback_if_wrong:
                    feedback.append(answer.feedback_if_wrong)

    return is_correct, awarded_score, correct_ids, feedback
