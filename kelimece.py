import tkinter as tk
from tkinter import simpledialog
import random
from googletrans import Translator

translator = Translator()

# Kullanıcı kelimelerini saklamak için bir sözlük oluştur
user_words = {}

# Kullanıcının eklediği kelimeleri yüklemek için bir işlev
def load_words():
    try:
        with open("user_words.txt", "r") as file:
            for line in file:
                # Her satırı İngilizce kelime ve Türkçe çeviri olarak böler ve sözlüğe ekler
                english_word, turkish_translation = line.strip().split(" - ")
                user_words[english_word] = turkish_translation
    except FileNotFoundError:
        # Dosya bulunamazsa sessizce devam et
        pass

def translate_english_to_turkish(event=None):
    english_word = english_entry.get()
    if english_word:
        turkish_translation = translator.translate(english_word, src='en', dest='tr').text
        turkish_entry.delete(0, 'end')
        turkish_entry.insert(0, turkish_translation)

def on_key_event(event):
    # Eğer metin kutusu aktif değilse veya basılan tuş "Alt_R" değilse hiçbir işlem yapma
    if event.widget == english_entry and event.keysym == "Alt_R":
        # İngilizce kelimeyi al
        english_word = english_entry.get()
        if english_word:
            turkish_translation = translator.translate(english_word, src='en', dest='tr').text
            turkish_entry.delete(0, 'end')
            turkish_entry.insert(0, turkish_translation)
    elif event.widget == turkish_entry and event.keysym == "Alt_R":
        # Türkçe kelimeyi al
        turkish_word = turkish_entry.get()
        if turkish_word:
            english_translation = translator.translate(turkish_word, src='tr', dest='en').text
            english_entry.delete(0, 'end')
            english_entry.insert(0, english_translation)


# Kullanıcının eklediği kelimeleri kaydetmek için bir işlev
def save_words():
    with open("user_words.txt", "w") as file:
        for english_word, turkish_translation in user_words.items():
            # Her kelimeyi dosyaya yaz
            file.write(f"{english_word} - {turkish_translation}\n")

def on_closing():
    # Program kapatılmadan önce kelimeleri kaydet
    save_words()
    root.destroy()

#Tuşa basmadan çevirme yapması için kullandığımız kod parçası (geliştirilmeli)
"""def delayed_translate_english_to_turkish():
    english_word = english_entry.get()
    if english_word:
        turkish_translation = translator.translate(english_word, src='en', dest='tr').text
        turkish_entry.delete(0, 'end')
        turkish_entry.insert(0, turkish_translation)

def translate_english_to_turkish(event=None):
    # Yalnızca gecikmeyi başlatın
    root.after(3000, delayed_translate_english_to_turkish)"""


# Kullanıcının yeni kelime eklemesine izin veren işlev
def add_word(event=None):
    english_word = english_entry.get()
    turkish_translation = turkish_entry.get()

    if english_word in user_words:
        print("Bu kelime zaten eklenmiş.")
        return  # Kelime zaten ekli, işlemi durdur

    # İngilizce kelimeyi ve Türkçe çevirisini listeye ekler
    word_listbox.insert(tk.END, f"{english_word} - {turkish_translation}")
    user_words[english_word] = turkish_translation
    # Metin kutularını temizler ve kelimeleri kaydeder
    english_entry.delete(0, 'end')
    turkish_entry.delete(0, 'end')
    save_words()

# Kullanıcının mevcut bir kelimeyi düzenlemesine izin veren işlev
def edit_word():
    selected_word = word_listbox.get(tk.ACTIVE)
    if selected_word:
        english_word, turkish_translation = selected_word.split(" - ")
        # Yeni İngilizce kelimeyi ve Türkçe çevirisini alır
        new_english_word = simpledialog.askstring("Düzenle", "Yeni İngilizce Kelime:", initialvalue=english_word)
        new_turkish_translation = simpledialog.askstring("Düzenle", "Yeni Türkçe Karşılık:", initialvalue=turkish_translation)
        if new_english_word and new_turkish_translation:
            # Eski kelimeyi sözlükten kaldırır, yeni kelimeyi ekler ve listeyi günceller
            user_words.pop(english_word)
            user_words[new_english_word] = new_turkish_translation
            word_listbox.delete(tk.ACTIVE)
            word_listbox.insert(tk.END, f"{new_english_word} - {new_turkish_translation}")
            save_words()

# Kullanıcının seçtiği bir kelimeyi silmesine izin veren işlev
def delete_word():
    selected_word = word_listbox.get(tk.ACTIVE)
    if selected_word:
        english_word, _ = selected_word.split(" - ")
        # Kelimeyi sözlükten kaldırır ve listeyi günceller
        user_words.pop(english_word)
        word_listbox.delete(tk.ACTIVE)
        save_words()

# Rastgele bir kelime yüklemeye izin veren işlev
def load_random_word():
    if user_words:
        # Sözlükten rastgele bir kelime seçer ve bu kelimeyi ekranda gösterir
        random_word = random.choice(list(user_words.keys()))
        question_label.config(text=random_word, font=("Helvetica", 20))
        show_answer_button.config(state="normal", font=("Helvetica", 16))
        load_random_word_button.config(state="normal", font=("Helvetica", 16))
    else:
        # Eğer hiç kelime eklenmemişse bir uyarı gösterir
        question_label.config(text="Lütfen önce kelimeler ekleyin.")

# Kelimenin Türkçe çevirisini göstermeye izin veren işlev
def show_answer(event=None):
    if user_words:
        question_word = question_label.cget("text")
        # Kelimenin çevirisini alır ve ekranda gösterir
        turkish_translation = user_words.get(question_word, "Bu kelimenin çevirisi yok.")
        question_label.config(text=f"Cevap: {turkish_translation}", font=("Helvetica", 16))
        show_answer_button.config(state="disabled", font=("Helvetica", 16))
        load_random_word_button.config(state="normal", font=("Helvetica", 16))

# Kelime listesini görüntülemeyi veya gizlemeyi sağlayan işlev
def toggle_word_list():
    if not word_list_frame.winfo_ismapped():
        word_list_frame.pack()
        show_list_button.config(text="Listeyi Gizle")
    else:
        word_list_frame.pack_forget()
        show_list_button.config(text="Listeyi Göster")


def load_words_to_listbox():
    try:
        with open("user_words_sorted.txt", "r") as file:
            # Önce mevcut kelimeleri temizle
            word_listbox.delete(0, tk.END)
            for line in file:
                # Her satırı İngilizce kelime ve Türkçe çeviri olarak böler ve sözlüğe ekler
                english_word, turkish_translation = line.strip().split(" - ")
                user_words[english_word] = turkish_translation
                # Kelimeleri listbox'a ekler
                word_listbox.insert(tk.END, f"{english_word} - {turkish_translation}")
    except FileNotFoundError:
        # Dosya bulunamazsa sessizce devam et
        pass

def space_pressed(event):
        load_random_word() 
        return "break"
    # Bu, karakter girişini engellemek için gereklidir

def cevap_gosterme(event):
        show_answer() 
        return "break"
    # Bu, karakter girişini engellemek için gereklidir

load_words()

sorted_user_words = {
    key.capitalize(): value[0].capitalize() + value[1:] for key, value in sorted(user_words.items())
}

# Sıralanmış verileri bir dosyaya yaz
with open("user_words_sorted.txt", "w") as file:
    for english_word, turkish_translation in sorted_user_words.items():
        file.write(f"{english_word} - {turkish_translation}\n")

# Ana Tkinter penceresini başlatır ve başlık ayarlar
root = tk.Tk()
root.title("Kelimece")

# Çeşitli arayüz öğelerini içeren bir çerçeve oluşturur ve bu çerçeveyi yerleştirir
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# İngilizce kelime ve Türkçe çeviri girişi için etiketler ve metin kutuları ekler
english_label = tk.Label(frame, text="İngilizce Kelime:", font=("Helvetica", 14))
english_label.grid(row=0, column=0)

turkish_label = tk.Label(frame, text="Türkçe Karşılık:", font=("Helvetica", 14))
turkish_label.grid(row=1, column=0)

english_entry = tk.Entry(frame, font=("Helvetica", 14))
english_entry.grid(row=0, column=1)
"""english_entry.bind('<FocusIn>', translate_english_to_turkish)
english_entry.bind('<KeyRelease>', translate_english_to_turkish)"""
root.bind("<Key>", on_key_event)

turkish_entry = tk.Entry(frame, font=("Helvetica", 14))
turkish_entry.grid(row=1, column=1)

# Kelime eklemeyi, düzenlemeyi, silmeyi ve liste göstermeyi sağlayan düğmeleri ekler
add_button = tk.Button(frame, text="Kelime Ekle", command=add_word, font=("Helvetica", 14))
add_button.grid(row=2, column=0, columnspan=2)
add_button.bind('<Return>', add_word)
english_entry.bind('<Return>', add_word)
turkish_entry.bind('<Return>', add_word)

edit_button = tk.Button(frame, text="Kelimeyi Düzenle", command=edit_word, font=("Helvetica", 5))
edit_button.grid(row=3, column=0, columnspan=2)

delete_button = tk.Button(frame, text="Kelimeyi Sil", command=delete_word, font=("Helvetica", 5))
delete_button.grid(row=4, column=0, columnspan=2)

show_list_button = tk.Button(frame, text="Listeyi Göster", command=toggle_word_list, font=("Helvetica", 14))
show_list_button.grid(row=5, column=0, columnspan=2)

# Kelime listesini içeren bir çerçeve ve bu çerçeveyi içeren bir liste kutusu oluşturur
word_list_frame = tk.Frame(root)
word_listbox = tk.Listbox(word_list_frame, selectmode=tk.SINGLE, height=5, width=40, font=("Helvetica", 14))
word_listbox.pack()

load_words_to_listbox()
# Kelime eğitimini içeren bir çerçeve oluşturur
training_frame = tk.Frame(root)
training_frame.pack(padx=4, pady=4)

# Soruyu ve cevap gösterme işlevlerini içeren etiket ve düğmeleri ekler
question_label = tk.Label(training_frame, text="", font=("Helvetica", 20))
question_label.pack()

show_answer_button = tk.Button(training_frame, text="Cevabı Göster", state="disabled", command=show_answer, font=("Helvetica", 16))
show_answer_button.pack()

load_random_word_button = tk.Button(training_frame, text="Antrenmana başla", command=load_random_word, font=("Helvetica", 16))
load_random_word_button.pack()
root.bind('<space>', space_pressed)
root.bind('<Control_R>', cevap_gosterme)

# Sağ alt köşeye metni ekler
designed_label = tk.Label(root, text="Designed by Dündar with ChatGPT", font=("Merlin", 10), anchor="se")
designed_label.pack(side="bottom", fill="x")



# Tkinter penceresini başlatır ve kullanıcının programı kullanmasına izin verir
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
