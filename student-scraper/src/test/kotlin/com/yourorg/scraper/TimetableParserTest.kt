package com.yourorg.scraper

import org.junit.Assert.assertEquals
import org.junit.Test
import java.nio.charset.StandardCharsets

class TimetableParserTest {
    @Test
    fun testParse() {
        val html = this::class.java.getResource("/timetable.html")!!.readText(StandardCharsets.UTF_8)
        val result = TimetableParser.parse(html)
        assertEquals(1, result.size)
        val first = result[0]
        assertEquals("Mon", first.day)
        assertEquals("A1", first.slot)
        assertEquals("CSE101", first.courseCode)
    }
}
