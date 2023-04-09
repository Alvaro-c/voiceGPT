import os
import openai
import json
import requests
import speech_recognition as sr


def recognize_audio():
    pass
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    # recognize speech using whisper
    try:
        print("Whisper thinks you said " + r.recognize_whisper(audio, language="spanish"))
        return r.recognize_whisper(audio, language="spanish")
    except sr.UnknownValueError:
        print("Whisper could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Whisper")


def send_query_to_chat(question):

    url = 'https://api.openai.com/v1/chat/completions'
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": f"{question}"}],
        "temperature": 0.2
    }

    post_headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}",
    }

    response = requests.post(url, json=payload, headers=post_headers)
    answer_object = json.loads(response.text)
    print(answer_object)
    chat_answer = answer_object.get('choices')[0].get('message').get('content')
    print(chat_answer)
    return chat_answer


def speak(text):
    os.system(f"say '{text}'")


def main():
    question = recognize_audio()
    answer = send_query_to_chat(question)
    speak(answer)


if __name__ == '__main__':
    main()

