async function sendMessage() {
    const input = document.getElementById("user-input");
    const message = input.value;

    if (!message) return;

    const chatBox = document.getElementById("chat-box");

    chatBox.innerHTML += `
        <p class="user"><b>You:</b> ${message}</p>
    `;

    input.value = "";

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message
            })
        });

        const data = await response.json();

        console.log(data);

        // SHOW ERROR IF EXISTS
        if (data.error) {
            chatBox.innerHTML += `
                <p class="bot" style="color:red;">
                    <b>Error:</b> ${data.error}
                </p>
            `;
            return;
        }

        chatBox.innerHTML += `
            <p class="bot">
                <b>Bot:</b> ${data.reply}
            </p>
        `;

    } catch (err) {
        console.log(err);

        chatBox.innerHTML += `
            <p style="color:red;">
                Failed to connect to backend
            </p>
        `;
    }

    chatBox.scrollTop = chatBox.scrollHeight;
}