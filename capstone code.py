import speech_recognition as spr
from googletrans import Translator
from gtts import gTTS
import os

# Create Recognizer() class object
recog1 = spr.Recognizer()

# Create microphone instance
mc = spr.Microphone()

# Capture Voice
with mc as source:
    print("Speak 'hello' to initiate the translation!")
    print("")
    recog1.adjust_for_ambient_noise(source, duration=0.2)
    audio = recog1.listen(source)
    
    try:
        # Recognize speech using Google Speech Recognition
        MyText = recog1.recognize_google(audio)
        MyText = MyText.lower()

        # Check if the word 'hello' is in the recognized text
        if 'hello' in MyText:
            print("You said 'hello', now speak a sentence to translate.")
            
            # Translator method for translation
            translator = Translator()
            
            # Source and target languages
            from_lang = 'en'
            to_lang = 'hi'
            
            with mc as source:
                print("Speak a sentence...")
                recog1.adjust_for_ambient_noise(source, duration=0.2)
                
                # Listen for a sentence
                audio = recog1.listen(source)
                
                try:
                    # Convert audio to text
                    get_sentence = recog1.recognize_google(audio)
                    print("Sentence to be translated: " + get_sentence)
                    
                    # Translate the text
                    text_to_translate = translator.translate(get_sentence, src=from_lang, dest=to_lang)
                    translated_text = text_to_translate.text
                    
                    # Use Google Text-to-Speech to speak the translated text
                    speak = gTTS(text=translated_text, lang=to_lang, slow=False)
                    
                    # Save the translated speech to an mp3 file
                    speak.save("captured_voice.mp3")
                    
                    # Play the mp3 file using the OS module
                    os.system("start captured_voice.mp3")

                except spr.UnknownValueError:
                    print("Google Speech Recognition could not understand the audio.")
                except spr.RequestError as e:
                    print(f"Could not request results from Google Speech Recognition service; {e}")
                except Exception as e:
                    print(f"An error occurred during translation or TTS: {e}")
        
        else:
            print("You did not say 'hello'. Please try again.")
    
    except spr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio.")
    except spr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
