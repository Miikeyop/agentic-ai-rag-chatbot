const form = document.getElementById("chatForm");
const input = document.getElementById("questionInput");
const chatMessages = document.getElementById("chatMessages");
const typingIndicator = document.getElementById("typingIndicator");
const sendButton = document.getElementById("sendButton");
const suggestions = document.getElementById("suggestions");


function scrollToBottom() {
    requestAnimationFrame(() => {
        chatMessages.scrollTop =
            chatMessages.scrollHeight;
    });
}


function addUserMessage(text) {
    const message =
        document.createElement("div");

    message.className =
        "message user-message";


    const content =
        document.createElement("div");

    content.className =
        "message-content";


    const bubble =
        document.createElement("div");

    bubble.className =
        "message-bubble";

    bubble.textContent = text;


    content.appendChild(bubble);

    message.appendChild(content);

    chatMessages.appendChild(message);

    scrollToBottom();
}


function addAssistantMessage(data) {
    const message =
        document.createElement("div");

    message.className =
        "message assistant-message";


    const avatar =
        document.createElement("div");

    avatar.className = "avatar";

    avatar.textContent = "AI";


    const content =
        document.createElement("div");

    content.className =
        "message-content";


    const label =
        document.createElement("div");

    label.className =
        "assistant-label";

    label.textContent =
        "Agentic AI Assistant";


    const bubble =
        document.createElement("div");

    bubble.className =
        "message-bubble";

    bubble.textContent =
        data.answer || "No answer returned.";


    content.appendChild(label);

    content.appendChild(bubble);


    if (
        data.confidence !== undefined &&
        data.confidence !== null
    ) {
        const meta =
            document.createElement("div");

        meta.className =
            "response-meta";


        const confidence =
            document.createElement("span");

        confidence.className =
            "confidence";


        const percentage =
            Math.max(
                0,
                Math.min(
                    100,
                    data.confidence * 100
                )
            );


        confidence.textContent =
            `Retrieval confidence ${percentage.toFixed(1)}%`;


        meta.appendChild(confidence);

        content.appendChild(meta);
    }


    if (
        Array.isArray(data.context) &&
        data.context.length > 0
    ) {
        const details =
            document.createElement("details");

        details.className =
            "sources";


        const summary =
            document.createElement("summary");

        summary.textContent =
            `Retrieved context (${data.context.length} chunks)`;


        details.appendChild(summary);


        data.context.forEach(
            (item, index) => {

                const source =
                    document.createElement("div");

                source.className =
                    "source-item";


                const info =
                    document.createElement("div");

                info.className =
                    "source-info";


                let page = "Unknown";

                if (
                    item.page !== undefined &&
                    item.page !== null
                ) {
                    page =
                        Number(item.page) + 1;
                }


                let scoreText = "";

                if (
                    item.score !== undefined &&
                    item.score !== null
                ) {
                    scoreText =
                        ` · Distance ${Number(item.score).toFixed(4)}`;
                }


                info.textContent =
                    `Chunk ${index + 1} · Page ${page}${scoreText}`;


                const sourceText =
                    document.createElement("div");

                sourceText.className =
                    "source-text";

                sourceText.textContent =
                    item.text || "";


                source.appendChild(info);

                source.appendChild(sourceText);

                details.appendChild(source);
            }
        );


        content.appendChild(details);
    }


    message.appendChild(avatar);

    message.appendChild(content);

    chatMessages.appendChild(message);

    scrollToBottom();
}


function addErrorMessage(messageText) {
    const message =
        document.createElement("div");

    message.className =
        "message assistant-message error-message";


    const avatar =
        document.createElement("div");

    avatar.className = "avatar";

    avatar.textContent = "AI";


    const content =
        document.createElement("div");

    content.className =
        "message-content";


    const bubble =
        document.createElement("div");

    bubble.className =
        "message-bubble";

    bubble.textContent =
        messageText;


    content.appendChild(bubble);

    message.appendChild(avatar);

    message.appendChild(content);

    chatMessages.appendChild(message);

    scrollToBottom();
}


async function sendQuestion(question) {
    addUserMessage(question);

    if (suggestions) {
        suggestions.style.display = "none";
    }

    typingIndicator.classList.remove("hidden");

    sendButton.disabled = true;

    input.disabled = true;

    scrollToBottom();


    try {
        const response = await fetch(
            "/chat",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    question: question
                })
            }
        );


        if (!response.ok) {
            throw new Error(
                `HTTP error ${response.status}`
            );
        }


        const data =
            await response.json();


        typingIndicator
            .classList
            .add("hidden");


        addAssistantMessage(data);
    }

    catch (error) {
        typingIndicator
            .classList
            .add("hidden");


        addErrorMessage(
            "Something went wrong while processing your question. Please try again."
        );


        console.error(error);
    }

    finally {
        sendButton.disabled = false;

        input.disabled = false;

        input.focus();
    }
}


form.addEventListener(
    "submit",
    function (event) {
        event.preventDefault();


        const question =
            input.value.trim();


        if (!question) {
            return;
        }


        input.value = "";

        input.style.height = "auto";

        sendQuestion(question);
    }
);


input.addEventListener(
    "keydown",
    function (event) {
        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {
            event.preventDefault();

            form.requestSubmit();
        }
    }
);


input.addEventListener(
    "input",
    function () {
        this.style.height = "auto";

        this.style.height =
            Math.min(
                this.scrollHeight,
                130
            ) + "px";
    }
);


document
    .querySelectorAll(".suggestion")
    .forEach(button => {

        button.addEventListener(
            "click",
            function () {

                const question =
                    this.textContent.trim();

                input.value = question;

                form.requestSubmit();
            }
        );

    });