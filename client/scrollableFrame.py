from tkinter import *


class ScrollableFrame(Frame):
    def __init__(self, container, flag, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = Canvas(self)
        self.flag = flag
        scrollbar = Scrollbar(self, orient="vertical", command=canvas.yview, width=15)
        self.scrollable_frame = Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        if self.flag == 1:
            canvas.create_window((5, 5), window=self.scrollable_frame, anchor="sw")
        else:
            canvas.create_window((5, 5), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill=BOTH)
        scrollbar.pack(side="right", fill=Y)
