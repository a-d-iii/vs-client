package com.yourorg.scraper

sealed class ScrapeResult {
    data class Success(val data: StudentData) : ScrapeResult()
    data class Failure(val message: String) : ScrapeResult()
}
