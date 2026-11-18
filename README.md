# From Code to Silicon — Blink. Sense. Connect.

A one-day embedded systems workshop with the ESP32, simulated in the **Wokwi** simulator.
For III year ECE students: Skill Development Cell and Dept. of ECE, NAVKIS College of Engineering, Hassan, on **25 November 2026** (10:30 AM – 4:00 PM).
Resource person: **Dr. Sathisha R N**, Siddaganga Institute of Technology, Tumakuru.

| Page | What it is |
|---|---|
| `index.html` | Home: schedule and links |
| `slides.html` | 42-slide animated deck. Keys: ← → navigate, **N** speaker notes, **F** fullscreen, **A** reveal all |
| `labs.html` | Labs 1–6 and the mini-challenge (in class), take-home Labs 7–8 (deep sleep, web API), each with wiring, copyable code, Try-this questions and stretch tasks for fast finishers |
| `dashboard.html` | Live MQTT class dashboard (Lab 5). Has a *Demo mode* for rehearsal |
| `quiz.html` | 15-question quiz, with optional score collection |
| `handout.html` | Printable 2-page handout (Print → Save as PDF) |
| `instructor.html` | Run-sheet for the instructor (not linked from the other pages) |
| `certificates.html` | Prints every student's certificate from the gradebook CSV (instructor only, not linked) |
| `labs/<lab>/` | `sketch.ino`, `diagram.json`, `libraries.txt` and solutions for each lab |
| `assets/config.js` | **The only file you need to edit** |

The labs are written in **MicroPython** (firmware v1.28 on the Wokwi **ESP32 DevKitC V4** board), which starts instantly on wokwi.com with no build queue. Each lab folder also has an `arduino/` copy in C for real boards; those sketches compile against ESP32 Arduino core 3.3.8.

---

## Step 1 — Publish on GitHub Pages (about 5 minutes)

1. On github.com, click **+ → New repository**. Name it `NAVKIS_Embedded`, make it **Public**, and click **Create**.
2. Click **uploading an existing file**. Drag in **everything inside this folder** (not the folder itself). `index.html` must sit at the top level. Click **Commit changes**.
3. Go to **Settings → Pages**. Under *Build and deployment*, choose **Deploy from a branch → main → / (root) → Save**.
4. After about a minute the site is live at `https://<your-username>.github.io/NAVKIS_Embedded/`.

The QR codes on the slides, handout and dashboard are generated from the page address, so they point to the right place automatically.

## Step 2 — Create the Wokwi projects (one-time, about 10 minutes)

With shared links, students just click **Open this lab in Wokwi** instead of pasting files.

For each folder in `labs/` (`lab1` … `lab8`, `ece1` … `ece3`, `challenge`; Labs 7–8 are take-home, so their links are optional):
1. Sign in at wokwi.com and open **wokwi.com/projects/new/micropython-esp32**.
2. Replace the contents of `diagram.json` and `main.py` with the files from the folder.
3. For `lab4`, also add `ssd1306.py` (the **▾** menu next to the tabs → *New file…*) and paste its contents.
4. Press **Save**, then copy the project URL (for example `https://wokwi.com/projects/41234…`).
5. Paste it into `assets/config.js` under `wokwi: { lab1: "…", … }`. Commit the change.

Until a link is filled in, the lab page shows students the copy-and-paste steps instead.

## Step 3 — Quiz scores, gradebook and certificates

Students are graded out of 100:

| Part | Weight | Where it comes from |
|---|---|---|
| Quiz | 40 | Recorded automatically when a student submits the quiz |
| Labs completed (1–6) | 30 | Ticked by the student on the quiz page; check against the dashboard's **Download list** (Lab 5) and correct if needed |
| Smart Street Light challenge | 20 | Your score out of 13 from the rubric, entered for each team member |
| Participation | 10 | Your rating out of 5 (default 3) |

| Total | Rating | Certificate |
|---|---|---|
| 85–100 | Outstanding ★★★★★ | Certificate of Excellence |
| 70–84 | Excellent ★★★★ | Certificate of Achievement |
| 55–69 | Very Good ★★★ | Certificate of Achievement |
| 40–54 | Good ★★ | Certificate of Merit |
| below 40 | Participated ★ | Certificate of Participation |

**Set up (once, about 5 minutes):**
1. Create a Google Sheet. Choose **Extensions → Apps Script**, paste `grading/gradebook.gs`, and click **Save**.
2. Choose **Deploy → New deployment → Web app**, with *Execute as*: **Me** and *Who has access*: **Anyone**. Click **Deploy** and copy the URL.
3. Paste the URL into `quizScriptUrl` in `config.js`. Take the quiz once yourself to test: a **Quiz** tab should appear in the Sheet.

**At the end of the day (print and hand out):**
1. While teams demo the challenge (3:20), type each student's **Challenge /13** into your score list. Give **Participation /5** ratings during the afternoon.
2. When the quiz closes (about 3:55), reload the Sheet and choose **Workshop → Build / update gradebook**. Paste in the challenge and participation marks, and correct **Labs /6** where needed. Total, Rating and Certificate No. update by themselves.
3. Download the Gradebook tab as CSV (**File → Download → Comma-separated values**).
4. Open **certificates.html** on the site (it's not linked from the student pages), load the CSV, check the preview, and press **Print all certificates**. Choose **A4 · Landscape · Margins: None** and tick **Background graphics**. Certificates are signed by Dr. Sathisha R N and Dr. Manjunath D V, Professor & HOD, Dept. of ECE; edit `hodName` and `hodTitle` in `config.js` if needed. The fonts are built into the page, so it prints the same even without internet.

A backup generator, `grading/certgen.py`, makes the same certificates as PDF files from the CSV.

The *Answers* column is a string of 1s and 0s, one per question (1 = correct). Options are shuffled for each student.

You can also put a Google Form link in `feedbackFormUrl`. A **Give feedback** button then appears after the quiz.

## The MQTT dashboard

- Students' ESP32s publish to `navkis/ews2026/<name>/data` and listen on `navkis/ews2026/<name>/led`.
- The dashboard listens to three public brokers at once (HiveMQ, EMQX, Mosquitto), and each student device connects to the first one that answers, so one broker being down doesn't stop the lab.
- These are free **public** brokers: anyone can read the topics, so no personal data should be sent.

## Credits

Simulator: [Wokwi](https://wokwi.com). Bundled libraries (MIT licence): [MQTT.js](https://github.com/mqttjs/MQTT.js) and [qrcode-generator](https://github.com/kazuhikoarase/qrcode-generator).
Arduino libraries used in the labs: PubSubClient, DHT sensor library for ESPx, Adafruit SSD1306 and Adafruit GFX.
