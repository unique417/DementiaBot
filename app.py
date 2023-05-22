from tkinter import *
import sys
from conversation_engine import conversation_engine
#from emotion_detector import Emotion
from personality_questions import MBTIClassifier
#from stanford_triple_extraction import StanfordOpenIEWrapper
from similarities import Similarity
from yes_no import Yes_no
from knowledgegraph import KnowledgeGraph

#emotion= Emotion()
ce = conversation_engine()
mbti= MBTIClassifier()
#stanford_triple_extractor = StanfordOpenIEWrapper()
sim= Similarity()
kg=KnowledgeGraph()
ynclassifier = Yes_no()
response = ce.start()
flag = 0
personality=[" - "," - "," - "," - "]
done=False
#from chat import *



bot_name= 'DementiaBot'
BG_GRAY = "#264769"
BG_COLOR = "#f0ece1"
TEXT_COLOR = "#000000"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"
class ChatApplication:

    def __init__(self):
        self.window = Tk()
        self._setup_main_window()
        self.flag = 0

    def run(self):
        self.window.mainloop()

    def _setup_main_window(self):
        self.window.title("DementiaBot")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=770, height=550, bg=BG_COLOR)

        # head label
        head_label = Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR,
                           text="Welcome", font=FONT_BOLD, pady=10)
        head_label.place(relwidth=1)

        # tiny divider
        line = Label(self.window, width=450, bg=BG_GRAY)
        line.place(relwidth=1, rely=0.07, relheight=0.012)

        # text widget
        self.text_widget = Text(self.window, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR,
                                font=FONT, padx=5, pady=5)
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.configure(cursor="arrow", state=DISABLED)

        # scroll bar
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.text_widget.yview)

        # bottom label
        bottom_label = Label(self.window, bg=BG_GRAY, height=80)
        bottom_label.place(relwidth=1, rely=0.825)

        # message entry box
        self.msg_entry = Entry(bottom_label, bg="#f0ece1", fg=TEXT_COLOR, font=FONT)
        self.msg_entry.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)

        # send button
        send_button = Button(bottom_label, text="Send", font=FONT_BOLD, width=20, bg=BG_GRAY,
                             command=lambda: self._on_enter_pressed(None))
        send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)

    def _on_enter_pressed(self, event):
        msg = input(response+'\n')
        self._insert_message(msg, "You")

    def _insert_message(self, msg, sender):
        if not msg:
            return

        self.msg_entry.delete(0, END)
        msg1 = f"{sender}: {msg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state=DISABLED)

        

        #relevant_triples = sim.sbert_similarity(text,kg.get_all_triples())
        #extract information:

        #knowledge=stanford_triple_extractor.extract_triples(text)
        #for triple in knowledge:
        #    kg.add_edge(triple)

    #    mo= emotion.get_emotion(text)


        response = ce.chat(text,q, verbose=True)
        msg2="resonse"
        #msg2 = f"{bot_name}:{response}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg2)
        self.text_widget.configure(state=DISABLED)

        self.text_widget.see(END)


if __name__ == "__main__":
    app = ChatApplication()
    app.run()
