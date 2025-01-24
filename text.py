import os
import speech_recognition as sr
import pyttsx3
import webbrowser
import subprocess

# Termux TTS kullanımı için pyttsx3
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.9)

def speak(text):
    """Metni sese çevirir."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Kullanıcının sesini dinler ve metne çevirir."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Dinliyorum...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio, language='tr-TR')
            print(f"Söylediğiniz: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sizi anlayamadım, lütfen tekrar edin.")
        except sr.RequestError:
            speak("Google API'ye bağlanılamadı.")
        except Exception as e:
            speak(f"Bir hata oluştu: {e}")
        return ""

def execute_command(command):
    """Komutları analiz eder ve çalıştırır."""
    if "dosya oluştur" in command:
        try:
            file_path = "/sdcard/Download/yeni_dosya.txt"
            with open(file_path, "w") as file:
                file.write("Bu bir test dosyasıdır.")
            speak(f"Dosya oluşturuldu: {file_path}")
        except Exception as e:
            speak(f"Bir hata oluştu: {e}")
    elif "youtube aç" in command:
        speak("Hangi videoyu açmamı istersiniz?")
        video = listen()
        if video:
            url = f"https://www.youtube.com/results?search_query={video.replace(' ', '+')}"
            webbrowser.open(url)
            speak(f"{video} YouTube'da açılıyor.")
    elif "dur" in command:
        speak("Program sonlandırılıyor.")
        exit()
    else:
        speak("Bu komutu anlayamadım.")

# Ana döngü
speak("Sistem hazır, komutlarınızı bekliyorum.")
while True:
    user_command = listen()
    if user_command:
        execute_command(user_command)
