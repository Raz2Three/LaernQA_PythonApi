json_text = {
    "messages": [
        {
            "message": "This is the first message",
            "timestamp": "2021-06-04 16:40:53"
        },
        {
            "message": "And this is a second message",
            "timestamp": "2021-06-04 16:41:01"
        }
    ]
}

second_message = json_text.get("messages", 0)[1].get("message", 0)
print(second_message)
