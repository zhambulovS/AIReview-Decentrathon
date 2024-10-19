from flask import Flask, render_template, request, redirect, url_for, session, flash
from Transcribe import getID, getTranscript, punctuateText
from Summarize import summarize
from Entity import entityToHTMLLinks, getFlashcards
import nltk

nltk.download('punkt')

app = Flask(__name__)
app.secret_key = "c9l3n5b1"

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        URL = request.form["url"]
        ID = getID(URL)
        if not ID:
            flash("Invalid URL or unable to extract video ID.")
            return redirect(url_for("home"))
        return redirect(url_for("summary", ID=ID))
    return render_template("home.html")

@app.route("/videoinfo/<ID>")
def summary(ID):
    URL = f"https://www.youtube.com/embed/{ID}"
    print(f"URL = {URL}")
    
    transcript = getTranscript(ID)
    if not transcript:
        flash("Transcript not available for this video.")
        return redirect(url_for("home"))
    
    transcript = punctuateText(transcript)
    summary = summarize(transcript)
    
    flashcards = getFlashcards(summary)
    transcript = entityToHTMLLinks(transcript)
    summary = entityToHTMLLinks(summary)
    
    return render_template("transcribe.html", URL=URL, transcript=transcript, summary=summary, flashcards=flashcards)

if __name__ == "__main__":
    app.run(debug=True)
