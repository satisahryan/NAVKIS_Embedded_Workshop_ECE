/* ==========================================================================
   Workshop configuration - edit this file only; every page reads from it.
   ========================================================================== */
window.WS = {
  title: "From Code to Silicon",
  caption: "Blink. Sense. Connect.",
  subtitle: "A hands-on embedded systems workshop with the ESP32",
  host: "Skill Development Cell and Department of Electronics & Communication Engineering, NAVKIS College of Engineering, Hassan",
  date: "Wednesday, 25 November 2026",
  time: "10:30 AM – 4:00 PM",
  speaker: "Dr. Sathisha R N",
  speakerRole: "Assistant Professor, Dept. of Electronics & Telecommunication Engg., Siddaganga Institute of Technology, Tumakuru",
  speakerEmail: "satisharyan@gmail.com",

  /* Wokwi project links. Create each project once in your Wokwi account
     (see README), then paste its share link here. Leave "" to show students
     the copy-paste steps instead.                                           */
  wokwi: {
    lab1: "", lab2: "", lab3: "", lab4: "", lab5: "", lab6: "", challenge: "", lab7: "", lab8: "", ece1: "", ece2: "", ece3: ""
  },

  /* MQTT broker for Lab 5 + the live class dashboard.
     The ESP32 uses TCP 1883; the browser dashboard uses secure WebSockets. */
  mqtt: {
    topicRoot: "navkis/ews2026",
    brokers: {
      hivemq: { name: "HiveMQ public", esp: "broker.hivemq.com", wss: "wss://broker.hivemq.com:8884/mqtt" },
      emqx:   { name: "EMQX public",   esp: "broker.emqx.io",    wss: "wss://broker.emqx.io:8084/mqtt" },
      mosquitto: { name: "Mosquitto test", esp: "test.mosquitto.org", wss: "wss://test.mosquitto.org:8081/mqtt" }
    },
    defaultBroker: "hivemq"
  },

  /* Optional: Google Apps Script web-app URL that records quiz scores
     (code in README.md). Leave "" to keep scores on the student's screen only. */
  quizScriptUrl: "",

  /* Certificates (certificates.html) */
  hodName: "Dr. Manjunath D V",
  hodTitle: "Professor & HOD, Dept. of ECE",
  /* Optional: the Gradebook tab published as CSV (File > Share > Publish to web > Gradebook > CSV).
     Leave "" and upload the downloaded CSV file instead. */
  gradebookCsvUrl: "",
  feedbackFormUrl: ""
};
