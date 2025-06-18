package com.yourorg.scraper

import org.junit.Assert.assertEquals
import org.junit.Test
import java.nio.charset.StandardCharsets

class MarksParserTest {
    @Test
    fun testParse() {
        val html = this::class.java.getResource("/marks.html")!!.readText(StandardCharsets.UTF_8)
        val result = MarksParser.parse(html)
        assertEquals(1, result.size)
        val first = result[0]
        assertEquals("CSE101", first.courseCode)
        assertEquals("95", first.score)
    }
}
