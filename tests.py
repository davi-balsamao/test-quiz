import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct


def test_new_question_has_default_settings_and_no_choices():
    question = Question(title='Qual e a capital de Minas Gerais?')

    assert question.points == 1
    assert question.max_selections == 1
    assert question.choices == []


def test_question_accepts_title_with_200_characters():
    title = 'a' * 200

    question = Question(title=title)

    assert question.title == title


def test_question_rejects_points_below_minimum():
    with pytest.raises(Exception, match='^Points must be between 1 and 100$'):
        Question(title='q1', points=0)


def test_question_rejects_points_above_maximum():
    with pytest.raises(Exception, match='^Points must be between 1 and 100$'):
        Question(title='q1', points=101)


def test_empty_choice_is_rejected_without_changing_question():
    question = Question(title='q1')

    with pytest.raises(Exception, match='^Text cannot be empty$'):
        question.add_choice('')

    assert question.choices == []


def test_choice_longer_than_100_characters_is_rejected():
    question = Question(title='q1')

    with pytest.raises(Exception, match='^Text cannot be longer than 100 characters$'):
        question.add_choice('a' * 101)

    assert question.choices == []


def test_question_accepts_correct_choice_with_100_characters():
    question = Question(title='q1')
    text = 'a' * 100

    choice = question.add_choice(text, is_correct=True)

    assert question.choices == [choice]
    assert choice.text == text
    assert choice.is_correct


def test_removing_choice_preserves_other_choices():
    question = Question(title='q1')
    first = question.add_choice('a')
    second = question.add_choice('b')

    question.remove_choice_by_id(first.id)

    assert question.choices == [second]


def test_removing_unknown_choice_is_rejected_without_changing_question():
    question = Question(title='q1')
    choice = question.add_choice('a')
    unknown_id = choice.id + 1

    with pytest.raises(Exception, match=f'^Invalid choice id {unknown_id}$'):
        question.remove_choice_by_id(unknown_id)

    assert question.choices == [choice]


def test_removing_all_choices_leaves_question_empty():
    question = Question(title='q1')
    question.add_choice('a', is_correct=True)
    question.add_choice('b')

    question.remove_all_choices()

    assert question.choices == []
