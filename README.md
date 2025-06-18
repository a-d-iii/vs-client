<br />
<p align="center">
    <img src="public/Final_Icon_512x512.png" width="100" height="100" style="margin-right: 60px;"> 
    <img src="public/vitaplogo.png" width="322" height="100"> 
</p>
<br>
<br>

<p align="center">
    <a href="https://github.com/Udhay-Adithya/vitap-vtop-client">
    <img src="https://img.shields.io/github/stars/Udhay-Adithya/vitap-vtop-client?style=social" alt="License: MIT">
    </a>
    <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT">
    </a>
    <img src="https://img.shields.io/badge/Version-0.2.7-blue.svg" alt="Version 0.2.7">
    <a href="https://github.com/Udhay-Adithya/vitap-vtop-client/issues">
    <img src="https://img.shields.io/github/issues/Udhay-Adithya/vitap-vtop-client" alt="License: MIT">
    </a>
</p>
<br>

`vitap-vtop-client` is a minimal Kotlin library for scraping the VIT‑AP VTOP portal. It handles login, CAPTCHA solving, and HTML parsing so your Android app can access attendance, marks, and timetable data with just one suspending call.

The library is intended for use as a small backend component inside other apps or services that require VTOP data.

**Disclaimer:** Use this library responsibly and in accordance with VIT-AP's terms of service. Web scraping is subject to changes in the target website's structure, which may occasionally affect the library's functionality.

## Table of Contents
1. [Features](#features)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Documentation](#documentation)
5. [Contributing](#contributing)
6. [License](#license)
7. [Related Project: VTOP API](#related-project-vtop-api)

## Features
*   **User Authentication:** Secure login and session management.
*   **Profile Information:** Retrieve comprehensive student profile details.
*   **Academic Data:** Access attendance records, timetables, marks, and exam schedules.
*   **Biometric Logs:** Fetch student biometric entry/exit logs.
*   **Contact Details:** View mentor, HOD, and Dean information.
*   **Financial Information:** Check pending payments and download receipts.
*   **Hostel Outing Requests:** Post and review weekend and general outing requests.
*   **Academic Performance:** Retrieve NCGPA and rank details.

## Installation

Clone the repository and build the Kotlin library with Gradle:

```bash
git clone https://github.com/Udhay-Adithya/vitap-vtop-client.git
cd vitap-vtop-client 
./gradlew :student-scraper:assembleRelease
```

If `gradle-wrapper.jar` is missing on first run, install Gradle and execute
`gradle wrapper` to generate it before running `./gradlew`.
 
The compiled AAR and JAR will be located under `student-scraper/build/outputs/aar`.

## Quick Start

Here's a basic example of how to fetch all data inside a coroutine:

```kotlin
suspend fun demo() {
    val scraper = StudentScraperImpl()
    val result = scraper.fetchAll(
        Credentials(regNo = "YOUR_REGNO", dob = "01-01-2000", password = "PASS"),
        captchaSolver = object : CaptchaSolver {
            override suspend fun solve(imageBase64: String): String {
                // Call your captcha API
                return "abcd"
            }
        }
    )
    when (result) {
        is ScrapeResult.Success -> println(result.data)
        is ScrapeResult.Failure -> println("Error: ${'$'}{result.message}")
    }
}
```

## Documentation

For comprehensive information on all available methods, data models, and advanced usage, please refer to the main documentation:

➡️ **[`DOCS.md`](DOCS.md)**

## Contributing
Contributions are welcome! We appreciate any help, from bug reports and fixes to feature suggestions and documentation improvements.

Please read our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute, set up your development environment, and submit pull requests.

## License
This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

## Related Project: VTOP API
For those looking for a ready-to-use API service built on top of this library, check out the **VITAP-VTOP API**:

➡️ **[VITAP-VTOP API Repository](https://github.com/Udhay-Adithya/vit_ap_vtop_api/)**

This FastAPI wrapper allows easy access to VTOP data without needing to integrate the client library directly. We encourage users to try out the API and provide feedback.
