import express from "express";
import { get } from "config";
import { MessengerBot } from "intelligo";

const app = express();

const bot = new MessengerBot({
  PAGE_ACCESS_TOKEN: get("PAGE_ACCESS_TOKEN"),
  VALIDATION_TOKEN: get("VALIDATION_TOKEN"),
  APP_SECRET: get("APP_SECRET"),
  app: app
});

bot.initWebhook();

bot.addGreeting("cryptocurrency trading bot.");

bot.addPersistentMenu([
  {
    locale: "default",
    composer_input_disabled: false,
    call_to_actions: [
      {
        title: "Home",
        type: "postback",
        payload: "HOME"
      },
      {
        title: "About",
        type: "nested",
        call_to_actions: [
          {
            type: "web_url",
            title: "Crypto Bot",
            url: "https://www.intelligo.systems",
            webview_height_ratio: "full"
          }
        ]
      },
      {
        title: "Contact Info",
        type: "postback",
        payload: "CONTACT"
      }
    ]
  }
]);

//Subscribe to messages sent by the user with the bot.on() method.
bot.on("message", event => {
  const senderID = event.sender.id,
    message = event.message;

  if (bot.textMatches(message.text, "зураг")) bot.sendImageMessage(senderID, "https://intelligo.js.org/logo.png");
  else if (bot.textMatches(message.text, "дуу")) bot.sendAudioMessage(senderID, "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-15.mp3");
  else if (bot.textMatches(message.text, "бичлэг"))
    bot.sendVideoMessage(senderID, "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4");
  else if (bot.textMatches(message.text, "файл")) bot.sendFileMessage(senderID, "https://intelligo.js.org/logo.png");
  else if (bot.textMatches(message.text, "товч"))
    bot.sendButtonMessage(senderID);
  else if (bot.textMatches(message.text, "quick reply"))
    bot.sendQuickReply(senderID);
  else if (bot.textMatches(message.text, "read receipt"))
    bot.sendReadReceipt(senderID);
  else if (bot.textMatches(message.text, "typing on"))
    bot.sendTypingOn(senderID);
  else if (bot.textMatches(message.text, "typing off"))
    bot.sendTypingOff(senderID);
  else if (bot.textMatches(message.text, "сургалт"))
    bot.sendGenericMessage(senderID);
  else if (bot.textMatches(message.text, "хичээл"))
    bot.sendReceiptMessage(senderID);
  else bot.sendTextMessage(senderID, result + "");
});
app.set("port", process.env.PORT || 5000);
app.listen(app.get("port"), function() {
  console.log("Server is running on port", app.get("port"));
});
