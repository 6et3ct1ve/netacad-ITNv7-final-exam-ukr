import os
import json
import random
from PIL import Image


# Функція для отримання шляху до зображення
def get_image_path(image_name):
    image_folder = "NetPhotos"  # Назва нової папки з зображеннями
    image_path = os.path.join( image_folder, image_name )  # Створюємо повний шлях до файлу
    if os.path.exists( image_path ):
        return image_path
    else:
        return None


# Завантажуємо питання з JSON файлу
def load_questions_from_json(file_path):
    try:
        with open( file_path, "r", encoding="utf-8" ) as file:
            questions = json.load( file )
        return questions
    except Exception as e:
        print( f"Не вдалося завантажити питання з файлу: {e}" )
        return []


# Функція для запуску тесту
def run_exam():
    # Вітання на початку тесту
    print( """
********************************************
**    Ласкаво просимо до симулятора тесту!    **
**  Ваше завдання — відповісти на всі питання,   **
**  обрати правильні варіанти та отримати результат. **
********************************************

    Починаємо тестування!
    """ )

    # Завантажуємо питання
    questions = load_questions_from_json( "NetExam_data.json" )
    if not questions:
        return  # Якщо питання не вдалося завантажити, припиняємо виконання

    # Перетасовуємо питання в випадковому порядку
    random.shuffle(questions)

    correct_answers = 0
    total_questions = len( questions )

    for idx, q in enumerate( questions, start=1 ):  # Додаємо змінну для нумерації питань
        print( f"\nПитання {idx}: {q['question']}" )  # Виводимо номер питання перед текстом питання

        # Перевірка наявності зображення для питання
        if "image" in q:
            image_name = q["image"]  # Отримуємо ім'я файлу з зображенням
            image_path = get_image_path( image_name )  # Генеруємо шлях до зображення

            if image_path:  # Якщо зображення існує за цим шляхом
                try:
                    img = Image.open( image_path )  # Відкриваємо зображення
                    img.show()  # Відображаємо зображення
                    print( f"Зображення для цього питання: {image_name}" )
                except Exception as e:
                    print( f"Не вдалося відкрити зображення: {e}" )
            else:
                print( f"Зображення '{image_name}' не знайдено." )

        # Обробка питання типу "підставте відповідність"
        if "matching" in q:  # Перевіряємо, чи є в питанні тип matching
            print( "Підставте правильні пари:" )
            for idx_1, option in enumerate( q["matching"] ):
                print( f"{chr( 97 + idx_1 )}) {option[0]}" )  # Виводимо варіанти для відповідності

            # Відповідність для варіантів
            print( "\nВідповідність:" )
            for i, ans in enumerate( q["answers"] ):
                print( f"{i + 1}) {ans}" )

            # Вводимо відповіді користувача
            answer = input( "Ваша відповідь (наприклад, '1,2,3'): " ).lower()

            # Парсимо введену відповідь
            user_answers = answer.split( "," )
            user_answers = [ans.strip() for ans in user_answers]  # Очищаємо від зайвих пробілів

            correct = True
            # Перевірка кожного варіанту
            for i, ans in enumerate( user_answers ):
                if not ans.isdigit() or int( ans ) < 1 or int( ans ) > len( q["answers"] ):
                    correct = False
                    break
                # Перевірка правильності
                if int( ans ) != q["answer"][i]:
                    correct = False
                    break

            if correct:
                correct_answers += 1
                print( "Правильна відповідь!\n" )
            else:
                print(
                    f"Неправильна відповідь. Правильні пари: {', '.join( [f'{chr( 97 + i )}-{q['answer'][i]}' for i in range( len( q['answer'] ) )] )}\n"
                )

        else:
            # Якщо питання не типу matching, працюємо як зазвичай
            for option in q["options"]:
                print( option )

            # Вводимо відповіді користувача
            answer = input( "Ваша відповідь (a/b/c/d): " ).lower()

            # Якщо є кілька правильних відповідей, користувач може ввести декілька літер
            if len( q["answer"] ) > 1:
                # Дозволяємо вибирати кілька відповідей
                user_answers = answer.split( "," )
                user_answers = [ans.strip() for ans in user_answers]  # Очищаємо від зайвих пробілів

                # Перевіряємо чи всі вибрані користувачем варіанти є правильними
                if sorted( user_answers ) == sorted( q["answer"] ):
                    correct_answers += 1
                    print( "Правильна відповідь!\n" )
                else:
                    print( f"Неправильна відповідь. Правильні варіанти: {', '.join( q['answer'] )}\n" )
            else:
                # Якщо одна правильна відповідь
                if answer == q["answer"][0]:
                    correct_answers += 1
                    print( "Правильна відповідь!\n" )
                else:
                    print( f"Неправильна відповідь. Правильний варіант: {q['answer'][0]}\n" )

    print( f"Іспит завершено! Ви відповіли правильно на {correct_answers} з {total_questions} питань." )
    score = (correct_answers / total_questions) * 100
    print( f"Ваш результат: {score:.2f}%" )


# Запуск тесту
if __name__ == "__main__":
    run_exam()
