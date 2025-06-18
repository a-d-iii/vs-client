package com.yourorg.scraper

import io.ktor.client.HttpClient
import io.ktor.client.call.body
import io.ktor.client.engine.okhttp.OkHttp
import io.ktor.client.request.forms.formData
import io.ktor.client.request.get
import io.ktor.client.request.post
import io.ktor.client.statement.bodyAsText
import io.ktor.client.plugins.contentnegotiation.ContentNegotiation
import io.ktor.serialization.kotlinx.json.json
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.jsoup.Jsoup

class StudentScraperImpl : StudentScraper {
    override suspend fun fetchAll(
        credentials: Credentials,
        captchaSolver: CaptchaSolver,
        endpoints: Endpoints
    ): ScrapeResult = withContext(Dispatchers.IO) {
        val client = HttpClient(OkHttp) {
            install(ContentNegotiation) { json() }
        }
        try {
            val loginPage = client.get(endpoints.baseUrl + endpoints.login).bodyAsText()
            val captchaBase64 = Jsoup.parse(loginPage)
                .selectFirst("img[id=captcha]")?.attr("src")?.substringAfter("base64,")
                ?: return@withContext ScrapeResult.Failure("Captcha not found")
            val captchaText = captchaSolver.solve(captchaBase64)

            val form = formData {
                append("regno", credentials.regNo)
                append("dob", credentials.dob)
                append("passwd", credentials.password)
                append("captcha", captchaText)
            }
            val loginResp = client.post(endpoints.baseUrl + endpoints.login) { setBody(form) }
            if (!loginResp.status.value.toString().startsWith("2")) {
                client.close()
                return@withContext ScrapeResult.Failure("Login failed")
            }

            val attendanceHtml = client.get(endpoints.baseUrl + endpoints.attendance).bodyAsText()
            val marksHtml = client.get(endpoints.baseUrl + endpoints.marks).bodyAsText()
            val timetableHtml = client.get(endpoints.baseUrl + endpoints.timetable).bodyAsText()

            val attendance = AttendanceParser.parse(attendanceHtml)
            val marks = MarksParser.parse(marksHtml)
            val timetable = TimetableParser.parse(timetableHtml)

            client.close()
            ScrapeResult.Success(StudentData(attendance, marks, timetable))
        } catch (e: Exception) {
            client.close()
            ScrapeResult.Failure(e.message ?: "Unknown error")
        }
    }
}
