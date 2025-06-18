package com.yourorg.scraper

import org.jsoup.Jsoup

object TimetableParser {
    fun parse(html: String): List<TimetableEntry> {
        val doc = Jsoup.parse(html)
        val rows = doc.select("table#TimetableTable tr").drop(1)
        return rows.map { row ->
            val cells = row.select("td")
            TimetableEntry(
                day = cells.getOrNull(0)?.text() ?: "",
                slot = cells.getOrNull(1)?.text() ?: "",
                courseCode = cells.getOrNull(2)?.text() ?: ""
            )
        }
    }
}
