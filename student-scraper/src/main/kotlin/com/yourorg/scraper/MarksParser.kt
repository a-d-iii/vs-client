package com.yourorg.scraper

import org.jsoup.Jsoup

object MarksParser {
    fun parse(html: String): List<Mark> {
        val doc = Jsoup.parse(html)
        val rows = doc.select("table#MarksTable tr").drop(1)
        return rows.map { row ->
            val cells = row.select("td")
            Mark(
                courseCode = cells.getOrNull(0)?.text() ?: "",
                score = cells.getOrNull(1)?.text() ?: ""
            )
        }
    }
}
