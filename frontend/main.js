const sendBtn = document.getElementById("sendBtn");
const voiceBtn = document.getElementById("voiceBtn");
const userInput = document.getElementById("userInput");
const responseBox = document.getElementById("responseBox");

sendBtn.addEventListener("click", async () => {
    const message = userInput.value;
    if (!message) return;
    const res = await fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({text: message})
    });
    const data = await res.json();
    responseBox.innerText = data.response;
    speakText(data.response);
});

function speakText(text) {
    const utter = new SpeechSynthesisUtterance(text);
    speechSynthesis.speak(utter);
}

voiceBtn.addEventListener("click", () => {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = "en-US";
    recognition.start();
    recognition.onresult = (event) => {
        userInput.value = event.results[0][0].transcript;
    };
});
