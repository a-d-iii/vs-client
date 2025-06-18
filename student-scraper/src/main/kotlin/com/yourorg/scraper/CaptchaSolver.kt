package com.yourorg.scraper

interface CaptchaSolver {
    suspend fun solve(imageBase64: String): String
}
