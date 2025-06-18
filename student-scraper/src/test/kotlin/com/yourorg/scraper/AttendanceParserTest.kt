package com.yourorg.scraper

import org.junit.Assert.assertEquals
import org.junit.Test
import java.nio.charset.StandardCharsets

class AttendanceParserTest {
    @Test
    fun testParse() {
        val html = this::class.java.getResource("/attendance.html")!!.readText(StandardCharsets.UTF_8)
        val result = AttendanceParser.parse(html)
        assertEquals(1, result.size)
        val first = result[0]
        assertEquals("CSE101", first.courseCode)
        assertEquals("Math", first.courseName)
        assertEquals(10, first.attended)
        assertEquals(12, first.total)
        assertEquals(83, first.percentage)
    }
}
