# Multi Tool Agent Setup Guide

This guide will help you set up your environment to use the Multi Tool Agent for interacting with course information stored in Google Firestore and using Vertex AI.


## 1. Firestore Service Account JSON Setup

To allow your agent to access Firestore, you need a Google Cloud service account key in JSON format.

### Steps:

1. **Create a Service Account:**
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Navigate to **IAM & Admin > Service Accounts**.
   - Click **Create Service Account**.
   - Give it a name (e.g., `firestore-access`).

2. **Assign Roles:**
   - Assign the role: `Cloud Datastore User` (or `Cloud Firestore User`).
   - Optionally, add `Vertex AI User` if you plan to use Vertex AI.

3. **Create and Download Key:**
   - After creating the service account, go to the **Keys** tab.
   - Click **Add Key > Create new key**.
   - Select **JSON** and download the file.

4. **Place the JSON File:**
   - Rename the file to `firestore.json`.
   - Place it in the root of your project directory (same level as `.gitignore`).

> **Note:** The `.gitignore` already excludes `firestore.json` from version control for security.

---

## 2. Firestore Database Schema

Your Firestore should have a collection named `courses` with documents structured as follows:

| Field Name         | Type    | Example / Notes                                  |
|--------------------|---------|--------------------------------------------------|
| courseId           | string  | "CS101"                                          |
| courseName         | map     | `{ "en": "Intro to CS" }`                        |
| courseOverview     | map     | `{ "en": "Overview text" }`                      |
| courseDuration     | string  | "3 months"                                       |
| classesPerWeek     | int     | 3                                                |
| batch              | string  | "2024 Spring"                                    |
| courseStartDate    | string  | "2024-09-01T00:00:00Z" (ISO format)              |
| fee                | number  | 500                                              |
| medium             | string  | "English"                                        |
| examDate           | string  | "2024-12-01T00:00:00Z" (ISO format)              |
| requirements       | map     | `{ "en": "Basic math" }`                         |
| outcomes           | map     | `{ "en": "Understand CS basics" }`               |
| description        | map     | `{ "en": "Full course description" }`            |

- All fields used in [`get_course_details`](multi_tool_agent/tools/firestore_query.py) and [`list_courses`](multi_tool_agent/tools/firestore_query.py) must be present for correct operation.
- The `courseName`, `courseOverview`, `requirements`, `outcomes`, and `description` fields are expected to be maps with an `"en"` key for English text.

---

## 3. Vertex AI Setup

1. **Enable Vertex AI:**
   - In the [Google Cloud Console](https://console.cloud.google.com/), go to **APIs & Services > Library**.
   - Search for **Vertex AI API** and enable it.

2. **Set Environment Variables:**
   - The `.env` file in `multi_tool_agent/` should contain:
     ```
     GOOGLE_GENAI_USE_VERTEXAI=TRUE
     GOOGLE_CLOUD_PROJECT=your-gcp-project-id
     GOOGLE_CLOUD_LOCATION=your-region
     ```
   - Replace `your-gcp-project-id` and `your-region` with your actual project ID and region (e.g., `us-central1`).

---

## 4. Install Dependencies

Install Python dependencies using pip:

```sh
pip install -r requirements.txt
```

---

## 5. Running the Agent

Ensure your environment is activated and the `firestore.json` file is in place. Then, run the application like below

```sh
adk web
```

---

## 6. Security Note

- Never commit your `firestore.json` or any credentials to version control.
- The `.gitignore` file already protects this.

---

## References

- [Firestore Python Client Docs](https://googleapis.dev/python/firestore/latest/index.html)
- [Vertex AI Python Client Docs](https://cloud.google.com/vertex-ai/docs/start/client-libraries)