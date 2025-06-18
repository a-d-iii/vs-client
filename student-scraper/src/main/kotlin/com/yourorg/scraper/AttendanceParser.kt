package com.yourorg.scraper

import org.jsoup.Jsoup

object AttendanceParser {
    fun parse(html: String): List<Attendance> {
        val doc = Jsoup.parse(html)
        val rows = doc.select("table#AttendanceTable tr").drop(1)
        return rows.map { row ->
            val cells = row.select("td")
            Attendance(
                courseCode = cells.getOrNull(0)?.text() ?: "",
                courseName = cells.getOrNull(1)?.text() ?: "",
                attended = cells.getOrNull(2)?.text()?.toIntOrNull() ?: 0,
                total = cells.getOrNull(3)?.text()?.toIntOrNull() ?: 0,
                percentage = cells.getOrNull(4)?.text()?.removeSuffix("%")?.toIntOrNull() ?: 0
            )
        }
    }
}
